from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#creating a db file to store the account details
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///AccountDetails.db'
db = SQLAlchemy(app)

#creating a table User in the db file
class User(db.Model):
    accountName = db.Column(db.String(80), primary_key=True, nullable=False)
    accountNumber = db.Column(db.Integer, unique=True, nullable=False)
    tradingbalance = db.Column(db.Integer, nullable=False)
    checkingbalance = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

#Filling the data with intial data
def createTablesWithInitialData():
    db.create_all()
    jack = User(accountName='jack', accountNumber=1234, tradingbalance = 2000, checkingbalance = 2000)
    jill = User(accountName='jill', accountNumber=1235, tradingbalance = 3000, checkingbalance = 1000)
    db.session.add(jack)
    db.session.add(jill)
    db.session.commit()

#Gets user balance given username
def getUserBalances(username):
    user1 = User.query.filter_by(accountName=username).first()
    return user1

#updates userbalance with the given values
def updateUserBalances(username, newUser1):
    task = db.session.query(User).get(username)
    task.tradingbalance = newUser1.tradingbalance
    task.checkingbalance = newUser1.checkingbalance
    db.session.commit()

#update method written to test if the method is working
#This is not being used  anywhere.
def update():
    task = db.session.query(User).get('jack')
    task.tradingbalance = 3000
    db.session.commit()
    '''
    conn = db.session.query(User)
    user1 = conn.filter_by(accountName='jack').first()
    user1.update({'tradingbalance':3000})
    #user1.tradinbalance = 3000
    #user1.checkingbalance = 2500
    print user1.tradinbalance
    '''
    #db.session.commit()

#This creates a db file in the current directory during thefirst  run and populates the intial data
#createTablesWithInitialData()
#update()
#print getUserBalances('jack').tradingbalance
