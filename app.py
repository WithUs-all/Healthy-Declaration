from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_required, current_user, LoginManager, login_user, logout_user
from distutils import util
from flask_sqlalchemy import SQLAlchemy
import pyqrcode
from datetime import datetime
import config
import base64
from flask_mail import Mail, Message
# import smtplib, ssl

app = Flask(__name__)

app.config['MAIL_SERVER'] = config.MAIL_SERVER
app.config['MAIL_PORT'] = config.MAIL_PORT
app.config['MAIL_USE_TLS'] = config.MAIL_USE_TLS
app.config['MAIL_USE_SSL'] = config.MAIL_USE_SSL
app.config['MAIL_USERNAME'] = config.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = config.MAIL_PASSWORD

app.config['SQLALCHEMY_DATABASE_URI'] = config.db_url()
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = 'HealthDeclaration'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

mail = Mail(app)

@login_manager.user_loader
def load_user(user_id):
  # since the user_id is just the primary key of our user table, use it in the query for the user
  return User.query.get(int(user_id))

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True) 
  username = db.Column(db.String(80), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(100)) 
  is_admin = db.Column(db.Boolean, default=False)
  def __repr__(self):
      return '<User %r>' % self.username

class Customer(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  # qrcode = db.Column(db.String(200), nullable=False)
  cname = db.Column(db.String(80), nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  company = db.Column(db.String(100))
  phoneNum = db.Column(db.String(100))
  visited = db.Column(db.Text)
  quarantine = db.Column(db.Boolean, default=False)
  contact = db.Column(db.Boolean, default=False)
  fever = db.Column(db.Boolean, default=False)
  cough = db.Column(db.Boolean, default=False)
  sore_throat = db.Column(db.Boolean, default=False)
  muscle_pain = db.Column(db.Boolean, default=False)
  shortness_breath = db.Column(db.Boolean, default=False)
  breathing_difficulty = db.Column(db.Boolean, default=False)
  vomiting = db.Column(db.Boolean, default=False)
  diarrhoea = db.Column(db.Boolean, default=False)
  body_temp = db.Column(db.String(10))
  register_date = db.Column(db.Date())

  def __repr__(self):
      return '<User %r>' % self.cname

@app.route("/")
def index():
  if current_user:
    return redirect(url_for('customer_lists'))
  else:
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
  if request.method == 'POST':
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login')) # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect('/lists')

  if request.method == 'GET':
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  if request.method == 'GET':
    return render_template('signup.html')
  if request.method == 'POST':

    email = request.form.get('email')
    username = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
      flash('Email address already exists')
      return redirect(url_for('signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('login'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
  if request.method == 'GET':
    return render_template('profile.html', user=current_user)

  if request.method == 'POST':
    profile = request.form.to_dict()
    if profile['npwd'] == profile['ncpwd']:
      username = profile['username']
      email = profile['email']
      old_pass = profile['cpwd']
      new_pass = generate_password_hash(profile['npwd'], method='sha256')
      if check_password_hash(current_user.password, old_pass):
        current_user.email = email
        current_user.username = username
        current_user.password = new_pass
        db.session.commit()
        flash('success')
      else:
        flash('Password is not correct. Please input correct password?')
    else:
      flash('new password and confirm password must be same, please input again!')
    return redirect(url_for('profile'))



@app.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('index'))    
  
@app.route("/register_customer/<body_temp>/<lang>", methods=['GET'])
def register_customer_get(body_temp, lang='china'):
  if request.method == "GET":
    decodedBytes = base64.b64decode(body_temp)
    decodedStr = str(decodedBytes, "utf-8")
    return render_template('customer_form.html', body_temp_decoder=body_temp, body_temp=decodedStr, lang=lang)

@app.route("/register_customer_post", methods=['POST'])
def register_customer_post():
  if request.method == "POST":
    details = request.form.to_dict()

    customer = Customer(
      body_temp = details['body_temp'],
      cname = details['cname'],
      company = details['company'],
      phoneNum = details['phoneNum'],
      email = details['email'],
      visited = details['visited'],
      quarantine = bool(util.strtobool(details['quarantine'])),
      contact = bool(util.strtobool(details['contact'])),
      fever = bool(util.strtobool(details['fever'])),
      cough = bool(util.strtobool(details['cough'])),
      sore_throat = bool(util.strtobool(details['sore_throat'])),
      muscle_pain = bool(util.strtobool(details['muscle_pain'])),
      shortness_breath = bool(util.strtobool(details['shortness_breath'])),
      breathing_difficulty = bool(util.strtobool(details['breathing_difficulty'])),
      vomiting = bool(util.strtobool(details['vomiting'])),
      diarrhoea = bool(util.strtobool(details['diarrhoea'])),
      register_date = datetime.today().strftime('%Y-%m-%d')
    )
    db.session.add(customer)
    db.session.commit()

    msg = Message('Health Declaration', sender=config.MAIL_USERNAME, recipients=[details['email']])
    msg.body = render_template('register_customer_mail.txt',  data = details,  )
    msg.html = render_template('register_customer_mail.html',  data = details,  )
    with app.app_context():
      mail.send(msg)
    
    return redirect('success')

@app.route("/lists")
@login_required
def customer_lists():
  customers = Customer.query.all()
  return render_template("lists.html", customers = customers)

@app.route("/success")
def success():
  return render_template("success.html")

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=80)