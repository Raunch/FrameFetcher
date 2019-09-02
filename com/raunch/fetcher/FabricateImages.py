#!/usr/bin/python 
# -*- coding: utf-8 -*-
'''
Created on 20190829

@author: shun
'''
from PIL import Image
import os

LARGE_HALF_WIDTH = 1440
LARGE_HALF_HEIGHT = 720

MEDIUM_HALF_WIDTH = 512
MEDIUM_HALF_HEIGHT = 256

LARGE_QUARTER_WIDTH = 1200
LARGE_QUARTER_HEIGHT = 900

MEDIUM_QUARTER_WIDTH = 800
MEDIUM_QUARTER_HEIGHT = 600


def removeOldThumbnail(path):
    if path.endswith("/") or path.endswith("\\"):
        dirName = os.path.basename(os.path.dirname(path)) + "_thumbnail"
        saveDirParent = os.path.dirname(os.path.dirname(path))
    else:
        dirName = os.path.basename(path) + "_thumbnail"
        saveDirParent = os.path.dirname(path)
    
    saveDir = os.path.join(saveDirParent, dirName)
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)
    for file in os.listdir(saveDir):
        os.remove(os.path.join(saveDir, file))


def getThumbnail(path):
    fileName = os.path.basename(path)
    dirName = os.path.basename(os.path.dirname(path)) + "_thumbnail"
    saveDirParent = os.path.dirname(os.path.dirname(path))
    saveDir = os.path.join(saveDirParent, dirName)
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)    
    savePath = os.path.join(saveDir, fileName)
    im = Image.open(path)
    vertical = True
    w,h = im.size
    # print ("size is w : " + str(w) + " h : " + str(h))
    if w >= h:
        vertical = False
    # print ("vertical is " + str(vertical))
    if vertical :
        backgroudImage = Image.new('RGB', (h, h), (0, 0, 0))    
        box = (int((h-w)/2), 0, int((h+w)/2), h)
        backgroudImage.paste(im, box)
    else:
        backgroudImage = Image.new('RGB', (w, w), (0, 0, 0))
        box = (0, int((w-h)/2), w, int((w+h)/2))
        backgroudImage.paste(im, box)
    backgroudImage.thumbnail((256, 256))
    #backgroudImage.save("e:/Webeye/FrameFetcher/testfolder/thumbnail.png")
    backgroudImage.save(os.path.abspath(savePath))

def getCover(path):
    im = Image.open(path)
    w,h = im.size
    # print ("size is w : " + str(w) + " h : " + str(h))
    if int(w/h) >= 2:
        backgroudImage = Image.new('RGB', (w, int(w/2)), (0, 0, 0))
        box = (0, int(w/4-h/2), int(w/4+h/2), w)
        backgroudImage.paste(im, box)
    else:
        backgroudImage = Image.new('RGB', (h*2, h), (0, 0, 0))
        box = (int(h-w/2), 0, int(h+w/2), h)
        backgroudImage.paste(im, box)
    print ("backgroud w " + str(backgroudImage.size[0]))
    if backgroudImage.size[0] >= 720:
        saveImage = backgroudImage.resize((1440, 720))
    else:
        saveImage = backgroudImage.resize((512, 256))
    print ("backgroud resize w " + str(saveImage.size[0]))
    # saveImage.save("e:/Webeye/FrameFetcher/testfolder/recover.png")

def getCoverRatio(path, ratioW, ratioH):
    im = Image.open(path)
    width,height = im.size
    # print ("size is w : " + str(width) + " h : " + str(height))
    if width/height >= ratioW/ratioH:
        heightNew = int(ratioH * width / ratioW)
        print ("new height is " + str(heightNew))
        backgroudImage = Image.new('RGB', (width, heightNew), (0, 0, 0))
        box = (0, int(heightNew/2-height/2), width, int(heightNew/2 + height/2))
        backgroudImage.paste(im, box)
    else:
        widthNew = int(ratioW * height / ratioH)
        backgroudImage = Image.new('RGB', (widthNew, height), (0, 0, 0))
        box = (int(widthNew/2 - width/2), 0, int(widthNew/2 + width/2), height)
        backgroudImage.paste(im, box)
    print ("backgroud w " + str(backgroudImage.size[0]))
    if backgroudImage.size[0] >= 720:
        if ratioW/ratioH == LARGE_HALF_WIDTH/LARGE_HALF_HEIGHT:
            saveImage = backgroudImage.resize((LARGE_HALF_WIDTH, LARGE_HALF_HEIGHT))
        elif ratioW/ratioH == LARGE_QUARTER_WIDTH/LARGE_QUARTER_HEIGHT:
            saveImage = backgroudImage.resize((LARGE_QUARTER_WIDTH, LARGE_QUARTER_HEIGHT))
    else:
        if ratioW/ratioH == MEDIUM_HALF_WIDTH / MEDIUM_HALF_HEIGHT:
            saveImage = backgroudImage.resize((MEDIUM_HALF_WIDTH, MEDIUM_HALF_HEIGHT))
        elif ratioW/ratioH == MEDIUM_QUARTER_WIDTH/MEDIUM_QUARTER_HEIGHT:
            saveImage = backgroudImage.resize((MEDIUM_QUARTER_WIDTH, MEDIUM_QUARTER_HEIGHT))
    print ("backgroud resize w " + str(saveImage.size[0]))
    saveImage.save(path)


if __name__ == '__main__':
    #getThumbnail("e:/Webeye/FrameFetcher/testfolder/20190829151602.jpg")
    getCoverRatio("e:/Webeye/FrameFetcher/testfolder/1566200679275_0001.jpeg", 4, 3)

    print ("hello")