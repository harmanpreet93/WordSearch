from inputProcedures import *

if __name__ == "__main__":
    # Read input user image from getInputImage
    inputImg = readInputImage()

    # Ask user for the word to search
    searchWord = getSearchWord()
    print "Search-Word:",searchWord

    # Copy of image
    copyImage = np.copy(inputImg)
    letterCount = len(searchWord)

    # convert image to grayScale and filter image
    grayImage = convertToGrayScale(inputImg)
    
    # apply filter
        # - medianBlur or gaussianBlur
        # - no argument applies medianBlur
    # filteredImage = applyFilter(grayImage,'medianBlur')

    # perform binarization
        # - simple, adaptive or otsu
        # - no argument applies adaptive
    binarizedImg = applyBinarization(grayImage,'adaptive')

    # plotImage(binarizedImg)

    size = binarizedImg.shape[0],binarizedImg.shape[1],3
    bb_mask = np.zeros(size, dtype=np.uint8)

    bwImgForTess = np.copy(binarizedImg)

    wordBox = cv2.cvtColor(binarizedImg,cv2.COLOR_GRAY2RGB)

    ret,thresh = cv2.threshold(grayImage,127,255,0)
    outputImg,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    outputImg = cv2.drawContours(outputImg,contours,-1,(0,255,0),3)

    # plotImage(outputImg)
    letterWithBox = np.copy(wordBox)
    boundRectangle = labelLettersWithBox(inputImg, contours)

    # calculate avg character width, height and area
    cArea,cHeight,cWidth,widthLimit = findCharacterSize(boundRectangle,letterCount)

    boundRectangle = mergeBox(boundRectangle,cHeight,cWidth,cArea)
    boundRectangle = clearNullRectangles(boundRectangle,cArea)

    testImg = np.copy(copyImage)
    drawBoxes(copyImage,boundRectangle)

    resultImage,bb_mask = searchAndLabelWord(bb_mask, wordBox, bwImgForTess, boundRectangle, searchWord, widthLimit,testImg)
    
    plotImage(resultImage)
