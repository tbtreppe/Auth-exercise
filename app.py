from flask import Flask, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm, DeleteForm
from sqlalchemy.exc import IntegrityError

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
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if "username" in session:
        return redirect(f"/users/{session['username']}")
    
    form = RegisterForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        user = User.register(username, password, email, first_name, last_name)
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken')
            return render_template('users/register.html', form=form)
        session['username'] = user.username
        flash ('Welcome!', 'success')
        return redirect(f"/users/{user.username}")
    else:
        return render_template("users/register.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    if "username" in session:
        return redirct(f"/users/{session['username']}")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f'Welcome Back, {user.username}!', 'success')
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ['Invalid/username/password', 'error']
            return render_template("users/login.html", form=form)
    return render_template("users/login.html", form=form)

@app.route('/logout')
def logout_user():
    session.pop('username')
    flash("Successfully logged out", 'success')
    return redirect ('/login')
    
@app.route("/users/<username>", methods=['GET', 'POST'])
def show_user_details(username):
    if "username" not in session:
        flash("Please log in first!", 'error')
        return redirect("users/register")
    user = User.query.get(username)

    return render_template("users/user_details.html", user=user)

@app.route("/users/<username>/delete", methods=['POST'])
def delete_user(username):
    if 'username' not in session:
        flash("Please login first", 'error')
        return redirect('/')
    if 'username' == session['username']:
        user = User.query.get(username)
        db.session.delete(user)
        db.session.commit()
        session.pop("username")
        flash("Username deleted!", "success")
        return redirect("users/login")
    flash("No permission", "error")
    return redirect('/')

@app.route('/users/<username>/feedback/new', methods=['GET', 'POST'])
def new_feedback(username):
    if 'username' not in session:
        flash("Please login first", 'error')
        return redirect('/')
    
    form=FeedbackForm()
   
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        feedback = Feedback(title=title, content=content, username=username)
        db.session.add(feedback)
        db.session.commit()
        flash("Feedback added!", "success")
        return redirect(f"/users/{feedback.username}")

    
    return render_template('feedback/new.html', form=form)

@app.route("/feedback/<int:id>/update", methods =['GET', 'POST'])
def update_feedback(id):
    feedback = Feedback.query.get(id)
    if 'username' not in session:
        flash("Please login first", 'error')
        return redirect('/')
    form=FeedbackForm(obj=feedback)
   
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        flash("Feedback updated!", "success")
        return redirect(f"/users/{feedback.username}")
    
    return render_template('feedback/edit.html', form=form, feedback=feedback)

@app.route("/feedback/<int:id>/delete", methods =['POST'])
def delete_feedback(id):
    feedback = Feedback.query.get_or_404(id)
    if 'username' not in session:
        flash("please login first", 'error')
        return redirect('/')
    form=DeleteForm
    if feedback.username == session['username']:
        db.session.delete(feedback)
        db.session.commit()
        flash ("Feedback deleted", "success")
        return redirect(f"/users/{feedback.username}")
    


