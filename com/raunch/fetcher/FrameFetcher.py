#!/usr/bin/python 
# -*- coding: utf-8 -*-
'''
Created on 20190814

@author: shun
'''
import functools
import os
import re
import subprocess

from DownloadHelper import HttpsDownloader
from DownloadHelper import YoutubeDownloader

def getVideoFromWeb(url, savePath):    
    if not os.path.exists(savePath):
        os.makedirs(savePath)    
    for file in os.listdir(savePath):
        os.remove(os.path.join(savePath, file))
    defaultName = "bematevideo"
    
    if str(url).startswith("youtube"):
        youtubeDownloader = YoutubeDownloader(url, savePath)
        splits = str(url).split("://")        
        if not youtubeDownloader.download(splits[1]):
            return None
    else:    
        myDownload = HttpsDownloader(url, savePath)              
        if not myDownload.download("bemate"):
            return None
    
        
    #cmdList = ["you-get", "-o", savePath, "-O", defaultName, url, "--force"]
    #print (cmdList)
    #result = subprocess.call(cmdList)
    targetFileWithMp4 = os.path.join(savePath, defaultName + ".mp4")
    targetFileWithWebm = os.path.join(savePath, defaultName + ".webm")
    
        
    if os.path.exists(targetFileWithMp4):
        return targetFileWithMp4
    elif os.path.exists(targetFileWithWebm):
        return targetFileWithWebm
    else:
        fileWithNoSuffix = os.path.join(savePath, defaultName)
        fileWithMp4Suffix = os.path.join(savePath, defaultName + ".MP4")
        fileWithWebmSuffix = os.path.join(savePath, defaultName + ".WEBM")
        if os.path.exists(fileWithNoSuffix):
            os.rename(fileWithNoSuffix, targetFileWithMp4)
            return targetFileWithMp4
        elif os.path.exists(fileWithMp4Suffix):
            os.rename(fileWithMp4Suffix, targetFileWithMp4)
            return targetFileWithMp4
        elif os.path.exists(fileWithWebmSuffix):
            os.rename(fileWithWebmSuffix, targetFileWithWebm)
            return targetFileWithWebm
        else:
            return None

def extract_frames(video_file, saveFolder, rate):
    """Return a list of PIL image frames uniformly sampled from an mp4 video."""
    try:
        if not os.path.exists(saveFolder):
            os.makedirs(saveFolder)
    except OSError:
        return None
    output = subprocess.Popen(['ffmpeg', '-i', video_file],
                              stderr=subprocess.PIPE).communicate()
    # Search and parse 'Duration: 00:05:24.13,' from ffmpeg stderr.
    re_duration = re.compile(r'Duration: (.*?)\.')
    duration = re_duration.search(str(output[1])).groups()[0]

    seconds = functools.reduce(lambda x, y: x * 60 + y,
                               map(int, duration.split(':')))
    
    num_frames = int (seconds / float(rate))
    rate = num_frames / float(seconds)
    
    output = subprocess.call(['ffmpeg', '-i', video_file,
                                '-vf', 'fps={}'.format(rate),
                               '-vframes', str(num_frames),
                               '-loglevel', 'panic',
                               os.path.join(saveFolder,'%d.jpeg')])
    
    


    if output == 0 :
        os.remove(video_file)
        frame_paths = sorted([os.path.join(saveFolder, frame)
                          for frame in os.listdir(saveFolder)])
        return frame_paths
    else:
        return None
    

def fetchFrameWithUrl(url, savePath, rate):
    videoPath = getVideoFromWeb(url, savePath)    
    if not videoPath == None :
        print ("the video now is " + videoPath)
        result = extract_frames(videoPath, savePath, rate)
        if not result == None:
            return result
        else:
            return None
    else:
        return None
        


if __name__ == '__main__':
    url = os.sys.argv[1]
    savePath= os.sys.argv[2]
    rate = os.sys.argv[3]
    result = fetchFrameWithUrl(url, savePath, rate)
    if result == None:
        print ("no pics")
    else:
        for frame in result :
            print ("final pic path: " + frame)
    pass