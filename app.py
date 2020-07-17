from flask import Flask , redirect , render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager , UserMixin , login_required ,login_user, logout_user,current_user
from flask_wtf.file import FileField
import os
import random
import requests
import json
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database/user.db'
app.config['SECRET_KEY']='619619'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(200))
    email = db.Column(db.String(200))
    password = db.Column(db.String(200))

class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))


@app.route('/create-task', methods=['POST'])
def create():
    content = request.form['content']
    new_task = Tasks(content=content)
    db.session.add(new_task)
    db.session.commit()
    return redirect('/home')


@app.route('/signup',methods=['POST'])
def signup_post():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    user = User(username=username,email=email,password=password)
    db.session.add(user)
    db.session.commit()
    user = User.query.filter_by(email=email).first()
    login_user(user)
    return redirect('/home')
@app.route('/delete/<id>')
def delete(id):
    Tasks.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('home'))

@login_manager.user_loader
def get(id):
    return User.query.get(id)

@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/login',methods=['GET'])
def get_login():
    return render_template('login.html')


@app.route('/home',methods=['GET'])
@login_required
def home():
    tasks = Tasks.query.all()
    return render_template('home.html',tasks = tasks)


@app.route('/about',methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/juegos',methods=['GET'])
def juegos():
    imgs = os.listdir('static/images')
    imgs = ['images/' + file for file in imgs]
    imgrand = random.sample(imgs,k=1)

    response = requests.get('https://api.themoviedb.org/3/movie/popular?api_key=3acab5e0f68601f14181a03d4cbc5ffd&language=es-ES&page=1')
    """
    response_json=response.json()
    origin=response_json['results']
    """
    response_json = json.loads(response.text)

    x = random.randrange(10)
    nombre = response_json['results'][x]['title']
    imagen = response_json['results'][x]['poster_path']
    overview = response_json['results'][x]['overview']


    return render_template('juegos.html', imgrand=imgrand, nombre=nombre, imagen=imagen, overview=overview)


@app.route('/signup',methods=['GET'])
def get_signup():
    return render_template('signup.html')

@app.route('/login',methods=['POST'])
def login_post():
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email).first()
    login_user(user)
    return redirect('/home')



@app.route('/logout',methods=['GET'])
def logout():
    logout_user()
    return redirect('/')

if __name__=='__main__':
    app.run(debug=True)