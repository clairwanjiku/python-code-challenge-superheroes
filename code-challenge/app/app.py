#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import db, Hero, Power, HeroPower



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

# Validation functions
def validate_strength(strength):
    valid_strengths = ['Strong', 'Weak', 'Average']
    return strength in valid_strengths

def validate_description(description):
    return len(description) >= 20

# Routes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    heroes_data = [{'id': hero.id, 'name': hero.name, 'super_name': hero.super_name} for hero in heroes]
    return jsonify(heroes_data)

@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if hero:
        hero_data = {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name,
            'powers': [{'id': power.id, 'name': power.name, 'description': power.description} for power in hero.powers]
        }
        return jsonify(hero_data)
    else:
        return jsonify({'error': 'Hero not found'}), 404

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    powers_data = [{'id': power.id, 'name': power.name, 'description': power.description} for power in powers]
    return jsonify(powers_data)

@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if power:
        power_data = {'id': power.id, 'name': power.name, 'description': power.description}
        return jsonify(power_data)
    else:
        return jsonify({'error': 'Power not found'}), 404

@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({'error': 'Power not found'}), 404

    data = request.get_json()
    if 'description' in data:
        description = data['description']
        if not validate_description(description):
            return jsonify({'errors': ['Invalid description. It must be at least 20 characters long']}), 400

        power.description = description
        db.session.commit()

        updated_power = {'id': power.id, 'name': power.name, 'description': power.description}
        return jsonify(updated_power)

    return jsonify({'error': 'Invalid data'}), 400

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()

    hero_id = data.get('hero_id')
    power_id = data.get('power_id')
    strength = data.get('strength')

    if not hero_id or not power_id or not strength:
        return jsonify({'errors': ['Hero ID, Power ID, and Strength are required']}), 400

    if not validate_strength(strength):
        return jsonify({'errors': ['Invalid strength value']}), 400

    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)

    if not hero or not power:
        return jsonify({'errors': ['Hero or Power not found']}), 404

    # Check if HeroPower already exists
    existing_hero_power = HeroPower.query.filter_by(hero_id=hero_id, power_id=power_id).first()
    if existing_hero_power:
        return jsonify({'errors': ['HeroPower already exists']}), 400

    hero_power = HeroPower(hero=hero, power=power, strength=strength)
    db.session.add(hero_power)
    db.session.commit()

    hero_data = {
        'id': hero.id,
        'name': hero.name,
        'super_name': hero.super_name,
        'powers': [{'id': power.id, 'name': power.name, 'description': power.description} for power in hero.powers]
    }

    return jsonify(hero_data), 201



if __name__ == '__main__':
    app.run(port=5555)
