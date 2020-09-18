#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from os.path import join, dirname, basename, isfile


def get_output_file(file):
    _basename = basename(file)
    _dirname = dirname(file)

    output_path = join(_dirname, "..", "output/NOAA/", _basename.replace(".meta", ".wav"))
    return output_path, isfile(output_path)


def get_image_file(file):
    image_path = file.replace(".wav", ".png")
    return image_path, isfile(image_path)


def demod(file_input, file_output):
    cmd = join(dirname(__file__), "../"*4 + 'radio/decoder/data/gr/noaa_demod.py -i "{}" -o "{}"'.format(file_input, file_output))
    print("demod: ", cmd)
    os.system(cmd)


def decode(file_output):
    print("decoding:", file_output)
    os.system('wxtoimg -t n -I "{}" "{}"'.format(file_output, get_image_file(file_output)[0]))


def main():
    input_path = join(dirname(__file__), "../"*4 + "persistent-data/input")
    for file in os.listdir(input_path):
        if file.startswith("NOAA") and file.endswith(".meta"):
            print(file)
            input_file = join(input_path, file)
            output_file, existing = get_output_file(input_file)
            if not existing:
                demod(input_file, output_file)

            image_file, existing = get_image_file(output_file)
            if not existing:
                decode(output_file)

            # TODO delete input files


if __name__ == '__main__':
    main()
