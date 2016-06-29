"""rotate-and-crop analysis."""

import os
import logging
import argparse

import numpy as np

from jicbioimage.core.image import Image
from jicbioimage.core.transform import transformation
from jicbioimage.core.io import AutoName, AutoWrite

from jicbioimage.transform import (
    remove_small_objects,
)

from jicbioimage.segment import Region
from jicbioimage.illustrate import AnnotatedImage

__version__ = "0.0.1"

AutoName.prefix_format = "{:03d}_"


@transformation
def identity(image):
    """Return the image as is."""
    return image


@transformation
def rotate(image):
    """Return correctly aligned image."""
    return np.rot90(image)


@transformation
def red_channel_diff_to_mask(image, min_diff):
    return image[:, :, 0] < (image[:, :, 2] - min_diff)


@transformation
def green_channel_diff_to_mask(image, min_diff):
    return image[:, :, 1] < (image[:, :, 2] - min_diff)


@transformation
def min_blue_mask(image, min_blue):
    return image[:, :, 2] > min_blue


@transformation
def blue_to_mask(image, min_blue, min_difference):
    blue_mask = min_blue_mask(image, min_blue)
    red_diff_mask = red_channel_diff_to_mask(image, min_difference)
    green_diff_mask = green_channel_diff_to_mask(image, min_difference)
    return np.logical_and(blue_mask, np.logical_and(red_diff_mask, green_diff_mask))


@transformation
def convex_hull(image):
    return Region(image).convex_hull


def analyse_file(fpath, output_directory):
    """Analyse a single file."""
    logging.info("Analysing file: {}".format(fpath))
    image = Image.from_file(fpath)
    image = rotate(image)
    grayscale = np.mean(image, axis=2)
    mask = blue_to_mask(image, 150, 60)
    mask = remove_small_objects(mask, min_size=20000)
    if np.sum(mask) < 10:
        print("skipping {}".format(fpath))
        return
    mask = convex_hull(mask)
    ys, xs = Region(mask).index_arrays

    name = os.path.splitext(os.path.basename(fpath))[0]
    fname = name + "-rotated-and-cropped.png"
    fpath = os.path.join(AutoName.directory, fname)


    with open(fpath, "wb") as fh:
        fh.write(image[min(ys):max(ys), min(xs):max(xs), :].png())
#   ann = AnnotatedImage.from_grayscale(grayscale)
#   ann.mask_region(Region(mask).border.dilate(10))
#   with open(fpath, "wb") as fh:
#       fh.write(ann.png())


def analyse_directory(input_directory, output_directory):
    """Analyse all the files in a directory."""
    logging.info("Analysing files in directory: {}".format(input_directory))
    for fname in os.listdir(input_directory):
        fpath = os.path.join(input_directory, fname)
        analyse_file(fpath, output_directory)


def main():
    # Parse the command line arguments.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_source", help="Input file/directory")
    parser.add_argument("output_dir", help="Output directory")
    parser.add_argument("--debug", default=False, action="store_true",
                        help="Write out intermediate images")
    args = parser.parse_args()

    # Create the output directory if it does not exist.
    if not os.path.isdir(args.output_dir):
        os.mkdir(args.output_dir)
    AutoName.directory = args.output_dir

    # Only write out intermediate images in debug mode.
    if not args.debug:
        AutoWrite.on = False

    # Setup a logger for the script.
    log_fname = "audit.log"
    log_fpath = os.path.join(args.output_dir, log_fname)
    logging_level = logging.INFO
    if args.debug:
        logging_level = logging.DEBUG
    logging.basicConfig(filename=log_fpath, level=logging_level)

    # Log some basic information about the script that is running.
    logging.info("Script name: {}".format(__file__))
    logging.info("Script version: {}".format(__version__))

    # Run the analysis.
    if os.path.isfile(args.input_source):
        analyse_file(args.input_source, args.output_dir)
    elif os.path.isdir(args.input_source):
        analyse_directory(args.input_source, args.output_dir)
    else:
        parser.error("{} not a file or directory".format(args.input_source))

if __name__ == "__main__":
    main()
