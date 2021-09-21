from PIL import Image
import random 
import numpy
def generateReferenceImage(originalImage,amountDataspoints):
    originalImageSize = originalImage.size
    minval = min(list(originalImageSize))
    XOffset1, YOffset1 = (originalImageSize[0]-minval)/2,(originalImageSize[1]-minval)/2
    XOffset2 , YOffset2 = minval+XOffset1, minval+YOffset1
    referenceImage = originalImage.crop((XOffset1,YOffset1,XOffset2, YOffset2))
    referenceImage = referenceImage.resize((amountDataspoints,amountDataspoints))
    referenceImage = referenceImage.convert("L")
    return referenceImage

def linify(url = "image2.jpeg", amountDataspoints = 100, factor = 2,criticalValues = (200,150,60)):

    originalImage = Image.open(url)
    referenceImage = generateReferenceImage(originalImage,amountDataspoints = amountDataspoints)
    # amountDataspoints = min([amountDataspoints,referenceImage.size[0]-10])
    factor = factor
    newImageSize = factor*amountDataspoints
    # newImageSize = max([newImageSize,referenceImage.size[0]])
    new = Image.new(mode="L", size=(newImageSize,newImageSize))
    originalImageSize = new.size
    pixel_map= new.load()
    def isBlack(i,j):
        return 0 if referenceImage.getpixel((i,j)) > criticalValues[0] else 1 if referenceImage.getpixel((i,j)) > criticalValues[1] else 2 if referenceImage.getpixel((i,j)) > criticalValues[2] else 3
    lines_hor = []
    lines_ver = []
    lines_diag = []
    for i in range(originalImageSize[0]//factor):
        active = False
        for j in range(originalImageSize[1]//factor):
            if not active and isBlack(i,j) > 1:
                active = True
                lines_hor.append((i,j))
            if active and not isBlack(i,j) > 1:
                active = False
                lines_hor.append((i,j-1))
        if active:
            lines_hor.append((i,amountDataspoints))
            active = False

    for i in range(originalImageSize[0]//factor):
        active = False
        for j in range(originalImageSize[1]//factor):
            if not active and isBlack(j,i) > 0:
                active = True
                lines_ver.append((j,i))
            if active and not isBlack(j,i) > 0:
                active = False
                lines_ver.append((j-1,i))
        if active:
            lines_ver.append((amountDataspoints,i))
            active = False
    def tupleAdd(first, second):
        return (first[0]+second[0],first[1]+second[1])

    def tupleMult(first, l):
        return (l*first[0],l*first[1])

    currPos = (-originalImageSize[0],0)
    movingDir = (1,1)
    active = False

    for i in range(-originalImageSize[0],originalImageSize[0]):
        if i < 0:
            currPos = (i+originalImageSize[0],0)
        else:
            currPos = (0,i)
        active = False
        while True:
            try:
                if isBlack(*currPos) > 2 and not active:
                    active = True
                    lines_diag.append(currPos)
                if active and not isBlack(*currPos) > 2:
                    active = False
                    lines_diag.append(tupleAdd(tupleMult(movingDir,-1),currPos))
                currPos = tupleAdd(currPos,movingDir)
            except:
                if active:
                    active = False
                    lines_diag.append(tupleAdd(tupleMult(movingDir,-1),currPos))
                break
    # print(lines_diag)
    for i in range(originalImageSize[0]):
        for j in range(originalImageSize[1]):
            if i%factor == 0 and j%factor == 0:
                pixel_map[i,j] = 0 if referenceImage.getpixel((i//factor,j//factor)) < 120 else 255
                # pixel_map[i,j] = 1
                pixel_map[i,j] = (255)
            else:
                pixel_map[i,j] = (255)

    for index in range(0,len(lines_hor), 2):
        start = lines_hor[index]
        end = lines_hor[index+1]
        for i in range(start[0]*factor, end[0]*factor+1):
            for j in range(start[1]*factor,end[1]*factor):
                pixel_map[i,j] = 0
    # # print(lines_ver)
    for index in range(0,len(lines_ver), 2):
        start = lines_ver[index]
        end = lines_ver[index+1]
        for i in range(start[1]*factor, end[1]*factor+1):
            for j in range(start[0]*factor,end[0]*factor):
                pixel_map[j,i] = 0

    for index in range(0,len(lines_diag), 2):
        start = lines_diag[index]
        end = lines_diag[index+1]
        # print(start,end)
        dimension = end[0]*factor-start[0]*factor
        for i in range(dimension):
            pixel_map[start[0]*factor+i,start[1]*factor+i] = 0

    return numpy.array(new)
    return pixel_map
# new.show()