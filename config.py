from flask import Flask
from flask_mail import Mail, Message

class Config:
    DEBUG = True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'monijerobon@gmail.com'
    MAIL_PASSWORD = '35233631@Mo'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

app = Flask(__name__)
app.config.from_object(Config)

mail = Mail(app)

@app.route("/")
def index():
   msg = Message(
                'Hello',
                sender ='yourId@gmail.com',
                recipients = ['receiver’sid@gmail.com']
               )
   msg.body = 'Hello Flask message sent from Flask-Mail'
   mail.send(msg)
   return 'Sent'

if __name__ == '__main__':
   app.run(debug=True)
