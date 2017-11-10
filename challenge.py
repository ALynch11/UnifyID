import requests
import re
from PIL import Image
import random
import numpy as np


def createURL(numberOfIntegers, minRand, maxRand, col, base):
    originalString = "https://www.random.org/integers/?"
    originalString += "num=" + str(numberOfIntegers)
    originalString += "&min=" + str(minRand)
    originalString += "&max=" + str(maxRand)
    originalString += "&col=" + str(col)
    originalString += "&base=" + str(base) + "&format=plain&rnd=new"
    return originalString

def decodeResponse(response):
    '''
    input- api response in byte stream
    returns - list of random numbers from response
    '''
    mid = response.content.decode("utf-8")
    numbers = re.split(r"[\t\n]+",mid)
    while "" in numbers:
        numbers.remove("")
    return numbers

def createColor():
    '''
    returns numpy array representing a color in the image
    '''
    pixelsStillNeeded = 16384
    minRand = 0
    maxRand = 255
    col = 128
    base = 2
    midList = []
    while pixelsStillNeeded > 0:
        if (pixelsStillNeeded - 10000) > 0:
            requestNumber =  10000
        else:
            requestNumber = pixelsStillNeeded
        print(requestNumber)
        pixelsStillNeeded -= requestNumber
        
        url = createURL(requestNumber,minRand, maxRand, col, base)
        response = requests.get(url)
        listOfNumbers = decodeResponse(response)
        
        listOfNumbers = populateList(requestNumber)
        midList += listOfNumbers
    #print(len(midList))
    finalArray = np.array(midList)
    return np.reshape(finalArray, (128,128))

def populateList(num):
    final = []
    for i in range(num):
        ran = random.randint(0,255)
        bi = str(bin(ran))
        final.append(bi[2:])
    return final
    
def createImage(red, blue, green):
    '''
    takes in 3 np arrays of size (128,128) representing
    red blue and green colors in the image


    '''
    imageArray = np.zeros([128,128,3])
    imageArray[:,:,0] = red
    imageArray[:,:,1] = blue
    imageArray[:,:,2] = green

    imageArray = np.uint8(imageArray)

    img = Image.fromarray(imageArray)
    img.save("randomImage.BMP")
    img.show() 
r = createColor()
g = createColor()
b = createColor()
createImage(r,b,g)
print(r.shape, g.shape, b.shape)
#https://www.random.org/integers/?num=10&min=1&max=6&col=1&base=10&format=plain&rnd=new