import numpy as np
import cv2, math, sys
import matplotlib.pyplot as plt

def padding_img_5(img):
	return padding_img_3(img)

def padding_img_3(img):
	imageW, imageH = img.shape
	# imageW, imageH = len(img), len(img[0])
	newImageW, newImageH = imageW+2, imageH+2
	res = np.zeros((newImageW, newImageH), dtype='int32')
	# corner
	res[0][0] = img[0][0]
	res[0][newImageH-1] = img[0][imageH-1]
	res[newImageW-1][0] = img[imageW-1][0]
	res[newImageW-1][newImageH-1] = img[imageW-1][imageH-1]
	# border
	for idx_x in range(1,newImageW-1):
		res[idx_x][0] = img[idx_x-1][0]
		res[idx_x][newImageH-1] = img[idx_x-1][imageH-1]
	for idx_y in range(1,newImageH-1):
		res[0][idx_y] = img[0][idx_y-1]
		res[newImageW-1][idx_y] = img[imageW-1][idx_y-1]
	# original case
	for x in range(1, newImageW-1):
		for idx_y in range(1,newImageH-1):
			res[x][idx_y] = img[x-1][idx_y-1]
	return res

def convolution(img, kernel):
	imageW, imageH = img.shape
	kernelW, kernelH = len(kernel), len(kernel[0])
	res = 0
	for x in range(imageW):
		for y in range(imageH):
			res += img[x][y] * kernel[x][y]
	return res

def roberts(img):
	imageW, imageH = img.shape
	r1 = np.zeros((imageW-2, imageH-2), dtype='int32')
	r2 = np.zeros((imageW-2, imageH-2), dtype='int32')
	kernel1 = np.array([[1, 0], [0, -1]])
	kernel2 = np.array([[0, 1], [-1, 0]])
	for x in range(1,imageW-1):
		for y in range(1,imageH-1):
			r1[x-1][y-1] = convolution(img[x:x+2, y:y+2], kernel1)
			r2[x-1][y-1] = convolution(img[x:x+2, y:y+2], kernel2)
	return np.sqrt(r1**2+r2**2)

def prewittsEdge(img):
	imageW, imageH = img.shape
	p1 = np.zeros((imageW-2, imageH-2), dtype='int32')
	p2 = np.zeros((imageW-2, imageH-2), dtype='int32')
	kernel1 = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])    
	kernel2 = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])
	for x in range(imageW-2):
		for y in range(imageH-2):
			p1[x][y] = convolution(img[x:x+3, y:y+3], kernel1)
			p2[x][y] = convolution(img[x:x+3, y:y+3], kernel2)
	return np.sqrt(p1**2+p2**2)

def sobelsEdge(img):
	imageW, imageH = img.shape
	s1 = np.zeros((imageW-2, imageH-2), dtype='int32')
	s2 = np.zeros((imageW-2, imageH-2), dtype='int32')
	kernel1 = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]) 
	kernel2 = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
	for x in range(imageW-2):
		for y in range(imageH-2):
			s1[x][y] = convolution(img[x:x+3, y:y+3], kernel1)
			s2[x][y] = convolution(img[x:x+3, y:y+3], kernel2)
	return np.sqrt(s1**2+s2**2)

def freiAndChensGradient(img):
	imageW, imageH = img.shape
	f1 = np.zeros((imageW-2, imageH-2), dtype='int32')
	f2 = np.zeros((imageW-2, imageH-2), dtype='int32')
	kernel1 = np.array([[-1, -np.sqrt(2), -1], [0, 0, 0], [1, np.sqrt(2), 1]]) 
	kernel2 = np.array([[-1, 0, 1], [-np.sqrt(2), 0, np.sqrt(2)], [-1, 0, 1]])
	for x in range(imageW-2):
		for y in range(imageH-2):
			f1[x][y] = convolution(img[x:x+3, y:y+3], kernel1)
			f2[x][y] = convolution(img[x:x+3, y:y+3], kernel2)
	return np.sqrt(f1**2+f2**2)

def kirschsCompass(img):
	imageW, imageH = img.shape
	res = np.zeros((imageW-2, imageH-2), dtype='int32')
	kernel1 = np.array([[-3, -3, 5], [-3, 0, 5], [-3, -3, 5]])
	kernel2 = np.array([[-3, 5, 5], [-3, 0, 5], [-3, -3, -3]])
	kernel3 = np.array([[5, 5, 5], [-3, 0, -3], [-3, -3, -3]])
	kernel4 = np.array([[5, 5, -3], [5, 0, -3], [-3, -3, -3]])
	kernel5 = np.array([[5, -3, -3], [5, 0, -3], [5, -3, -3]])
	kernel6 = np.array([[-3, -3, -3], [5, 0, -3], [5, 5, -3]])
	kernel7 = np.array([[-3, -3, -3], [-3, 0, -3], [5, 5, 5]])
	kernel8 = np.array([[-3, -3, -3], [-3, 0, 5], [-3, 5, 5]])
	for x in range(imageW-2):
		for y in range(imageH-2):
			res[x][y] = max( convolution(img[x:x+3, y:y+3], kernel1),
				convolution(img[x:x+3, y:y+3], kernel2),
				convolution(img[x:x+3, y:y+3], kernel3),
				convolution(img[x:x+3, y:y+3], kernel4),
				convolution(img[x:x+3, y:y+3], kernel5),
				convolution(img[x:x+3, y:y+3], kernel6),
				convolution(img[x:x+3, y:y+3], kernel7),
				convolution(img[x:x+3, y:y+3], kernel8))
	return res

def robinsonsCompass(img):
	imageW, imageH = img.shape
	res = np.zeros((imageW-2, imageH-2), dtype='int32')
	kernel1 = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
	kernel2 = np.array([[0, 1, 2], [-1, 0, 1], [-2, -1, 0]])
	kernel3 = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])
	kernel4 = np.array([[2, 1, 0], [1, 0, -1], [0, -1, -2]])
	kernel5 = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])
	kernel6 = np.array([[0, -1, -2], [1, 0, -1], [2, 1, 0]])
	kernel7 = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
	kernel8 = np.array([[-2, -1, 0], [-1, 0, 1], [0, 1, 2]])
	for x in range(imageW-2):
		for y in range(imageH-2):
			res[x][y] = max( convolution(img[x:x+3, y:y+3], kernel1),
				convolution(img[x:x+3, y:y+3], kernel2),
				convolution(img[x:x+3, y:y+3], kernel3),
				convolution(img[x:x+3, y:y+3], kernel4),
				convolution(img[x:x+3, y:y+3], kernel5),
				convolution(img[x:x+3, y:y+3], kernel6),
				convolution(img[x:x+3, y:y+3], kernel7),
				convolution(img[x:x+3, y:y+3], kernel8))
	return res
	
def nevatiaBabu(img):
	imageW, imageH = img.shape
	res = np.zeros((imageW-5, imageH-5), dtype='int32')
	kernel1 = np.array([[100, 100, 100, 100, 100],
						[100, 100, 100, 100, 100],
						[0, 0, 0, 0, 0],
						[-100, -100, -100, -100, -100],
						[-100, -100, -100, -100, -100]])
	kernel2 = np.array([[100, 100, 100, 100, 100],
						[100, 100, 100, 78, -32],
						[100, 92, 0, -92, -100],
						[32, -78, -100, -100, -100],
						[-100, -100, -100, -100, -100]])
	kernel3 = np.array([[100, 100, 100, 32, -100],
						[100, 100, 92, -78, -100],
						[100, 100, 0, -100, -100],
						[100, 78, -92, -100, -100],
						[100, -32, -100, -100, -100]])
	kernel4 = np.array([[-100, -100, 0, 100, 100],
						[-100, -100, 0, 100, 100],
						[-100, -100, 0, 100, 100],
						[-100, -100, 0, 100, 100],
						[-100, -100, 0, 100, 100]])
	kernel5 = np.array([[-100, 32, 100, 100, 100],
						[-100, -78, 92, 100, 100],
						[-100, -100, 0, 100, 100],
						[-100, -100, -92, 78, 100],
						[-100, -100, -100, -32, 100]])
	kernel6 = np.array([[100, 100, 100, 100, 100],
						[-32, 78, 100, 100, 100],
						[-100, -92, 0, 92, 100],
						[-100, -100, -100, -78, 32],
						[-100, -100, -100, -100, -100]])
	for x in range(imageW-5):
		for y in range(imageH-5):
			res[x][y] = max( convolution(img[x:x+5, y:y+5], kernel1),
				convolution(img[x:x+5, y:y+5], kernel2),
				convolution(img[x:x+5, y:y+5], kernel3),
				convolution(img[x:x+5, y:y+5], kernel4),
				convolution(img[x:x+5, y:y+5], kernel5),
				convolution(img[x:x+5, y:y+5], kernel6))
	return res


if __name__ == '__main__':
	print("hw9")
	img = cv2.imread('lena.bmp', cv2.IMREAD_GRAYSCALE)
	img_pad3 = padding_img_3(img)	
	img_pad5 = padding_img_5(img_pad3)	
	
	# (a) Robert's Operator: 12	
	img_Robert = (roberts(img_pad3) < 12) * 255
	cv2.imwrite('robert.bmp', img_Robert)
	print("[Done] Robert")
	
	# (b) Prewitt's Edge Detector: 24
	img_Prewitt = (prewittsEdge(img_pad3) < 24) * 255
	cv2.imwrite('prewitt.bmp', img_Prewitt)
	print("[Done] Prewitt")
    
	# (c) Sobel's Edge Detector: 38
	img_Sobel = (sobelsEdge(img_pad3) < 38) * 255 
	cv2.imwrite('sobel.bmp', img_Sobel)
	print("[Done] Sobel")
    
	# (d) Frei and Chen's Gradient Operator: 30
	img_Frei_Chen = (freiAndChensGradient(img_pad3) < 30) * 255
	cv2.imwrite('freichen.bmp', img_Frei_Chen)
	print("[Done] Frei Chen")
	
	# (e) Kirsch's Compass Operator: 135
	img_Krisch = (kirschsCompass(img_pad3) < 135) * 255
	cv2.imwrite('kirsch.bmp', img_Krisch)
	print("[Done] Krisch")
    
	# (f) Robinson's Compass Operator: 43
	img_Robinson = (robinsonsCompass(img_pad3) < 43) * 255
	cv2.imwrite('robinson.bmp', img_Robinson)
	print("[Done] Robinson")

	# (g) Nevatia-Babu 5x5 Operator: 12500
	img_NB = (nevatiaBabu(img_pad5) < 12500) * 255
	cv2.imwrite('eviatiababu.bmp', img_NB)	
	print("[Done] Neviatia Babu")
