#!/usr/bin/python
#
#    M3U to JSON Converter
#    Made in Python3
#    02/2020
#    0fabris
#

import json
import requests
import sys
import re

class Channel():
    name = ""
    prop = {}
    url = ""
    def json(self):
        return {
                "name":self.name,
                "properties":self.prop,
                "url":self.url
                }

class M3U_to_JSON():
    def __init__(self):
        self.nomep = sys.argv[1]
        self.listach = []
        if not ("m3u" in self.nomep or "json" in self.nomep):
            print("Error, please input a json or m3u filename")
        
        try:
            self.nomeout = sys.argv[2]
        except:
            self.nomeout = self.nomep+".json"

        self.start()

    def start(self):
        with open(self.nomep,"r") as f:
            if "json" in self.nomep:
                self.fcontent = json.load(f)
            else:
                self.fcontent = f.read()

        ch = Channel()
        for i in self.fcontent.split("\n"):
            if "#EXTM3U" in i:
                pass
            elif "#EXT" in i:
                try:
                    ch.prop = self._parseProperties(i)
                except:
                    ch.prop = {}
                ch.name = i.split(",")[-1].strip()
                
            elif "://" in i:
                ch.url = i
                self.listach.append(ch)
                ch = Channel()

        for x in self.listach:
            print(x.json())
        self._writeJSON()

    def _parseProperties(self,row):
        retdict = {}
        for x in re.findall(r"#EXT.*:(-?\d+)\s(.*?=.*?)\s?\,\s?(.*?$)",row)[0]:
            print(x)
            if "=" in x:
                for i in x.split("\" "):
                    tmp = i.replace("\"","").split("=")
                    retdict[tmp[0]] = tmp[1]
        return retdict

    def _writeJSON(self):
        listaw=[]
        for i in self.listach:
            listaw.append(i.json())
        with open(self.nomeout,"w") as f:
            json.dump(listaw,f)
        print("Writing JSON: ok")

if __name__ == "__main__":
    if len(sys.argv)>1 and len(sys.argv)<3:
        try:
            M3U_to_JSON()
        except:
            print("Error, please report this to the dev.")
    else:
        print("Usage: ./m2j.py nomepl.(m3u|json) [nomefile.(json|m3u)]")
