from djitellopy import Tello
from DroneController import DroneController


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
