import argparse
import os.path
import sys
from PIL import Image


def encode_image(imgpath, text):
    binary_text = ""
    for char in text:
        # print(char_to_binary(char))
        binary_text += char_to_binary(char)
    binary_text += "11111111"
    img_name = os.path.basename(imgpath).split(".")[0]
    text_index = 0
    try:
        with Image.open(imgpath) as img:
            pixels = img.load()

            MAX_BINARY_LENGTH = img.size[0] * img.size[1]
            MAX_BINARY_LENGTH -= MAX_BINARY_LENGTH % 8

            if len(binary_text) > MAX_BINARY_LENGTH:
                print("WARNING: Text too large, truncating...")
                print("TIP: Use larger resolution image to encode the entire text.")
            binary_text = binary_text[:MAX_BINARY_LENGTH]

            for i in range(img.size[0]):
                for j in range(img.size[1]):
                    rgb_list = list(pixels[i, j])
                    blue = rgb_list[-1]
                    if blue % 2:
                        if binary_text[text_index] == "0":
                            blue -= 1
                            rgb_list[-1] = blue
                            pixels[i, j] = tuple(rgb_list)
                    else:
                        if binary_text[text_index] == "1":
                            blue += 1
                            rgb_list[-1] = blue
                            pixels[i, j] = tuple(rgb_list)

                    text_index += 1
                    if text_index == len(binary_text):
                        break
                if text_index == len(binary_text):
                    break

            img.save(f"encoded-{img_name}.png")
            print("Done!")

    except OSError:
        msg = "File '{}' is not a valid image"
        raise TypeError(msg.format(imgpath))


def char_to_binary(char):
    if ord(char) >= 128:
        raise ValueError("Unknown Input Characters.")
    return "{:0>8s}".format(bin(ord(char))[2:])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", help="path to image to be encoded")
    parser.add_argument("--text", help="text to be encoded in")

    args = parser.parse_args()
    if args.image:
        if args.text:
            if os.path.exists(args.image) and os.path.exists(args.text):
                with open(args.text, "r") as textfile:
                    text = textfile.read()

                encode_image(args.image, text)
            else:
                msg = "File '{}' doesn't exist"
                raise ValueError(msg.format(args.text))
        else:
            msg = "File '{}' doesn't exist"
            raise ValueError(msg.format(args.image))
    else:
        parser.print_help(sys.stderr)
