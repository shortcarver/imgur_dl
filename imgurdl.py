#!python3

import os
import argparse
import json
import requests
import time
from pathlib import Path

current_milli_time = lambda: int(round(time.time() * 1000))

parser = argparse.ArgumentParser(description="Downloads the images in an imgur post")
parser.add_argument("--imgurhash", help="The hash of the post that you want to download")
parser.add_argument("--output", help="Path to place the files")
args, unknown = parser.parse_known_args()

# downloads the image list json file
def downloadJson(hash):
    jsonPath = "http://imgur.com/ajaxalbums/getimages/" + hash + "/hit.json"
    
    session = requests.session()
    response = session.get(jsonPath, stream=True)
    return json.loads(response.content.decode("utf-8"))

# downloads an individual image
def downloadImage(session, url, output):
    # print(output)
    response = session.get(url,stream=True)
    with open(output,"wb") as img:
        img.write(response.content)
    
# displays file sizes in human readable form
def displayHumanSize(size):
    if size < 1024: # less than 1KB
        return str(size) + "B"
    if size < 1048576: # less than 1MB
        return str(round(size/1024,2)) + "KB"
    if size < 1073741824: # less than 1GB
        return str(round(size/1048576,2)) + "MB"
    return str(round(size/1073741824,2)) + "GB"

# displays the duration value in human readable form
def displayHumanDuration(milliseconds):
    amount = ""
    amount = amount + str(int(round(milliseconds / 3600000))) + "h "
    milliseconds = milliseconds % 3600000
    
    amount = amount + str(int(round(milliseconds / 60000))) + "m "
    milliseconds = milliseconds % 60000
    
    amount = amount + str(int(round(milliseconds / 1000))) + "s "
    milliseconds = milliseconds % 1000
    
    amount = amount + str(int(round(milliseconds))) + "ms"
    return amount

       
# Get the images data
images = downloadJson(args.imgurhash)['data']['images']

# Generate the output dir
output = args.output + "/" + args.imgurhash

try:
    os.makedirs(output, exist_ok=True)
except OSError as exc:  # Python >2.5
    if exc.errno == errno.EEXIST and os.path.isdir(path):
        pass
    else:
        raise

# Generate the starting values
startTime = current_milli_time()
totalFiles = len(images)
completedSize = 0

# Get the size of all the images. Note: This is an estimate. I've found that these sizes do not always match the real files
totalSize = 0
for image in images:
    totalSize = totalSize + image['size']

# Display summary
print("Downloading " + str(len(images)) + " images @ " + displayHumanSize(totalSize))

# Start the http session
session = requests.session()

# Download the images
while(images):
    image = images.pop()
    outputFile = Path(output + "/" + image['hash'] + image['ext'])
    
    # check if we already have the file, if not, then download
    if outputFile.is_file() and os.path.getsize(output + "/" + image['hash'] + image['ext']) > 0:
        totalSize = totalSize - image['size']
    else:
        downloadImage(session,"http://i.imgur.com/" + image['hash'] + image['ext'], output + "/" + image['hash'] + image['ext'])
        completedSize = completedSize + image['size']
   
    # calculate the remaining time, speed, and number of files left to download
    completedTime = current_milli_time() - startTime
    if completedSize > 0:
        remainFiles = str(len(images)) + "/" + str(totalFiles)
        remainTime = displayHumanDuration((completedTime * totalSize/completedSize) - completedTime)
        speed = displayHumanSize(completedSize/(completedTime/1000))
        print(remainFiles + " " + remainTime + " " +  speed + "/s          \r", end="")

