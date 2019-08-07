# image-encode
A steganographic image encoder and decoder written in Python3.6

# Installation:
Open a terminal and type:

    git clone https://github.com/tusharsadhwani/image-encode.git
    cd image-encode
    pip install -r requirements.txt

# How to run:

## 1. Encoding 
Copy an image file to the `/image-encode` directory (or use the provided `dog.jpg` image)

Then run:

    python encode.py --image=dog.jpg --text=encode.txt
    
(replace `dog.jpg` with your image name and `encode.txt` with any ASCII text file)
This will create an image named `encoded-dog.png`, which will have the message encoded in it.

---

## 2. Decoding 

    python decode.py --image=encoded-dog.png
 
 this will create a textfile named `decoded-encoded-dog.txt`, whose contents should be identical to `encode.txt`
 
