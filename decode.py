import argparse
import os.path
import sys
from PIL import Image


def decode_image(imgpath):
    img_name = os.path.basename(imgpath).split('.')[0]

    out = ""
    byte = ""
    try:
        with Image.open(imgpath) as img:
            pixels = img.load()
            for i in range(img.size[0]):
                for j in range(img.size[1]):
                    rgb_list = list(pixels[i, j])

                    blue = rgb_list[-1]
                    if blue % 2:
                        byte += "1"
                    else:
                        byte += "0"
                    
                    if len(byte) == 8:
                        if byte == "11111111":
                            break
                        # print(byte)
                        out += byte
                        byte = ""
                if byte == "11111111":
                    break
            
            
            output_text = ""
            for i in range(0, len(out), 8):
                byte = out[i:i+8]
                output_text += binary_to_char(byte)

            outfile_name = f"decoded-{img_name}.txt"
            with open(outfile_name, 'w') as outfile:
                outfile.write(output_text)
            
            print(outfile_name, "created")
            

    except OSError:
            msg = "File '{}' is not a valid image"
            raise TypeError(msg.format(imgpath))


def binary_to_char(binary):
    asc = int(binary, base=2)
    if asc >= 128:
        print(binary)
        raise ValueError("Unknown Input Characters.")
    return chr(asc)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", help="path to image to be encoded")
    
    args = parser.parse_args()
    if args.image:
        if os.path.exists(args.image):
            decode_image(args.image)
        else:
            msg = "File '{}' doesn't exist"
            raise ValueError(msg.format(args.image))
    else:
        parser.print_help(sys.stderr)
