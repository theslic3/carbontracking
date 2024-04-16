from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Footprint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #user = db.relationship('Users', backref=db.backref('footprints', lazy=True))
    electricity_emission_factor = db.Column(db.Float, nullable=False)
    heating_emission_factor = db.Column(db.Float, nullable=False)
    car_emission_factor = db.Column(db.Float, nullable=False)
    flight_emission_factor = db.Column(db.Float, nullable=False)
    meat_and_dairy_emission_factor = db.Column(db.Float, nullable=False)
    grocery_emission_factor = db.Column(db.Float, nullable=False)
    goods_emission_factor = db.Column(db.Float, nullable=False)
    services_emission_factor = db.Column(db.Float, nullable=False)
    waste_emission_factor = db.Column(db.Float, nullable=False)
    water_emission_factor = db.Column(db.Float, nullable=False)
    household_size = db.Column(db.Integer, nullable=False)
    income_category = db.Column(db.String(255), nullable=False)
    recycling_status = db.Column(db.String(255), nullable=False)
    total_carbon_footprint = db.Column(db.Float, nullable=False)
    forecasted_annual_footprint = db.Column(db.Float, nullable=False)
    regional_annual_average_per_person = db.Column(db.Float, nullable=False)
    UK_annual_average_per_person = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def to_dict(self):
        return {
            'electricity_emission_factor': self.electricity_emission_factor,
            'heating_emission_factor': self.heating_emission_factor,
            'car_emission_factor': self.car_emission_factor,
            'flight_emission_factor': self.flight_emission_factor,
            'meat_and_dairy_emission_factor': self.meat_and_dairy_emission_factor,
            'grocery_emission_factor': self.grocery_emission_factor,
            'goods_emission_factor': self.goods_emission_factor,
            'services_emission_factor': self.services_emission_factor,
            'waste_emission_factor': self.waste_emission_factor,
            'water_emission_factor': self.water_emission_factor,
            'household_size': self.household_size,
            'income_category': self.income_category,
            'recycling_status': self.recycling_status,
            'total_carbon_footprint': self.total_carbon_footprint,
            'forecasted_annual_footprint': self.forecasted_annual_footprint,
            'regional_annual_average_per_person': self.regional_annual_average_per_person,
            'UK_annual_average_per_person': self.UK_annual_average_per_person,
            # add all other fields you need to include in the dictionary
        }

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    footprints = db.relationship('Footprint', backref='user', lazy=True)
    footprints = db.relationship('Test', backref='user', lazy=True)


'''
@views.route('/recent_footprint', methods=['GET'])
@login_required
def recent_footprint():
    user_id = session.get('user_id')  # Assuming you stored the user ID in the session during login

    if user_id:
        # Query the database for the user's footprints and retrieve the most recent one
        recent_footprint = Footprint.query.filter_by(user_id=user_id).order_by(Footprint.date.desc()).first()

        if recent_footprint:
            # Do something with the most recent footprint, such as displaying it in a template
            return render_template('recent_footprint.html', recent_footprint=recent_footprint)
        else:
            # Handle the case where the user has no footprints
            return render_template('no_footprints.html')
    else:
        # Handle the case where there's no user ID in the session (user not logged in)
        return redirect(url_for('auth.signin'))
'''
