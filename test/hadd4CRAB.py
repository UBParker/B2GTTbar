#!/usr/bin/env python

import os, argparse, sys

# You need to include the last / after the last part of the directory you enter, otherwise is will put the output file in the directory back from where you are

#########
#EXAMPLE#
#########

# The following ex. 1) will go into the directory you specify first and search that directory then all subdirectories for the extension you request. Note that it will skip ALL directories that have "fail" anywhere in their path. Also note that append is true, this will add the files found to the output file if that file exists in the specified directory. The second example will only search the specified directory for .extension files, and will open to write to a file, if it exists it will allow the user to escape before overwriting the file.

# ex. 1) python hadd4CRAB.py /store/user/asparker/B2G2016/TTreesV5/SingleMuon/crab_b2gtreeV5_SingleMuon_Run2016C_03Feb2017_v1_JSONfinal_JECV4dataBCD_JERV10MC_try2/170410_055800/ . b2gtreeV5_singleMuon_Run2016Call-03Feb_JSONfinal_JECV4dataBCD_JERV10MC .root

# Deal with command line arguments
parse = argparse.ArgumentParser(prog='NTupleReader')
parse.add_argument('input_directory', type = str, nargs = 1, help = 'The directory you would like to access');
parse.add_argument('output_directory', type = str, nargs = 1, help = 'The directory you would like your output file to go in' );
parse.add_argument('file_name', type = str, nargs =1, help = 'The name of the output file');
parse.add_argument('file_extension', type = str, default = '.root', nargs = 1, help = 'The file extension for the files you want recorded in the output file' );
parse.add_argument( '--delve', default = True, help = 'If marked true, subdirectories of the given directory will be entered and their contents with the specified extension will be coppied to the output file. Default value is false');
parse.add_argument('--append', default = False, help = 'If marked true, the output file listed will be appended with the files found in the specified search directory. default is false');
args = parse.parse_args()


#obtain input file directory
inputDirectory = args.input_directory[0];

#obtain placement directory and ensure proper format
preplacementDirectory = args.output_directory[0].split(os.sep);

placementDirectory = ""

for parts in preplacementDirectory:
    placementDirectory = placementDirectory + parts + "/"

#obtain the new filename
fileName = args.file_name[0]
rootfileName = str(args.file_name[0]) + str(args.file_extension[0])

#otain the file type extension to be used and put in the output file
fileType = args.file_extension[0]


#create and open the file in the desired directory
os.chdir(placementDirectory)

if args.append == False:
    if os.path.isfile(str(preplacementDirectory) + str(fileName) + ".txt") == True:
        if raw_input( "WARNING: The file you wanted to create already exists. Do you want to overwrite it? enter 'N' to escape: ") == "N" or "n" or "No" or "no" or "NO":
            print "script cancelled"
            sys.exit();
    myfile = open(placementDirectory + fileName + ".csh", 'w')
    
if args.append == True:
    myfile = open(placementDirectory + fileName + ".csh", 'a')


# create a list of files to hadd
myfilelist = []

#enter specified root directory and recursively enter all subdirectories to get pertinent files
print "Delving.........."
if args.delve == True:
    print("Searching the  directory " + inputDirectory + " and all subdirectories for " + fileType + " files and adding them to the output file")
    dirlist = []
    print filter(None,os.popen("xrdfs root://cmseos.fnal.gov/ ls -u "+ inputDirectory ).read().split('\n'))
    for i, eossubDir in enumerate(filter(None,os.popen("xrdfs root://cmseos.fnal.gov/ ls -u "+ inputDirectory ).read().split('\n'))):
        dirlist.append(eossubDir)
        print"The eosDir is {}".format(eossubDir) #[-4:])
        for eosFile in filter(None,os.popen("xrdfs root://cmseos.fnal.gov/ ls -u "+ inputDirectory+ eossubDir[-4:]).read().split('\n')) :
            filenameFull =  eosFile
            if filenameFull.endswith(fileType) and "fail" not in inputDirectory.split(os.sep) :
                myfilelist.append(filenameFull)       
                print"Adding file to list for hadd: {}".format(filenameFull)
#enter only the specified directory and copy file names
else:
    print("Searching specified direcotry for " + fileType + " files...")
    for eosFile in filter(None,os.popen("xrdfs root://cmseos.fnal.gov/ ls -u "+ inputDirectory ).read().split('\n')):
        myfilelist.Add(eosFile)

filestring = ' '
for afile in myfilelist:
    filestring += str(afile) + ' '
print"..................................................................."
print"Finished forming list of {} files to hadd".format(len(myfilelist))
print"..................................................................."

#haddCmd = ['hadd '] 
#haddCmd.append( rootfileName)
#haddCmd.append(' ') 
#haddCmd.append(filestring)
#haddCmd.append( file.replace( idirs[0], odir ) )
#for dir in idirs:
#    haddCmd.append( file.replace( idirs[0], dir ) )
#import pdb; pdb.set_trace()
#cmd = ' '.join(haddCmd)

cmd = 'hadd ' + rootfileName + filestring
print cmd
myfile.write(cmd)
print"hadd command written to file {}".format(myfile)
myfile.close()
#os.system(cmd)
