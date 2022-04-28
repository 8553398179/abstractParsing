# -*- coding: utf-8 -*-
import os


#import methods 
from abstractParse import abstractAnalysis


def abstractParseEntireFolder(folderLocation):
   files = os.listdir(folderLocation)
   for file in files:
      if ".pdf" in file:
          abstractAnalysis(folderLocation+'/'+file)
          #print(folderLocation+'/'+file)
          

#abstractParseEntireFolder("C:/Users/darshanRaghunath/Downloads/process")
