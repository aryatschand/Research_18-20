import sys
import findW
import changePredict
import idealColor
import getColor
import insertPoint
import timeit

#Your statements here
def getWater(plant_num, temp, light, color, now):
    newTemp = temp
    newLight = light
    #f = open('image.txt', 'w')
    #f.write(sys.argv[3])
    #collectedColor = getColor.getColor("image.txt")
    collectedColor = color
    idealcolor = float(idealColor.idealColor())
    healthy1 = False
    healthy2 = False
    theoreticalX, healthy1 = findW.findW(plant_num, newTemp, newLight)
    empiricalX, healthy2 = changePredict.changePredict(plant_num, collectedColor, idealcolor)
    healthy = False
    if healthy1 == True and healthy2 == True:
        healthy = True
    else:
        healthy = False
    insertPoint.insertPoint(plant_num, empiricalX, theoreticalX, collectedColor, newTemp, newLight, healthy, now)
    return empiricalX, theoreticalX

if __name__ == "__main__":
    print(getWater('1', int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), ""))