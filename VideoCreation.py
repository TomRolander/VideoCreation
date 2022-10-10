"""
/**************************************************************************
  VideoCreation
    The purpose of this Python program is to input a folder of image
  files (JPG), watermark the images (ImageMagick), rename the files, 
  and create a video of the watermarked files (FFMPEG).

  Original Code:  2022-10-08
  Revision:       2022-10-09

  Tom Rolander, MSEE
  Mentor, Circuit Design & Software
  Miller Library, Fabrication Lab
  Hopkins Marine Station, Stanford University,
  120 Ocean View Blvd, Pacific Grove, CA 93950
  +1 831.915.9526 | rolander@stanford.edu

 **************************************************************************/

 launch.json additional values

                "--inputdir", ".\\Input",
                "--outputdir", ".\\Output",
                "--fps", "8",
To Do List
    --numberofpoints
    mkdir .\Videos_16fps    etc
    start time, end time, elapsed time


"""
Version = "Ver 0.11"
RevisionDate = "2022-10-09"

import sys
import os
import time
import subprocess
import argparse
#from types import NoneType
NoneType = type(None)

print ("VideoCreation",Version, RevisionDate)

parser = argparse.ArgumentParser("Video Creation from Photos")
parser.add_argument('--verbose', action='store_true', help="Show more context")
parser.add_argument('--inputdir', type=str, required=False)
parser.add_argument('--outputdir', type=str, required=False)
parser.add_argument('--firstimagenumber', type=int, required=False)
parser.add_argument('--fps', type=int, required=False)
parser.add_argument('--videocreate', required=False, choices=('True','False'))
args = parser.parse_args()

if args.verbose:
    print(f"Create MP4 time lapse video from a folder of JPGs")
print("done")


if type(args.inputdir) is NoneType:
    input_dir_name = os.getcwd() + "\\Input"
else:
    input_dir_name = args.inputdir
print("Input Dir = ", end ="")
print(input_dir_name)

if type(args.outputdir) is NoneType:
    output_dir_name = os.getcwd() + "\\Output"
    watermarked_dir_name = output_dir_name + "\\Watermarked"
    videos_dir_name = output_dir_name + "\\Videos"
else:
    output_dir_name = args.outputdir
    watermarked_dir_name = args.outputdir + "\\Watermarked"
    videos_dir_name = args.outputdir + "\\Videos"
print("Output Dir Watermarked = ", end ="")
print(watermarked_dir_name)
print("Output Dir Videos = ", end ="")
print(videos_dir_name)

if type(args.firstimagenumber) is NoneType:
    isExist = os.path.exists(watermarked_dir_name + "\\0")
    if (isExist == False):
        base = 0
    else:
        base = 0
        # Iterate directory
        for path in os.listdir(watermarked_dir_name + "\\0"):
            # check if current path is a file
            if os.path.isfile(os.path.join(watermarked_dir_name + "\\0", path)):
                base += 1
else:
    base = args.firstimagenumber
print("First image number = ", end ="")
print(base+1)

if type(args.fps) is NoneType:
    frames_per_second = 16
else:
    frames_per_second = args.fps
print("Frames per second = ", end ="")
print(frames_per_second)

if type(args.videocreate) is NoneType or args.videocreate == True:
    print("Create MP4 video")
    bVideocreate = True
else:
    print("Only watermark files, no video will be created")
    bVideocreate = False

isExist = os.path.exists(input_dir_name)
if (isExist == False):
    print("Input Dir does not exist", input_dir_name)
    exit(1)

isExist = os.path.exists(output_dir_name)
if (isExist == False):
    print("Creating Output Dir ", output_dir_name)
    os.mkdir(output_dir_name)

isExist = os.path.exists(watermarked_dir_name)
if (isExist == False):
    print("Creating Output Watermarked Dir ", watermarked_dir_name)
    os.mkdir(watermarked_dir_name)

if bVideocreate == True:
    isExist = os.path.exists(videos_dir_name)
    if (isExist == False):
        print("Creating Output Videos Dir ", videos_dir_name)
        os.mkdir(videos_dir_name)


count = 0
# Iterate directory
for path in os.listdir(input_dir_name):
    # check if current path is a file
    if os.path.isfile(os.path.join(input_dir_name, path)):
        count += 1
print('Input file count:', count)

#quit()



# Get list of all files only in the given directory
list_of_files = filter( lambda x: os.path.isfile(os.path.join(input_dir_name, x)),
                        os.listdir(input_dir_name) )
# Sort list of files based on last modification time in ascending order
list_of_files = sorted( list_of_files,
                        key = lambda x: os.path.getmtime(os.path.join(input_dir_name, x))
                        )

for i in range(0, 10):
    #print("\"" + watermarked_dir_name + "\\" + str(i) + "\"")
    isExist = os.path.exists(watermarked_dir_name + "\\" + str(i))
    if (isExist == False):
        print("\"" + watermarked_dir_name + "\\" + str(i) + "\"")
        os.mkdir(watermarked_dir_name + "\\" + str(i))

index = 0
#base = 0
for file_name in list_of_files:
    if ((index % 10) == 0):
        base += 1
    input_file_path = os.path.join(input_dir_name, file_name)
    timestamp_str = time.strftime(  '%m/%d/%Y %H:%M:%S',
                                time.gmtime(os.path.getmtime(input_file_path))) 
    print(str(index).zfill(6), str((index % 10)), str(base).zfill(6), timestamp_str, file_name) 
    output_file_path =  watermarked_dir_name + "\\" + str((index % 10)) + "\\" + str(base).zfill(6) + ".jpg"
    #print(output_file_path)
    os.system("magick convert " + "\"" + input_file_path + "\"" + " -quiet -gravity northwest -font Arial-bold -pointsize 72 -fill black -annotate 90x90+100+30 %[exif:DateTimeOriginal] -fill white -annotate 90x90+103+33 %[exif:DateTimeOriginal] " + "\"" + output_file_path + "\"")
    #print ("Done")
    index += 1

if bVideocreate == True:
    for i in range(0, 10):
        #print (output_dir_name + "\\" + "P" + str(i) + "_%05d")
        #print (videos_dir_name + "\\" + "VideoPoint_" + str(i) + ".mp4")
        print ("ffmpeg -r " + str(frames_per_second) + " -f image2 -s 1920x1080 -i " + "\"" + watermarked_dir_name + "\\" + str(i) + "\\"+ "%06d.jpg" + "\"" + " -vcodec libx264 -crf 35 -pix_fmt yuv420p -y " + "\"" + videos_dir_name + "\\" + "VideoPoint_" + str(i) + ".mp4" + "\"")
        os.system("ffmpeg -r " + str(frames_per_second) + " -f image2 -s 1920x1080 -i " + "\"" + watermarked_dir_name + "\\" + str(i) + "\\"+ "%06d.jpg" + "\"" + " -vcodec libx264 -crf 35 -pix_fmt yuv420p -y " + "\"" + videos_dir_name + "\\" + "VideoPoint_" + str(i) + ".mp4" + "\"")
        print ("Done")
