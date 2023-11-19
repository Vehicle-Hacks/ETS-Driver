import truck_telemetry
import time
import pprint
import dxcam
import cv2

# initialize dxcam to create screenshots
camera = dxcam.create()

# initialize connection to ETS2/ATS
truck_telemetry.init()


file = open("data\\data.csv", "w")
file.write("Simulation Timestamp;Game Brake; Game Steer; Game Throttle; Odometer; X; Y; Z; Acc X; Acc Y; Acc Z; aa ACC X; aa ACC Y; aa ACC Z;Head Off X;Head Off Y;Head Off Z;Head Rot X;Head Rot Y;Head Rot Z;")
data = truck_telemetry.get_data()

# Run an infinite loop until the user aborts by pressing ctrl+c
try:
    while True:
        time.sleep(0.2)
        data = truck_telemetry.get_data()
        if data["paused"]:
            print("Paused")
        else:
            # Try to grab a frame. Record data only if a valid frame was grabbed
            frame = camera.grab()
            if frame is None:
                continue

            # First get the timestamp because we use it as image filename
            data = truck_telemetry.get_data()
            timestamp = str(data["simulatedTime"])
            imgname = "data\\" + timestamp + ".jpg"

            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            cv2.imwrite(imgname, frame)

            file.write( timestamp + ";")
            file.write(str(data["gameBrake"]) + ";")
            file.write(str(data["gameSteer"]) + ";")
            file.write(str(data["gameThrottle"]) + ";")
            file.write(str(data["truckOdometer"]) + ";")
            file.write(str(data["coordinateX"]) + ";")
            file.write(str(data["coordinateY"]) + ";")
            file.write(str(data["coordinateZ"]) + ";")
            file.write(str(data["accelerationX"]) + ";")
            file.write(str(data["accelerationY"]) + ";")
            file.write(str(data["accelerationX"]) + ";")
            file.write(str(data["aa_accelerationX"]) + ";")
            file.write(str(data["aa_accelerationY"]) + ";")
            file.write(str(data["aa_accelerationZ"]) + ";")
            file.write(str(data["headOffsetX"]) + ";")
            file.write(str(data["headOffsetY"]) + ";")
            file.write(str(data["headOffsetX"]) + ";")
            file.write(str(data["headOffsetrotationX"]) + ";")
            file.write(str(data["headOffsetrotationY"]) + ";")
            file.write(str(data["headOffsetrotationZ"]) + ";")

            file.write("\n")
except KeyboardInterrupt:
    print('exection stopped')

file.close()
del camera

etsdata = open("structure.txt", "w")
pprint.pprint(etsdata, stream=etsdata)
etsdata.close()