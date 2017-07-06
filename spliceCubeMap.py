#!/usr/bin/env python

from PIL import Image
import os, math

test       = 0
resolution = 0

for r in xrange(100,-1,-1):
    try:
        fileName   = "./Cubemap/back/%s/%d_%d.jpg" % (r, 0, 0)
        test       = Image.open(fileName).convert("RGBA")
        resolution = r
        
        break
    except IOError:
        pass
        print 'Resolution level %d doesn\'t exist.' % r

posns        = {'front' : [1, 1], 'left' : [0, 1], 'right' : [2, 1], 'back' : [3, 1], 'top' : [1, 0], 'bottom' : [1, 2]}
final        = 0
faceW, faceH = (0, 0)
faceLength   = 0

for folder in posns.keys():
    p, d, files = os.walk("./Cubemap/%s/%s/" % (folder, resolution)).next()
    faceLength  = int(math.sqrt(len(files))) if faceLength == 0 else faceLength
    bottomImage = Image.open('./Cubemap/%s/%s/%d_%d.jpg' % (folder, resolution, 0, faceLength - 1)).convert("RGBA")
    rightImage  = Image.open('./Cubemap/%s/%s/%d_%d.jpg' % (folder, resolution, faceLength - 1, 0)).convert("RGBA")

    w, edgeH = bottomImage.size
    edgeW, h = rightImage.size

    if faceW == 0 and faceH == 0:
        faceW, faceH = (w * (faceLength - 1) + edgeW, h * (faceLength - 1) + edgeH)
    
    face = Image.new("RGBA", (faceW, faceH))

    for i in xrange(0, faceLength):
        for j in xrange(0, faceLength):    
            fileName = "./Cubemap/%s/%s/%d_%d.jpg" % (folder, resolution, i, j)
            current  = Image.open(fileName).convert("RGBA")
            x, y     = (w * i, h * j)

            print "Adding: %s" % fileName
            face.paste(current, (x, y))        
    
    print "Adding face...."
    # face.save('./Cubemap/%s.png' % folder)
    
    if final == 0:
        final = Image.new("RGBA", (faceW * 4, faceH * 3))

    final.paste(face, (posns[folder][0] * faceW, posns[folder][1] * faceH))


final.save('./FinalHorizontalCross.png')
print "Finished!"
