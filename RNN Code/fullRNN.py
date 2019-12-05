import sys
import findW
import changePredict
import idealColor
import getColor
import insertPoint

newTemp = float(sys.argv[1])
newLight = float(sys.argv[2])
f = open('image.txt', 'w')
f.write(sys.argv[3])
collectedColor = getColor.getColor("image.txt")
idealColor = float(idealColor.idealColor())

theoreticalX = findW.findW(newTemp, newLight)
empericalX = changePredict.changePredict(collectedColor, idealColor)
water = (theoreticalX+empericalX)/2
insertPoint.insertPoint(water, collectedColor, newTemp, newLight)
print(water)