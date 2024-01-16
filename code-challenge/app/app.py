#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from sqlalchemy.orm import validates

from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

with app.app_context():
    @app.route('/')
    def home():
        return ''

    @app.route('/heroes', methods=['GET'])
    def get_heroes():
        heroes = Hero.query.all()
        heroes_data = [
            {"id": hero.id, "name": hero.name, "super_name": hero.super_name}
            for hero in heroes
        ]
        return jsonify(heroes_data)

    # Route to get a specific hero by ID
                # Route to get a specific hero by ID
    @app.route('/heroes/<int:id>', methods=['GET'])
    def get_hero_by_id(id):
                hero = Hero.query.get(id)
                if hero:
                    hero_data = {
                        "id": hero.id,
                        "name": hero.name,
                        "super_name": hero.super_name,
                        "powers": [
                            {"id": hp.power.id, "name": hp.power.name, "description": hp.power.description}
                            for hp in hero.hero_powers  # Use hero.hero_powers instead of hero.powers
                        ]
                    }
                    return jsonify(hero_data)
                else:
                    return jsonify({"error": "Hero not found"}), 404


    # Route to get all powers
    @app.route('/powers', methods=['GET'])
    def get_powers():
        powers = Power.query.all()
        powers_data = [
            {"id": power.id, "name": power.name, "description": power.description}
            for power in powers
        ]
        return jsonify(powers_data)

    # Route to get a specific power by ID
    @app.route('/powers/<int:id>', methods=['GET'])
    def get_power_by_id(id):
        power = Power.query.get(id)
        if power:
            power_data = {"id": power.id, "name": power.name, "description": power.description}
            return jsonify(power_data)
        else:
            return jsonify({"error": "Power not found"}), 404

    # Route to update a power by ID
    @app.route('/powers/<int:id>', methods=['PATCH'])
    def update_power(id):
        power = Power.query.get(id)
        if power:
            try:
                data = request.get_json()
                power.description = data['description']
                db.session.commit()
                return jsonify({"id": power.id, "name": power.name, "description": power.description})
            except ValueError as e:
                return jsonify({"errors": [str(e)]}), 400
        else:
            return jsonify({"error": "Power not found"}), 404

    # Route to create a new hero power
    @app.route('/hero_powers', methods=['POST'])
    def create_hero_power():
        try:
            data = request.get_json()
            hero_id = data['hero_id']
            power_id = data['power_id']
            strength = data['strength']

            hero = Hero.query.get(hero_id)
            power = Power.query.get(power_id)

            if hero and power:
                hero_power = HeroPower(strength=strength, hero=hero, power=power)
                db.session.add(hero_power)
                db.session.commit()

                # Fetch the hero again to get the updated hero_powers relationship
                hero = Hero.query.get(hero_id)

                hero_data = {
                    "id": hero.id,
                    "name": hero.name,
                    "super_name": hero.super_name,
                    "powers": [
                        {"id": hp.power.id, "name": hp.power.name, "description": hp.power.description}
                        for hp in hero.hero_powers  # Use hero.hero_powers instead of hero.powers
                    ]
                }
                return jsonify(hero_data)
            else:
                return jsonify({"errors": ["Invalid hero_id or power_id"]}), 400

        except ValueError as e:
            return jsonify({"errors": [str(e)]}), 400



    if __name__ == '__main__':
        app.run(port=5555)