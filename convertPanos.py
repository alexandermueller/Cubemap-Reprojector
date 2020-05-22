#!/usr/bin/env python

from PIL import Image
from shutil import copyfile
import os, sys, zipfile


logFileName = './log.txt'
logFile = open(logFileName, 'a')

def log(string, silent = False):
    if not silent: 
        print string
    logFile.write(string + '\n')

assetsFolder = 'assets'
panoramasFolder = '%s/panoramas' % assetsFolder
cubemapsFolder = '%s/cubemaps' % assetsFolder

def main(argc, argv):
	global logFile
	
	if os.path.isfile(logFileName):
		os.remove(logFileName)
		logFile = open(logFileName, 'a')

	if not os.path.isdir('./%s' % panoramasFolder):
		os.makedirs('./%s' % panoramasFolder)

	log('Converting .pano files:')
	subDirectories, directories, files = os.walk('./%s' % panoramasFolder).next()

	for panorama in files:
	    if '.pano' not in panorama:
	    	continue

	    log('Found .pano file %s...' % panorama)
	    source = './%s/%s' % (panoramasFolder, panorama)
	    destination = './%s/%s.zip' % (cubemapsFolder, panorama[:-5])

	    try:
	    	if not os.path.isdir('./%s' % cubemapsFolder):
	       		os.makedirs('./%s' % cubemapsFolder)

	       	log('Converting %s to %s...' % (source, destination))
	       	copyfile(source, destination)

	       	log('Extracting %s contents...' % destination)
	       	with zipfile.ZipFile(destination, 'r') as zip_ref:
	       		zip_ref.extractall(destination[:-4])

	       	log('Cleaning up %s' % destination)
	       	os.remove(destination)
	    except:
	    	log('Encountered an issue during the conversion process.')
	    	continue

	log('Finished!')
	logFile.close()

if __name__ == '__main__':
   main(len(sys.argv) - 1, sys.argv[1:])