## General Settings
- Set the correct path in `OPENNI_CONFIG` in `config.py`


## Camera Calibration
- Modified `CALIBRATION_CONFIG` in `config.py`
- run: `python tools/calibration.py {rgb|ir}`
- press enter key to keep capture images
- press 'q' to end capture and start chessboard calibration
- copy the values to `CAMERA_CONFG` in `config.py`


## RGBD Image Capture
- Set the correct path in `RGBD_CAPTURE_CONFIG` in `config.py`
- run: `python tools/capture_rgbd_images.py`
- press enter key or 's' to save rgb and depth images


## Generate .ply File from RGB-D Images
- Make sure the `CAMERA_CONFIG` is set correctly in `config.py`
- Set the correct path in `PLY_CONFIG` in `config.py`
- run: `python tools/rgbd2ply.py`