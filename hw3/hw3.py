import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

def img2histogram(img):
	hist = [0 for i in range(256)]
	imageW, imageH = img.width, img.height
	for x in range(imageW):
		for y in range(imageH):
			hist[img.getpixel((x,y))] += 1
	plt.bar(range(0, 256), hist)
	plt.savefig('./histogram_lena.png')
	plt.clf()

def img_div3_and_2histogram(img):
	imageW, imageH = img.width, img.height
	new_img = img.copy()
	new_img_pixel = new_img.load()
	hist = [0 for i in range(256)]
	for x in range(imageW):
		for y in range(imageH):
			new_img_pixel[x, y] = new_img_pixel[x, y] // 3
			hist[new_img_pixel[x, y]] += 1
	new_img.save('./div3_lena.bmp')
	plt.bar(range(0, 256), hist)
	plt.savefig('./histogram_div3_lena.png')
	plt.clf()

def img_eq_and_2histogram(img):
	# (1) Count original histogram
	hist = [0 for i in range(256)]
	imageW, imageH = img.width, img.height
	for x in range(imageW):
		for y in range(imageH):
			hist[img.getpixel((x,y))] += 1
	# (2) Compute cdf, cdf_max, cdf_min	
	cdf, cdf_val, cdf_max_pixel, cdf_min_pixel = [0 for i in range(256)], 0, 0, 256
	for pixel in range(256):
		if hist[pixel] > 0 :
			cdf_max_pixel = max(cdf_max_pixel, pixel)
			cdf_min_pixel = min(cdf_min_pixel, pixel)
			cdf[pixel] = cdf_val + hist[pixel]
			cdf_val = cdf[pixel]
	# (3) Compute pixel values after transformation
	# 			 cdf(v) - cdf_min
	#   h(v) = ------------------- * (Gray Scale Level - 1)
	#           cdf_max - cdf_min
	trans_pixel = [0 for i in range(256)]	
	for pixel in range(256):
		trans_pixel[pixel] = round( float(cdf[pixel] - cdf[cdf_min_pixel]) \
								/ float(cdf[cdf_max_pixel] - cdf[cdf_min_pixel]) * 255)
								# / float(imageW*imageH - cdf[cdf_min_pixel]) * 255)
	# (4) Assign transformed values
	new_img = img.copy()
	new_img_pixel = new_img.load()
	eq_hist = [0 for i in range(256)]
	for x in range(imageW):
		for y in range(imageH):
			new_img_pixel[x, y] = trans_pixel[img.getpixel((x, y))]
			eq_hist[new_img_pixel[x, y]] += 1
	new_img.save('./eq_lena.bmp')
	plt.bar(range(0, 256), eq_hist)
	plt.savefig('./histogram_eq_lena.png')
	plt.clf()
	
if __name__ == '__main__':
	img1 = Image.open('./lena.bmp')
	if not img1: print("Error occurs while loading")
	else: print("Image loaded successfully!")
	# Part1
	img2histogram(img1)
	# Part2
	img_div3_and_2histogram(img1)
	# Part3
	img2 = Image.open('./div3_lena.bmp')
	if not img2: print("Error occurs while loading")
	else: print("Image loaded successfully!")
	img_eq_and_2histogram(img2)
