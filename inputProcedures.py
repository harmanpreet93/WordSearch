from myImports import *

def getSearchWord():
	searchWord = raw_input("Enter the word to search from image: ")
	return searchWord

def readInputImage():
	# inputImg = raw_input("Please provide the input image to search: ")
	inputImg = 'l.png'
	# print "Image path you entered is: ", inputImg

	# Check if valid image path and valid image extension
	if not validateImage(inputImg):
		exit(0)

	# If valid image path and valid image extension, then go ahead
	# Read input image and word to search here
	colorFlag = True
	return cv2.imread(inputImg,colorFlag)

	# Plot image
	# plotImage(inputImg)

def validateImage(inputImg):
	validImageExts = ['.bmp', '.pbm', '.pgm', '.ppm', '.sr', '.ras', '.jpeg', '.jpg', 
	    				'.jpe', '.jp2', '.tiff', '.tif', '.png']
	
	# Check if input image has valid path
	if not os.path.exists(inputImg):
		print "*****IMAGE NOT FOUND*****"
		return False
		
	else:
		# Check if input image has valid extension
		if not os.path.splitext(inputImg)[1] in validImageExts:
			print "*****NOT A VALID IMAGE EXTENSION*****"
			return False
		return True

def convertToGrayScale(image):
	return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def applyFilter(image,filter):
	ksize = (3,3)
	if filter == 'gaussianBlur':
		return applyGaussianFilter(image,ksize)
	
	elif filter == 'medianBlur':
		return applyMedianFilter(image,ksize[0])
	
	return applyMedianFilter(image,ksize[0])

def applyGaussianFilter(image,ksize):
	sigmaX = 0
	return cv2.GaussianBlur(image,ksize,sigmaX)

def applyMedianFilter(image,ksize):
	return cv2.medianBlur(image, ksize)

def applyBinarization(image,thresholdType):
	if thresholdType == 'simple':
		return simpleThresholding(image)

	elif thresholdType == 'adaptive':
		return adaptiveThresholding(image)

	elif thresholdType == 'otsu':
		return otsuThresholding(image)

	return adaptiveThresholding(image)

def simpleThresholding(image):
	threshold = 127
	maxValue = 255
	thresholdType = cv2.THRESH_BINARY_INV
	ret,outputImg = cv2.threshold(image,threshold,maxValue,thresholdType)
	return outputImg 

def adaptiveThresholding(image):
	maxValue = 255
	adaptiveMethod = cv2.ADAPTIVE_THRESH_MEAN_C
	thresholdType = cv2.THRESH_BINARY_INV
	# block size can vary
	blockSize = 51
	subtractionConst = 10
	return cv2.adaptiveThreshold(image, maxValue, adaptiveMethod, thresholdType, blockSize,subtractionConst) 

def otsuThresholding(image):
	threshold = 0
	maxValue = 255
	thresholdType = cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU
	ret,outputImg = cv2.threshold(image,threshold,maxValue,thresholdType)
	return outputImg 

def plotImage(inputImg):
	cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
	cv2.imshow('Image',inputImg)
	cv2.waitKey(0)
	cv2.destroyAllWindows()


