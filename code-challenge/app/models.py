from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Power(db.Model):
    __tablename__ = 'power'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    # Define the back_populates attribute
    hero_powers = db.relationship('HeroPower', back_populates='power', lazy=True)

    @validates('description')
    def validate_description(self, key, value):
        if not value or len(value) < 20:
            raise ValueError('Description must be present and at least 20 characters long')
        return value

class Hero(db.Model):
    __tablename__ = 'hero'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    super_name = db.Column(db.String(255), nullable=False)

    hero_powers = db.relationship('HeroPower', back_populates='hero', lazy=True)

class HeroPower(db.Model):
    __tablename__ = 'hero_power'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(255), nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('power.id'), nullable=False)

    # Define the back_populates attribute
    power = db.relationship('Power', back_populates='hero_powers')
    hero = db.relationship('Hero', back_populates='hero_powers')

    @validates('strength')
    def validate_strength(self, key, value):
        valid_strengths = ['Strong', 'Weak', 'Average']
        if value not in valid_strengths:
            raise ValueError('Invalid strength value')
        return value
