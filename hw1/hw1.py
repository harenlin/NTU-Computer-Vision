from PIL import Image

def upside_down(img):
	imageW, imageH = img.width, img.height # img.size[0], img.size[1]
	new_img = img.copy()
	new_img_pixel = new_img.load()
	for x in range(imageW):
		for y in range(int(imageH/2)):
			new_img_pixel[x, y], new_img_pixel[x, imageH-1-y] \
			= new_img_pixel[x, imageH-1-y], new_img_pixel[x, y]
	new_img.save('./upside-down_lena.bmp')

def right_side_left(img):
	imageW, imageH = img.width, img.height # img.size[0], img.size[1]
	new_img = img.copy()
	new_img_pixel = new_img.load()
	for y in range(imageH):
		for x in range(int(imageW/2)):
			new_img_pixel[x, y], new_img_pixel[imageW-1-x, y] \
			= new_img_pixel[imageW-1-x, y], new_img_pixel[x, y]
	new_img.save('./right-side-left_lena.bmp')

def diagonally_mirror(img):
	imageW, imageH = img.width, img.height # img.size[0], img.size[1]
	new_img = img.copy()
	new_img_pixel = new_img.load()
	for x in range(int(imageW)):
		for y in range(x+1, int(imageH)):
			new_img_pixel[x, y], new_img_pixel[y, x] = img.getpixel((y, x)), img.getpixel((x, y))
	new_img.save('./diagonally-mirror_lena.bmp')
	
def rotate_45_degree(img):
	new_img = img.rotate(360-45)
	new_img.save('./rotate-45-degree_lena.bmp')

def shrink(img):	
	new_img = img.resize((256,256))
	new_img.save('./shrink_lena.bmp')

def binarize(img):
	imageW, imageH = img.width, img.height # img.size[0], img.size[1]
	new_img = img.copy()
	new_img_pixel = new_img.load()
	for x in range(imageW):
		for y in range(imageH):
			new_img_pixel[x, y] = 255 if img.getpixel((x,y)) >= 128 else 0
	new_img.save('./binarize_lena.bmp')


if __name__ == '__main__':

	img = Image.open('./lena.bmp')
	if not img: 
		print("Error occurs while loading")
	else: 
		print("Image loaded successfully!")

	# imageW, imageH = img.width, img.height # img.size[0], img.size[1]
	# print(img.mode, img.size, imageW, imageH)

	upside_down(img)       # Part1-1
	right_side_left(img)   # Part1-2
	diagonally_mirror(img) # Part1-3
	rotate_45_degree(img)  # Part2-1
	shrink(img)            # Part2-2
	binarize(img)	       # Part2-3
