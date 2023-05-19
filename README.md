# WMHFalsePosMin
Written by Jacqueline Heaton

Code for using csfgm masks and dilation to remove WMH false positives

To run WMH:

python3 fake_CSFGM_mask.py Users/Data/AMIE_001/AMIE_001_T1_seg_vcsf.img . Users/Data/AMIE_001/AMIE_001_T1acq_FL_mc_flwmt_lesions_relabelled.img -o output.img -d cross -v 3 5 -m 5 7      

(send in 3 files - mask extraction file (typically the vcsf and gm is extracted from this file), the mask application file (same image) and the dilated-mask application file (the one with the WMH lesions)

optionally, specify output file, dilation type, mask values, voxel values for dilation, kernel size of dilation, and smoothing intensity 

To run just mimo (masking in/out script):

python3 CSFGM_mask/mimo.py AMIE_003_T1_seg.img AMIE_003_T1acq_FL_mc_flwmt_lesions.img -mi 3

(send in 2 files - mask extraction file and mask application model, the mode (masking in, masking out, or masking everything out)

optionally, specify output file

To run just dilation:

python3 Dilation/dilation.py AMIE_001/AMIE_001_T1_seg_vcsf.img -d cross -v 7 -k 2 -o newOutput.img -s 3

(send in 1 file to dilate)

optionally, specify output file, dilation type, voxel value to dilate, kernel value for dilation, and smoothing value


For more information on any of these scripts, run:

python3 script.py --help

where script is either fake_CSFGM_mask, dilation, or mimo


Note: these scripts can also be run from an IDE. This can be done by generating an object of the corresponding class and supplying all the required parameters:
Ex: to generate an WMHArg(), in the except block (line 108 at the time of writing), modify the args = WMHArg() line to be, for example, args = WMHArg(image1="x.img", image2="y.img", image3="z.img", mask=[5,7], voxel=[5,7], kernel=2, output="output.img"). All values supplied here are the same as their corresponding command line arguments. You do not have to supply all arguments - any left out (like dilateType in this example) will be set to their default values. To know the names for all the inputs, navigate to the __init__ function. You can change the default values, though it is not recommended.

If something goes wrong, you should be able to find the code at https://github.com/rowanreader/WMHFalsePosMin
