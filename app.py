from datetime import datetime, timedelta
from flask import current_app, Flask, flash, redirect, render_template, request, session
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
import os
import phonenumbers
import re
from twilio.twiml.messaging_response import Message, MessagingResponse
from twilio.rest import Client
from wtforms import StringField, ValidationError, validators

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
mail = Mail(app)
app.secret_key = 's3cr3t'
ACCOUNT_SID = os.environ.get('ACCOUNT_SID')
AUTH_TOKEN = os.environ.get('AUTH_TOKEN')
twilio_client = Client(ACCOUNT_SID, AUTH_TOKEN)

from models import Lead
from _email import send_email


def get_timedelta(a_datetime):
    return datetime.today() - a_datetime


def remove_telephone_chars(telephone):
    if telephone.startswith('+1'):
        return re.sub("\D", "", telephone[2:])
    else:
        return re.sub("\D", "", telephone)


def message_admin(from_phone):
    twilio_client.messages.create(
        to=app.config['PHONE_ADMIN'],
        from_=app.config['TWILIO_PHONE'],
        body='%s confirmed their phone number' % from_phone)


class PhoneForm(FlaskForm):
    telephone = StringField('Telephone', [validators.DataRequired()], )

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


def message_response(from_number, from_body='web form'):
    check_telephone = Lead.query.filter_by(telephone=from_number).first()
    if check_telephone is None:
        db.session.add(Lead(from_body, from_number))
        db.session.commit()
        return 'Text Yes to verify your phone number so that we can connect you with a contractor, or No to cancel', False
    elif get_timedelta(check_telephone.received_on).days >= 2:
        return 'Hold tight. We are in the process of connecting you with a contractor.', True
    elif from_body.lower() == 'yes' and check_telephone.is_verified is False:
        check_telephone.is_verified = True
        db.session.add(check_telephone)
        db.session.commit()
        message_admin(from_number)
        if app.config['MAIL_ON'] is True:
            send_email(current_app.config['MAIL_ADMIN'], 'Text a Pro Confirmed Phone Number',
                    'mail/contac    t_me', telephone=from_number)
        return 'Thanks for verifying your number. We will connect you with a contractor shortly', True
    elif from_body.lower() == 'yes' and check_telephone.is_verified is True:
        return 'Hold tight. We are in the process of connecting you with a contractor.'
    elif from_body.lower() == 'no' and check_telephone.is_verified is True:
        return None, True
    elif from_body.lower() == 'no' and check_telephone.is_verified is False:
        check_telephone.is_verified = False
        db.session.add(check_telephone)
        db.session.commit()
        return 'Ok we\'ve cancelled your request', True
    elif check_telephone.is_verified is False:
        return 'We\'ve received your request, but please text Yes to continue or No to cancel', True
    else:
        return None, True



@app.route('/', methods=('GET', 'POST'))
def index():
    form = PhoneForm()
    if form.validate_on_submit():
        try:
            telephone = form.telephone
            form.validate_phone(telephone)
            message_body = message_response("+1"+remove_telephone_chars(telephone.data))
            if message_body[0] and message_body[1] is False:
                twilio_client.messages.create(
                    to=remove_telephone_chars("+1"+telephone.data),
                    from_=app.config['TWILIO_PHONE'],
                    body=message_body)
            if message_body[1]:
                flash('Thank you for submitting. Please check your phone.')
                return redirect('/')
            else:
                flash('Thank You')
                return redirect('/thank-you')
        except:
            flash('Please enter a valid phone number.')
            return redirect('/')

    return render_template('index.html', form=form)


@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')


@app.route("/pro-response", methods=['GET', 'POST'])
def pro_response():
    # Increment the counter
    counter = session.get('counter', 0)
    counter += 1

    # Save the new counter value in the session
    session['counter'] = counter

    response = MessagingResponse()
    message = Message()

    from_number = request.values.get('From')
    from_body = request.values.get('Body')

    if not from_body:
        from_body = 'web form'

    if session['counter'] >= 7:
        message.body(None)
    else:
        message_body = message_response(from_number, from_body)
        message.body(message_body[0])

    response.append(message)

    if message_body[0]:
        return str(response)
    else:
        return '', 204


if __name__ == '__main__':
    app.run()
