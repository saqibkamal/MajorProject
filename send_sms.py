import time
from sinchsms import SinchSMS
def sendsms():


	number = '+918059710704'
	message = 'New Garbage Detected'

	client = SinchSMS("0ca08f70-4fa2-4547-a9b0-5b1280115d6d", "QKewCNo4oEqXbgwxEglPxA==")

	print("Sending '%s' to %s" % (message, number))
	response = client.send_message(number, message)
	message_id = response['messageId']

	response = client.check_status(message_id)
	while response['status'] != 'Successful':
	    print(response['status'])
	    time.sleep(1)
	    response = client.check_status(message_id)
	    print(response['status'])

sendsms()