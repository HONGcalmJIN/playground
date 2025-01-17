#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time

import numpy as np
import cv2

from cyber_py3 import cyber
from modules.sensors.proto.sensor_image_pb2 import Image

sys.path.append("../")

# roll
src_corners = [[283,223 ], [419,223 ], [265,283 ], [452,283 ]]

# turn to
dst_corners = [[165,236 ], [352,236 ], [165,423 ], [352,423 ]]

M = cv2.getPerspectiveTransform(
    np.float32(src_corners), np.float32(dst_corners))


def perspective_transform(image, m, img_size=None):
    if img_size is None:
        img_size = (image.shape[1], image.shape[0])
    warped = cv2.warpPerspective(image, m, img_size, flags=cv2.INTER_LINEAR)
    return warped


class Exercise(object):

    def __init__(self, node):
        self.node = node
        self.msg = Image()

        # TODO create reader
        self.node.create_reader(
            "/realsense/color_image/compressed", Image, self.callback)
        # TODO create writer
        self.writer = self.node.create_writer(
            "/perception/vertical_view", Image)

    def callback(self, data):
        # TODO
        print(data.frame_no)
        # TODO reshape
        self.reshape(data)
        # TODO publish, write to channel
        self.write_to_channel()

    def write_to_channel(self):
        # TODO
        self.writer.write(self.msg)

    def reshape(self, data):
        new_image = np.frombuffer(data.data, dtype=np.uint8)
        image = cv2.imdecode(new_image, cv2.IMREAD_COLOR)

        wrap_img = perspective_transform(image, M, img_size=(580, 560))

        img_param = [int(cv2.IMWRITE_JPEG_QUALITY), 30]

        img_encode = cv2.imencode('.jpeg', wrap_img, img_param)[1]
        data_encode = np.array(img_encode)
        str_encode = data_encode.tostring()
        data.data = str_encode
        self.msg = data


if __name__ == '__main__':
    cyber.init()

    # TODO update node to your name
    exercise_node = cyber.Node("exe2.1_HONG")
    exercise = Exercise(exercise_node)

    exercise_node.spin()

    cyber.shutdown()
