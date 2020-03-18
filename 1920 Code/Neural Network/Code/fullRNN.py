import sys
import FindIdealW
import PredictChange
import GetIdealColor
import insertPoint
import timeit

# Main RNN runner function
def getWater(plant_num, temp, light, color, now):
    # Get new data points
    newTemp = temp
    newLight = light
    collectedColor = color
    idealcolor = float(GetIdealColor.idealColor())
    healthy1 = False
    healthy2 = False

    # Execute functions to find theoretical and empirical irrigation volumes
    theoreticalX, healthy1 = FindIdealW.findW(plant_num, newTemp, newLight)
    empiricalX, healthy2 = PredictChange.changePredict(plant_num, collectedColor, idealcolor)

    # Check if crop is considered healthy
    healthy = False
    if healthy1 == True and healthy2 == True:
        healthy = True
    else:
        healthy = False

    # After calculation, insert new point into SQL database
    insertPoint.insertPoint(plant_num, empiricalX, theoreticalX, collectedColor, newTemp, newLight, healthy, now)
    return empiricalX, theoreticalX

if __name__ == "__main__":
    print(getWater('1', int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), ""))