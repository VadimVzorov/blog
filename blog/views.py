from flask import render_template

from . import app
from .database import session, Entry, Role
from flask_login import login_required, current_user
from .decorators import check_role, check_author
# defaut = 10, update it with new value

@app.route("/")
@app.route("/page/<int:page>")
def entries(page=1, PAGINATE_BY=10):
    # Zero-indexed page
    # import pdb; pdb.set_trace()
    try:
        PAGINATE_BY= int(request.args.get('PAGINATE_BY'))
    except (KeyError, TypeError):
        pass
    page_index = page - 1

    if PAGINATE_BY == 5 or PAGINATE_BY==10 or PAGINATE_BY==20:
        pass
    else:
        PAGINATE_BY = 10

    count = session.query(Entry).count()

    start = page_index * PAGINATE_BY
    end = start + PAGINATE_BY

    total_pages = (count - 1) // PAGINATE_BY + 1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0

    entries = session.query(Entry)
    entries = entries.order_by(Entry.datetime.desc())
    entries = entries[start:end]
    user = current_user
    role = session.query(Role)
    return render_template("entries.html",
        entries=entries,
        has_next=has_next,
        has_prev=has_prev,
        page=page,
        total_pages=total_pages,
        user = user,
        role = role
    )

@app.route("/entry/add", methods=["GET"])
@login_required
def add_entry_get():
    return render_template("add_entry.html")

from flask import request, redirect, url_for
from flask_login import current_user

@app.route("/entry/add", methods=["POST"])
@login_required
def add_entry_post():
    entry = Entry(
        title=request.form["title"],
        content=request.form["content"],
        author=current_user
    )
    role = Role(
        roles = current_user,
        role_name = "Author"
    )
    session.add(entry,role)
    session.commit()
    return redirect(url_for("entries"))

@app.route("/entry/id/<int:id>")
def one_entry(id):
    entry = session.query(Entry).get(id)
    session.add(entry)
    session.commit()
    return render_template("one_entry.html",
        entry = entry
    )

@app.route("/entry/id/<int:id>/edit", methods=["GET"])
@login_required
@check_role(current_user, ['Author','Admin'])
def edit_entry_get(id):
    entry = session.query(Entry).get(id)
    # if something in ['x', 'y', 'z'] or??
    if current_user.id == entry.author_id or "Admin" in [role.role_name for role in current_user.roles]:
        return render_template("entry_edit.html",
            entry = entry
        )
    else:
        abort(403)

@app.route("/entry/id/<int:id>/edit", methods=["POST"])
@login_required
@check_role(current_user, ['Author','Admin'])
def edit_entry_post(id):
    entry = session.query(Entry).get(id)
    entry.title = request.form["title"],
    entry.content = request.form["content"]
    # session.add(entry) -> creates another entry!! :-(
    session.commit()
    return redirect(url_for('one_entry', id=id))

@app.route("/entry/id/<int:id>/delete", methods=["GET"])
@login_required
@check_role(current_user, ['Author','Admin'])
def delete_entry_get(id):
    entry = session.query(Entry).get(id)
    return render_template(
        "delete_entry.html",
         entry = entry
    )

@app.route("/entry/id/<int:id>/delete", methods=["POST"])
@login_required
@check_role(current_user, ['Author','Admin'])
def delete_entry_post(id):
    entry = session.query(Entry).get(id)
    print(dir(session))
    session.commit()
    return redirect(url_for("entries", page=1))

@app.route("/entry/id/<int:id>/cancel", methods=["GET"])
@login_required
@check_role(current_user, ['Author','Admin'])
def delete_entry_cancel(id):
    return redirect(url_for("entries", page=1))

@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")

from flask import flash
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash
from .database import User

@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    user = session.query(User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash("Incorrect username or password", "danger")
        return redirect(url_for("login_get"))

    login_user(user)
    return redirect(request.args.get('next') or url_for("entries"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("entries"))
