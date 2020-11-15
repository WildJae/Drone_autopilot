
import setup_path 
import airsim

import numpy as np
import os
import tempfile
import pprint
import cv2

# gps and position info
def displayPos(client):
    gps = client.getGpsData()
    print("Position")
    print(gps.gnss.velocity)
    print("GPS coordinates")
    print(gps.gnss.geo_point)

# getting position of drone
def getVector(client):
    return client.getGpsData().gnss.velocity
# taking a picture
def takePic(client):
    print("getting image...")
    png_image = client.simGetImage("0", airsim.ImageType.Scene)
    with open('images/test_image.png', 'wb') as f:
        f.write(png_image)


# connect to the AirSim simulator
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

# get poses
pose1 = client.simGetObjectPose("OrangeBall")
print("OrangeBall x_val: " + str(pose1.position.x_val))
print("OrangeBall y_val: " + str(pose1.position.y_val))
print("OrangeBall z_val: " + str(pose1.position.z_val))

landed = client.getMultirotorState().landed_state
if landed == airsim.LandedState.Landed:
    print("taking off...")
    client.takeoffAsync().join()
else:
    print("already flying...")
    client.hoverAsync().join()

#displayPos(client)
print(getVector(client))

print("rotating...")
# rotates to absolute yaw
client.rotateToYawAsync(60).join()

takePic(client)

#print("moving to position...")
#client.moveToPositionAsync(pose1.position.x_val, pose1.position.y_val, -20, 15).join()

displayPos(client)
