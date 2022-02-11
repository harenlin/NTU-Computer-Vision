import numpy as np
from PIL import Image

def downsample(img, sampleSize=(64,64)):
	downsample_img = Image.new('L', sampleSize)
	downsample_img_pixel = downsample_img.load()
	for x in range(sampleSize[0]):
		for y in range(sampleSize[1]):
			downsample_img_pixel[x, y] = img.getpixel((x*8, y*8))
	downsample_img.save('./downsampled_lena.bmp')
	return downsample_img

def binarize(img):
	imageW, imageH = img.width, img.height
	new_img = img.copy()
	new_img_pixel = new_img.load()
	for x in range(imageW):
		for y in range(imageH):
			new_img_pixel[x, y] = 255 if img.getpixel((x,y)) > 127 else 0
	new_img.save('./binarize_lena.bmp')
	return new_img

def pixel_val(x, y):
	if (x >= 0 and x < 64 and y >= 0 and y < 64): return img.getpixel((x,y))
	return 0

def neighborhood(img, x, y):
	return [
		pixel_val(x,y)    , # x0
		pixel_val(x+1,y)  , # x1
		pixel_val(x,y-1)  , # x2
		pixel_val(x-1,y)  , # x3
		pixel_val(x,y+1)  , # x4
		pixel_val(x+1,y+1), # x5
		pixel_val(x+1,y-1), # x6
		pixel_val(x-1,y-1), # x7
		pixel_val(x-1,y+1)  # x8
	]

def hFunction(b, c, d, e):
	if b == c and ( b != d or b != e ): return 'q'
	elif b == c and ( b == d or b == e ): return 'r'
	elif b != c: return 's'
	return ' '

def fFunction(a1, a2, a3, a4):
	if a1 == 'r' and a2 == 'r' and a3 == 'r' and a4 == 'r': return 5
	numberOfQ, records = 0, [a1, a2, a3, a4]
	for r in records: numberOfQ = numberOfQ + (1 if r == 'q' else 0)
	return numberOfQ

def YokoiConnectivityNumber(x):
	return fFunction(
				hFunction(x[0], x[1], x[6], x[2]),
				hFunction(x[0], x[2], x[7], x[3]),
				hFunction(x[0], x[3], x[8], x[4]),
				hFunction(x[0], x[4], x[5], x[1])
		   )

def writeYokoiResult(yokoi_res, sampleSize=(64,64)):
	f = open("yokoi.txt", "w+")
	for x in range(sampleSize[0]):
		for y in range(sampleSize[1]):
			f.write(str(yokoi_res[y][x]))
		f.write('\n')
	f.close()

if __name__ == '__main__':
	img = Image.open('./lena.bmp')
	# downsample and binarize image
	sampleSize = (64,64)
	img = binarize(downsample(img, sampleSize))
	# yokoi_res initialization
	yokoi_res = []
	for x in range(sampleSize[0]):
		tmp = []
		for y in range(sampleSize[1]): tmp.append(' ')
		yokoi_res.append(tmp)
	# start computing yokoi connectivity number
	for x in range(sampleSize[0]):
		for y in range(sampleSize[1]):
			if img.getpixel((x,y)) > 0 :
				yokoi_res[x][y] = YokoiConnectivityNumber(neighborhood(img, x, y))
	# save result
	writeYokoiResult(yokoi_res)
