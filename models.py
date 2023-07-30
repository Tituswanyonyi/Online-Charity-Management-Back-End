
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///charity_management.db'
db = SQLAlchemy(app)

class Admin(db.Model,SerializerMixin):
    __tablename__ = 'admins'
    id = db.Column(db.Integer(),primary_key=True )
    name = db.Column(db.String(100))
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))
    

    def __repr__(self):
        return f'{self.id},{self.name},{self.email},{self.password}'
    
class Donor(db.Model,SerializerMixin):
    __tablename__= 'donors'
    id = db.Column(db.Integer(),primary_key=True )
    name = db.Column(db.String(100))
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))
    
    def __repr__(self):
        return f'{self.id},{self.name},{self.email}{self.password}'
    
    
    
    
class Ngo(db.Model,SerializerMixin):
    __tablename__ = 'ngos'
    id = db.Column(db.Integer(),primary_key = True)
    org_name = db.Column(db.String(100))
    org_email = db.Column(db.String(50))
    org_address = db.Column(db.String())
    registration_number = db.Column(db.Integer())
    location =db.Column(db.String())
    password = db.Column(db.String(50))
    confirm_password = db.Column(db.String())
    donor_id = db.Column(db.Integer, db.ForeignKey('donors.id'))
    donor = db.relationship('Donor', backref='ngos')
    
    
    def __repr__(self):
        return f'{self.id},{self.org_name},{self.org_email},{self.org_address},{self.registration_number} {self.location}{self.password}{self.confirm_password}'
    
class Donation(db.Model,SerializerMixin):
    __tablename__ = 'donations'
    id = db.Column(db.Integer(),primary_key= True)
    donor_name =db.Column(db.String(50))
    bank_name = db.Column(db.String())
    donated_amount = db.Column(db.Integer())
    date_of_donation = db.Column(db.DateTime,server_default= db.func.now())
    balance = db.Column(db.Integer())
    ngo_id = db.Column(db.Integer, db.ForeignKey('ngos.id'))
    donor_id = db.Column(db.Integer, db.ForeignKey('donors.id'))
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'))
    
    donor = db.relationship('Donor', backref='donation')
    ngo = db.relationship('Ngo', backref='donation')
    admin = db.relationship('Admin', backref='donation')
    
    def __repr__(self):
        return f'{self.id},{self.donor_name},{self.bank_name}{self.donated_amount}{self.date_of_donation}{self.balance}{self.ngo_id}{self.admin_id}{self.donor_id}' 
    
class Ngo_donation_request(db.Model,SerializerMixin):
    __tablename__ = 'ngo_donation_requests'
    id = db.Column(db.Integer(), primary_key = True)
    org_name = db.Column(db.String(50))
    org_email = db.Column(db.String(50))
    project_name = db.Column(db.String(50))
    donation_purpose = db.Column(db.String())
    amount = db.Column(db.Integer())
    date = db.Column(db.Date())
    ngo_id = db.Column(db.Integer, db.ForeignKey('ngos.id'))
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'))
    donor_id = db.Column(db.Integer, db.ForeignKey('donors.id'))
    ngo = db.relationship('Ngo', backref='ngo_donation_request')
    donor = db.relationship('Donor', backref='ngo_donation_request')
    
    
    
    def __repr__(self):
        return f'{self.id},{self.org_name}{self.org_email}{self.project_name}{self.donation_purpose}{self.amount}{self.date}{self.ngo_id},{self.admin_id}'
    
        
with app.app_context():
    db.create_all()     