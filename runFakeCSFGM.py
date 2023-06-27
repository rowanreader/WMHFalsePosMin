# this calls the fake CSFGM script on all subdirectories of AMIE
import os
import re
import fake_CSFGM_mask as mask
import argparse
import pathlib
# single folder given, just run on that
def singleRun(subjectPath):
    print(subjectPath)
    # assume last segment after / is AMIE_XXX
    amie = subjectPath.split("/")[-1]
    image1Name = "{}/{}_T1_seg_vcsf.img".format(subjectPath, amie)
    image3Name = "{}/{}_T1acq_FL_mc_flwmt_lesions.img".format(subjectPath, amie)
    outputName = "{}/{}_T1acq_FL_mc_flwmt_lesions_edit.img".format(subjectPath, amie)
    tempName = "{}/temp.img".format(subjectPath)
    args = mask.WMHArg(image1=image1Name, image3=image3Name, output=outputName, tempSave=tempName)
    mask.fakeCSFGM(args)
def run(path):
    dirs = os.listdir(path)
    for i in dirs:
        if re.search("^(good)|(bad)_T1_(good)|(bad)_FL", i):
            # now need to iterate through all AMIE folders
            amiePath = "{}/{}".format(path, i) # path to AMIE files inside good/bad_T1_good/bad_FL
            for amie in os.listdir(amiePath):
                if re.search("^AMIE_[0-9]{3}$", amie):
                    subjectPath = "{}/{}".format(amiePath, amie) # actual AMIE folder with image files
                    print(subjectPath)
                    image1Name = "{}/{}_T1_seg_vcsf.img".format(subjectPath, amie)
                    image3Name = "{}/{}_T1acq_FL_mc_flwmt_lesions.img".format(subjectPath, amie)
                    outputName = "{}/{}_T1acq_FL_mc_flwmt_lesions_edit.img".format(subjectPath,amie)
                    tempName = "{}/temp.img".format(subjectPath)
                    args = mask.WMHArg(image1=image1Name, image3=image3Name, output=outputName, tempSave=tempName)
                    mask.fakeCSFGM(args)

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(prog='run fake_CSFGM on all files. Requires path',
                                         description='runs script on all AMIE_XXX folders in current directory if given no path',
                                         usage=argparse.SUPPRESS)
        # image to extract mask from
        parser.add_argument("path", default=None)
        # default="/net/synapse/data2/temp/users/dandriuta/orientations_test/AMIE"
        args = parser.parse_args()

        if args.path == None:
            print("Running on current directory:")
            path = str(pathlib.Path().resolve())
            run(path)
        else:
            print(args.path)
            singleRun(args.path)

    except Exception as e:

        print("Error: {}".format(e))
    # finally:
    #     run(args.path)


