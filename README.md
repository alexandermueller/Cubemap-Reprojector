
This program salvages .pano files (or any other panorama that follows a similar cubemap folder structure, as shown below.)
Given a cubemap folder, it can piece the original panorama back into a horizontal-cross image.
The panorama is now more useful to us, but not really that great to look at, which is why we need to reproject this image to another type of projection. Most panorama/photosphere websites prefer to work with equirectangle projections, so I've made a script that also reprojects horizontal-cross images into equirectangle images. 

**Requirements:**

This script requires python 2, pip, and the pillow image library (or more commonly, PIL) installed in pip.

**Usage:**

After cloning this project, place all panorama folders inside `/assets/cubemaps/`. 
Due to the fact that .pano files are the intent for this project (so it's already pretty niche), I've supplied an example .pano file in the cubemaps folder to compare with. At the very least, the panoramas supplied should resemble the following 
format: `PanoramaName/formats/cubemap/...`.

Run the runAll.py script to automate the entire process. Otherwise, first run the spliceCubeMaps.py script to convert the panorama cubemap folders into horizontal-cross images. The resulting images can be found inside `/assets/horizontal_crosses/`.
Next, if horizontal-cross images aren't exactly what you're into (who can blame you), run the horizontalCrossToEquirectangle.py script to reproject all the horizontal-cross images inside `/assets/horizontal_crosses/` to equirectangle images. The new projections can be found inside `/assets/equirectangles/`.
