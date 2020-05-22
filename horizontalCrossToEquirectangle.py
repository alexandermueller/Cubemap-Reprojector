#!/usr/bin/env python

#################################################################################################
## Note, this code was heavily inspired by https://github.com/Mapiarz/CubemapToEquirectangular ##
#################################################################################################

from PIL import Image, ImageDraw
import os, math, sys, multiprocessing, random

Image.MAX_IMAGE_PIXELS = 1000000000                                                                                           
logFileName = './log.txt'
logFile = open(logFileName, 'a')

chunks = 6
assetsFolder = 'assets'
horizontalCrossesFolder = '%s/horizontal_crosses' % assetsFolder
equirectanglesFolder = '%s/equirectangles' % assetsFolder
source = 0

def log(string, silent = False):
    if not silent: 
        print string
    logFile.write(string + '\n')

def convert(args):
    global source
    chunk, cubeFaceWidth, cubeFaceHeight = args
    lastProgress = -1
    width = cubeFaceWidth * 4
    height = cubeFaceHeight * 2
    chunkWidth = int(width / chunks)
    total = chunkWidth * height
    newImage = Image.new('RGB', (chunkWidth, height))
    draw = ImageDraw.Draw(newImage)
    
    for j in range(height):
        # Rows start from the bottom
        v = 1 - (float(j) / height)
        theta = v * math.pi

        for i in range(chunk * chunkWidth, (chunk + 1) * chunkWidth):
            # Columns start from the left
            u = float(i) / width
            phi = u * 2 * math.pi 

            # Unit Vector
            x = math.sin(phi) * math.sin(theta) * -1
            y = math.cos(theta)
            z = math.cos(phi) * math.sin(theta) * -1

            a = max(abs(x), abs(y), abs(z))
            
            # Vector parallel to the unit vector that lies on one of the cube faces
            xa = x / a
            ya = y / a
            za = z / a

            xPixel = 0
            yPixel = 0
            xOffset = 0
            yOffset = 0

            if xa == 1: 
                # Right face
                xPixel = int((((za + 1.0) / 2.0) - 1.0) * cubeFaceWidth)
                yPixel = int(((ya + 1.0) / 2.0) * cubeFaceHeight)
                xOffset = 2 * cubeFaceWidth
                yOffset = cubeFaceHeight
            elif xa == -1: 
                # Left face
                xPixel = int(((za + 1.0) / 2.0) * cubeFaceWidth)
                yPixel = int(((ya + 1.0) / 2.0) * cubeFaceHeight)
                xOffset = 0
                yOffset = cubeFaceHeight
            elif ya == 1: 
                # Up face 
                xPixel = int(((xa + 1.0) / 2.0) * cubeFaceWidth)
                yPixel = int((((za + 1.0) / 2.0) - 1.0) * cubeFaceHeight)
                xOffset = cubeFaceWidth
                yOffset = 2 * cubeFaceHeight
            elif ya == -1: 
                # Down face
                xPixel = int(((xa + 1.0) / 2.0) * cubeFaceWidth)
                yPixel = int(((za + 1.0) / 2.0) * cubeFaceHeight)
                xOffset = cubeFaceWidth
                yOffset = 0
            elif za == 1: 
                # Front face
                xPixel = int(((xa + 1.0) / 2.0) * cubeFaceWidth)
                yPixel = int(((ya + 1.0) / 2.0) * cubeFaceHeight)
                xOffset = cubeFaceWidth
                yOffset = cubeFaceHeight
            elif za == -1: 
                # Back face
                xPixel = int((((xa + 1.0) / 2.0) - 1.0) * cubeFaceWidth)
                yPixel = int(((ya + 1.0) / 2.0) * cubeFaceHeight)
                xOffset = 3 * cubeFaceWidth
                yOffset = cubeFaceHeight
            else:
                xPixel = 0
                yPixel = 0
                xOffset = 0
                yOffset = 0

            xPixel = abs(xPixel) + xOffset
            yPixel = abs(yPixel) + yOffset
                        
            pixel = j * chunkWidth + i
            progress = int((pixel * 100) / total)

            if progress != lastProgress and progress % 5 == 0:
                log('[Chunk %d @ %d Percent] - Writing pixel %d/%d (%d, %d)' % (chunk, progress, pixel, total, xPixel, yPixel))
            
            lastProgress = progress
            draw.point((i - chunk * chunkWidth, j), source.getpixel((min(xPixel, source.width - 1), min(yPixel, source.height - 1))))

    log('[Chunk %d @ %d Percent] - Finished' % (chunk, progress))
    return (chunk, newImage)

def main(argc, argv):
    global source, logFile
    
    if os.path.isfile(logFileName):
        os.remove(logFileName)
        logFile = open(logFileName, 'a')

    if not os.path.isdir('./%s' % horizontalCrossesFolder):
        log('No horizontal crosses folder found at ./%s' % horizontalCrossesFolder)
        exit()

    subDirectories, directories, files = os.walk('./%s/' % horizontalCrossesFolder).next()

    log('Reprojecting horizontal cross files:')

    for horizontalCross in files:
        log('Opening horizontal cross file %s...' % horizontalCross)
        
        try:
            source = Image.open('./%s/%s' % (horizontalCrossesFolder, horizontalCross)).convert('RGB')
        except:
            log('Invalid image file encountered. %s will be skipped.' % horizontalCross)
            continue

        cubeFaceWidth = int(source.width / 4)
        cubeFaceHeight = int(source.height / 3)
        destination = Image.new('RGB', (cubeFaceWidth * 4, cubeFaceHeight * 2))
        results = []

        try:    
            pool = multiprocessing.Pool(processes = chunks)
            r = pool.map_async(convert, [(chunk, cubeFaceWidth, cubeFaceHeight) for chunk in range(chunks)], callback = results.append)
            r.wait()
            pool.close()
        except:
            log('Pool encountered a race condition, moving on to next file.')
            results = []

        if len(results) == 0:
            log('Something went wrong with the multiprocessing for %s.' % horizontalCross)
            return

        results = results[0]

        for chunk, image in results:
            log('Adding chunk %s...' % chunk)
            # image.save('./%s/equirectangleFace%d.tiff' % (assetsFolder, chunk))
            destination.paste(image, (chunk * image.width, 0))
            image.close()

        if not os.path.isdir('./%s' % equirectanglesFolder):
            os.makedirs('./%s' % equirectanglesFolder)

        log('Saving equirectangle file...')
        destination.save('./%s/equirectangle_%s.tiff' % (equirectanglesFolder, horizontalCross.split('_')[-1][:-4]))
        destination.close()
        source.close()

    log('Finished!')
    logFile.close()

if __name__ == '__main__':
   main(len(sys.argv) - 1, sys.argv[1:])