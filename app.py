import os
# from cloudinary.uploader import upload
import base64
import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth
from flask import Flask,jsonify,request,make_response,current_app
from flask_migrate import Migrate
from flask_cors import CORS
from models import Admin,Donor,Ngo,Donation,db,Ngo_donation_request
import jwt
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_mail import Message,Mail
from config import Config
from flask_jwt_extended import JWTManager, create_access_token
import bcrypt
import cloudinary
# import cloudinary.uploader
from werkzeug.utils import secure_filename

from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///charity_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'abvsjdgdb'
cloudinary.config(
    cloud_name='de2douzby',
    api_key='483724135818845',
    api_secret='t7-8D3imhX3u4T8ur9hVhAxFUFM'
)


jwt = JWTManager(app)
app.config.from_object(Config)
mail = Mail(app)
migrate=Migrate(app, db)
db.init_app(app)
cors = CORS(app)


UPLOAD_FOLDER = '/home/moringa/Desktop/code/phase-5/Online-Charity-Management-Back-End'
ALLOWED_EXTENSIONS = set(['txt','pdf','png','jpg','gif'])
def allowed_file(filename):
    return '.'in filename and filename.rsplit('.',1)[1].lower()in ALLOWED_EXTENSIONS
app.config['UPLOAD_FOLDER']= UPLOAD_FOLDER


@app.route('/upload',methods=['POST'])
def upload_media():
    if 'file' not in request.files:
        return jsonify({'error':'media not provided'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error':'no file selected'}),400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        return jsonify({'msg':'media uploaded successfully'})
        
         
# cloudinary.config(cloud_name = os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), 
#     api_secret=os.getenv('API_SECRET'))


# cloudinary.config(
#     cloud_name='your_cloud_name',
#     api_key='123456789we',
#     api_secret='thisisthesecret'
# )

# # Upload an image
# file_path = os.path.abspath("Desktop/code/phase-5/Online-Charity-Management-Back-End")
# result = upload(file_path)
# from werkzeug.utils import secure_filename
# UPLOAD_FOLDER = '/home/moringa/Desktop/code/phase-5/Online-Charity-Management-Back-End'
# ALLOWED_EXTENSIONS = set(['txt','pdf','png','jpg','gif'])
# def allowed_file(filename):
#     return '.'in filename and filename.rsplit('.',1)[1].lower()in ALLOWED_EXTENSIONS




            

USER_TYPES = ['admin', 'ngo', 'donor']
USER_TYPE_CLASSES = {
    'admin': Admin,
    'ngo': Ngo,
    'donor': Donor
}

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    user_type = data.get('user_type')

    if not all([username, email, password, user_type]):
        return jsonify({'error': 'Missing required fields.',
                        'responseCode': 400}), 400

    user_class = USER_TYPE_CLASSES.get(user_type.lower())
    if not user_class:
        return jsonify({'error': 'Invalid user_type.',
                        'responseCode': 400}), 400

    hashed_password = generate_password_hash(password)
    new_user = user_class(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    welcome_message = f"Welcome, {username}! You have successfully registered."

    return jsonify({'message': welcome_message,
                    'responseCode': 201}), 201



# @app.route('/verify_email/<token>', methods=['GET'])
# def verify_email(token):
#     user = user_class.query.filter_by(verification_token=token).first()
#     if user:
#         user.verification_token = None
#         user.is_verified = True
#         db.session.commit()
#         return render_template('email_verified.html', message='Email verification successful!')
#     else:
#         return render_template('email_verified.html', message='Invalid or expired verification token.')
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user_type = request.json.get('user_type')  

    if not username or not password or not user_type:
        return jsonify({'error': 'Username, password, and user_type are required.'}), 400

    user_class = USER_TYPE_CLASSES.get(user_type.lower())
    if not user_class:
        return jsonify({'error': 'Invalid user_type.'}), 400

    user = user_class.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):  # Check the password using bcrypt
        access_token = create_access_token(identity={'username': username, 'user_type': user_type})
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'error': 'Invalid username or password.'}), 401


my_endpoint = 'https://ab92-102-213-93-55.ngrok-free.app'
@app.route('/pay',methods=['POST'])
def MpesaExpress():
    if request.method == 'POST':
        data = request.get_json()
        amount = data.get('amount')
        phoneNumber = data.get('phoneNumber')
        print(phoneNumber)
        # Safaricom M-Pesa API request
        endpoint = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
        access_token = getAccessToken()  # Assuming you have this function implemented to get the access token
        headers = {"Authorization": "Bearer %s" % access_token}
        Timestamp = datetime.now()
        times = Timestamp.strftime("%Y%m%d%H%M%S")
        password_str = "174379" + "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919" + times
        password_bytes = password_str.encode('utf-8')
        password = base64.b64encode(password_bytes).decode('utf-8')
        # password = hashlib.sha1(password_bytes).hexdigest()
    data = {
        "BusinessShortCode": "174379",
        "Password": password,
        "Timestamp": times,
        "TransactionType": "CustomerPayBillOnline",
        "PartyA": phoneNumber,
        "PartyB": "174379",
        "PhoneNumber":phoneNumber,
        "CallBackURL": my_endpoint + '/lnmo-callback',
        "AccountReference": "TestPay",
        "TransactionDesc": "HelloTest",
        "Amount": amount
    }
    res = requests.post(endpoint, json=data, headers=headers)
    print(res)
    response_json = res.json()
@app.route('/lnmo-callback', methods=['POST'])
def incoming():
    data = request.get_json()
    print(data)
    return 'ok'

def getAccessToken():
    consumer_key = "k32F8H8rh9CHOxGhuQCqqKALJRF1aAz0"
    consumer_secret = "FwyAyldHKLpzdKnH"
    endpoint = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r = requests.get(endpoint, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    data = r.json()
    return data['access_token']


@app.route("/upload", methods=['POST'])
def upload_file():
  app.logger.info('in upload route')

  cloudinary.config(cloud_name = os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), 
    api_secret=os.getenv('API_SECRET'))
  upload_result = None
  if request.method == 'POST':
    file_to_upload = request.files['file']
    app.logger.info('%s file_to_upload', file_to_upload)
    if file_to_upload:
      upload_result = cloudinary.uploader.upload(file_to_upload)
      app.logger.info(upload_result)
      return jsonify(upload_result)



   
@app.route('/admins', methods=['GET'])
def get_admins():
    admins = Admin.query.all()
    admins_data = [
        {
            'id': admin.id,
            'username': admin.username,
            'email': admin.email,
        }
        for admin in admins
    ]

    return make_response(jsonify(admins_data), 200)
@app.route('/admins', methods=['POST'])
def create_admin():
    request_data = request.get_json()
    username = request_data.get('username')
    email = request_data.get('email')
    password = request_data.get('password')

    new_admin = Admin(username=username, email=email,password = password)

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
            'username': admin.username,
            'email': admin.email,
        }
        return make_response(jsonify(admin_data), 200)
    elif request.method == 'PATCH':
        if not admin:
            return make_response(jsonify({"message": "Admin not found"}), 404)
        request_data = request.get_json()

        admin.username = request_data.get('username', admin.username)
        admin.email = request_data.get('email', admin.email)
        admin.password = request_data.get('password',admin.password)

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
            'username': donor.username,
            'email': donor.email,
            'password':donor.password
        }
        for donor in donors 
    ]

    return make_response(jsonify(donors_data), 200)
@app.route('/donors', methods=['POST'])
def new_donor():
    request_data = request.get_json()
    username = request_data.get('username')
    email = request_data.get('email')


    new_donor = Donor(username=username, email=email)
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
            'username': donor.username,
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
                'username': ngo.username,
                'email': ngo.email,
                'org_address': ngo.org_address,
                'registration_number': ngo.registration_number,
                'location': ngo.location,
                'is_verified': ngo.is_verified,
            }
            for ngo in ngos
        ]

        return make_response(jsonify(ngos_data), 200)
    elif request.method == 'POST':
        request_data = request.get_json()
        username = request_data.get('org_name')
        email = request_data.get('org_email')
        org_address = request_data.get('org_address')
        registration_number = request_data.get('registration_number')
        location = request_data.get('location')
        password = request_data.get('password')
        confirm_password = request_data.get('confirm_password')
        is_verified = request_data.get('is_verified')


        new_ngo = Ngo(
            username=username,
            email=email,
            org_address=org_address,
            registration_number=registration_number,
            location=location,
            password=password,
            confirm_password=confirm_password,
            is_verified=False
            
            
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
            'username': ngo.username,
            'email': ngo.email,
            'org_address': ngo.org_address,
            'registration_number': ngo.registration_number,
            'location': ngo.location,
        }
        return make_response(jsonify(ngo_data), 200)
    elif request.method == 'PATCH':
        request_data = request.get_json()
        username = request_data.get('ngo.username')
        email = request_data.get('ngo.email' )
        ngo.org_address = request_data.get('org_address', ngo.org_address)
        ngo.registration_number = request_data.get('registration_number', ngo.registration_number)
        ngo.location = request_data.get('location', ngo.location)


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

      

        db.session.commit()
        return make_response(jsonify({"message": "Ngo donation request updated successfully"}), 200)

    elif request.method == 'DELETE':
        db.session.delete(ngo_donation_requests)
        db.session.commit()
        return make_response(jsonify({"message": "Ngo donation request deleted successfully"}), 200)

    else:
        return make_response(jsonify({"message": "Method not allowed"}), 405)




