import base64
import colorsummarizer

def getColor(imgFile):
    imgString = open(imgFile, 'r')
    imageString = imgString.read()
    with open("newImage.png", "wb") as fh:
        fh.write(base64.b64decode(imageString))

    return colorsummarizer.colorsummarizer("C:\\Users\\Arya\\Documents\\GitHub\\Research-19-20\\RNN Code\\newImage.png")