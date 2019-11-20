from subprocess import check_output as cmd
import requests
import urllib.request

response = str(cmd("""C:\\colorsummarizer\\bin\\colorsummarizer -image "C:\\colorsummarizer\\img\\tucan.jpg" -clusters 7""", shell=True))
respArray = response.split(' ')
indices = [i for i, x in enumerate(respArray) if x == "hsv"]

colorArray = [[]]
for x in range(len(indices)):
    tempArray = []
    tempArray.append(respArray[indices[x]+1])
    tempArray.append(respArray[indices[x]+2])
    tempArray.append(respArray[indices[x]+3])
    tempArray.append(round(float(respArray[indices[x]-7])*100,3))
    colorArray.append(tempArray)
colorArray.pop(0)

print(colorArray)