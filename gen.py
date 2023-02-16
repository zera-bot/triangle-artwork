import math
import random
from PIL import Image, ImageDraw

l = 75 #SIDE length of triangle

cRange = 6 # color range (smaller = less color variation)
setting = 'shade' #shade or random
colorStr = "ff7777" #color (without hashtag)

#generates random color close to given color
def hexCloseTo(str_,range_):
    hexNumbers = [str_[i:i+2] for i in range(0, len(str_), 2)]
    outputNumbers = []
    if setting == 'random': #random color near color (gray input can have some random color in the output)
        for i in hexNumbers:
            number = int(i,16)
            number += random.randrange(-range_,range_)
            if number > 255: number = 255
            if number < 0: number = 0

            number = ("0"+str(hex(number))[2:])[-2:]
            outputNumbers.append(number)
    elif setting == 'shade': #random close shade of color (gray input will remain gray output)
        scale = random.randrange(-range_,range_)
        for i in hexNumbers:
            number = int(i,16)
            number += scale
            if number > 255: number = 255
            if number < 0: number = 0

            number = ("0"+str(hex(number))[2:])[-2:]
            outputNumbers.append(number)
        
    return "".join(outputNumbers)



median = math.sqrt( l**2 - ((l/2)**2) )
r = median/3
R = median/3*2
xLengthBetweenPoints = l/2 #(l*math.sqrt(3)**2)/(2*math.sqrt(3))
#print(xLengthBetweenPoints, median)

x_size = 1280
y_size = 720

x_triangles = math.ceil(x_size/l*2)+12
y_triangles = math.ceil(y_size/l*2)+12

posList = [] #you can copy + paste this list into desmos
coordsList = [] #position coordinates + roatation

#find center points
for x in range(x_triangles):
  for y in range(y_triangles):
    xEven = x%2==0
    yEven = y%2==0
    
    if xEven == True:
      if yEven == True:
        pos = (-l+(xLengthBetweenPoints*x),-l+(median*y))
        rot = 0
      else:
        pos = (-l+(xLengthBetweenPoints*x),-l+(median*y)+r)
        rot = 180
    else:
      if yEven == True:
        pos = (-l+(xLengthBetweenPoints*x),-l+(median*y)+r)
        rot = 180
      else:
        pos = (-l+(xLengthBetweenPoints*x),-l+(median*y))
        rot = 0

    coord = [pos,rot]
    
    coordsList.append(coord)
    posList.append(pos)

#start drawing
img = Image.new('RGB',(x_size,y_size))
draw = ImageDraw.Draw(img)
for p in coordsList:
  pPos = p[0]
  pRot = p[1]

  if pRot == 0:
    point1 = (pPos[0]+math.sqrt(R**2 - r**2),pPos[1]-r)
    point2 = (pPos[0]-math.sqrt(R**2 - r**2),pPos[1]-r)
    point3 = (pPos[0],pPos[1]+R)
  elif pRot == 180: #reverse the Y coord if rotated 180
    point1 = (pPos[0]-math.sqrt(R**2 - r**2),pPos[1]+r)
    point2 = (pPos[0]+math.sqrt(R**2 - r**2),pPos[1]+r)
    point3 = (pPos[0],pPos[1]-R)

  draw.polygon([point1,point2,point3], fill = f"#{hexCloseTo(colorStr,cRange)}")
img.save('test.png')