#!/usr/bin/env python

import sqlite3
from flask import g, Flask, request, render_template, redirect


app = Flask(__name__)

def connect_db():
    return sqlite3.connect('../db/bichar.db')

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route('/')
def main():
    pn = request.args.get('pn')
    pn = int(pn) if pn else 1
    limit = 20
    offset = (int(pn)-1) * limit
    cur = g.db.execute("SELECT * FROM tweets WHERE label IS NOT NULL LIMIT ? OFFSET ?", (limit, offset))
    res = [(row[0], row[1], row[2]) for row in cur.fetchall()]

    cur = g.db.execute("SELECT count(*) FROM tweets WHERE label IS NOT NULL")
    labelled = cur.fetchone()[0]
    return render_template('index.html', res=res, pn=pn, labelled=labelled)

@app.route('/action', methods=['POST'])
def action():
    id = int(request.form.get('id'))
    label = request.form.get('label')

    if label == 'rem':
        g.db.execute("DELETE FROM tweets WHERE id=?", (id,))
    else:
        g.db.execute("UPDATE tweets SET label=? WHERE id=?", (label, id))

    g.db.commit()
    return 'success'


app.run('0.0.0.0', 80, debug=True)
