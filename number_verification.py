# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

# Set environment variables for your credentials
# Read more at http://twil.io/secure
def mobile_otp(verified_number):
  account_sid = "AC129181ef3caec9a6fb8e6d67a726f3a5"
  auth_token = "b58b7cd1f536f449332722492bc7102b"
  verify_sid = "VA3e4e885e437cc75d19f7d1a4e736d996"
  #verified_number = "+916350193596"
  client = Client(account_sid, auth_token)
  verification = client.verify.v2.services(verify_sid) \
    .verifications \
    .create(to="+91"+verified_number, channel="sms")
  print(verification.status)
def check_mobile_otp(verified_number,otp_code):
  account_sid = "AC129181ef3caec9a6fb8e6d67a726f3a5"
  auth_token = "b58b7cd1f536f449332722492bc7102b"
  verify_sid = "VA3e4e885e437cc75d19f7d1a4e736d996"
  client = Client(account_sid, auth_token)

  verification_check = client.verify.v2.services(verify_sid) \
    .verification_checks \
    .create(to="+91"+verified_number, code=otp_code)
  return (verification_check.status)
