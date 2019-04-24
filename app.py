from abcdef1 import run_inference_on_image
from class_list import class_dictionary
from PIL import Image
import glob,os,fnmatch
import cv2

Image_folder_name='Images/'

# Set trash type hash
waste_type = {"r":"Recycling", "c":"Compost"}

class_dictionary = class_dictionary()

print("Running")
list_of_images = glob.glob(Image_folder_name+'/far.jpg')
for i in list_of_images:
	top_5_prediction = run_inference_on_image(i)
	print(top_5_prediction)

	top = top_5_prediction[4]
	top_name = top[0]

	print(i)
	print("The object is : ",top_name)
	print(waste_type[class_dictionary[top_name]])