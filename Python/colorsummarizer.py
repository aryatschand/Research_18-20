from subprocess import check_output as cmd
import requests
import urllib.request

response = str(cmd("""C:\\colorsummarizer\\bin\\colorsummarizer -image "C:\\colorsummarizer\\img\\greenplant.jpg" -clusters 4""", shell=True))
respArray = response.split(' ')
indices = [i for i, x in enumerate(respArray) if x == "hsv"]

colorArray = [[]]
for x in range(len(indices)):
    tempArray = []
    tempArray.append(int(respArray[indices[x]+1]))
    tempArray.append(int(respArray[indices[x]+2]))
    tempArray.append(int(respArray[indices[x]+3]))
    tempArray.append(round(float(respArray[indices[x]-7])*100,3))
    colorArray.append(tempArray)
colorArray.pop(0)

greenArray = []
for x in range(len(colorArray)):
    if colorArray[x][0] > 50 and colorArray[x][0] < 150 and colorArray[x][1] > 30:
        greenArray.append(colorArray[x][2] * colorArray[x][3]/100)

total = 0
for x in range(len(greenArray)):
    total += greenArray[x]

print(total)