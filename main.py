import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import datetime
import time


app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post




@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    posts.reverse()
    return render_template('index.html', posts=posts)


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


# @app.route('/create', methods=('GET', 'POST'))
# def create():
#     if request.method == 'POST':
#         title = request.form['title']
#         content = request.form['content']

#         if not title:
#             flash('Title is required!')
#         else:
#             conn = get_db_connection()
#             conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
#                          (title, content))
#             conn.commit()
#             conn.close()
#             return redirect(url_for('index'))

#     return render_template('create.html')
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['username']
        content = request.form['reason']
        whom_to_meet = request.form['whom_to_meet']
        created = request.form['entryTime']
        exitTime = request.form['exitTime']
        # exitTime = time.strptime(str(exitTime),"%Y-%m-%d %H:%M")
        # created = time.strptime(str(created),"%Y-%m-%d %H:%M")
        # exitTime = DateTimeConvert(exitTime)
        # created = DateTimeConvert(created)

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (username, reason,whom_to_meet,exit,created) VALUES (?, ? ,?,?,?)',
                         (title, content,whom_to_meet,exitTime,created))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/info', methods=('GET', 'POST'))
def info():
    conn = get_db_connection()
    HighVisited = conn.execute('SELECT id,whom_to_meet,COUNT(whom_to_meet) FROM posts GROUP BY whom_to_meet ORDER BY whom_to_meet DESC LIMIT 1').fetchone()
    ReasonForFrequentVisits = conn.execute('SELECT id,reason,COUNT(reason) FROM posts GROUP BY reason ORDER BY reason DESC LIMIT 1').fetchone()
    conn.close()

    if request.method == 'POST':
        try:
            print("post")
            date = request.form['findDate']
            period = request.form['period']
            period = int(period)
            print(date)
            print(period)
            conn = get_db_connection()
            query = "select * from posts where DATE(created) == strftime('%Y-%m-%d','"+date+"')"
            posts = conn.execute(query).fetchall()
            conn.close()
            
            intimes = []
            outtimes =[]
            for i in posts:
                print(i[1])
                print(DateTimeConvert(i[1]))
                intimes.append(DateTimeConvert(i[1]))
                outtimes.append(DateTimeConvert(i[5]))

            first_entry = min((intimes))
            last_exit = max((outtimes))

            print('-----------------------')

            step = 60
            period = period * 60
            max_number = 0
            startTime = 0
            endTIme = 0
            for i in range(first_entry,last_exit,step):
                count = 0
                for out in outtimes:
                    if out >= i and out <=i+period:
                        count+=1
                if count>max_number:
                    max_number = count
                    startTime = i
                    endTIme = i+period

            print(max_number)
            print(startTime)
            print(endTIme)
            print(datetime.datetime.fromtimestamp(startTime / 1e3))
            print(datetime.datetime.fromtimestamp(endTIme / 1e3))
            st_date=datetime.datetime.fromtimestamp(startTime)
            end_date=datetime.datetime.fromtimestamp(endTIme)
            return render_template('info.html', post=HighVisited,postted=ReasonForFrequentVisits,startDate=st_date,endDate=end_date,MaxCount=max_number)
        except Exception as e:
            
            return render_template('info.html', post=HighVisited,postted=ReasonForFrequentVisits,startDate="No entries on this date")    
    
    return render_template('info.html', post=HighVisited,postted=ReasonForFrequentVisits)
    
def DateTimeConvert(date_in):
    date_processing = date_in.replace('T', '-').replace(':', '-').split('-')
    date_processing = [int(v) for v in date_processing]
    return int(time.mktime(datetime.datetime(*date_processing).timetuple()))

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)
    
    print(post[1])
    if request.method == 'POST':
        title = request.form['username']
        content = request.form['reason']
        whom_to_meet = request.form['whom_to_meet']
        exitTime = request.form['exitTime']
        created = request.form['entryTime']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            #(username, reason,whom_to_meet,exit,created) VALUES (?, ? ,?,?,?)
            conn.execute('UPDATE posts SET username = ?, reason = ? ,whom_to_meet = ?,exit = ? ,created = ?'
                         ' WHERE id = ?',
                         (title, content,whom_to_meet,exitTime,created,id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['username']))
    return redirect(url_for('index'))


