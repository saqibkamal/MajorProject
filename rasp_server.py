from flask import Flask,jsonify,request
import base64
from abcdef1 import run_inference_on_image
from class_list import class_dictionary
from shutil import copy
import uuid
import os
import time 
from time import sleep 
from sinchsms import SinchSMS
import pyimgur
from PIL import Image

CLIENT_ID = "ea87ff14c8d3947"

# Set trash type hash
waste_type = {"r":"Recyclable", "c":"Compost"}

class_dictionary = class_dictionary()


def upload_image_to_imgur(fname,lname,rname):

	print("Uploading Image to Database")

	im = pyimgur.Imgur(CLIENT_ID)
	f_image = im.upload_image(fname, title="Garbage Image")
	l_image = im.upload_image(lname, title="Left Image")
	r_image = im.upload_image(rname, title="right Image")

	print("Image Successlly uploaded to databse")

	return f_image.link,l_image.link,r_image.link
	


def get_filename():
	return str(time.strftime("%Y%m%d-%H%M%S"))


def send_sms(a,b,c):


	number = '+918059710704'
	message = 'New Garbage Detected Image : '+a+" Left Image Image : "+b+" Right Image : "+c

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

app = Flask(__name__)
@app.route("/predict",methods=['POST'])
def predict():

    
    print("Request Recieved on Server")
    print("Reading Images")
    content = request.get_json()
    m_imgdata =base64.b64decode(content["main_image"])
    l_imgdata =base64.b64decode(content["left_image"])
    r_imgdata =base64.b64decode(content["right_image"])
    filename = 'Garbage Image.jpg'  # I assume you have a way of picking unique filenames
    with open(filename, 'wb') as f:
    	f.write(m_imgdata)

    left_filename = "Left Image.jpg"
    with open(left_filename, 'wb') as f:
    	f.write(l_imgdata)

    right_filename = "Right Image.jpg"
    with open(right_filename, 'wb') as f:
    	f.write(r_imgdata)

    print("Running")
    top_5_prediction = run_inference_on_image(filename)
    print(top_5_prediction)
    top = top_5_prediction[4]
    top_name = top[0]
    #print("The object is : ",top_name)

    final_result= waste_type[class_dictionary[top_name]]
    print("The garbage is : ",final_result)
    if final_result == "Recyclable":
        prediction = 'Recyclable Garbage'
        folder_name=get_filename()
        os.mkdir('Recyclable/'+folder_name)
        copy(filename,'Recyclable/'+folder_name+'/')
        copy(left_filename,'Recyclable/'+folder_name+'/')
        copy(right_filename,'Recyclable/'+folder_name+'/')
    else:
        prediction = 'Compost'
        folder_name=get_filename()
        os.mkdir('Compost/'+folder_name)
        copy(filename,'Compost/'+folder_name+'/')
        copy(left_filename,'Compost/'+folder_name+'/')
        copy(right_filename,'Compost/'+folder_name+'/')


    a,b,c=upload_image_to_imgur(filename,left_filename,right_filename)
    send_sms(a,b,c)
    os.remove(filename)
    os.remove(left_filename)
    os.remove(right_filename)


    print("Image Processing Complete")    
    return jsonify(final_result)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=233)
 

