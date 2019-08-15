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


    def __init__(self, url, savepath):
        '''
        Constructor
        '''
        self.url = url
        self.outputFolder = savepath
        self.defaultName = "bematevideo"
        
    def download(self):
        print ("download the url")
        return None
        
class YoutubeDownloader(Downloader):
    '''
    classdocs
    '''


    def __init__(self, url, savepath):
        '''
        Constructor
        '''
        Downloader.__init__(self, url, savepath)
        
    def download(self, name):        
        downUrl = "https://www.youtube.com/watch?v=" + name
        tagResult = self.getItagfor18(downUrl)
        if tagResult:            
            cmdList = ["you-get", "--itag=" + tagResult["tag"], "-o", self.outputFolder, "-O", self.defaultName, downUrl]            
        else:
            return False                
        print (cmdList)
        print (tagResult["container"])
        
        result = subprocess.call(cmdList)
        if result == 0:            
            return True
        else:
            return False
        
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


    def __init__(self, url, savepath):
        '''
        Constructor
        '''
        Downloader.__init__(self, url, savepath)
        
    def download(self, name):
        cmdList = ["you-get", "-o", self.outputFolder, "-O", self.defaultName, self.url, "--force"]
        print (cmdList)
        result = subprocess.call(cmdList)
        if result == 0:
            return True
        else:
            return False


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