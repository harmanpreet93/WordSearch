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
    for i in range(0,len(boundRect)):
        # check for boundRect if already set to nullRect
        for j in range(i+1,len(boundRect)):
            if (boundRect[i] != emptyRect and boundRect[j] != emptyRect) and isNeighbour(boundRect[i],boundRect[j],cHeight,cWidth):
                boundRect = mergeBoundRect(boundRect,i,j)
                break
    return boundRect

def mergeBoundRect(boundRect,i,j):
    # left = max(boundRect[i][0], boundRect[j][0])
    # top  = max(boundRect[i][1], boundRect[j][1])
    # right = min(boundRect[i][0] + boundRect[i][2], boundRect[j][0] + boundRect[j][2])
    # bottom = min(boundRect[i][1] + boundRect[i][3], boundRect[j][1] + boundRect[j][3])
    
    # mergedRect = (left,top,right-left,bottom-top )

    # mergedRect = (boundRect[i][0], boundRect[i][1], max(boundRect[i][2], boundRect[j][2]), boundRect[j][1]+boundRect[j][3]-boundRect[i][1])
    mergedRect = (boundRect[i][0], boundRect[i][1], boundRect[j][0]+boundRect[j][2]-boundRect[i][0], max(boundRect[i][3],boundRect[j][3]) )
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


#check if rectangles are neighbours of each other
def isNeighbour(rect1,rect2,cHeight,cWidth):

    if rect1[2]*rect1[3] == 0 or rect2[2]*rect2[3] == 0:
        return False

    y1 = rect1[1]+(rect1[1]+rect1[3])
    y2 = rect2[1]+(rect2[1]+rect2[3])

    dy = abs(y1 - y2)/2

    dy1 = abs(rect1[1] - rect2[1])
    dy2 = abs(rect1[1]+rect1[3] - (rect2[1]+rect2[3]))

    dx1 = abs(rect1[0] - rect2[0] - rect2[2])
    dx2 = abs(rect1[0] + rect1[2] - rect2[0])

    # if ((rect1 & rect2).area() != 0 ):
    #   return true
    
    l1 = [rect1[0],rect1[1]]
    r1 = [l1[0]+rect1[2],l1[1]+rect1[3]]
    l2 = [rect2[0],rect2[1]]
    r2 = [l2[0]+rect2[2],l2[1]+rect2[3]]
    
    # two dx is because when the bounding box becomes a rectangle, the original dx will not work anymore
    # two rectangles intersect
    # if checkOverlap(rect1,rect2):
        # return True
    if checkOverlap(l1,r1,l2,r2):
        return True

    if ((dy < 0.65 * cHeight or dy1 < 0.28 * cHeight or dy2 < 0.32 * cHeight)  and (dx1 < 0.31 * cWidth or dx2 < 0.31 *cWidth)):
        return True
    else:
        return False

# Returns true if two rectangles (l1, r1) and (l2, r2) overlap
# def checkOverlap(rect1,rect2):
#     left = max(rect1[0], rect2[0])
#     top  = max(rect1[1], rect2[1])
#     right = min(rect1[0] + rect1[2], rect2[0] + rect2[2])
#     bottom = min(rect1[1] + rect1[3], rect2[1] + rect2[3])
#     if(left <= right and top <= bottom):
#         return True
#     else:
#         return False

# Returns true if two rectangles (l1, r1) and (l2, r2) overlap
def checkOverlap(l1,r1,l2,r2):
     # If one rectangle is on left side of other
    if (l1[0] > r2[0] or l2[0] > r1[0]):
        return False

    # If one rectangle is above other
    if (l1[1] < r2[1] or l2[1] < r1[1]):
        return False

    return True

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
    blankImage = np.zeros(size, dtype=np.uint8)

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






    











    




    


