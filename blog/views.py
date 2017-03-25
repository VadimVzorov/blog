from flask import render_template

from . import app
from .database import session, Entry

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

    return render_template("entries.html",
        entries=entries,
        has_next=has_next,
        has_prev=has_prev,
        page=page,
        total_pages=total_pages
    )

@app.route("/entry/add", methods=["GET"])
def add_entry_get():
    return render_template("add_entry.html")

from flask import request, redirect, url_for

@app.route("/entry/add", methods=["POST"])
def add_entry_post():
    entry = Entry(
        title=request.form["title"],
        content=request.form["content"],
    )
    session.add(entry)
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
def edit_entry_get(id):
    entry = session.query(Entry).get(id)
    session.add(entry)
    return render_template("entry_edit.html",
        entry = entry
    )

@app.route("/entry/id/<int:id>/edit", methods=["POST"])
def edit_entry_post(id):
    entry = session.query(Entry).get(id)
    entry.title = request.form["title"],
    entry.content = request.form["content"]
    session.add(entry)
    session.commit()
    return redirect(url_for('one_entry', id=id))

@app.route("/entry/id/<int:id>/delete", methods=["GET"])
def delete_entry_get(id):
    entry = session.query(Entry).get(id)
    return render_template(
        "delete_entry.html",
         entry = entry
    )

@app.route("/entry/id/<int:id>/delete", methods=["POST"])
def delete_entry_post(id):
    entry = session.query(Entry).get(id)
    print(dir(session))
    session.commit()
    return redirect(url_for("entries", page=1))

@app.route("/entry/id/<int:id>/cancel", methods=["GET"])
def delete_entry_cancel(id):
    return redirect(url_for("entries", page=1))
