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
import urllib

def getVideoFromWeb(url, savePath):
    #scheme, _, path, _, _, = urllib.parse.urlsplit(url)
    if not os.path.exists(savePath):
        os.makedirs(savePath)
    defaultName = "bematevideo"
    for file in os.listdir(savePath):
        os.remove(os.path.join(savePath, file))
    cmdList = ["you-get", "-o", savePath, "-O", defaultName, url, "--force"]
    print (cmdList)
    result = subprocess.call(cmdList)
    targetFile = os.path.join(savePath, defaultName + ".mp4")
    if result == 0:
        print (targetFile)
        if os.path.exists(targetFile):
            return targetFile
        else:
            fileWithNoSuffix = os.path.join(savePath, defaultName)
            fileWithOtherSuffix = os.path.join(savePath, defaultName + ".MP4")
            if os.path.exists(fileWithNoSuffix):
                os.rename(fileWithNoSuffix, targetFile)
            elif os.path.exists(fileWithOtherSuffix):
                os.rename(fileWithOtherSuffix, targetFile)
            else:
                return None
            return targetFile
        
    else:
        return None    

def extract_frames(video_file, saveFolder, num_frames=8):
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
    print ("time long is " + str(seconds))
    #rate = num_frames / float(seconds)
    num_frames = seconds
    rate = 1
    

    output = subprocess.call(['ffmpeg', '-i', video_file,
                               '-vf', 'fps={}'.format(rate),
                               '-vframes', str(num_frames),
                               '-loglevel', 'panic',
                               saveFolder + '%d.jpeg'])
    if output == 0 :
        os.remove(video_file)
        frame_paths = sorted([os.path.join(saveFolder, frame)
                          for frame in os.listdir(saveFolder)])
        return frame_paths
    else:
        return None
        
 
    
    

def fetchFrameWithUrl(url, savePath):
    videoPath = getVideoFromWeb(url, savePath)
    print ("the video now is " + videoPath)
    if not videoPath == None :
        result = extract_frames(videoPath, savePath)
        if not result == None:
            return result
        else:
            return None
    else:
        return None
        


if __name__ == '__main__':
    url = os.sys.argv[1]
    savePath= os.sys.argv[2]
    result = fetchFrameWithUrl(url, savePath)
    for frame in result :
        print ("final pic path: " + frame)
    pass