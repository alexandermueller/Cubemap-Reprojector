
This program salvages .pano files (or any other panorama that follows a similar cubemap folder structure, as shown below.)
Given a cubemap folder, it can piece the original panorama back into a horizontal-cross image.
The panorama is now more useful to us, but not really that great to look at, which is why we need to reproject this image to another type of projection. Most panorama/photosphere websites prefer to work with equirectangle projections, so I've made a script that also reprojects horizontal-cross images into equirectangle images. 

**Requirements:**

This script requires python 2, pip, and the pillow image library (or more commonly, PIL) installed with pip.

**Usage:**

After cloning this project, place all .pano files inside `/assets/panoramas/`.
Due to the fact that .pano files are the intent for this project (so it's already pretty niche), I've supplied an example .pano file that can be extracted using the convertPanos.py script. Running this will extract the useful information from the .pano file into `/assets/cubemaps/`. 

For those that would like to convert from cubemaps only, create the `/assets/cubemaps/` folder, or run the spliceCubeMaps.py script once to generate the folder (if it's missing.) Using the supplied Farm.pano file as an example, make sure the folder structure of your panorama looks similar to the resulting Farm panorama's cubemap folder (after running convertPanos.py first.) Your panorama cubemaps should at least have `/formats/cubemap/<front, left, back, bottom, right, top>/` present, along with numbered folders within them (resolution levels), with images inside them (`/formats/cubemap/front/13/<image files>`, for example.)

For those that wish to convert horizontal cross images to equirectangle format, place the source images inside `/assets/horizontal_crosses/` and run the horizontalCrossToEquirectangle.py script. The resulting equirectangle files will be located inside `/assets/equirectangles/`.

Run the runAll.py script to automate the entire process.
