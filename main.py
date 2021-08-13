import os

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, url_for, request, flash, redirect, send_from_directory, send_file
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
db = SQLAlchemy(app)
app.secret_key = os.urandom(24)
global param


def reset():
    qr = Students.query.filter_by(gueststatus=False).all()
    for x in qr:
        x.balance = x.mealplan
    db.session.commit()


# initialize scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(func=reset, trigger="cron", day_of_week="sun", hour="0", misfire_grace_time=None)
scheduler.start()


class Students(db.Model):
    id = db.Column('student_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    idno = db.Column(db.Integer())
    mealplan = db.Column(db.Integer())
    balance = db.Column(db.Integer())
    gueststatus = db.Column(db.Boolean())
    count = db.Column(db.Integer())

    def __init__(self, name, idno, mealplan, balance, gueststatus, count):
        self.name = name
        self.idno = idno
        self.mealplan = mealplan
        self.balance = balance
        self.gueststatus = gueststatus
        self.count = count


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = Students.query.filter_by(idno=request.form['idno']).first()
        global param
        param = request.form['idno']
        if query is None:
            flash('User not found!')
        else:
            if query.balance > 0:
                query.balance -= 1
                query.count += 1
                db.session.commit()
            elif query.balance == 0:
                return redirect(url_for('insufficient'))
            return render_template('success.html', user=query)
    return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/pfp')
def pfp():
    file_path = 'static/pics/' + param + ".jpg"
    file_path_jpeg = 'static/pics/' + param + ".jpeg"
    file_path_png = 'static/pics/' + param + ".png"
    if os.path.isfile(file_path):
        return send_file(file_path)
    elif os.path.isfile(file_path_jpeg):
        return send_file(file_path_jpeg)
    else:
        return file_path_png


@app.route("/show_all")
def show_all():
    return render_template('show_all.html', students=Students.query.filter_by(gueststatus=False))


@app.route("/swiped", methods=['GET', 'POST'])
def swiped():
    if request.method == 'POST':
        global param
        param = request.get_json()
    return param


@app.route("/success", methods=['GET'])
def success():
    query = Students.query.filter_by(idno=param).first()
    if query.balance > 0:
        query.balance -= 1
        query.count += 1
        db.session.commit()
    elif query.balance == 0:
        return redirect(url_for('insufficient'))
    return render_template('success.html', user=query)


@app.route("/insufficient", methods=['GET'])
def insufficient():
    return render_template('insufficient.html')


@app.route('/guest', methods=['GET', 'POST'])
def guest():
    if request.method == 'POST':
        if not request.form['name']:
            flash('Please enter name', 'error')
        elif request.form['name']:
            query = Students.query.filter_by(name=request.form['name']).first()
            if query is None:
                student = Students(request.form['name'], None, None, None, True, 1)
                db.session.add(student)
                db.session.commit()
                flash('Good to go!')
            else:
                query.count += 1
                db.session.commit()
                flash('Good to go!')
            return redirect(url_for('index'))
    return render_template('guest.html')


@app.route('/guestcsv', methods=['GET', 'POST'])
def guestcsv():
    return render_template('show_all.html', students=Students.query.filter_by(gueststatus=True))


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['idno'] or not request.form['mealplan'] or not \
                request.form['balance']:
            flash('Please enter all the fields', 'error')
        else:
            student = Students(request.form['name'], request.form['idno'],
                               request.form['mealplan'], request.form['balance'], False, 0)

            db.session.add(student)
            db.session.commit()

            flash('Record was successfully added')
            return redirect(url_for('show_all'))
    return render_template('new.html')


if __name__ == '__main__':
    db.create_all()
    db.session.commit()
    app.run()
