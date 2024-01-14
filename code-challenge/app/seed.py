from models import db, Hero, Power, HeroPower

# Initialize the Flask application and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create a context to bind the SQLAlchemy app and the app context
with app.app_context():
    # Drop existing tables and recreate them
    db.drop_all()
    db.create_all()

    # Create sample heroes
    hero1 = Hero(name='Tony Stark', super_name='Iron Man')
    hero2 = Hero(name='Steve Rogers', super_name='Captain America')
    hero3 = Hero(name='Natasha Romanoff', super_name='Black Widow')

    # Create sample powers
    power1 = Power(name='Flight', description='Enables the ability to fly at high speeds')
    power2 = Power(name='Super Strength', description='Grants superhuman strength')
    power3 = Power(name='Invisibility', description='Allows the user to become invisible')

    # Add heroes and powers to the session
    db.session.add_all([hero1, hero2, hero3, power1, power2, power3])
    db.session.commit()

    # Create sample hero powers
    hero_power1 = HeroPower(hero=hero1, power=power1, strength='Strong')
    hero_power2 = HeroPower(hero=hero1, power=power2, strength='Average')
    hero_power3 = HeroPower(hero=hero2, power=power3, strength='Weak')

    # Add hero powers to the session
    db.session.add_all([hero_power1, hero_power2, hero_power3])
    db.session.commit()



