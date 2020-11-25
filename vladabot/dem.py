import requests
import PIL
from PIL import Image, ImageDraw, ImageFont
import random

str1 = 'dddd'
str2 = 'dddsfsfsddd'

TEMPLATE_FILENAME = 'template.jpg'
EXTENSIONS = ['.jpg', '.png']

RESULT_FILENAME = 'result.jpg'

UPPER_FONT = 'times.ttf'
UPPER_SIZE = 45
UPPER_FONT_Y = 390
LOWER_FONT = 'arialbd.ttf'
LOWER_SIZE = 14
LOWER_FONT_Y = 450

TEMPLATE_WIDTH = 574
TEMPLATE_HEIGHT = 522
TEMPLATE_COORDS = (75, 45, 499, 373)
PADDING = 10

def isValidExtension(filename):
    for extension in EXTENSIONS:
        if filename.endswith(extension):
            return True
    return False


def drawXAxisCenteredText(image, text, font, size, pos_y):
    draw = ImageDraw.Draw(image)
    textFont = ImageFont.truetype(font, size)
    textWidth = textFont.getsize(text)[0]

    while textWidth >= TEMPLATE_WIDTH - PADDING * 2:
        textFont = ImageFont.truetype(font, size)
        textWidth = textFont.getsize(text)[0]
        size -= 1
    
    draw.text(((TEMPLATE_WIDTH - textWidth) / 2, pos_y), text, font = textFont)

def getSizeFromArea(area):
    return (area[2] - area[0], area[3] - area[1])

def makeImage(str1, str2):
    frame = PIL.Image.open(TEMPLATE_FILENAME)
    demot = PIL.Image.open("img.jpg")
    demot = demot.resize(getSizeFromArea(TEMPLATE_COORDS), PIL.Image.ANTIALIAS)
    frame.paste(demot, TEMPLATE_COORDS)

    drawXAxisCenteredText(frame, str1,
                          UPPER_FONT, UPPER_SIZE,
                          UPPER_FONT_Y)
    drawXAxisCenteredText(frame, str2,
                          LOWER_FONT, LOWER_SIZE,
                          LOWER_FONT_Y)
    frame = frame.convert("RGB")
    frame.save(RESULT_FILENAME)
    frame.show()
