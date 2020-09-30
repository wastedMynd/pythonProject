import cv2 as computer_vision

# WINDOW DIMENSIONS
WINDOW_WIDTH = 320
WINDOW_HEIGHT = 240

# WEB CAMERA PROPERTIES
WEB_CAMERA_WIDTH_PROPERTY = 3
WEB_CAMERA_HEIGHT_PROPERTY = 4
WEB_CAMERA_DEVICE_ID_PROPERTY = 0
WEB_CAMERA_BRIGHTNESS_PROPERTY = 10
WEB_CAMERA_WAIT_PROPERTY = 1000
WEB_CAMERA_QUIT_PROPERTY = 'q'

# SETUP CAPTURED VIDEO STREAM
captured_video_stream = computer_vision.VideoCapture(WEB_CAMERA_DEVICE_ID_PROPERTY)
captured_video_stream.set(WEB_CAMERA_WIDTH_PROPERTY, WINDOW_WIDTH)
captured_video_stream.set(WEB_CAMERA_HEIGHT_PROPERTY, WINDOW_HEIGHT)
captured_video_stream.set(WEB_CAMERA_BRIGHTNESS_PROPERTY, 50)

while True:
    try:
        success, image_stream = captured_video_stream.read()
        if success:
            computer_vision.imshow("Web Camera Live Stream", image_stream)
    finally:
        if computer_vision.waitKey(WEB_CAMERA_WAIT_PROPERTY) & 0xFF == ord(WEB_CAMERA_QUIT_PROPERTY):
            captured_video_stream.release()
            break
    pass
