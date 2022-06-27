# Entering Virtual Environment and starting Git Bash
# source virt/Scripts/activate
# export FLASK_ENV=development
# export FLASK_APP=main.py

from flask import request, Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

# Create a flask instance
app = Flask(__name__)

# Add MySQL Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Bitrux*777@localhost/users'
# Secret Key
app.config['SECRET_KEY'] = "NonProductionWeb"
# Initialize Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Flask Login Management
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# Create Database Model
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    favorite_color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Create A String
    def __repr__(self):
        return '<Name %r>' % self.name

# Create a route decorator
@app.route('/')
def index():
    return render_template('index.html')

# Create an Add User Page
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        username = request.form.get('username')
        favorite_color = request.form.get('favorite_color')
        password_hash = request.form.get('password_hash')
        password_hash2 = request.form.get('password_hash2')

        user = Users.query.filter_by(email=email).first()
        if password_hash != password_hash2:
            flash('Password mismatch')
        elif len(email) < 4:
            flash('Invalid Email Address.')
        elif len(name) < 2:
            flash('First name must be greater than 1 character(s).')
        elif len(password_hash) < 7:
            flash('Password must be atleast 7 characters')
        elif user:
            flash("This user is already registered. Please log in.")
        else:
            hashed_pw = generate_password_hash(password_hash, "sha256")
            user = Users(name=name, 
            username=username, 
            email=email, 
            favorite_color=favorite_color, 
            password_hash=hashed_pw)

            db.session.add(user)
            db.session.commit()
            flash("User added successfully!")
            return redirect(url_for('dashboard'))
    our_users = Users.query.order_by(Users.date_added)

    return render_template("add_user.html", our_users=our_users)

# Create an Update User Page
@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    id = name_to_update.id
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        try:
            db.session.commit()
            flash("User updated successfully!")
            return render_template('update.html', form=form, name_to_update=name_to_update, id=id)
        except:
            flash("Something went wrong! Try again.")
            return render_template('update.html', form=form, name_to_update=name_to_update, id=id)
    else:
        return render_template('update.html', form=form, name_to_update=name_to_update, id=id)

# Create a Delete User Page
@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name= None
    form = UserForm()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Successfully!")

        our_users = Users.query.order_by(Users.date_added)
        return render_template("add_user.html", form=form, name=name, our_users=our_users)
    except:
        flash("Something went wrong while deleting the user! Please try again.")
        return render_template("add_user.html", form=form, name=name, our_users=our_users)

# Create Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = Users.query.filter_by(username=request.form.get('username')).first()
        if user:
            # Check the hash
            if check_password_hash(user.password_hash, request.form.get('password')):
                login_user(user)
                flash("Login Succesfull!")
                return redirect(url_for('dashboard'))
            else:
                flash("Wrong Password - Try Again")
        else:
            flash("That username isn't registered on the database. Please sign up!")

    return render_template('login.html')

# Create Dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

# Create a logout route
@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    flash("You have been logged out!")
    return redirect(url_for('login'))



# Create custom error pages
# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template('404.html'), 500