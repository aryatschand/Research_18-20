import sys
import findW
import changePredict
import idealColor
import getColor
import insertPoint
import timeit

#Your statements here
def getWater(temp, light, color):
    newTemp = temp
    newLight = light
    #f = open('image.txt', 'w')
    #f.write(sys.argv[3])
    #collectedColor = getColor.getColor("image.txt")
    collectedColor = color
    idealcolor = float(idealColor.idealColor())

    theoreticalX = findW.findW(newTemp, newLight)
    empericalX = changePredict.changePredict(collectedColor, idealcolor)
    water = min([theoreticalX, empericalX]) * 0.67 + max([theoreticalX, empericalX]) * 0.33
    insertPoint.insertPoint(water, collectedColor, newTemp, newLight)
    return water

if __name__ == "__main__":
    print(getWater(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])))