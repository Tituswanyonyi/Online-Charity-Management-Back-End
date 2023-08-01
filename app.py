from flask import Flask,jsonify,request,make_response
from flask_migrate import Migrate
from flask_cors import CORS
from models import Admin,Donor,Ngo,Donation,db,Ngo_donation_request
import jwt
from datetime import datetime
from functools import wraps
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///charity_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = b'thisisthesecretkey'

migrate=Migrate(app, db)
db.init_app(app)

cors = CORS(app)
def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message':'token is missing!'})
        try:
            data = jwt.encode(token,app.config['SECRET_KEY'])
        except:
            return jsonify({'message':'token is invalid'})
        return f(*args,**kwargs)
    return decorated
            
                
            
@app.route('/unprotected')
def unprotected():
    return ({'message':'available for everyone'})
@app.route('/protected')
def protected():
    return ({'message':'only available for people with valid tokens'})

@app.route('/register')

@app.route('/login',methods = ['POST'])
def login():
    auth = request.authorization
    if auth and auth.password == '@d1234':
        token = jwt.encode({'user':auth.username,'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=30)},app.config['SECRET_KEY'])
        return jsonify({'token': token})
    return make_response('could not verify',401, {'WWW-Authenticate':'Basic realm="login Requires"'})


@app.route('/signup')
def signup():
    return 'Signup'
@app.route('/logout')

@app.route('/admins', methods=['GET'])
def get_admins():
    admins = Admin.query.all()
    admins_data = [
        {
            'id': admin.id,
            'name': admin.name,
            'email': admin.email,
        }
        for admin in admins
    ]

    return make_response(jsonify(admins_data), 200)
@app.route('/admins', methods=['POST'])
def create_admin():
    request_data = request.get_json()
    name = request_data.get('name')
    email = request_data.get('email')
    password = request_data.get('password')

    # Perform necessary validation on name and email fields (you can add more)

    
    new_admin = Admin(name=name, email=email,password = password)

    db.session.add(new_admin)
    db.session.commit()

    return make_response(jsonify({"message": "Admin created successfully", "id": new_admin.id}), 201)
    
@app.route('/admins/<int:id>',methods = ['GET', 'PATCH','DELETE'])
def get_admin(id):
    admin = Admin.query.filter(id==id).first()
    if request.method == 'GET':
        if not admin:
            return make_response(jsonify({"message": "Admin not found", "id":"admin_id"}), 404)
        admin_data = {
            'id': admin.id,
            'name': admin.name,
            'email': admin.email,
        }
        return make_response(jsonify(admin_data), 200)
    elif request.method == 'PATCH':
        if not admin:
            return make_response(jsonify({"message": "Admin not found"}), 404)
        request_data = request.get_json()

        admin.name = request_data.get('name', admin.name)
        admin.email = request_data.get('email', admin.email)
        admin.password = request_data.get('password',admin.password)

        # Perform necessary validation on name and email fields (you can add m
        db.session.commit()

        return make_response(jsonify({"message": "Admin updated successfully"}), 200)
    elif request.method == 'DELETE':
        if not admin:
            return make_response(jsonify({"message": "Admin not found"}), 404)

        db.session.delete(admin)
        db.session.commit()

        return make_response(jsonify({"message": "Admin deleted successfully"}), 200)

    else:
        return make_response(jsonify({"message": "Method not allowed"}), 405)
       
@app.route('/donors', methods = ['GET', 'POST'])
def get_donors():
    donors = Donor.query.all()
    donors_data = [
        {
            'id': donor.id,
            'name': donor.name,
            'email': donor.email,
            'password':donor.password
        }
        for donor in donors 
    ]

    return make_response(jsonify(donors_data), 200)
@app.route('/donors', methods=['POST'])
def new_donor():
    request_data = request.get_json()
    name = request_data.get('name')
    email = request_data.get('email')

    # Perform necessary validation on name and email fields (you can add more)

    new_donor = Donor(name=name, email=email)
    db.session.add(new_donor)
    db.session.commit()
    return make_response(jsonify({"message": "Donor created successfully", "id": new_donor.id}), 201)


@app.route('/donors/<int:id>', methods=['GET', 'DELETE'])
def donor(id):
    donor = Donor.query.filter_by(id=id).first()

    if request.method == 'GET':
        if not donor:
            return make_response(jsonify({"message": "Donor not found"}), 404)
        donor_data = {
            'id': donor.id,
            'name': donor.name,
            'email': donor.email,
        }
        return make_response(jsonify(donor_data), 200)

    elif request.method == 'DELETE':
        if not donor:
            return make_response(jsonify({"message": "Donor not found"}), 404)

        db.session.delete(donor)
        db.session.commit()

        return make_response(jsonify({"message": "Donor deleted successfully"}), 200)

    else:
        return make_response(jsonify({"message": "Method not allowed"}), 405)

@app.route('/ngos', methods=['GET', 'POST'])
def ngos():
    if request.method == 'GET':
        ngos = Ngo.query.all()

        ngos_data = [
            {
                'id': ngo.id,
                'org_name': ngo.org_name,
                'org_email': ngo.org_email,
                'org_address': ngo.org_address,
                'registration_number': ngo.registration_number,
                'location': ngo.location,
            }
            for ngo in ngos
        ]

        return make_response(jsonify(ngos_data), 200)
    elif request.method == 'POST':
        request_data = request.get_json()
        org_name = request_data.get('org_name')
        org_email = request_data.get('org_email')
        org_address = request_data.get('org_address')
        registration_number = request_data.get('registration_number')
        location = request_data.get('location')
        password = request_data.get('password')
        confirm_password = request_data.get('confirm_password')

        # Perform necessary validation on the data fields (you can add more)

        new_ngo = Ngo(
            org_name=org_name,
            org_email=org_email,
            org_address=org_address,
            registration_number=registration_number,
            location=location,
            password=password,
            confirm_password=confirm_password
        )

        db.session.add(new_ngo)
        db.session.commit()

        return make_response(jsonify({"message": "Ngo created successfully", "id": new_ngo.id}), 201)

    else:
        return make_response(jsonify({"message": "Method not allowed"}), 405)
    
@app.route('/ngos/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def ngo(id):
    ngo = Ngo.query.filter_by(id=id).first()

    if not ngo:
        return make_response(jsonify({"message": "Ngo not found"}), 404)

    if request.method == 'GET':
        ngo_data = {
            'id': ngo.id,
            'org_name': ngo.org_name,
            'org_email': ngo.org_email,
            'org_address': ngo.org_address,
            'registration_number': ngo.registration_number,
            'location': ngo.location,
        }
        return make_response(jsonify(ngo_data), 200)
    elif request.method == 'PATCH':
        request_data = request.get_json()
        ngo.org_name = request_data.get('org_name', ngo.org_name)
        ngo.org_email = request_data.get('org_email', ngo.org_email)
        ngo.org_address = request_data.get('org_address', ngo.org_address)
        ngo.registration_number = request_data.get('registration_number', ngo.registration_number)
        ngo.location = request_data.get('location', ngo.location)

        # Perform necessary validation on the data fields (you can add more)

        db.session.commit()

        return make_response(jsonify({"message": "Ngo updated successfully"}), 200)
    elif request.method == 'DELETE':
        db.session.delete(ngo)
        db.session.commit()

        return make_response(jsonify({"message": "Ngo deleted successfully"}), 200)
    else:
        return make_response(jsonify({"message": "Method not allowed"}), 405)

@app.route('/donations',methods = ['GET', 'POST'])

def get_all_donation():
    if request.method == 'GET':
        donations = Donation.query.all()

        donations_data = [
            {
                'id': donation.id,
                'donor_name': donation.donor_name,
                'bank_name': donation.bank_name,
                'donated_amount': donation.donated_amount,
                'date_of_donation': donation.date_of_donation,
                'balance': donation.balance,
                'donor_id': donation.donor_id,
                'ngo_id': donation.ngo_id,
                'admin_id': donation.admin_id,
            }
            for donation in donations
        ]

        return make_response(jsonify(donations_data), 200)
    elif request.method == 'POST':
        request_data = request.get_json()
        donor_name = request_data.get('donor_name')
        bank_name = request_data.get('bank_name')
        donated_amount = request_data.get('donated_amount')
        date_of_donation = request_data.get('date_of_donation')
        donor_id = request_data.get('donor_id')
        ngo_id = request_data.get('ngo_id')
        admin_id = request_data.get('admin_id')

        # Perform necessary validation on the data fields (you can add more)
        new_donation = Donation(
            donor_name=donor_name,
            bank_name=bank_name,
            donated_amount=donated_amount,
            date_of_donation=date_of_donation,
            donor_id=donor_id,
            ngo_id=ngo_id,
            admin_id=admin_id
        )

        db.session.add(new_donation)
        db.session.commit()

        return make_response(jsonify({"message": "Donation made successfully", "id": new_donation.id}), 201)




@app.route('/donations/<int:id>', methods=['GET',  'PATCH','DELETE'])
def get_donation_by_id(id):
    donation = Donation.query.filter_by(id=id).first()

    if not donation:
        return make_response(jsonify({"message": "Donation not found"}), 404)

    if request.method == 'GET':
        donation_data = {
            'id': donation.id,
            'donor_name': donation.donor_name,
            'bank_name': donation.bank_name,
            'donated_amount': donation.donated_amount,
            'date_of_donation': datetime.utcnow(),
            'balance': donation.balance,
            'donor_id': donation.donor_id,
            'ngo_id': donation.ngo_id,
            'admin_id': donation.admin_id,
        }
        return make_response(jsonify(donation_data), 200)
    elif request.method == 'PATCH':
        request_data = request.get_json()
        donation.donor_name = request_data.get('donor_name', donation.donor_name)
        donation.bank_name = request_data.get('bank_name', donation.bank_name)
        donation.donated_amount = request_data.get('donated_amount', donation.donated_amount)
        donation.date_of_donation = request_data.get('date_of_donation', donation.date_of_donation)
        donation.balance = request_data.get('balance', donation.balance)
        donation.donor_id = request_data.get('donor_id', donation.donor_id)
        donation.ngo_id = request_data.get('ngo_id', donation.ngo_id)
        donation.admin_id = request_data.get('admin_id', donation.admin_id)

        # Perform necessary validation on the data fields (you can add more)

        db.session.commit()
        return make_response(jsonify({"message": "Donation made successfully"}), 200)
    elif request.method == 'DELETE':
        db.session.delete(donation)
        db.session.commit()
        return make_response(jsonify({"message": "Donation deleted successfully"}), 200)

    else:
        return make_response(jsonify({"message": "Method not allowed"}), 405)


@app.route('/ngo_donation_requests',methods = ['GET', 'POST'])
def ngo_donation_requests():
    if request.method == 'GET':
        ngo_donation_requests = Ngo_donation_request.query.all()

        ngo_donation_requests_data = [
            {
                'requests_id': ngo_donation_requests.id,
                'org_name': ngo_donation_requests.org_name,
                'org_email': ngo_donation_requests.org_email,
                'project_name': ngo_donation_requests.project_name,
                'donation_purpose': ngo_donation_requests.donation_purpose,
                'amount': ngo_donation_requests.amount,
                'date': ngo_donation_requests.date,
                'ngo_id': ngo_donation_requests.ngo_id,
                'admin_id': ngo_donation_requests.admin_id,
            }
            for ngo_donation_requests in ngo_donation_requests
        ]

        return make_response(jsonify(ngo_donation_requests_data), 200)
    elif request.method == 'POST':
        request_data = request.get_json()
        org_name = request_data.get('org_name')
        org_email = request_data.get('org_email')
        project_name = request_data.get('project_name')
        donation_purpose = request_data.get('donation_purpose')
        amount = request_data.get('amount')
        date = request_data.get('date')
        ngo_id = request_data.get('ngo_id')
        admin_id = request_data.get('admin_id')

        # Perform necessary validation on the data fields (you can add more)
        new_request = ngo_donation_requests(
            org_name=org_name,
            org_email=org_email,
            project_name=project_name,
            donation_purpose=donation_purpose,
            amount=amount,
            date=date,
            ngo_id=ngo_id,
            admin_id=admin_id
        )

        
        db.session.add(new_request)
        db.session.commit()
        return make_response(jsonify({"message": "Ngo donation request created successfully", "id": new_request.id}), 201)

    else:
        return make_response(jsonify({"message": "Method not allowed"}), 405)


@app.route('/ngo_donation_requests/<int:id>',methods =['GET','PATCH','DELETE'])

def ngo_donation_requests_by_id(id):
    ngo_donation_requests = Ngo_donation_request.query.filter_by(id=id).first()

    if not ngo_donation_requests:
        return make_response(jsonify({"message": "Ngo donation request not found"}), 404)

    if request.method == 'GET':
        requests_data = {
            'id': ngo_donation_requests.id,
            'org_name': ngo_donation_requests.org_name,
            'org_email': ngo_donation_requests.org_email,
            'project_name': ngo_donation_requests.project_name,
            'donation_purpose': ngo_donation_requests.donation_purpose,
            'amount': ngo_donation_requests.amount,
            'date': ngo_donation_requests.date.isoformat(),
            'ngo_id': ngo_donation_requests.ngo_id,
            'admin_id': ngo_donation_requests.admin_id,
        }
        return make_response(jsonify(requests_data), 200)

    elif request.method == 'PATCH':
        request_data = request.get_json()
        ngo_donation_requests.org_name = request_data.get('org_name', ngo_donation_requests.org_name)
        ngo_donation_requests.org_email = request_data.get('org_email', ngo_donation_requests.org_email)
        ngo_donation_requests.project_name = request_data.get('project_name', ngo_donation_requests.project_name)
        ngo_donation_requests.donation_purpose = request_data.get('donation_purpose', ngo_donation_requests.donation_purpose)
        ngo_donation_requests.amount = request_data.get('amount', ngo_donation_requests.amount)
        ngo_donation_requests.date = request_data.get('date', ngo_donation_requests.date)
        ngo_donation_requests.ngo_id = request_data.get('ngo_id', ngo_donation_requests.ngo_id)
        ngo_donation_requests.admin_id = request_data.get('admin_id', ngo_donation_requests.admin_id)

        # Perform necessary validation on the data fields (you can add more)

        db.session.commit()
        return make_response(jsonify({"message": "Ngo donation request updated successfully"}), 200)

    elif request.method == 'DELETE':
        db.session.delete(ngo_donation_requests)
        db.session.commit()
        return make_response(jsonify({"message": "Ngo donation request deleted successfully"}), 200)

    else:
        return make_response(jsonify({"message": "Method not allowed"}), 405)




# input validators
# validate input for email in the login
# validate password
# authentication using JWT 
# authentication for NGo,
# /login,/register,/signup, logout,then will directed to NGO dashboard
# import redirect and JWT