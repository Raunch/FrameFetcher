#!/usr/bin/python 
# -*- coding: utf-8 -*-
'''
Created on 20190520

@author: shun
'''

import subprocess
import os
import json

class Downloader(object):
    '''
    classdocs
    '''


    def __init__(self, url):
        '''
        Constructor
        '''
        self.url = url
        self.outputFolder = "/home/centos/Downloads/tensorvideo"
        #self.outputFolder = os.path.join("G:\\", "testfilename", "hello")
        
    def download(self):
        print ("download the url")
        return None
        
class YoutubeDownloader(Downloader):
    '''
    classdocs
    '''


    def __init__(self, url):
        '''
        Constructor
        '''
        Downloader.__init__(self, url)
        
    def download(self, name):        
        downUrl = "https://www.youtube.com/watch?v=" + name
        tagResult = self.getItagfor18(downUrl)
        if tagResult:
            videoFile = os.path.join(self.outputFolder,"\"" + tagResult["name"] + "." + tagResult["container"] +"\"")
            if os.path.exists(videoFile):
                os.remove(videoFile)
            cmdList = cmdList = ["you-get", "--itag=" + tagResult["tag"], "-o", self.outputFolder, downUrl]            
        else:
            return None                
        print (cmdList)
        
        result = subprocess.call(cmdList)
        if result == 0:            
            return os.path.join(self.outputFolder,tagResult["name"] + "." + tagResult["container"])
        else:
            print ("youtube fetch err")
            return None
        
    def getItagfor18(self, url):
        result = {}
        try:
            cmdList = ["you-get", "--json", url]
            process = subprocess.Popen(cmdList, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            process.wait()
            jsonInfo = process.stdout.read()
            youtubeJson = json.loads(jsonInfo)
            print (youtubeJson["title"])
            result["name"] = youtubeJson["title"]
            streamInfo = youtubeJson["streams"]
            sortKeys = sorted(streamInfo.keys())
            for key in sortKeys:
                tagInfo = streamInfo[key]
                if tagInfo["container"] == "mp4" or tagInfo["container"] == "webm":
                    result["tag"] = key
                    result["container"] = tagInfo["container"]
                    break
                else:
                    continue
        except Exception as e:
            print ("has err in get itag for 18")
        finally:
            return result
           
    
class HttpsDownloader(Downloader):
    '''
    classdocs
    '''


    def __init__(self, url):
        '''
        Constructor
        '''
        Downloader.__init__(self, url)
        
    def download(self, name):
        splitsNames = str(name).split(".")
        outputName = os.path.join(self.outputFolder, splitsNames[0])
        if os.path.exists(outputName):
            os.remove(outputName)
        cmdList = ["you-get", "-o", self.outputFolder, "-O", splitsNames[0], self.url, "--force"]
        print (cmdList)
        result = subprocess.call(cmdList)
        if result == 0:
            return os.path.join(self.outputFolder, name)
        else:
            return None


def getItagfor18(url):
    result = {}
    try:
        cmdList = ["you-get", "--json", url]
        process = subprocess.Popen(cmdList, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        process.wait()
        jsonInfo = process.stdout.read()
        youtubeJson = json.loads(jsonInfo)
        print (youtubeJson["title"])
        result["name"] = youtubeJson["title"]
        streamInfo = youtubeJson["streams"]
        sortKeys = sorted(streamInfo.keys())
        for key in sortKeys:
            tagInfo = streamInfo[key]
            if tagInfo["container"] == "mp4" or tagInfo["container"] == "webm":
                result["tag"] = key
                result["container"] = tagInfo["container"]
                break
            else:
                continue
    except Exception as e:
        print ("has err in get itag for 18")
    finally:
        return result
   
if __name__ == '__main__':
    url = "https://www.youtube.com/watch?v=VqgsDcNN-x8"
    print (getItagfor18(url))
        
    print ("hello boy")    