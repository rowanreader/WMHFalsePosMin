from Dilation import dilation
from CSFGM_mask import mimo
import argparse
from argparse import RawTextHelpFormatter


class WMHArg():
    def __init__(self, image1="/home/jacqueline/PycharmProjects/Data/AMIE_001/AMIE_001_T1_seg_vcsf.img",
                 image2=".",
                 image3="/home/jacqueline/PycharmProjects/Data/AMIE_001/AMIE_001_T1acq_FL_mc_flwmt_lesions_relabelled.img",
                 dilateType="cross",
                 output="WMHMaskoutput.img", tempSave="/home/jacqueline/PycharmProjects/WMHFalsePosMin/tempFCSFGMoutput.img", mask=[5, 7], voxel=[5, 7], kernel=2, smooth=0):
        self.image1 = image1
        self.image2 = image2
        self.image3 = image3
        self.output = output
        self.tempSave = tempSave
        self.dilateType = dilateType
        self.mask = mask
        self.voxel = voxel
        self.kernel = kernel
        self.smooth = smooth



def fakeCSFGM(args):

    # to make it easier to identify what this script is doing, print out the equivalent commands
    scriptString = ["This script is doing the equivalent of running:"]

    # based on inputs, call mimo and dilation to get wanted mask
    outputFile = args.tempSave
    mimoArgs1 = mimo.mimoArg(image1=args.image1, image2=args.image2, output=outputFile, maskIn=args.mask)
    mimo.mimo(mimoArgs1)
    # mask = ''.join(f'"{e}"' for e in args.mask)
    scriptString.append("python3 CSFGM_mask/mimo.py {} {} -o {} -mi {}".format(args.image1, args.image2, outputFile, ''.join(f'{e} ' for e in args.mask)))

    # mimo output written to outputFile. Use as input to dilate
    # overwrite output file
    # dilate type should be 'cross'
    # apply individually for each voxel number
    for i in args.voxel:
        dilateArgs = dilation.dilateArg(image=outputFile, output=outputFile, voxel=i, kernel=args.kernel,
                                         dilateType=args.dilateType, smooth=args.smooth)
        dilation.dilate(dilateArgs)
        scriptString.append("python3 Dilation/dilation.py {} -d {} -v {} -o {} -k {} -s {}".format(outputFile, args.dilateType, i, outputFile,
                                                                    args.kernel, args.smooth))

    mimoArgs2 = mimo.mimoArg(image1=outputFile, image2=args.image3, output=args.output, maskOut=args.mask)
    mimo.mimo(mimoArgs2)
    scriptString.append("python3 CSFGM_mask/mimo.py {} {} -o {} -mo {}".format(outputFile, args.image3, args.output, ''.join(f'{e} ' for e in args.mask)))


    return scriptString


if __name__=="__main__":
        helpStr = """    This is the fake_CSFGM script
            Written by Jacqueline Heaton

            Please run with:
            Image 1 (image initial mask is extracted from, based on maskout values), 
            Image 2 (image mask is applied to), 
            Image 3 (image the dilated mask is applied to)
            
            Note: Image paths may need to be absolute to avoid error.
            WMHFalsePosMin must contain child directories Dilation and CSFGM_mask, which contain dilation.py and mimo.py respectively
            
            Optional flag:
            -o: Output file, default is WMHMaskoutput.img
            -t: Temporary save location, will have dilated mask at end of running
            -d: Dilation type, either 'ball' or 'cross', default is 'cross' 
            -m Maskout values (for first mask extraction), default is [5, 7]. This will also be what is masked in for the final image
            -v Voxel to dilate, default is 1
            -k Kernel size for dilation, default is 1
            -s Smoothing, default is 0 (no smoothing applied)

            Example 1:
            
            python3 fake_CSFGM_mask.py Users/Data/AMIE_001/AMIE_001_T1_seg_vcsf.img . Users/Data/AMIE_001/AMIE_001_T1acq_FL_mc_flwmt_lesions_relabelled.img -o output.img -t tempSave.img -d cross -v 3 5 -m 5 7      

            """

        # parse in arguments
        try:
            parser = argparse.ArgumentParser(prog='White Matter Hyperintensity False Positive Minimization',
                                             description='Minimizes number of WMH by extracting and applying a dilated '
                                                         'mask of CSF and GM to remove any WMH in these areas',
                                             epilog=helpStr, formatter_class=RawTextHelpFormatter,
                                             usage=argparse.SUPPRESS)
            # image to extract mask from
            parser.add_argument("image1")
            # image to stamp mask onto
            parser.add_argument("image2")
            parser.add_argument("image3")

            parser.add_argument('-d', "--dilateType", choices=['ball', 'cross'], default="cross")
            # voxels to apply dilation to - can take in as many as needed, applies 1 at a time
            parser.add_argument('-v', "--voxel", default=[5, 7], nargs='*', type=int)

            parser.add_argument('-k', '--kernel', default=2, type=int)
            parser.add_argument('-s', '--smooth', default=0, type=int)

            parser.add_argument('-m', '--mask', default=[5, 7], nargs='*', type=int)

            # if they want to change the save file
            parser.add_argument('-o', '--output', default="WMHMaskoutput.img")
            parser.add_argument('-t', '--tempSave', default="WMHFalsePosMin/tempFCSFGMoutput.img")

            args = parser.parse_args()
            command = True

        except:
            print("Attempting to automatically assign image1 and image2")
            args = WMHArg()
            command = False
        finally:
            try:
                scriptStr = fakeCSFGM(args)
                if not command:
                    print()
                    for i in scriptStr:
                        print(i)
                    print("Slight modifications to image paths may be required due to file structure. Use absolute paths to be certain the correct file is being used")
            except Exception as e:
                print("fake_CSFGM_mask.py failed, please ensure all file paths and inputs are correct, use -h flag for more info")
                print("Full error:")
                print(e)


