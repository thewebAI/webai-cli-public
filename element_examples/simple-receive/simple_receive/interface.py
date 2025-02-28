import cv2
from webai_element_sdk.comms.messages import ImageFrame


def generate_image_from_frame(frame: ImageFrame):
    _, buffer = cv2.imencode(".jpg", cv2.cvtColor(frame.ndframe, cv2.COLOR_BGR2RGB))

    return b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n"
