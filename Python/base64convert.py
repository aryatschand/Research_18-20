import base64
import colorsummarizer

imgString = open('image.txt', 'r')
imageString = imgString.read()
with open("newImage.png", "wb") as fh:
    fh.write(base64.b64decode(imageString))

print(colorsummarizer.colorsummarizer("C:\\Users\\Arya\\Documents\\GitHub\\Research-19-20\\Python\\newImage.png"))
