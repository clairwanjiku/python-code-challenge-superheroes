from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from models import db, Power, Hero, HeroPower

# Initialize the Flask app instance
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Link the Flask app to the SQLAlchemy instance
db.init_app(app)

# Function to seed data into the database
def seed_data():
    # Fixed data for seeding
    powers_data = [
        {"name": "Flight", "description": "Ability to fly and soar through the skies"},
        {"name": "Telekinesis", "description": "Move objects using the power of the mind"},
        
        # Add more powers as needed
    ]

    heroes_data = [
        {"name": "Superman", "super_name": "Clark Kent"},
        {"name": "Wonder Woman", "super_name": "Diana Prince"},
        {"name": "Superman", "super_name": "Clark Kent"},
        {"name": "Wonder Woman", "super_name": "Diana Prince"},
        {"name": "Chrono Guardian", "super_name": "Time Weaver"},
        {"name": "Reality Shifter", "super_name": "Dimensional Dynamo"},
        {"name": "Energy Channeler", "super_name": "Luminescent Absorber"},
        {"name": "Molecular Sculptor", "super_name": "Quantum Morph"},
        {"name": "Psionic Sentinel", "super_name": "Thought Bender"},
        {"name": "Invisible Phantom", "super_name": "Vanishing Specter"},
        {"name": "Teleportation Master", "super_name": "Swift Jumper"},
        {"name": "Flora Sorcerer", "super_name": "Verdant Enchantress"},
        {"name": "Mind Dominator", "super_name": "Psyche Master"},
        {"name": "Gravity Warden", "super_name": "Graviton Guardian"},
        # Add more heroes as needed
    ]

    hero_powers_data = [
        {"strength": "Strong", "hero_name": "Superman", "power_name": "Flight"},
        {"strength": "Average", "hero_name": "Wonder Woman", "power_name": "Telekinesis"},
        # Assign more hero powers as needed
    ]

    # Populate Powers
    powers = []
    for power_info in powers_data:
        power = Power(**power_info)
        powers.append(power)

    db.session.add_all(powers)
    db.session.commit()

    # Populate Heroes
    heroes = []
    for hero_info in heroes_data:
        hero = Hero(**hero_info)
        heroes.append(hero)

    db.session.add_all(heroes)
    db.session.commit()

    # Populate HeroPowers
    for hero_power_info in hero_powers_data:
        hero = Hero.query.filter_by(name=hero_power_info["hero_name"]).first()
        power = Power.query.filter_by(name=hero_power_info["power_name"]).first()

        hero_power = HeroPower(
            strength=hero_power_info["strength"],
            hero=hero,
            power=power,
        )
        db.session.add(hero_power)

    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        seed_data()
