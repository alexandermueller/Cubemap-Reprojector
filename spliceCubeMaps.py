#!/usr/bin/env python

from PIL import Image
import os, math, sys, multiprocessing

logFileName = './log.txt'

if os.path.isfile(logFileName):
    os.remove(logFileName)

logFile = open(logFileName, 'a')

def log(string, silent = False):
    if not silent: 
        print string
    logFile.write(string + '\n')

assetsFolder = 'assets'
cubemapsFolder = '%s/cubemaps' % assetsFolder
horizontalCrossesFolder = '%s/horizontal_crosses' % assetsFolder

if not os.path.isdir('./%s' % cubemapsFolder):
    log('No cubemaps folder found at ./%s' % cubemapsFolder)
    exit()

def spliceFace(face):
    faceName = face.split('/')[-2]
    log('Splicing %s face...' % faceName)

    rows = 0
    columns = 0

    try: 
        subDirectories, directories, files = os.walk('./%s/' % face).next()
    
        for file in files:
            column, row = file.split('.')[0].split('_')
            
            if int(column) == 0:
                rows += 1
            if int(row) == 0:
                columns += 1
    except:
        log('Face does not exist, creating empty face image.')
        return (faceName, Image.new('RGB', (0, 0))) 

    faceSideLength = max(rows, columns)
    bottomImage = Image.open('./%s/%d_%d.jpg' % (face, 0, rows - 1)).convert('RGB')
    rightImage = Image.open('./%s/%d_%d.jpg' % (face, columns - 1, 0)).convert('RGB')

    w, edgeH = bottomImage.size
    edgeW, h = rightImage.size
 
    bottomImage.close()
    rightImage.close()
 
    faceW, faceH = (w * (faceSideLength - 1) + edgeW, h * (faceSideLength - 1) + edgeH)
    faceImage = Image.new('RGB', (faceW, faceH))

    for i in xrange(0, columns):
        for j in xrange(0, rows):    
            fileName = './%s/%d_%d.jpg' % (face, i, j)
            image = Image.open(fileName).convert('RGB')
            x, y = (w * i, h * j)

            log('Adding: %s' % fileName.split('/')[-1], silent = True)
            faceImage.paste(image, (x, y))        
            image.close()
    
    log('Finished splicing %s face...' % faceName)
    # faceImage.save('./%s/%s.jpg' % (assetsFolder, faceName))
    return (faceName, faceImage)

def main(argc, argv):
    log('Splicing cubemaps:')
    posns = {'front' : [1, 1], 'left' : [0, 1], 'right' : [2, 1], 'back' : [3, 1], 'top' : [1, 0], 'bottom' : [1, 2]}
    subDirectories, directories, files = os.walk('./%s' % cubemapsFolder).next()
    
    for cubemap in directories:
        cubemapFolder = '%s/%s/formats/cubemap' % (cubemapsFolder, cubemap)

        s, cubeMapDirectories, f = os.walk('./%s/front/' % cubemapFolder).next()
        resolutions = [int(r) for r in cubeMapDirectories]

        if len(resolutions) == 0:
            log('Resolution could not be determined for %s.' % cubemap)
            continue

        resolution = max(resolutions)
        log('Resolution level %d used for %s.' % (resolution, cubemap))

        results = []
        faces = ['%s/%s/%d' % (cubemapFolder, face, resolution) for face in posns.keys()]
        
        try:
            pool = multiprocessing.Pool(processes = len(faces))
            r = pool.map_async(spliceFace, faces, callback = results.append)
            r.wait()
            pool.close()    
        except:
            log('Pool encountered a race condition, moving on to next file.')
            results = []

        if len(results) == 0:
            log('Something went wrong with the multiprocessing for %s.' % cubemap)
            continue

        results = results[0]
        faceW, faceH = max(map(lambda x: x[1].size, results))
        horizontal_cross = Image.new('RGB', (faceW * 4, faceH * 3))
        
        for faceName, faceImage in results:
            log('Adding %s face to horizontal_cross...' % faceName)
            horizontal_cross.paste(faceImage, (posns[faceName][0] * faceW, posns[faceName][1] * faceH))
            faceImage.close()

        if not os.path.isdir('./%s' % horizontalCrossesFolder):
            os.makedirs('./%s' % horizontalCrossesFolder)

        log('Saving horizontal cross...')
        horizontal_cross.save('./%s/horizontal_cross_%s.jpg' % (horizontalCrossesFolder, cubemap))
        horizontal_cross.close()

    log('Finished!')
    logFile.close()

if __name__ == '__main__':
   main(len(sys.argv) - 1, sys.argv[1:])