import pyimgur

CLIENT_ID = "ea87ff14c8d3947"
PATH = "a.jpg"

im = pyimgur.Imgur(CLIENT_ID)
uploaded_image = im.upload_image(PATH, title="Uploaded with PyImgur")
print(uploaded_image.link)
