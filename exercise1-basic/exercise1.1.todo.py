#!/usr/bin/env python
import sys

import cv2
import numpy as np

from cyber_py3 import cyber
from modules.sensors.proto.sensor_image_pb2 import Image
# from modules.exercises.common.image_utils import reshape

sys.path.append("../")


class Exercise(object):

    def __init__(self, node):
        self.node = node
        self.msg = Image()

        # TODO create reader
        self.node.create_reader("/realsense/color_image", Image, self.callback)
        # TODO create writer
        self.writer = self.node.create_writer("/realsense/color_image/compressed", Image)

    def callback(self, data):
        # TODO print frame number
        print('Frame number is :%s' % data.frame_no)
        # TODO api to reshape image
        self.msg = data
        self.msg.data = self.reshape(data.data)
        # TODO publish, write compressed image
        self.writer.write(self.msg)
        print('Comressed image have wrote to channel /realsense/color_image/compressed')

    def reshape(self, data):
        """api to reshape and encodes image, you can call self.reshape(data)"""
        new_image = np.frombuffer(data, dtype=np.uint8)
        img_param = [int(cv2.IMWRITE_JPEG_QUALITY), 20]
        # https://stackoverflow.com/questions/50306863/valueerror-cannot-reshape-array-of-size-50176-into-shape-1-224-224-3
        new_image = new_image.reshape((360, 640, 3))
        img_encode = cv2.imencode('.jpeg', new_image, img_param)[1]
        data_encode = np.array(img_encode)
        return data_encode.tostring()




if __name__ == '__main__':
    cyber.init()

    # TODO update node to your gourp_name or other thing
    exercise_node = cyber.Node("exercise1_node_HONG")
    exercise = Exercise(exercise_node)

    exercise_node.spin()

    cyber.shutdown()

