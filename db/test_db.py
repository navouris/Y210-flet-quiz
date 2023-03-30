from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class User(db.Model):
    username = db.Column(db.String(80), primary_key=True)
    password = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

class Game(db.Model):
    name = db.Column(db.String(80), db.ForeignKey('user.username'), primary_key=True)
    when = db.Column(db.String(80), primary_key=True)
    score = db.Column(db.Float(), nullable=False)

    def __repr__(self):
        return f'<Game {self.name}-{self.when}>'

with app.app_context():
    db.session.rollback()
    db.create_all()
    User.query.delete()
    # Game.query.delete()
    
    ## test - new users created
    for user in ['xenon', 'maria', 'kleopatra']:
        name = user
        password = "1234"
        password_hash = generate_password_hash(password)
        new_user = User(username=name, password=password_hash)
        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as error:
            print('Error in creating user {name}', error)
    
    ## create a user 
    name = 'zeon'
    password = '5678'
    user = User.query.filter_by(username=name).first()
    if user:
        print(f'----> user with name {name} already exists')
    else:
        password_hash = generate_password_hash(password)
        new_user = User(username=name, password=password_hash)
        db.session.add(new_user)
        db.session.commit()

    # user login with correct login password
    name = 'xenon'
    password = '1234'
    try: 
        user = User.query.filter_by(username=name).first()
        print(user);
        if user and check_password_hash(user.password, password):
            print(f"Καλωσήλθες {name}!!!")
        else: print('Εσφαλμένο όνομα/κωδικός χρήστη, ξαναπροσπαθήστε!')
    except Exception as error:
        print('σφάλμα ανάγνωσης', error)

    ## insert game
    name = "xenon"
    score = 0.8
    when =  datetime.datetime.now().strftime('%d-%m-%y %a %H:%M:%S')
    new_game = Game(name=name, when=when, score=score)
    try:
        db.session.add(new_game)
        db.session.commit()
        print(f'game of {name} was successfully inserted')
    except:
        print(f'error in saving game of user {name}')
    
    ## retrive all games of user...
    name = "zenon"
    try:
        games = Game.query.filter_by(name=name)
        out = f'{"**when":20s}\tscore**\n'
        for game in games:
            out += f"{game.when:20s}\t{game.score*100:0.1f}%\n"
        print(out)
    except:
        print('error in retrieving games of user {name}')

    ## retreive all users and games from the database
    users = User.query.all()
    for u in users:
        print(u.username, u.password)
    games = Game.query.all()
    for g in games:
        print(g)

if __name__ == "__main__":
    app.run(debug=True)

