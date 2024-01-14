from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Hero(db.Model):
    __tablename__ = 'hero'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    super_name = db.Column(db.String(255), nullable=False)
    hero_powers = db.relationship('HeroPower', back_populates='hero')
    powers = db.relationship('Power', secondary='hero_power', back_populates='heroes')

# add any models you may need. 

class Power(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    power_heroes = db.relationship('HeroPower', back_populates='power')
    heroes = db.relationship('Hero', secondary='hero_power', back_populates='powers')
