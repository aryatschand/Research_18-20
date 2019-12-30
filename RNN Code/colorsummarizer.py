from subprocess import check_output as cmd
import requests
import urllib.request

def colorsummarizer(directory):
    response = str(cmd("""C:\\colorsummarizer\\bin\\colorsummarizer -image "{}" -clusters 4""".format(directory), shell=True))
    print(response)
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

    return total

if __name__ == "__main__":
    colorsummarizer("C:\\Users\\Arya\\Documents\\GitHub\\Research-19-20\\RNN Code\\newImage.png")