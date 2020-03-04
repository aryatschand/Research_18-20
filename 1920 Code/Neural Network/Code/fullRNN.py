import sys
import FindIdealW
import PredictChange
import GetIdealColor
import InsertPoint
import timeit

#Your statements here
def getWater(plant_num, temp, light, color, now):
    newTemp = temp
    newLight = light
    #f = open('image.txt', 'w')
    #f.write(sys.argv[3])
    #collectedColor = getColor.getColor("image.txt")
    collectedColor = color
    idealcolor = float(GetIdealColor.idealColor())
    healthy1 = False
    healthy2 = False
    theoreticalX, healthy1 = FindIdealW.findW(plant_num, newTemp, newLight)
    empiricalX, healthy2 = PredictChange.changePredict(plant_num, collectedColor, idealcolor)
    healthy = False
    if healthy1 == True and healthy2 == True:
        healthy = True
    else:
        healthy = False
    insertPoint.insertPoint(plant_num, empiricalX, theoreticalX, collectedColor, newTemp, newLight, healthy, now)
    return empiricalX, theoreticalX

if __name__ == "__main__":
    print(getWater('1', int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), ""))