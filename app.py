from abcdef1 import run_inference_on_image
from class_list import class_dictionary
from PIL import Image
import glob,os,fnmatch
import cv2

Image_folder_name='Images/'

def convert_gray_to_color():

	list_of_img = fnmatch.filter(os.listdir(Image_folder_name),'*.*')

	for image in list_of_img:
		print(image)
		a=image[:-4]
		img=cv2.imread(Image_folder_name+ image,0)
		color_img=cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
		cv2.imwrite('Images/'+a+'.jpeg',color_img)
		os.remove(Image_folder_name+image)


def convert_bmp_to_jpg():

	list_of_bmp = fnmatch.filter(os.listdir(Image_folder_name),'*.BMP')

	for image in list_of_bmp:
		a=image[:-4]
		img = Image.open(Image_folder_name+image)
		new_img = img.resize((240,320))
		new_img.save(Image_folder_name+a+'.jpeg','jpeg')

		os.remove(Image_folder_name+image)



# Set trash type hash
waste_type = {"r":"Recycling", "c":"Compost"}

class_dictionary = class_dictionary()

#convert_gray_to_color()
#convert_bmp_to_jpg()


print("Running")
list_of_images = glob.glob(Image_folder_name+'/*.*')
for i in list_of_images:
	top_5_prediction = run_inference_on_image(i)
	print(top_5_prediction)

	top = top_5_prediction[4]
	top_name = top[0]
	print(i)

	print("The object is : ",top_name)

	print(waste_type[class_dictionary[top_name]])

