import bcrypt
from flask import Flask, render_template, request, url_for, g, session, redirect
import sqlite3

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
db_location = 'var/login.db'

def check_auth(email, password):
    db = get_db()
    passwordcheck = ""
    export = "select password from userinfo where email = '%s'" % (email)
    for row in db.cursor().execute(export):
        passwordcheck=passwordcheck+(str(row))
    passwordcheck = passwordcheck[2:-3]
    if (bcrypt.checkpw(password.encode('utf-8'), passwordcheck.encode('utf-8'))):
        return True
    else:
        return False

def requires_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        status = session.get('logged_in', False)
        if not status:
            return redirect(url_for('/main/'))
        return f(*args, **kwargs)
    return decorated

@app.route('/logout/')
def logout():
    session['logged_in'] = False
    return redirect(url_for('/login/'))
def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = sqlite3.connect(db_location)
        g.db = db
    return db

@app.teardown_appcontext
def close_db_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['email']
        password = request.form['password']
        passtest = ""
        passtest = check_auth(request.form['email'],request.form['password'])
        if check_auth(request.form['email'],request.form['password']):
            session['logged_in'] = True
            return redirect (url_for('main'))
    return render_template('registration.html')
@app.route('/registration/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if (email == ""):
            return render_template('registration.html')
        if (password == ""):
            return render_template('registration.html')
        db = get_db()
        encoding = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        encoding = encoding.decode('utf-8')
        insert = "insert into userinfo values ('%s', '%s')" % (email, encoding)
        db.cursor().execute(insert)
        db.commit()
        return redirect(url_for('login'))
    return render_template('registration.html')

@app.route('/main/')
def main():
    return render_template('mainPage.html')
@app.route('/main/venus/')
def venus():
    return render_template('venus.html')
@app.route('/main/mercury/')
def mercury():
    return render_template('mercury.html')
@app.route('/main/pluto/')
def pluto():
    return render_template('pluto.html')
@app.route('/main/mars/')
def mars():
    return render_template('mars.html')
@app.route('/main/earth/')
def earth():
    return render_template('earth.html')
@app.route('/main/jupiter/')
def jupiter():
    return render_template('jupiter.html')
@app.route('/main/saturn/')
def saturn():
    return render_template('saturn.html')
@app.route('/main/uranus/')
def uranus():
    return render_template('uranus.html')
@app.route('/main/neptune/')
def neptune():
    return render_template('neptune.html')

if __name__ == ("__main__"):
    app.run(host='0.0.0.0', debug=True)
