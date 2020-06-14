from flask import jsonify, request, Flask
from flask_mail import Message, Mail
from flask_cors import CORS
import os


app = Flask(__name__)
cors = CORS(app)
mail = Mail()

app.config["MAIL_SERVER"] = "smtp.gmail.com" #gmail smtp settings
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = os.environ.get('DB_USER')
app.config["MAIL_PASSWORD"] = os.environ.get('DB_PASS')

mail.init_app(app)

@app.route('/contact', methods=['POST'])
def contact():
    data = request.get_json()
    name = data['name']
    email = data['email']
    subject = data['subject']
    message = data['message']

    msg = Message(subject, sender=email, recipients=[os.environ.get('DB_USER')])
    msg.body = """
    From: {} <{}>
    {}
    """.format(name, email, message)
    mail.send(msg)

@app.errorhandler(404)
def err_404(e):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(405)
def err_405(e):
    return jsonify({"error":"method not allowed"})

