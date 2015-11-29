from myImports import *

def getSearchWord():
	searchWord = raw_input("Enter the word to search from image: ")
	return searchWord

def readInputImage():
	inputImg = raw_input("Please provide the input image to search: ")
	# inputImg = 'i.png'
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

def drawBoxes(img,boundRectangle):
    color = (0,0,255)
    for i in range(0,len(boundRectangle)):
        pt1 = (boundRectangle[i][0],boundRectangle[i][1])
        pt2 = (boundRectangle[i][0]+boundRectangle[i][2],boundRectangle[i][1]+boundRectangle[i][3])
        cv2.rectangle(img,pt1,pt2,color,1,8,0)

    # plotImage(img)

def labelLettersWithBox(letterWithBox,contours):
    numContours = len(contours)
    boundRectangle = []

    color = (0,0,255)

    for i in range(0,numContours):
        ans = cv2.boundingRect(contours[i])
        boundRectangle.append(ans)
        # cv2.rectangle(letterWithBox,boundRectangle[i],color,1,8,0)
        pt1 = (ans[0],ans[1])
        pt2 = (ans[0]+ans[2],ans[1]+ans[3])
        cv2.rectangle(letterWithBox,pt1,pt2,color,1,8,0)
    # plotImage(letterWithBox)
    return boundRectangle

def findCharacterSize(boundRectangle,letterCount):
    areaMap = {}
    for i in range(0,len(boundRectangle)):
        area = boundRectangle[i][2]*boundRectangle[i][3]
        if areaMap.has_key(area):
            areaMap[area]+=1
        else:
            areaMap[area] = 1

    sorted_area = sorted(areaMap.items(), key=lambda x:x[1],reverse=True)
    
    areaAvg = 0.0
    for key in sorted_area[0:10]:
        areaAvg += key[0]
    areaAvg = areaAvg / 10.0;
    math.pow(3, 0)
    cHeight = math.pow(areaAvg,0.5)*1.1
    cWidth = math.pow(areaAvg,0.5)*0.75
    # cHeight = (areaAvg) **0.5 * 1.1;
    # cWidth = (areaAvg) **0.5 * 0.75;
    cArea = areaAvg;
    widthLimit = letterCount * cWidth;

    return areaAvg,cHeight,cWidth,widthLimit

def mergeBox(boundRectangle,cHeight,cWidth,cArea):
    emptyRect = [0,0,0,0]
    for k in range(5):
        for i in range(0,len(boundRectangle)):
            # check for boundRectangle if already set to nullRect
            for j in range(i+1,len(boundRectangle)):
                # if (boundRectangle[i] != emptyRect and boundRectangle[j] != emptyRect) and isInside(boundRectangle[i],boundRectangle[j]):
                #     boundRectangle[j] = emptyRect
                # elif (boundRectangle[i] != emptyRect and boundRectangle[j] != emptyRect) and isInside(boundRectangle[j],boundRectangle[i]):
                #     boundRectangle[i] = emptyRect
                #     # break
                if (boundRectangle[i] != emptyRect and boundRectangle[j] != emptyRect) and isNeighbour(boundRectangle[i],boundRectangle[j],cHeight,cWidth):
                    boundRectangle = mergeBoundRectangle(boundRectangle,i,j)
                    break

    for i in xrange(0,len(boundRectangle)):
        for j in xrange(i+1,len(boundRectangle)):
            # area = boundRectangle[j][2] * boundRectangle[j][3]
            if (boundRectangle[i] != emptyRect and boundRectangle[j] != emptyRect) and isInside(boundRectangle[i],boundRectangle[j]) and boundRectangle[i][2] * boundRectangle[i][3] < 50*cArea:
                boundRectangle[j] = emptyRect
            elif (boundRectangle[i] != emptyRect and boundRectangle[j] != emptyRect) and isInside(boundRectangle[j],boundRectangle[i]) and boundRectangle[j][2]*boundRectangle[j][3] < 50*cArea:
                boundRectangle[i] = emptyRect
                break

    # for k in range(2):
    #     for i in range(0,len(boundRectangle)):
    #         # check for boundRectangle if already set to nullRect
    #         for j in range(i+1,len(boundRectangle)):
    #             # if (boundRectangle[i] != emptyRect and boundRectangle[j] != emptyRect) and isInside(boundRectangle[i],boundRectangle[j]):
    #             #     boundRectangle[j] = emptyRect
    #             # elif (boundRectangle[i] != emptyRect and boundRectangle[j] != emptyRect) and isInside(boundRectangle[j],boundRectangle[i]):
    #             #     boundRectangle[i] = emptyRect
    #             #     # break
    #             if (boundRectangle[i] != emptyRect and boundRectangle[j] != emptyRect) and isNeighbour(boundRectangle[i],boundRectangle[j],cHeight,cWidth):
    #                 boundRectangle = mergeBoundRectangle(boundRectangle,i,j)
    #                 break

    return boundRectangle

def mergeBoundRectangle(boundRectangle,i,j):
    left = min(boundRectangle[i][0], boundRectangle[j][0])
    top  = min(boundRectangle[i][1], boundRectangle[j][1])
    right = max(boundRectangle[i][0] + boundRectangle[i][2], boundRectangle[j][0] + boundRectangle[j][2])
    bottom = max(boundRectangle[i][1] + boundRectangle[i][3], boundRectangle[j][1] + boundRectangle[j][3])
    
    mergedRect = (left,top,right-left,bottom-top )

    # mergedRect = (boundRectangle[i][0], boundRectangle[i][1], max(boundRectangle[i][2], boundRectangle[j][2]), boundRectangle[j][1]+boundRectangle[j][3]-boundRectangle[i][1])
    # mergedRect = (boundRectangle[i][0], boundRectangle[i][1], boundRectangle[j][0]+boundRectangle[j][2]-boundRectangle[i][0], max(boundRectangle[i][3],boundRectangle[j][3]) )
    #store x,y,w,h for an empty rectangle, i.e., a point
    emptyRect = [0,0,0,0]
    # boundRectangle[i] = emptyRect
    boundRectangle[i] = mergedRect
    boundRectangle[j] = emptyRect
    # boundRectangle.append(mergedRect)
    return boundRectangle

def clearNullRectangles(boundRectangle,cArea):
    boundRectangle = [x for x in boundRectangle if (x[2]*x[3] != 0 and x[2]*x[3] >= 0.35*cArea and x[2]*x[3] <= 50*cArea)]
    return boundRectangle

def textRecognition(img):
    return pytesser.image_to_string(img)

def addPadding(wordWindow):
    top = int(wordWindow.shape[0])
    bottom = int(wordWindow.shape[0])
    left = int(wordWindow.shape[1])
    right = int(wordWindow.shape[1])

    # wordWindowWithPadding = wordWindow
    wordWindowWithPadding = cv2.copyMakeBorder(wordWindow, top, bottom, left, right, cv2.BORDER_CONSTANT, (0,0,0))
    return wordWindowWithPadding

def isMatch(result, wordToSearch):
    dist = findEditDistance(result, wordToSearch, len(wordToSearch)*0.3, 0)
    ratio = dist/len(wordToSearch)

    if dist == 0:
        return 0
    elif ratio<0.25 and dist>0:
        return 1
    elif ratio<0.43 and dist>0:
        return 2
    else:
        return -1

def findEditDistance(str1, str2, cutoff, order):
    if str1 == str2:
        return 0
    if order>cutoff:
        return cutoff+1
    if str1 == "":
        return len(str2)
    if str2 == "":
        return len(str1)
    if str1[0] == str2[0]:
        return findEditDistance(str1[1:],str2[1:],cutoff,order)
    if str1[0] != str2[0]:
        dist1 = findEditDistance(str1,str2[1:],cutoff,order+1)+1
        dist2 = findEditDistance(str2,str1[1:],cutoff,order+1)+1
        dist3 = findEditDistance(str1[1:],str2[1:],cutoff,order+1)+1
        return min(dist1,dist2,dist3)
    return -1

#check if one rectangle is inside another
def isInside(rect1, rect2):
    if rect1[0]<=rect2[0] and rect1[1]<rect2[1] and (rect1[0]+rect1[2])>=(rect2[0]+rect2[2]) and (rect1[1]+rect1[3])>=(rect2[1]+rect2[3]):
        return True
    else:
        return False

#check if rectangles are neighbours of each other
def isNeighbour(rect1,rect2,cHeight,cWidth):

    if rect1[2]*rect1[3] == 0 or rect2[2]*rect2[3] == 0:
        return False

    l1 = [rect1[0],rect1[1]]
    r1 = [l1[0]+rect1[2],l1[1]+rect1[3]]
    l2 = [rect2[0],rect2[1]]
    r2 = [l2[0]+rect2[2],l2[1]+rect2[3]]
    
    # two dx is because when the bounding box becomes a rectangle, 
    # the original dx will not work anymore two rectangles intersect
    if checkOverlap(rect1,rect2):
        return True

    y1 = rect1[1]+(rect1[1]+rect1[3])
    y2 = rect2[1]+(rect2[1]+rect2[3])

    dy = abs(y1 - y2)/2

    dy1 = abs(rect1[1] - rect2[1])
    dy2 = abs(rect1[1]+rect1[3] - (rect2[1]+rect2[3]))

    dx1 = abs(rect1[0] - rect2[0] - rect2[2])
    dx2 = abs(rect1[0] + rect1[2] - rect2[0])

    # if ((rect1 & rect2).area() != 0 ):
    #   return true
    
    # l1 = [rect1[0],rect1[1]]
    # r1 = [l1[0]+rect1[2],l1[1]+rect1[3]]
    # l2 = [rect2[0],rect2[1]]
    # r2 = [l2[0]+rect2[2],l2[1]+rect2[3]]
    
    # # two dx is because when the bounding box becomes a rectangle, the original dx will not work anymore
    # # two rectangles intersect
    # # if checkOverlap(rect1,rect2):
    #     # return True
    # if checkOverlap(l1,r1,l2,r2):
    #     return True

    if ((dy < 0.65 * cHeight or dy1 < 0.28 * cHeight or dy2 < 0.32 * cHeight)  and (dx1 < 0.31 * cWidth or dx2 < 0.31 *cWidth)):
        return True
    else:
        return False

# Returns true if two rectangles (l1, r1) and (l2, r2) overlap
# def checkOverlap(l1,r1,l2,r2):
def checkOverlap(rect1,rect2):
    left = max(rect1[0], rect2[0])
    top  = max(rect1[1], rect2[1])
    right = min(rect1[0] + rect1[2], rect2[0] + rect2[2])
    bottom = min(rect1[1] + rect1[3], rect2[1] + rect2[3])
    
    if(left <= right and top <= bottom):
        return True
    else:
        return False
    
    # If one rectangle is on left side of other
    # if (l1[0] > r2[0] or l2[0] > r1[0]):
    #     return False

    # # If one rectangle is above other
    # if (l1[1] < r2[1] or l2[1] < r1[1]):
    #     return False

    return True


def withinLengthRange(rectBox,widthLimit):
    width = rectBox[2]
    if width > 0.1*widthLimit and width < 1.7*widthLimit:
        return True
    else:
        return False


def searchAndLabelWord(bb_mask,wordBox,bwImgForTess,boundRectangle,searchWord,widthLimit,testImg):

    resultImage = np.copy(testImg)
    for i in range(0,len(boundRectangle)):
        if boundRectangle[i]!=[0,0,0,0]:
            pt1 = (boundRectangle[i][0],boundRectangle[i][1])
            pt2 = (pt1[0]+boundRectangle[i][2],pt1[1]+boundRectangle[i][3])
            
            if withinLengthRange(boundRectangle[i],widthLimit):
                # print pt1,pt2,testImg.shape
                # cv2.rectangle(resultImage,pt1,pt2,(0,0,255),4,8,0)
                # plotImage(resultImage)
                # wordWindow = testImg[boundRectangle[i][0]:(boundRectangle[i][0]+boundRectangle[i][2]),boundRectangle[i][1]:(boundRectangle[i][1]+boundRectangle[i][3])]
                wordWindow = bwImgForTess[boundRectangle[i][1]:(boundRectangle[i][1]+boundRectangle[i][3]),boundRectangle[i][0]:(boundRectangle[i][0]+boundRectangle[i][2])]
                wordWindowWithPadding = addPadding(wordWindow)
                immg = 'tmp.bmp'
                cv2.imwrite(immg, wordWindowWithPadding)
                # plotImage(wordWindow)
               # tmp = Image.frotmpmarray(wordWindowWithPadding).save("tmp.png")
                
                sResult = textRecognition(Image.open(immg))

                # print sResult

                matchCode = isMatch(sResult,searchWord)
                if matchCode >= 0:
                    # exact match: red
                    if (matchCode == 0):
                        color = (0,0,255)
                        cv2.rectangle(resultImage,pt1,pt2,color,2,8,0)
                        cv2.rectangle(bb_mask,pt1,pt2,color,2,8,0)

                    elif matchCode == 1:
                        # not exactly match: blue
                        color = (0,0,255)
                        cv2.rectangle(resultImage,pt1,pt2,color,2,8,0)
                        cv2.rectangle(bb_mask,pt1,pt2,color,2,8,0)
                    
                    elif matchCode == 2:
                        # even further: green
                        color = (0,255,0)
                        cv2.rectangle(resultImage,pt1,pt2,color,2,8,0)
                        cv2.rectangle(bb_mask,pt1,pt2,color,2,8,0)
        cv2.rectangle(wordBox,pt1,pt2,(0,0,255),2,8,0)
    return resultImage,bb_mask