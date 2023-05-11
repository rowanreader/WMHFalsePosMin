import nibabel as nib
import sys
import argparse
from argparse import RawTextHelpFormatter
# import numpy as np
import matplotlib.pyplot as plt
import os

if __name__ == "__main__":
    # help string, printed out when help flag is used
    helpStr = """    This is the mimo (mask-in-mask-out) script
    Written by Jacqueline Heaton
    
    Please run with:
    Image 1 (the image the mask is extracted from), 
    Image 2 (the image the mask is stamped on to), 
    and the mask flag (-mi for masking in, -mo for masking out, -m for masking everything out - no numbers required), 
    followed by the numbers to be masked in or out for -mi and -mo
    
    The -m flag means everything in Image 1 will be masked out of Image 2
    
    If Image 2 is . the script will stamp the extracted mask back onto Image 1
    
    Optional flag:
    -o: specify output file, default is CSFGMoutput.img
    
    Example 1 (masks in value 3. Any area that has a value of 3 in Image 1 will be preserved in Image 2. Everything else will be removed):
    
    python3 mimo.py AMIE_003_T1_seg.img AMIE_003_T1acq_FL_mc_flwmt_lesions.img -mi 3
    
    Example 2 (masks out values 4, 5, and 8. Any area that has a value of 4, 5, or 8 in Image 1 will be removed in Image 2. Everything else will be preserved):
    
    python3 mimo.py /user/files/T1_seg_vcsf.img /user/files/T1acq_lesions_relabelled.img -mo 4 5 8
    
    Example 3 (masks in values 4 and 5, saves to newOutput.img):
    
    python3 mimo.py /user/files/T1_seg_vcsf.img /user/files/T1acq_lesions_relabelled.img -mi 4 5 -o newOutput.img
    
    Example 4 (uses -m flag to mask out everything):
    
    python3 mimo.py /user/files/T1_seg_vcsf.img /user/files/T1acq_lesions_relabelled.img -m
    
    """
    # parse in arguments
    # parser = argparse.ArgumentParser(prog='mask in, mask out', description='Extracts mask from Image 1 and applies to Image 2. '
    #                                                                        'Can be used for masking in and masking out',
    #                                  epilog=helpStr, formatter_class=RawTextHelpFormatter)
    # # image to extract mask from
    # parser.add_argument("image1")
    # # image to stamp mask onto
    # parser.add_argument("image2")
    # # nargs will take in as many inputs as are available before the next flag
    # parser.add_argument('-mi', '--maskIn', nargs='*')
    # parser.add_argument('-mo', '--maskOut', nargs='*')
    # # no numbers supplied, just set to true
    # parser.add_argument('-m', '--maskAll', action='store_true')
    # # if they want to change the save file
    # parser.add_argument('-o', '--output', default="CSFGMoutput.img")
    #
    # args = parser.parse_args()

    ##################
    # TO RUN FROM IDE, CHANGE VALUES HERE AND RUN (COMMENT OUT EVERYTHING ABOVE THIS UP UNTIL __main__(self)
    class Arg():
        def __init__(self):
            self.image1 = "../../Data/AMIE_001/AMIE_001_T1acq_FL_mc_flwmt_lesions_relabelled.img"
            self.image2 = "../../Data/AMIE_001/AMIE_001_T1_seg.img"
            self.output = "CSFGMoutput.img"
            self.maskIn = [1, 2, 3]
            self.maskOut = None
            self.maskAll = False
    args = Arg()
    ##################

    if not args.maskIn and not args.maskOut and not args.maskAll:
        print("Error, please select a flag. Use -h flag for more information")
        exit(0)

    maskFile = args.image1
    if args.image2 == ".":  # if this is given as image2, set image2 to be image1 - stamp onto self
        imageFile = args.image1
    else:
        imageFile = args.image2

    outputFile = args.output

    # assign maskVals
    # if -m flag, apply full mask, remove everything that isn't background
    if args.maskAll:
        maskVals = [0]

    # check whether -mi or -mo flag was used
    else:
        if args.maskIn and args.maskOut:
            print("Error, please use either -mi or -mo, not both")
            exit(0)
        if args.maskIn:
            maskVals = [int(x) for x in args.maskIn]
        if args.maskOut:
            maskVals = [int(x) for x in args.maskOut]

    print("Loading....")
    # load T1 csf image - take as input for other
    data = nib.load(maskFile)
    # get image data
    image = data.get_fdata()

    # set all values in maskVals to val (some value that is not a real label)
    # done in case there is more than 1 value to be masked out
    val = -1  # CHANGE THIS TO WHATEVER LABEL YOU WANT, SO LONG AS IT IS NOT A LABEL ALREADY PRESENT IN THE MASK IMAGE
    # purpose is to homogenize all submitted values for easier extraction/stamping
    for i in maskVals:
        image[image == i] = val

    # image to stamp mask on to
    data2 = nib.load(imageFile)
    image2 = data2.get_fdata()

    # mask out all things set to value
    # could condense it but this is more organized
    if args.maskAll:
        print("Masking all of Image 1")
        image2[image == val] = 0

    # anything that is not val gets set to 0 for mask in
    if args.maskIn:
        print("Masking in values")
        image2[image != val] = 0
    # anything that is val gets set to 0 for mask out
    elif args.maskOut:
        print("Masking out values")
        image2[image == val] = 0

    print("Saving....")
    final_img = nib.Nifti1Image(image2, data2.affine)
    nib.save(final_img, outputFile)
    print("Done!")
    print("Image saved to {}".format(args.output))