import argparse
from argparse import RawTextHelpFormatter
import nibabel as nib
from scipy import ndimage as ndi
from skimage import morphology
import numpy as np
from matplotlib import pyplot as plt

if __name__ == "__main__":
    # help string, printed out when help flag is used
    helpStr = """    This is the dilation script
    Written by Jacqueline Heaton

    Please run with:
    Image 1 (the image you want to dilate), 
    Dilation type (the type of dilation to apply - options include 'ball' and 'cross'), 
    Voxel value (the value to dilate)
    
    Optional flags:
    -o: specify output file, default is dilatedOutput.img
    -k: kernel size for dilation, default is 1
    -s: apply smoothing filter (not applied automatically), provide size of filter

    Example 1:

    python3 dilation.py AMIE_001/AMIE_001_T1_seg_vcsf.img cross 7 -k 2 -o newOutput.img -s 10
    
    Example 2:

    python3 dilation.py AMIE_001/AMIE_001_T1_seg_vcsf.img ball 7

    """

    # parse in arguments
    # parser = argparse.ArgumentParser(prog='dilation',
    #                                  description='Dilates image based on requested dilation and voxel value',
    #                                  epilog=helpStr, formatter_class=RawTextHelpFormatter)
    # # image to dilate
    # parser.add_argument("image")
    #
    # # nargs will take in as many inputs as are available before the next flag
    # parser.add_argument("dilateType", choices=['ball', 'cross'])
    # # voxels to apply dilation to - can take in as many as needed
    # parser.add_argument("voxel", type=int)
    #
    # parser.add_argument('-k', '--kernel', default=1, type=int)
    # parser.add_argument('-s', '--smooth', default=0, type=int)
    #
    # # if they want to change the save file
    # parser.add_argument('-o', '--output', default="dilatedOutput.img")
    #
    # args = parser.parse_args()

    ##################
    # TO RUN FROM IDE, CHANGE VALUES HERE AND RUN (COMMENT OUT EVERYTHING ABOVE THIS UP UNTIL __main__(self)
    class Arg():
        def __init__(self):
            self.image = "../../Data/AMIE_001/AMIE_001_T1_seg_vcsf.img"
            # self.image = "../Data/AMIE_001/AMIE_001_T1_seg.img" # dimension mismatch
            self.output = "dilatedOutput.img"
            self.voxel = 7
            self.kernel = 1
            self.dilateType = "cross"
            self.smooth = 10
    args = Arg()
    ##################


    print("Loading...")
    data = nib.load(args.image)
    # get image data
    initialImage = data.get_fdata()

    image = np.array(initialImage)
    if len(image.shape) == 4:
        image = image.squeeze()
        print("Extra dimension found, reducing to 3 dimensions")
        print("There will be a header mismatch in the output file. "
              "If this is an issue please rerun with another file that only has 3 dimensions")

    # extract binary image, where all values in voxels are 1, and everything else is 0
    binary = np.zeros(image.shape)
    binary[image == args.voxel] = 1

    # check if it's ball or diamond, assign appropriate morph
    if args.dilateType == "ball":
        morph = ndi.generate_binary_structure(rank=3, connectivity=2)
        # morph = morphology.ball(args.kernel)
    elif args.dilateType == "cross":
        morph = ndi.generate_binary_structure(rank=3, connectivity=1)
        # morph = morphology.diamond(args.kernel)

    # apply morph to binary image
    # dilated = morphology.binary_dilation(binary, morph)
    print("Dilating...")
    dilated = ndi.binary_dilation(binary, morph, iterations=args.kernel)

    # apply smoothing filter if requested
    if args.smooth != 0:
        print("Smoothing...")
        dilated2 = ndi.median_filter(dilated, size=args.smooth)
    else:
        dilated2 = dilated

    # to plot side by side comparison of before and after dilation and smoothing, uncomment:
    #######################
    # fig, ax = plt.subplots(1, 3)
    # temp = np.copy(image)
    # ax[0].imshow(temp[200])
    #
    # # modify original image such that everywhere that is a 1 in dilated is now VOXEL in image
    # temp[dilated == 1] = args.voxel
    #
    # ax[1].imshow(temp[200])
    #
    # # modify image such that everywhere in dilated2 (which is a smoothed version of the mask)
    # # that is a 1 is now VOXEL in image
    # image[dilated2 == 1] = args.voxel
    # ax[2].imshow(image[200])
    #
    # plt.show()
    ########################

    final_img = nib.Nifti1Image(dilated, data.affine, data.header)
    nib.save(final_img, args.output)
    print("Done!")
    print("Image saved to {}".format(args.output))