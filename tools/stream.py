import cv2
import numpy as np
from primesense import _openni2 as c_api


def depth_stream_init(dev):
    stream = dev.create_depth_stream()
    stream.set_video_mode(
        c_api.OniVideoMode(
            pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_100_UM,
            # pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_1_MM,
            resolutionX=640,
            resolutionY=480,
            fps=30
        )
    )
    return stream


def color_stream_init(dev):
    stream = dev.create_color_stream()
    stream.set_video_mode(
        c_api.OniVideoMode(
            pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_RGB888,
            resolutionX=640,
            resolutionY=480,
            fps=30
        )
    )
    return stream


def ir_stream_init(dev):
    stream = dev.create_ir_stream()
    stream.set_video_mode(
        c_api.OniVideoMode(
            pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_GRAY16,
            resolutionX=640,
            resolutionY=480,
            fps=30
        )
    )
    return stream


def get_color(stream):
    frame_data = stream.read_frame().get_buffer_as_uint8()
    frame = np.frombuffer(frame_data, dtype=np.uint8).reshape(480, 640, 3)
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


def get_depth(stream):
    frame_data = stream.read_frame().get_buffer_as_uint16()
    frame = np.frombuffer(frame_data, dtype=np.uint16).reshape(480, 640)
    return frame


def get_ir(stream):
    frame_data = stream.read_frame().get_buffer_as_uint16()
    frame = np.frombuffer(frame_data, dtype=np.uint16).reshape(480, 640)
    frame = np.uint8((frame/frame.max())*255)
    frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
    return frame
