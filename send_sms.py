# /usr/bin/env python
# Download the twilio-python library from http://twilio.com/docs/libraries
from twilio.rest import Client

# Find these values at https://twilio.com/user/account
account_sid = "ACbf835e6507e16f25dd94f020295f21d3"
auth_token = "9c82b2d0d3d321d8d9216ae0578c2e0e"
client = Client(account_sid, auth_token)

message = client.api.account.messages.create(to="+18059011596",
                                             from_="+18057492645",
                                             body="Hello there!")