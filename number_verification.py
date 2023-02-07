# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

# Set environment variables for your credentials
# Read more at http://twil.io/secure
def mobile_otp(verified_number):
  account_sid = appConf['ph_no_cred']['account_sid']
  auth_token = appConf['ph_no_cred']['auth_token']
  verify_sid = appConf['ph_no_cred']['verify_sid']
  #verified_number = "+916350193596"
  client = Client(account_sid, auth_token)
  verification = client.verify.v2.services(verify_sid) \
    .verifications \
    .create(to="+91"+verified_number, channel="sms")
  print(verification.status)
def check_mobile_otp(verified_number,otp_code):
  account_sid = appConf['ph_no_cred']['account_sid']
  auth_token = appConf['ph_no_cred']['auth_token']
  verify_sid = appConf['ph_no_cred']['verify_sid']
  client = Client(account_sid, auth_token)

  verification_check = client.verify.v2.services(verify_sid) \
    .verification_checks \
    .create(to="+91"+verified_number, code=otp_code)
  return (verification_check.status)
