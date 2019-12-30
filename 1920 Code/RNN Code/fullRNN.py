import sys
import findW
import changePredict
import idealColor
import getColor
import insertPoint
import timeit

start = timeit.default_timer()

#Your statements here


newTemp = float(sys.argv[1])
newLight = float(sys.argv[2])
f = open('image.txt', 'w')
f.write(sys.argv[3])
#collectedColor = getColor.getColor("image.txt")
collectedColor = 30
idealColor = float(idealColor.idealColor())

theoreticalX = findW.findW(newTemp, newLight)
empericalX = changePredict.changePredict(collectedColor, idealColor)
water = min([theoreticalX, empericalX]) * 0.67 + max([theoreticalX, empericalX]) * 0.33
insertPoint.insertPoint(water, collectedColor, newTemp, newLight)
print(water)

stop = timeit.default_timer()

print('Time: ', stop - start)  