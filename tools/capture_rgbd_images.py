import cv2
from primesense import openni2
from stream import color_stream_init, depth_stream_init, get_color, get_depth


if __name__ == '__main__':
    import sys
    import os
    ROOT_DIR = os.path.dirname(__file__)
    sys.path.append(ROOT_DIR)

    from config import OPENNI_CONFIG, RGBD_CAPTURE_CONFIG

    OPENNI2_REDIST_DIR = OPENNI_CONFIG['OPENNI2_REDIST_DIR']

    RGB_SAVE_PATH = RGBD_CAPTURE_CONFIG['RGB_SAVE_PATH']
    DEPTH_SAVE_PATH = RGBD_CAPTURE_CONFIG['DEPTH_SAVE_PATH']
    os.makedirs(RGB_SAVE_PATH, exist_ok=True)
    os.makedirs(DEPTH_SAVE_PATH, exist_ok=True)

    openni2.initialize(OPENNI2_REDIST_DIR)
    dev = openni2.Device.open_any()

    color_stream = color_stream_init(dev)
    depth_stream = depth_stream_init(dev)

    # dev.set_depth_color_sync_enabled(True)
    # dev.set_image_registration_mode(openni2.IMAGE_REGISTRATION_DEPTH_TO_COLOR)

    color_stream.start()
    depth_stream.start()

    while True:
        index = input('Starting index: ')
        try:
            index = int(index)
            break
        except ValueError:
            print('Please enter an integer as starting index')

    while True:
        color_frame = get_color(color_stream)
        depth_frame = get_depth(depth_stream)

        cv2.imshow("Color", color_frame)
        cv2.imshow("Depth", depth_frame)

        key = cv2.waitKey(34) & 0xFF
        if key in [ord('s'), 13]:
            cv2.imwrite(os.path.join(RGB_SAVE_PATH, '{}.png'.format(index)), color_frame)
            cv2.imwrite(os.path.join(DEPTH_SAVE_PATH, '{}.png'.format(index)), depth_frame)
            print('{} saved'.format(index))
            index += 1
        elif key in [ord('q'), 27]:
            break

    cv2.destroyAllWindows()
    color_stream.stop()
    depth_stream.stop()
    openni2.unload()
