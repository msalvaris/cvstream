import numpy as np
import cv2
import urllib.request
import time
import os
import fire

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"


def from_camera():
    cap = cv2.VideoCapture(1)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Display the resulting frame
        cv2.imshow("frame", gray)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


def from_http_stream(ip, port):
    """ Stream video from http stream

    To stream video from your android phone install IPWebcam
    """
    # Replace the URL with your own IPwebcam shot.jpg IP:port
    url = f"http:/{ip}:{port}/shot.jpg"

    while True:

        # Use urllib to get the image and convert into a cv2 usable format
        img_arr = np.array(
            bytearray(urllib.request.urlopen(url).read()), dtype=np.uint8
        )
        img = cv2.imdecode(img_arr, -1)
        cv2.imshow("IPWebcam", img)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cv2.destroyAllWindows()


def from_rtsp_stream(ip, port):
    """ Stream video from rtsp stream

    To stream video from your android phone install IPWebcam
    """
    url = f"rtsp://{ip}:{port}/h264_pcm.sdp"
    vcap = cv2.VideoCapture(url)
    while True:
        ret, frame = vcap.read()
        if ret == False:
            print("Frame is empty")
            break
        else:
            cv2.imshow("VIDEO", frame)
            cv2.waitKey(1)


if __name__ == "__main__":
    fire.Fire(
        {
            "camera": from_camera,
            "http": from_http_stream,
            "rtsp": from_rtsp_stream,
        }
    )
