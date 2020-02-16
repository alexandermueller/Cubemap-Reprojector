#!/usr/bin/env python

from PIL import Image
import os, math, sys

logFileName = './log.txt'

if os.path.isfile(logFileName):
    os.remove(logFileName)

logFile = open(logFileName, 'a')

def log(string, silent = False):
    if not silent: 
        print string
    logFile.write(string + '\n')

def main(argc, argv):
    if not os.path.isfile('./Cubemap/back'):
        log('No proper cubemap found at ./Cubemap')
        return

    subDirectories, directories, files = os.walk('./Cubemap/back').next()
    resolutions = [int(r) for r in directories]
    
    if len(resolutions) == 0:
        log('Resolution could not be determined.')
        return

    resolution = max(resolutions)
    log('Resolution level %d used.' % resolution)

    posns = {'front' : [1, 1], 'left' : [0, 1], 'right' : [2, 1], 'back' : [3, 1], 'top' : [1, 0], 'bottom' : [1, 2]}
    final = 0
    faceW = 0
    faceH = 0
    faceLength = 0

    for folder in posns.keys():
        subDirectories, directories, files = os.walk("./Cubemap/%s/%s/" % (folder, resolution)).next()
        rows = 0
        columns = 0
        
        for file in files:
            column, row = file.split('.')[0].split('_')
            if int(column) == 0:
                rows += 1
            if int(row) == 0:
                columns += 1

        faceLength = max(rows, columns) if faceLength == 0 else faceLength
        bottomImage = Image.open('./Cubemap/%s/%s/%d_%d.jpg' % (folder, resolution, 0, rows - 1)).convert("RGBA")
        rightImage  = Image.open('./Cubemap/%s/%s/%d_%d.jpg' % (folder, resolution, columns - 1, 0)).convert("RGBA")

        w, edgeH = bottomImage.size
        edgeW, h = rightImage.size

        if faceW == 0 and faceH == 0:
            faceW, faceH = (w * (faceLength - 1) + edgeW, h * (faceLength - 1) + edgeH)
        
        face = Image.new("RGBA", (faceW, faceH))

        for i in xrange(0, columns):
            for j in xrange(0, rows):    
                fileName = "./Cubemap/%s/%s/%d_%d.jpg" % (folder, resolution, i, j)
                current = Image.open(fileName).convert("RGBA")
                x, y = (w * i, h * j)

                log("Adding: %s" % fileName)
                face.paste(current, (x, y))        
        
        log("Adding face....")
        # face.save('./Cubemap/%s.png' % folder)
        
        if final == 0:
            final = Image.new("RGBA", (faceW * 4, faceH * 3))

        final.paste(face, (posns[folder][0] * faceW, posns[folder][1] * faceH))


    if final != 0:
        final.save('./FinalHorizontalCross.png')
    else:
        log('Nothing to save!')

    log('Finished!')
    logFile.close()

if __name__ == '__main__':
   main(len(sys.argv) - 1, sys.argv[1:])