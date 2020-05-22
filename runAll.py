#!/usr/bin/env python

import sys
import convertPanos
import spliceCubeMaps
import horizontalCrossToEquirectangle

def main(argc, argv):
	convertPanos.main(0,[])
	spliceCubeMaps.main(0,[])
	horizontalCrossToEquirectangle.main(0,[])

if __name__ == '__main__':
   main(len(sys.argv) - 1, sys.argv[1:])