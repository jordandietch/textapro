from flask import current_app, Flask, flash, redirect, render_template, request
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
import os
import phonenumbers
from twilio.twiml.messaging_response import Message, MessagingResponse
from twilio.rest import Client
from wtforms import StringField
from wtforms import ValidationError
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
mail = Mail(app)
app.secret_key = 's3cr3t'
account_sid = "ACbf835e6507e16f25dd94f020295f21d3"
auth_token = "9c82b2d0d3d321d8d9216ae0578c2e0e"
twilio_client = Client(account_sid, auth_token)

from models import Lead
from _email import send_email


class PhoneForm(FlaskForm):
    telephone = StringField('Telephone', validators=[DataRequired()])

    def validate_phone(self, field):
        if len(self.data) > 16:
            raise ValidationError('Invalid phone number.')
        try:
            input_number = phonenumbers.parse(field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')
        except:
            input_number = phonenumbers.parse("+1"+field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')


@app.route('/', methods=('GET', 'POST'))
def index():
    form = PhoneForm()
    if form.validate_on_submit():
        try:
            telephone = form.telephone
            form.validate_phone(telephone)
            check_telephone = Lead.query.filter_by(telephone=telephone.data).first()
            if check_telephone is None:
                db.session.add(Lead(telephone.data))
                db.session.commit()
                twilio_client.messages.create(
                    to=telephone.data,
                    from_="+18057492645",
                    body="Text a pro test response!")
                send_email(current_app.config['MAIL_ADMIN'], 'Text a Pro Phone Number',
                           'mail/contact_me', telephone=telephone.data)
                flash('Thank You')
                return redirect('/thank-you')
            else:
                flash('Thank you for submitting. A contractor will reach out shortly.')
                return redirect('/')
        except Exception as e:
            print(e)
            flash('Please enter a valid phone number.')
            return redirect('/')

    return render_template('index.html', form=form)


@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')


@app.route("/pro-response", methods=['GET', 'POST'])
def pro_response():
    """Respond to incoming calls with a simple text message."""
    from_number = request.values.get('From')
    print(from_number)
    response = MessagingResponse()
    message = Message()
    message.body('Text a pro test response!')
    response.append(message)
    return str(response)


if __name__ == '__main__':
    app.run()
