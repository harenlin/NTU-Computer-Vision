import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

def validPixel(x, bound):
	return (x >= 0 and x <= bound)

def Dilation(img, kernel):
	imageW, imageH = img.width, img.height 
	new_img = Image.new('L', (imageW, imageH))
	new_img_pixel = new_img.load()
	for x in range(imageW):
		for y in range(imageH):
			localMaximum = 0
			for [ex, ey] in kernel:
				dest_x, dest_y = x + ex, y + ey
				if ( validPixel(dest_x, imageW-1) and validPixel(dest_y, imageH-1) ):
					localMaximum = max( localMaximum, img.getpixel((dest_x, dest_y)))
			new_img_pixel[x, y] = localMaximum
	return new_img

def Erosion(img, kernel):
	imageW, imageH = img.width, img.height
	new_img = Image.new('L', (imageW, imageH))
	new_img_pixel = new_img.load()
	for x in range(imageW):
		for y in range(imageH):
			localMinimum = 255
			savePixel = True
			for [ex, ey] in kernel:
				dest_x, dest_y = x + ex, y + ey
				if ( validPixel(dest_x, imageW-1) and validPixel(dest_y, imageH-1) ): # valid pixel
					if img.getpixel((dest_x, dest_y)) == 0: # but no value
						savePixel = False
						break
					else: localMinimum = min( localMinimum, img.getpixel((dest_x, dest_y))) # erosion
				else: # non-valid pixel
					savePixel = False
					break
			if savePixel: new_img_pixel[x, y] = localMinimum
	return new_img

def Opening(img, kernel):
	return Dilation(Erosion(img, kernel), kernel)

def Closing(img, kernel):
	return Erosion(Dilation(img, kernel), kernel)

if __name__ == '__main__':
	img = Image.open('./lena.bmp')
	# kernel is a 3-5-5-5-3 octagon, where the orgin is at the center
	kernel = [    [-2, -1], [-2, 0], [-2, 1],
		[-1, -2], [-1, -1], [-1, 0], [-1, 1], [-1, 2],
		[0, -2],  [0, -1],  [0, 0],  [0, 1],  [0, 2],
		[1, -2],  [1, -1],  [1, 0],  [1, 1],  [1, 2],
				  [2, -1],  [2, 0],  [2, 1]]
	# Part1
	dilation_img = Dilation(img, kernel)
	dilation_img.save('dilation_lena.bmp')
	# Part2
	erosion_img = Erosion(img, kernel)
	erosion_img.save('erosion_lena.bmp')
	# Part3
	opening_img = Opening(img, kernel)
	opening_img.save('opening_lena.bmp')
	# Part4
	closing_img = Closing(img, kernel)
	closing_img.save('closing_lena.bmp')
