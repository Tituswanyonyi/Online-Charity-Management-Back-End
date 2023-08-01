from models import db,Donation,Donor,Ngo_donation_request,Admin,Ngo
from app import app
import random
from datetime import datetime


def seed():
    
    admin1 = Admin(
        name="Monica",
        email='monica@gmail.com',
    )
    admin1.set_password('password')

    admin2 = Admin(
        name='Benter',
        email='benter@gmail.com',
    )
    admin2.set_password('password')

    admin3 = Admin(
        name='Dan',
        email='dan@gmail.com',
    )
    admin3.set_password('password')
    db.session.add_all([admin1, admin2, admin3])
    db.session.commit()
    
    donor1 = Donor(
        name='Victor',
        email='john@example.com',
    )
    donor1.set_password('password123')

    donor2 = Donor(
        name='Titus',
        email='titus@gmail.com',
    )
    donor2.set_password('myp@ssw0rd')
    
    donor3 = Donor(
        name='Benta',
        email='benta@gmail.com',
    )
    donor3.set_password('myp@ssw0rd')

    
    db.session.add_all([donor1, donor2,donor3])
    db.session.commit()
    
    ngo1 = Ngo(
        org_name='Africa Harvest Biotech Foundation International',
        org_email='Kenya@africaharvest@gmail.com',
        org_address='PO Box 642-00621 Nairobi',
        registration_number=12345,
        location='Nairobi',
        donor_id=1,
    )
    ngo1.set_password('ngop@ssw0rd')

    ngo2 = Ngo(
        org_name='EngenderHealth',
        org_email='info@engenderhealth',
        org_address='PO Box: 57964, Nairobi ',
        registration_number=67890,
        location='ABC Place, Nairobi, Nairobi County, Kenya Waiyaki Way Parklands, Nairobi ',
        donor_id=2,
    )
    ngo2.set_password('password123')

    
    db.session.add_all([ngo1, ngo2])
    db.session.commit()
    
    
    
    donation1 = Donation(
        donor_name='Safaricom foundation',
        bank_name='National Bank',
        donated_amount=1000000,
        balance=0,
        ngo_id=1,       
        donor_id=1,     
        admin_id=None,  
        date_of_donation=datetime.utcnow(),  
    )

    donation2 = Donation(
        donor_name='KCB foundation',
        bank_name='KCB Bank',
        donated_amount=5000000,
        balance=0,
        ngo_id=2,       
        donor_id=2,     
        admin_id=None,  
        date_of_donation=datetime.utcnow(),  
    )
    db.session.add_all([donation1, donation2])
    db.session.commit()
    
    request1 = Ngo_donation_request(
        org_name='World Vision',
        org_email='worldvision@gmail.com',
        project_name='Protection of children',
        donation_purpose='Protection and saving chilldren',
        amount=1000,
        date=datetime.utcnow(),
        ngo_id=1,       
        admin_id=None,   
        donor_id=1,     
    )

    request2 = Ngo_donation_request(
        org_name='UNEP',
        org_email='	unepinfo@unep.org',
        project_name='Environmental Impact Assessment',
        donation_purpose='Environmental protection during construction activities',
        amount=5000000,
        date=datetime.utcnow(),
        ngo_id=2,       
        admin_id=None,  
        donor_id=2,     
    )
    db.session.add_all([request1, request2])
    db.session.commit()

    

with app.app_context():
    db.create_all()
    seed()
        
    