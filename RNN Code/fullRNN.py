import sys
import findW
import changePredict
import idealColor
import getColor

newTemp = float(sys.argv[1])
newHeat = float(sys.argv[2])
collectedColor = getColor.getColor(sys.argv[3])
idealColor = float(idealColor.idealColor())

theoreticalX = findW.findW(newTemp, newHeat)
empericalX = changePredict.changePredict(collectedColor, idealColor)

print((theoreticalX+empericalX)/2)