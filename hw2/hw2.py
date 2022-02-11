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
			new_img_pixel[x, y] = 255 if img.getpixel((x,y)) >= 128 else 0
	new_img.save('./binarize_lena.bmp')

def img_2_histogram(img):
	hist = [0 for i in range(256)]
	imageW, imageH = img.width, img.height
	for x in range(imageW):
		for y in range(imageH):
			hist[img.getpixel((x,y))] += 1
	plt.bar(range(0, 256), hist)
	plt.savefig('./histogram_lena.png')

def create_bounding_boxes(object_count_map, img_objects, imageW, imageH, THRESHOLD):
	boxes = []
	for object_id, count in enumerate(object_count_map):
		if count >= THRESHOLD:
			left, right, up, down = imageW, 0, imageH, 0
			for x in range(imageW):
				for y in range(imageH):
					if img_objects[x, y] == object_id:
						left = x if x < left else left
						right = x if x > right else right
						up = y if y < up else up
						down = y if y > down else down
			boxes.append((left, right, up, down, object_id))
	return boxes

def neighbor_dfs_traversal(neighbors, x, y, imageW, imageH, traversal, img, stk):
	if neighbors == 8:
		for px in range(x-1, x+2):
			for py in range(y-1, y+2):
				if px >= 0 and px < imageW and py >= 0 and py < imageH:
					if traversal[px, py] == 0 and img.getpixel((px,py)) != 0: 
						stk.append((px, py))
	if neighbors == 4:
		for (px, py) in [(x-1, y-1), (x+1, y+1), (x-1, y+1), (x+1, y-1)]: 
			if px >= 0 and px < imageW and py >= 0 and py < imageH:	
				if traversal[px, py] == 0 and img.getpixel((px,py)) != 0: 
					stk.append((px, py))
	return stk

def getCentroid(object_id, img_objects, amount_of_pixel, imageW, imageH):
	centerX, centerY = 0, 0
	for x in range(imageW):
		for y in range(imageH):
			if img_objects[x, y] == object_id:
				centerX += x
				centerY += y
	return int(centerX/amount_of_pixel), int(centerY/amount_of_pixel)

def connected_components(img, NEIGHBOR):
	THRESHOLD, OBJECTNUM = 500, 1 
	binarized_img = Image.open('./binarize_lena.bmp')
	imageW, imageH = binarized_img.width, binarized_img.height
	# traversal = for DFS recording the location traversal or not; img_objects = for recording objects
	traversal, img_objects = np.zeros((imageW, imageH)), np.zeros((imageW, imageH))
	# record how many pixels in each region
	object_count_map = np.zeros(imageW*imageH+1)
	# create new image and process image pixel values and convert binary to RGB format
	connected_components_img = Image.new('RGB', (imageW, imageH))
	connected_components_img_pixel = connected_components_img.load()
	for x in range(imageW):
		for y in range(imageH):
			if binarized_img.getpixel((x, y)) == 0: connected_components_img_pixel[x, y] = (0, 0, 0)
			else: connected_components_img_pixel[x, y] = (255, 255, 255)
	# mark objects
	for x in range(imageW):
		for y in range(imageH):
			# no need to deal with 0 value pixel
			if binarized_img.getpixel((x, y)) == 0: traversal[x, y] = 1 
			elif binarized_img.getpixel((x, y)) == 255 and traversal[x, y] == 0:
				# start DFS traversal for marking region
				stk = [(x, y)] # stack for DFS traversal
				while len(stk):
					(c, r) = stk.pop()
					# print((c,r))
					# if the node is visited, continue; 
					# if not, mark as visited & give label & update count & DFS traversal
					if traversal[c, r] == 1: continue 
					traversal[c, r] = 1 
					img_objects[c, r] = OBJECTNUM 
					object_count_map[OBJECTNUM] += 1
					# YOU CAN CHANGE NUMBER IN FIRST PARAMETER (4 or 8)
					stk = neighbor_dfs_traversal(NEIGHBOR, c, r, imageW, imageH, traversal, binarized_img, stk)
				OBJECTNUM += 1 # print(OBJECTNUM)
	# get bounding boxes
	bounding_boxes = create_bounding_boxes(object_count_map, img_objects, imageW, imageH, THRESHOLD)
	# draw bounding boxes and box centers
	draw = ImageDraw.Draw(connected_components_img)
	for bounding_box in bounding_boxes:
		(left, right, up, down, object_id) = bounding_box[0], bounding_box[1], bounding_box[2], bounding_box[3], bounding_box[4]
		centerX, centerY = getCentroid(object_id, img_objects, object_count_map[object_id], imageW, imageH)
		draw.rectangle(((left, up), (right, down)), outline='blue')
		draw.line(((centerX-6, centerY), (centerX+6, centerY)), fill='red', width=3) # horizontal
		draw.line(((centerX, centerY-6), (centerX, centerY+6)), fill='red', width=3) # vertical 
	connected_components_img.save('./connected_components_lena_' + str(NEIGHBOR) + '.bmp')

if __name__ == '__main__':
	img = Image.open('./lena.bmp')
	if not img: print("Error occurs while loading")
	else: print("Image loaded successfully!")
	binarize(img)                 # Part1-a
	img_2_histogram(img)          # Part1-b
	connected_components(img, 4)  # Part1-c
	connected_components(img, 8)  # Part1-c
