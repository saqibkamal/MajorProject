server_url="http://192.168.43.185:233"
def send_image(mimage):
    
    print("Sending Image")


    with open(mimage,"rb") as a:
        right_jpg_as_text=base64.b64encode(a.read())
    
    image_josn = {"main_image": main_jpg_as_text,"left_image":left_jpg_as_text,"right_image":right_jpg_as_text}

    response = requests.post("{}/predict".format(server_url), json = image_josn)

    #print(response.json())
    print("Image sent Successfully")
   
    return response.json()