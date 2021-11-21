import argparse
from PIL import Image
import sys

def parse_args(args):
    """
    Argparse initialization and adding arguments
    """
    parser = argparse.ArgumentParser(prog='MediaMonk-Image-Filter',
                                     # usage='%(prog)s [options] [input_image] [output_image]',
                                     description='MediaMonks Custom Image Filter')
    parser.add_argument('input_image',
                        help='REQUIRED - The input image file name which you want to apply filters to.')
    parser.add_argument('output_image',
                        # type=argparse.FileType('wb', 0),  # not used, because it creates a file regardless of errors.
                        help='REQUIRED - The file name you want to give to the outputted image. '
                             '(only .jpg and .png extensions are supported)')
    parser.add_argument('--gray_scale',
                        # type=bool,  # unnecessary
                        # nargs='?', const=True, default=False,
                        action='store_true',
                        help='Filter. Change color scheme of the image (as processed up to that point) to gray scale.')
    parser.add_argument('--overlay',
                        type=str,
                        action='append',
                        help='Filter. Overlay another image on top of the input image. '
                             'Specify the file name of the overlay image.')
    parser.add_argument('--rotate',
                        type=int,
                        action='append',
                        help='Filter. Rotate image by [N] degrees.')
    parser = parser.parse_args(args)
    return parser

def make_grayscale(img):
    """
    returns the image in black & white.
    """
    img = img.convert('L')
    return img

def add_overlay(img, overlay):
    """
    Adds an overlay image on top of the (processed) image in the top left corner.
    """
    with Image.open(overlay).convert('RGBA') as overlay:  # converting overlay to RGBA to allow transparency
        location = (0, 0)  # assuming location is not important for now. defaults to left-top
        img = img.convert('RGBA')
        img.paste(overlay, location, overlay)
        return img

def rotate(img, n):
    """
    Rotates the image by n degrees.
    """
    img = img.rotate(n)
    return img

def save_image(img, out):
    filetype = out.split('.')[-1]
    if filetype == "jpg":
        img = img.convert('RGB')  # cant convert RGBA into jpg
        extension = "JPEG"
    elif filetype == "png":
        extension = "PNG"
    else:
        raise ValueError(f"The file type '{filetype}' is not supported. try '.jpg' or '.png'.")

    img.seek(0)  # needed due to 0KB error
    img.save(out, extension)
    print(f"image {out} saved to project_folder")

    if __name__ == '__main__':
        img.show()

def get_filtered_order():
    filter_order = []
    for i, v in enumerate(sys.argv):  # finds the sequence of the commands
        if v.startswith('--'):  # only gets the optionals
            filter_order.append(v[2:])
    return filter_order

def apply_filters(args, image):
    # Counter to make sure that we get the right value for each filter in the for-loop below
    gray_scale_count = 0
    overlay_count = 0
    rotate_count = 0

    for option in get_filtered_order():
        if option == "gray_scale":
            if args.gray_scale:
                image = make_grayscale(image)
                print("applying gray scale filter")
            gray_scale_count += 1
        if option == "overlay":
            image = add_overlay(image, args.overlay[overlay_count])
            print(f"adding overlay number {overlay_count + 1}")
            overlay_count += 1
        if option == "rotate":
            image = rotate(image, args.rotate[rotate_count])
            print(f"adding rotation number {rotate_count + 1}")
            rotate_count += 1
    return image

def process_image(args):
    with Image.open(args.input_image) as image:
        image = apply_filters(args, image)
        image.seek(0)  # to avoid 0KB image issues
        save_image(image, args.output_image)
        return image

def main():
    args = parse_args(args=sys.argv[1:])
    process_image(args)

if __name__ == '__main__':
    main()
