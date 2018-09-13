# Software License Agreement (BSD License)
#
# Copyright (c) 2013, Juergen Sturm, TUM
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of TUM nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# the resulting .ply file can be viewed for example with meshlab
# sudo apt-get install meshlab

import numpy as np
import cv2
from PIL import Image


def generate_ply_from_rgbd(rgb_file, depth_file, config):
    rgb = Image.open(rgb_file)
    depth = Image.open(depth_file)

    if rgb.size != depth.size:
        raise Exception(
            "Color and depth image do not have the same resolution.")
    if rgb.mode != "RGB":
        raise Exception("Color image is not in RGB format")
    if depth.mode != "I":
        raise Exception("Depth image is not in intensity format")

    points = []
    for v in range(rgb.size[1]):
        for u in range(rgb.size[0]):
            color = rgb.getpixel((u, v))
            Z = depth.getpixel((u, v)) / config['SCALING_FACTOR']
            if Z == 0:
                continue
            X = (u - config['CENTER_X']) * Z / config['FOCAL_LENGTH']
            Y = (v - config['CENTER_Y']) * Z / config['FOCAL_LENGTH']
            points.append(f"{X:f} {Y:f} {Z:f} {color[0]:d} {color[1]:d} {color[2]:d} 0\n")
    ply = f"""\
ply
format ascii 1.0
element vertex {len(points):d}
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
property uchar alpha
end_header
{''.join(points)}\
"""
    return ply


if __name__ == '__main__':
    import sys
    import os
    ROOT_DIR = os.path.dirname(__file__)
    sys.path.append(ROOT_DIR)

    from config import PLY_CONFIG, CAMERA_CONFIG

    RGB_LOAD_PATH = os.path.join(ROOT_DIR, PLY_CONFIG['RGB_LOAD_PATH'])
    DEPTH_LOAD_PATH = os.path.join(ROOT_DIR, PLY_CONFIG['DEPTH_LOAD_PATH'])
    PLY_SAVE_PATH = os.path.join(ROOT_DIR, PLY_CONFIG['PLY_SAVE_PATH'])
    os.makedirs(PLY_SAVE_PATH, exist_ok=True)
    print(PLY_SAVE_PATH)

    image_names = os.listdir(DEPTH_LOAD_PATH)
    for image_name in image_names:
        rgb_file = os.path.join(RGB_LOAD_PATH, image_name)
        depth_file = os.path.join(DEPTH_LOAD_PATH, image_name)

        ply_filename = os.path.splitext(image_name)[0] + '.ply'
        output_file = os.path.join(PLY_SAVE_PATH, ply_filename)

        ply_content = generate_ply_from_rgbd(
            rgb_file, depth_file, CAMERA_CONFIG)
        with open(output_file, 'w') as output:
            output.write(ply_content)
        print(ply_filename, ' done')
