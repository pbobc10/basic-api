from enum import unique
import os
from flask import Flask, app,request,jsonify
from flask.json import jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.query import Query

basedir=os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,"data.sqlite")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)



class Drink(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80),unique=True, nullable=False)
    description = db.Column(db.String(128))

    def __repr__(self) -> str:
        return f' {self.name} - {self.description}'



@app.route('/',methods=['GET','POST'])
def index():
    return "Bonjour le monde"

@app.route('/drinks',methods=['GET','POST'])
def all_drinks():
    drinks=Drink.query.all()

    output=[]
    for drink in drinks:
        drink_obj={'name':drink.name,'description':drink.description}
        output.append(drink_obj)
    return jsonify({'drinks':output})

@app.route('/drinks/<int:id>',methods=['GET','POST'])
def get_drink(id):
    #drink = Drink.query.filter_by(id=id).first()
    drink = Drink.query.get_or_404(id)
    return jsonify({"name":drink.name,"description":drink.description})

@app.route('/add/drinks',methods=['POST'])
def add_drink():
    drink = Drink(name=request.json['name'],description=request.json['description'])
    db.session.add(drink)
    db.session.commit()
    return f"succesful adding  {drink.id}"

@app.route('/delete/drinks/<int:id>',methods=['DELETE'])
def delete_drink(id):
    drink = Drink.query.get(id)
    if drink is None:
        return {"error":"not found"}
    db.session.delete(drink)
    db.session.commit()
    return f"delete {drink.id} succesfully"

if __name__=='__main__':
    app.run(debug=True)
