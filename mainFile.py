from inputProcedures import *

def drawBoxes(img,boundRect):
    color = (0,0,255)
    for i in range(0,len(boundRect)):
        pt1 = (boundRect[i][0],boundRect[i][1])
        pt2 = (boundRect[i][0]+boundRect[i][2],boundRect[i][1]+boundRect[i][3])
        cv2.rectangle(img,pt1,pt2,color,1,8,0)

    plotImage(img)

def labelLettersWithBox(letterWithBox,contours):
    numContours = len(contours)
    boundRect = []

    color = (0,0,255)

    for i in range(0,numContours):
        ans = cv2.boundingRect(contours[i])
        boundRect.append(ans)
        # cv2.rectangle(letterWithBox,boundRect[i],color,1,8,0)
        pt1 = (ans[0],ans[1])
        pt2 = (ans[0]+ans[2],ans[1]+ans[3])
        cv2.rectangle(letterWithBox,pt1,pt2,color,1,8,0)
    # plotImage(letterWithBox)
    return boundRect

def findCharSize(boundRect,numLetters):
    areaMap = {}
    numRects = len(boundRect)
    for i in range(0,numRects):
        area = boundRect[i][2]*boundRect[i][3]
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
    widthLimit = numLetters * cWidth;

    return areaAvg,cHeight,cWidth,widthLimit

def mergeBox(boundRect,cHeight,cWidth):
    emptyRect = [0,0,0,0]
    for k in range(5):
        for i in range(0,len(boundRect)):
            # check for boundRect if already set to nullRect
            for j in range(i+1,len(boundRect)):
                if (boundRect[i] != emptyRect and boundRect[j] != emptyRect) and isInside(boundRect[i],boundRect[j]):
                    boundRect[j] = emptyRect
                elif (boundRect[i] != emptyRect and boundRect[j] != emptyRect) and isNeighbour(boundRect[i],boundRect[j],cHeight,cWidth):
                    boundRect = mergeBoundRect(boundRect,i,j)
                    break
    return boundRect

def mergeBoundRect(boundRect,i,j):
    left = min(boundRect[i][0], boundRect[j][0])
    top  = min(boundRect[i][1], boundRect[j][1])
    right = max(boundRect[i][0] + boundRect[i][2], boundRect[j][0] + boundRect[j][2])
    bottom = max(boundRect[i][1] + boundRect[i][3], boundRect[j][1] + boundRect[j][3])
    
    mergedRect = (left,top,right-left,bottom-top )

    # mergedRect = (boundRect[i][0], boundRect[i][1], max(boundRect[i][2], boundRect[j][2]), boundRect[j][1]+boundRect[j][3]-boundRect[i][1])
    # mergedRect = (boundRect[i][0], boundRect[i][1], boundRect[j][0]+boundRect[j][2]-boundRect[i][0], max(boundRect[i][3],boundRect[j][3]) )
    #store x,y,w,h for an empty rectangle, i.e., a point
    emptyRect = [0,0,0,0]
    # boundRect[i] = emptyRect
    boundRect[i] = mergedRect
    boundRect[j] = emptyRect
    # boundRect.append(mergedRect)
    return boundRect


def clearNullRect(boundRect,cArea):
    boundRect = [x for x in boundRect if (x[2]*x[3] != 0 and x[2]*x[3] >= 0.35*cArea and x[2]*x[3] <= 22*cArea)]
    return boundRect

def textRecognition(img):
    return pytesseract.image_to_string(img)

def addPadding(wordWindow):
    top = int(wordWindow.shape[0])
    bottom = int(wordWindow.shape[0])
    left = int(wordWindow.shape[1])
    right = int(wordWindow.shape[1])

    cv2.copyMakeBorder(wordWindow, wordWindowWithPadding, top, bottom, left, right, cv2.BORDER_CONSTANT, (0,0,0))
    return wordWindowWithPadding

def isMatch(result, wordToSearch):
    dist = findEditDistance(result, wordToSearch, len(wordToSearch)*0.3, 0)
    ratio = dist/len(wordToSearch)

    if dis == 0:
        return 0
    elif ratio<0.25 and dis>0:
        return 1
    elif ration<0.43 and dis>0:
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
    if rect1[0]<rect2[0] and rect1[1]<rect2[1] and (rect1[0]+rect1[2])>(rect2[0]+rect2[2]) and (rect1[1]+rect1[3])>(rect2[0]+rect2[3]):
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
    
    # two dx is because when the bounding box becomes a rectangle, the original dx will not work anymore
    # two rectangles intersect
    # if checkOverlap(rect1,rect2):
        # return True
    # if checkOverlap(l1,r1,l2,r2):
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


def searchAndLabelWord(bb_mask,wordWithBox,bwImageForTess,boundRect,searchWord,widthLimit):

    for i in range(0,len(boundRect)):
        pt1 = (boundRect[i][0],boundRect[i][1])
        pt2 = (pt1[0]+boundRect[i][2],pt1[1]+boundRect[i][3])
        
        if withinLengthRange(boundRect[i],widthLimit):
            wordWindow = bwImageForTess[boundRect[i][0]:boundRect[i][0]+boundRect[i][2],boundRect[i][1]:boundRect[i][1]+boundRect[i][3]]
            wordWindowWithPadding = addPadding(wordWindow)

            sResult = textRecognition(wordWindowWithPadding)
            
            matchCode = isMatch(sResult,searchWord)
            if matchCode >= 0:
                # exact match: red
                if (matchCode == 0):
                    color = Scalar(0,0,255)
                    cv2.rectangle(resultImage,pt1,pt2,color,4,8,0)
                    cv2.rectangle(bb_mask,pt1,pt2,color,4,8,0)

                elif matchCode == 1:
                    # not exactly match: blue
                    color = Scalar(0,0,255)
                    cv2.rectangle(resultImage,pt1,pt2,color,4,8,0)
                    cv2.rectangle(bb_mask,pt1,pt2,color,4,8,0)
                
                elif matchCode == 2:
                    # even further: green
                    color = Scalar(0,255,0)
                    cv2.rectangle(resultImage,pt1,pt2,color,4,8,0)
                    cv2.rectangle(bb_mask,pt1,pt2,color,4,8,0)

        cv2.rectangle(wordWithBox,pt1,pt2,(0,0,255),4,8,0)
    return resultImage,bb_mask


if __name__ == "__main__":
    # Read input user image from getInputImage
    inputImg = readInputImage()

    # Ask user for the word to search
    searchWord = getSearchWord()
    print "Search-Word:",searchWord

    # Copy of image
    copyImage = np.copy(inputImg)
    numLetters = len(searchWord)

    # convert image to grayScale and filter image
    grayImage = convertToGrayScale(inputImg)
    
    # apply filter
        # - medianBlur or gaussianBlur
        # - no argument applies medianBlur
    filteredImage = applyFilter(grayImage,'gaussianBlur')

    # perform binarization
        # - simple, adaptive or otsu
        # - no argument applies adaptive
    binarizedImg = applyBinarization(filteredImage,'otsu')

    # plotImage(binarizedImg)

    # skipped deskew part for now

    size = binarizedImg.shape[0],binarizedImg.shape[1],3
    bb_mask = np.zeros(size, dtype=np.uint8)

    bwImageForTess = np.copy(binarizedImg)

    wordWithBox = cv2.cvtColor(binarizedImg,cv2.COLOR_GRAY2RGB)

    ret,thresh = cv2.threshold(filteredImage,127,255,0)
    outputImg,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    outputImg = cv2.drawContours(outputImg,contours,-1,(0,255,0),3)

    # plotImage(outputImg)
    letterWithBox = np.copy(wordWithBox);
    boundRect = labelLettersWithBox(inputImg, contours)

    cArea,cHeight,cWidth,widthLimit = findCharSize(boundRect,numLetters)

    # print cHeight

    boundRect = mergeBox(boundRect,cHeight,cWidth)
    boundRect = clearNullRect(boundRect,cArea)

    drawBoxes(copyImage,boundRect)

    resultImage,bb_mask = searchAndLabelWord(bb_mask, wordWithBox, bwImageForTess, boundRect, searchWord, widthLimit)
    
    cv2.imwrite("bb_mask.jpg", bb_mask)
    cv2.imwrite("result_image.jpg",resultImage)
