import argparse
from argparse import RawTextHelpFormatter
import nibabel as nib
from scipy import ndimage as ndi
# from skimage import morphology
import numpy as np
# from matplotlib import pyplot as plt


class dilateArg():
    def __init__(self, image="../../Data/AMIE_001/AMIE_001_T1_seg_vcsf.img", output="dilatedOutput.img",
                 voxel=7, kernel=1, dilateType="cross", smooth=0):

        self.image = image
        # self.image = "../Data/AMIE_001/AMIE_001_T1_seg.img" # dimension mismatch
        self.output = output
        self.voxel = voxel
        self.kernel = kernel
        self.dilateType = dilateType
        self.smooth = smooth


def dilate(args):
    print("Loading...")
    data = nib.load(args.image)
    # get image data
    initialImage = data.get_fdata()

    image = np.rint(np.array(initialImage))
    if len(image.shape) == 4:
        image = image.squeeze()
        print("Extra dimension found, reducing to 3 dimensions")

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
    image[dilated == 1] = args.voxel

    # apply smoothing filter if requested
    if args.smooth != 0:
        print("Smoothing...")
        dilated2 = ndi.median_filter(image, size=args.smooth)
    else:
        dilated2 = image

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

    final_img = nib.Nifti1Image(dilated2, data.affine, data.header)
    nib.save(final_img, args.output)
    print("Done!")
    print("Image saved to {}".format(args.output))

if __name__ == "__main__":
    # help string, printed out when help flag is used
    helpStr = """    This is the dilation script
    Written by Jacqueline Heaton

    Please run with:
    Image 1 (the image you want to dilate), 
    
    
    Optional flags:
    -d: dilation type (the type of dilation to apply - options include 'ball' and 'cross'), default is 'cross' 
    -v: voxel value (the value to dilate), default is 1
    -o: specify output file, default is dilatedOutput.img
    -k: kernel size for dilation, default is 1
    -s: apply smoothing filter (not applied automatically), provide size of filter

    Example 1:

    python3 dilation.py AMIE_001/AMIE_001_T1_seg_vcsf.img -d cross -v 7 -k 2 -o newOutput.img -s 3
    
    Example 2 (using all defaults):

    python3 dilation.py AMIE_001/AMIE_001_T1_seg_vcsf.img

    """
    try:
        # parse in arguments
        parser = argparse.ArgumentParser(prog='dilation',
                                         description='Dilates image based on requested dilation and voxel value',
                                         epilog=helpStr, formatter_class=RawTextHelpFormatter, usage=argparse.SUPPRESS)
        # image to dilate
        parser.add_argument("image")

        # nargs will take in as many inputs as are available before the next flag
        parser.add_argument('-d', "--dilateType", choices=['ball', 'cross'], default='cross')
        # voxels to apply dilation to - can take in as many as needed
        parser.add_argument('-v', "--voxel", type=int, default=1)

        parser.add_argument('-k', '--kernel', default=1, type=int)
        parser.add_argument('-s', '--smooth', default=0, type=int)

        # if they want to change the save file
        parser.add_argument('-o', '--output', default="dilatedOutput.img")

        args = parser.parse_args()

    except:
        print("Attempting to automatically assign image, dilateType, and voxel")
        args = dilateArg() # get default values if no parser args or if there is an error

    finally:
        try:
            dilate(args)
        except Exception as e:
            print("dilation.py failed, please ensure file paths and inputs are correct, use -h flag for more info")
            print("Full error:")
            print(e)