# -*- coding: utf-8 -*-
#import packages
import json




#import methods
from predictiveAnalysis.predictiveAnalysis import textAndCharacteristics
from predictiveAnalysis.predictiveAnalysis import removeRedundantCharacterists
from predictiveAnalysis.predictiveAnalysis import newPdfGetTextLabelsAndTextIndex
from predictiveAnalysis.predictiveAnalysis import classGrouping
from predictiveAnalysis.predictiveAnalysis import clusterFormation
from predictiveAnalysis.predictiveAnalysis import removeOtherClassCharacteristics
from predictiveAnalysis.predictiveAnalysis import uniqueTitleCharacteristics
from docxAndPdfGenerator.docxAndPdfGenerator import previewPdf
from docxAndPdfGenerator.docxAndPdfGenerator import createDocxWithDeliminator
from docxAndPdfGenerator.docxAndPdfGenerator import individualAbstractDocxCreation
from docxAndPdfGenerator.docxAndPdfGenerator import convertDocxToPdfEachAbstract
from docxAndPdfGenerator.docxAndPdfGenerator import folderCreation


def abstractAnalysis(filename):

	#getting config data like model Location , tokenizer location, output location
	configurationFile = open('config.json')
	configData = json.load(configurationFile)


	#Initialize the default values
	modelLocation = configData["modelLocation"]
	TokenizerLocation = configData["TokenizerLocation"]
	fileLocation = configData["outputLocation"]

    
    #creates folder in the name of the file name in output location
	filenameDocx = folderCreation(filename, fileLocation)


	#paragraph along with their characterisitics is extracted
	try:
        
        	print("Succesfully opened the pdf and extracted the required details")
        	text , characteristics, docObject = textAndCharacteristics(filename, filenameDocx)
        	print()

	except Exception as e:
        
        	print(e)
        
    


	#remove the redundant Characteristics if present
	characteristics = removeRedundantCharacterists(characteristics)

	#get the Labels for each paragraph
	textLabels , textIndex= newPdfGetTextLabelsAndTextIndex(text,characteristics,modelLocation,TokenizerLocation)

	#group all of them to differenct class
	title, author, affliation , abstract , noise , ids = classGrouping(textIndex, textLabels, text, characteristics)

	#form clusters for each classes
	titleCluster = clusterFormation(title , "Title")
	authorCluster = clusterFormation(author , "Author")
	affliationCluster = clusterFormation(affliation, "Affliation")
	abstractCluster = clusterFormation(abstract, "Abstract")
	noiseCluster = clusterFormation(noise, "Noise")
	idCluster = clusterFormation(ids, "Ids")


	#remove overlapping characteristics 
	otherCharacteristics = []
	otherCharacteristics = removeOtherClassCharacteristics(authorCluster,otherCharacteristics)
	otherCharacteristics = removeOtherClassCharacteristics(affliationCluster,otherCharacteristics)
	otherCharacteristics = removeOtherClassCharacteristics(abstractCluster,otherCharacteristics)



	#Extract title characteristics
	try:
    		print("Compeleted Cluster formation")
    		fontSize, fontFamily, colour, titleCharacteristicsList = uniqueTitleCharacteristics(titleCluster,otherCharacteristics)
    
	except Exception as e:
    		print(e)



	#print a preview of the pdf with deliminator
	#previewPdf(text , characteristics,titleCharacteristicsList)


	#creates docx file with deliminator
	try:
    		print("Preview Docx file for pdf started created")
    		createDocxWithDeliminator(text , characteristics,titleCharacteristicsList,filenameDocx,fileLocation)
    		print()

	except Exception as e:
    		print(e)
    

 
	#creates docx file for each abstract
	try:    
    		countOfDocx = individualAbstractDocxCreation(text ,characteristics,titleCharacteristicsList,filenameDocx,fileLocation,docObject)
    		print("Completed creating each abstract docx file")
	except Exception as e:
    		
    		print(e)
    	    
    
  
	#each docx files are converted to pdf 
	try:
    		convertDocxToPdfEachAbstract(countOfDocx,filenameDocx,fileLocation)   
    		print("Process completed")
	except Exception as e:
    		print(e)
    		print("Failed to  convert docx to pdf")    
    
  




