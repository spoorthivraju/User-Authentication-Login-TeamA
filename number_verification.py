# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

# Set environment variables for your credentials
# Read more at http://twil.io/secure
def mobile_otp(verified_number):
  account_sid = "AC72717268dce65b12d572f2ea90eaab9a"
  auth_token = "46e1c03750883bae98644be11de0bf08"
  verify_sid = "VA1955eab841f8046dcf132566e2371941"
  #verified_number = "+916350193596"

  client = Client(account_sid, auth_token)

  verification = client.verify.v2.services(verify_sid) \
    .verifications \
    .create(to="+91"+verified_number, channel="sms")
  print(verification.status)
def check_mobile_otp(verified_number,otp_code):
  account_sid = "AC72717268dce65b12d572f2ea90eaab9a"
  auth_token = "46e1c03750883bae98644be11de0bf08"
  verify_sid = "VA1955eab841f8046dcf132566e2371941"
  client = Client(account_sid, auth_token)

  verification_check = client.verify.v2.services(verify_sid) \
    .verification_checks \
    .create(to="+91"+verified_number, code=otp_code)
  return (verification_check.status)
