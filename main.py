from time import time
import cv2 as cv
from djitellopy import Tello
import time
from threading import Thread
from FaceRec import SimpleFaceRec
from DroneController import DroneController


def rescale_frame(frame, scale=0.75):
    height = int(frame.shape[0] * scale)
    width = int(frame.shape[1] * scale)

    dimensions = (width, height)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)


def analyze_video(drone):
    sfr = SimpleFaceRec()
    sfr.load_encoding_images("images")

    frame_read = drone.get_frame_read()

    while True:
        drone_frame = frame_read.frame
        drone_frame_resized = rescale_frame(drone_frame, scale=0.5)

        face_locations, face_names = sfr.detect_known_faces(
            drone_frame_resized)
        for face_loc, name in zip(face_locations, face_names):
            y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

            cv.putText(drone_frame_resized, name, (x1, y1 - 10),
                       cv.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
            cv.rectangle(drone_frame_resized, (x1, y1),
                         (x2, y2), (0, 0, 200), 4)

        cv.imshow('DroneCam', drone_frame_resized)

        if cv.waitKey(20) & 0xFF == ord('q'):
            break

        time.sleep(1/30)

    cv.destroyAllWindows()


def main():
    drone = Tello()
    droneController = DroneController(tello=drone)

    drone.connect()

    drone.streamoff()
    drone.streamon()

    # analyze_video(drone)
    droneController.run()

    print("Hello World!")


if __name__ == "__main__":
    main()
