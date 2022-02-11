import cv2
import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

def binarize(img):
	imageW, imageH = img.width, img.height
	new_img = img.copy()
	new_img_pixel = new_img.load()
	for x in range(imageW):
		for y in range(imageH):
			new_img_pixel[x, y] = 255 if img.getpixel((x,y)) > 127 else 0
	new_img.save('./binarize_lena.bmp')

def validPixel(x, bound):
	if x >= 0 and x <= bound:
		return True
	return False

def Dilation(img, kernel):
	imageW, imageH = img.shape[0], img.shape[1]
	new_img = np.zeros((imageW, imageW), dtype='int32')	
	for x in range(imageW):
		for y in range(imageH):
			if img[x,y] == 255:
				new_img[x,y] = 255
				for [ex, ey] in kernel:
					dest_x, dest_y = x + ex, y + ey
					if validPixel(dest_x, imageW-1) == True \
						and validPixel(dest_y, imageH-1) == True:
						new_img[dest_x, dest_y] = 255
	return new_img

def Erosion(img, kernel):
	imageW, imageH = img.shape[0], img.shape[1]
	new_img = np.zeros((imageW, imageW), dtype='int32')	
	for x in range(imageW):
		for y in range(imageH):
			if img[x,y] == 255:
				savePixel = True
				for [ex, ey] in kernel:
					dest_x, dest_y = int(x + ex), int(y + ey)
					if (validPixel(dest_x, imageW-1) == False) or \
					   (validPixel(dest_y, imageH-1) == False) or \
					    img[dest_x, dest_y] != 255:
						savePixel = False
						break
				if savePixel == True: new_img[x, y] = 255
	del savePixel
	return new_img

def Erosion_2(img, kernel):
	imageW, imageH = img.shape[0], img.shape[1]
	new_img = np.zeros((imageW, imageW), dtype='int32')	
	for x in range(imageW):
		for y in range(imageH):
			savePixel = True
			for [ex, ey] in kernel:
				dest_x, dest_y = int(x + ex), int(y + ey)
				if (validPixel(dest_x, imageW-1) == False) or \
				   (validPixel(dest_y, imageH-1) == False) or \
				    img[dest_x, dest_y] != 255:
					savePixel = False
					break
			if savePixel == True: new_img[x, y] = 255
	del savePixel
	return new_img

def Opening(img, kernel):
	return Dilation(Erosion(img, kernel), kernel)

def Closing(img, kernel):
	return Erosion(Dilation(img, kernel), kernel)

def HitAndMissTransform(img, J, K):
	# (A erose by J) and (A's complement erose by K)
	imageW, imageH = img.shape[0], img.shape[1]
	complement_img = np.zeros((imageW, imageW), dtype='int32')	
	for x in range(imageW):
		for y in range(imageH):
			complement_img[x,y] = 255 - img[x,y]
	new_img = np.zeros((imageW, imageW), dtype='int32')	
	img_erosion_j, img_c_erosion_k = Erosion(img, J), Erosion_2(complement_img, K)
	for x in range(imageW):
		for y in range(imageH):
			if img_erosion_j[x,y] == 255 and img_c_erosion_k[x,y] == 255:
				new_img[x,y] = 255 
	del img, complement_img, img_erosion_j, img_c_erosion_k
	return new_img

if __name__ == '__main__':
	# load in original image
	img = Image.open('./lena.bmp')
	# binarize original image first
	binarize(img)
	del img

	# kernel is a 3-5-5-5-3 octagon, where the orgin is at the center
	kernel = [    [-2, -1], [-2, 0], [-2, 1],
		[-1, -2], [-1, -1], [-1, 0], [-1, 1], [-1, 2],
		[0, -2],  [0, -1],  [0, 0],  [0, 1],  [0, 2],
		[1, -2],  [1, -1],  [1, 0],  [1, 1],  [1, 2],
				  [2, -1],  [2, 0],  [2, 1]]

	img	= cv2.imread("./binarize_lena.bmp", cv2.IMREAD_GRAYSCALE)

	# Part1
	dilation_img = Dilation(img, kernel)
	cv2.imwrite('dilation_lena.bmp', dilation_img)
	# Part2
	erosion_img = Erosion(img, kernel)
	cv2.imwrite('erosion_lena.bmp', erosion_img)
	# Part3
	opening_img = Opening(img, kernel)
	cv2.imwrite('opening_lena.bmp', opening_img)
	# Part4
	closing_img = Closing(img, kernel)
	cv2.imwrite('closing_lena.bmp', closing_img)
	# Part5
	J_kernel = [[0, -1], [0, 0], [1, 0]]
	K_kernel = [[-1, 0], [-1, 1], [0, 1]]
	hitandmiss_img = HitAndMissTransform(img, J_kernel, K_kernel)
	cv2.imwrite('hitandmiss_lena.bmp', hitandmiss_img)
