# imgur_dl
A simple script that downloads all the images from a post on imgur

Given the hash from an imgur URL, it will download all the images in the post to disk. I wrote this because imgur's download feature often breaks for me, especially with large downloads.

# Requirements
Requires python3, only tested on Ubuntu 16.04

# Usage

python3 imgurdl.py --imgurhash HASH --output /home/me/Pictures

* *imgurhash* The hash string from the HASH part of the imgur URL: http://imgur.com/gallery/HASH
* *output* The path to store the images
