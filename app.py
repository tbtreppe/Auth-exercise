from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import RegisterForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///auth"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secrets"
app.config ['DEBUG_TB_INTERCEPT_REDIRECTS']= False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def homepage():
    return redirect('/register')

#@app.route('/register')
#def show_register_form():

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    form = RegisterForm
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        new_user = Upser.register(username, password)
#error handling if username is taken. try to add
        db.session.add(new_user)
        db.session.commit()
        flash ('Welcome!')
        return redirect('/secrets')
    return render_template('register.html', form=form)

@app.route('/secret')
def show_secret():
    return render_template("secret.html")

#@app.route('/login')
#def show_login_form():


#@app.route('/login', methods=['POST'])
#def login():
    #if authenticated login and go to /secret

    #else go back to home page and flash a message saying must be logged in
