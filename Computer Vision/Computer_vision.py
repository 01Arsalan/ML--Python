# we use open cv library for this

import cv2
from google.colab.patches import cv2_imshow 
import numpy as np

#to give a black background
black=np.zeros([300,300,3]) # number of channels in input for coloured images should always be 3 and 1 in greyscale.
cv2_imshow(black)

#to give a white background
white=np.ones([300,300,3])*255  # 255 for brightness
cv2_imshow(white)


# we can get other shapes also
cv2.rectangle(black,(20,20),(200,200),(0,0,255),3)   
cv2.circle(black,(150,150),15,(0,255,0),3)
cv2_imshow(black)

cv2.circle(black,(150,150),70,(0,255,0),3)
cv2_imshow(black)

cv2.line(black,(20,20),(180,180),(255,0,0),2)
cv2_imshow(black)

# cv2.text()#to put text


# downloading image from net and saving it as ("image.jpg")
# !wget 'https://cdn.pixabay.com/photo/2015/12/01/20/28/road-1072821__480.jpg' -O "image.jpg"           #linx command
# [ response... 200 ]OK means sucess, Anything other than 200 is unsucessfull

img=cv2.imread("image.jpg") # to read and show image
cv2_imshow(img)

r_sixe=cv2.resize(img,(1200,900)) # to resize
cv2_imshow(r_sixe)

cv2.imwrite("new.jpg",r_sixe)   # create and save as new file

# color to greyScale 
# 
# [Method 1]

img1=cv2.imread("new.jpg")
greyscale=cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
cv2_imshow(greyscale)

#[Method 2]

img2=cv2.imread("new.jpg",0)
cv2_imshow(img2)


# binary image [0 and 1 || white and black]
# step: get colored image -> convet it into grayScale -> convert it into bonary image.   By threshold Function

img3=cv2.imread("new.jpg",0)
ret,binary=cv2.threshold(img3,127,255,cv2.THRESH_BINARY)      #[127]->threshold for blacks and white seperation. [255]-> limit
cv2_imshow(binary)

#Applying tints on image using [RGB Extraction]

img4=cv2.imread("new.jpg")
B,G,R=cv2.split(img4)
Zeros=np.zeros(img4.shape[:2],dtype='unit8')
cv2_imshow(cv2.merge([Zeros,Zeros,R]))


# Edge Dectection       -> marks the edges of objects in images
# Techniques
# 1: sobel
# 2: laplacian
# 3: canny

# uisng Sobel

img5=cv2.imread("new.jpg",0)
sobel_x=cv2.Sobel(img5,cv2.CV_8U,dx=1,dy=0,ksize=-1)
sobel_y=cv2.Sobel(img5,cv2.CV_8U,dx=0,dy=1,ksize=-1)
sobel_f=cv2.bitwise_or(sobel_x,sobel_y)
cv2_imshow(sobel_x)
cv2_imshow(sobel_y)
cv2_imshow(sobel_f)


#using Laplacian

img7=cv2.imread("new.jpg")
laplacian=cv2.Laplacian(img7,cv2.CV_8U)
cv2_imshow(laplacian)


#using canny 

img=cv2.imread("image.jpg",0)
canny=cv2.Canny(img,250,250)
cv2_imshow(canny)



#Blur

# 1: Direct blur function
img=cv2.imread("image.jpg")
blur_1=cv2.blur(img,(6,6))   # we can icrease or decrease blur by changing (2nd parameter)->6x6 matrix/Kernal
cv2_imshow(blur_1)

#Sharpen

#Filter 2D
img=cv2.imread("image.jpg")
filter1=np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])         #to sharpen the image, we used [3X3]custom Kernal
op=cv2.filter2D(img,-1,filter1)
cv2_imshow(op)


