import cv2
import numpy as np
from glob import glob
from primesense import openni2
from stream import color_stream_init, ir_stream_init, get_color, get_ir


def capture_chessboards(camera_type, save_dir):
    dev = openni2.Device.open_any()

    if camera_type == 'ir':
        stream = ir_stream_init(dev)
        get_frame = get_ir
    elif camera_type == 'rgb':
        stream = color_stream_init(dev)
        get_frame = get_color
    else:
        raise ValueError()

    stream.start()

    index = 1
    while True:
        frame = get_frame(stream)
        cv2.imshow("frame", frame)

        key = cv2.waitKey(34) & 0xFF
        if key in [ord('s'), 13]:
            cv2.imwrite('{}/{:03d}.png'.format(save_dir, index), frame)
            print('{:03d}.png'.format(index))
            index += 1
        elif key in [ord('q'), 27]:
            break
    cv2.destroyAllWindows()
    stream.stop()
    openni2.unload()


def calibration_with_chessboards(pattern_size, square_size, img_dir):
    IMG_NAMES = glob('{}/*.png'.format(img_dir))

    pattern_points = np.zeros((np.prod(pattern_size), 3), np.float32)
    pattern_points[:, :2] = np.indices(pattern_size).T.reshape(-1, 2)
    pattern_points *= square_size

    obj_points = []  # 3D points in real world
    img_points = []  # 2D points in image plane

    for fname in IMG_NAMES:
        img = cv2.imread(fname, cv2.IMREAD_GRAYSCALE)

        found, corners = cv2.findChessboardCorners(img, PATTERN_SIZE)
        if found:
            # termination criteria
            term = (cv2.TERM_CRITERIA_EPS +
                    cv2.TERM_CRITERIA_MAX_ITER, 30, 0.1)
            corners2 = cv2.cornerSubPix(img, corners, (5, 5), (-1, -1), term)

            vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            vis = cv2.drawChessboardCorners(vis, PATTERN_SIZE, corners2, found)
            cv2.imshow('img', vis)
            key = cv2.waitKey(500)

            img_points.append(corners2.reshape(-1, 2))
            obj_points.append(pattern_points)
        else:
            print('chessboard not found')

    cv2.destroyAllWindows()

    h, w = cv2.imread(IMG_NAMES[0], 0).shape[:2]
    rms, camera_matrix, dist_coefs, rvecs, tvecs = cv2.calibrateCamera(
        obj_points, img_points, (w, h), None, None)
    print('RMS:', rms)
    print('Camera Matrix:\n', camera_matrix)
    print('Distortion Coefficients:', dist_coefs.ravel())


if __name__ == '__main__':
    import sys
    import os
    ROOT_DIR = os.path.join(os.path.dirname(__file__), '../')
    sys.path.append(ROOT_DIR)

    from config import OPENNI_CONFIG, CALIBRATION_CONFIG

    if len(sys.argv) < 2:
        raise ValueError('Camera type not provided')

    CAMERA_TYPE = sys.argv[1]
    if CAMERA_TYPE.lower() not in ['rgb', 'ir']:
        raise ValueError(
            'Please specifiy either "rgb" or "ir" for camera type')

    OPENNI2_REDIST_DIR = OPENNI_CONFIG['OPENNI2_REDIST_DIR']
    PATTERN_SIZE = CALIBRATION_CONFIG['PATTERN_SIZE']
    SQUARE_SIZE = CALIBRATION_CONFIG['SQUARE_SIZE']

    SAVE_DIR = os.path.join(
        ROOT_DIR, CALIBRATION_CONFIG['SAVE_DIR'], CAMERA_TYPE)
    os.makedirs(os.path.dirname(SAVE_DIR), exist_ok=True)

    openni2.initialize(OPENNI2_REDIST_DIR)
    capture_chessboards(CAMERA_TYPE, SAVE_DIR)
    calibration_with_chessboards(PATTERN_SIZE, SQUARE_SIZE, SAVE_DIR)
