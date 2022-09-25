# import hashlib
# import hmac

# import requests
# account_id = '101011930'
# password = 'Vodafone.1'
# sender_name = 'accept'
# vodafone_secret = '4AF532AF261445E6910200229AF1CD7D'
# phone_number = '01064384307'
# headers = {'Content-Type': 'application/xml'}
# url = "https://e3len.vodafone.com.eg/web2sms/sms/submit/"
# your_message = 'Hello There,How are you?!'
# base_hash = "AccountId={}&Password={}&".format(account_id, password)
# base_hash += "SenderName={}&ReceiverMSISDN={} &SMSText={}&".format(sender_name, phone_number, your_message)
# sms_value = "<SMSList><SenderName>{}</SenderName><ReceiverMSISDN>{}</ReceiverMSISDN><SMSText>{}</SMSText> </SMSList>".format(
#     sender_name, phone_number, your_message)
# base_hash = base_hash[:-1]
# vodafone_secret = bytes(vodafone_secret, 'UTF-8')
# base_hash = bytes(base_hash, 'UTF-8')
# secure_hash = hmac.new(vodafone_secret, base_hash, hashlib.sha256).hexdigest().upper()
# xml = "<?xml version='1.0' encoding='UTF-8'?><SubmitSMSRequest xmlns:='http://www.edafa.com/web2sms/sms/model/' xmlns:xsi='http://www.w3.org/2001/XMLSchema - instance' xsi:schemaLocation='http://www.edafa.com/web2sms/sms/model/ SMSAPI.xsd ' xsi:type='SubmitSMSRequest'><AccountId>{}</AccountId><Password>{}</Password> <SecureHash>{}</SecureHash>{}</SubmitSMSRequest>".format(
#     account_id, password, secure_hash, sms_value)
# response = requests.post(url, data=xml.encode('UTF-8'), headers=headers)
# print(response.text)