import setup_path 
import airsim
import pprint
import math
import random
import time

def load_poles(client, file):
    res = []
    file = open(file, 'r')
    lines = file.readlines()
    for li in lines:
        pos = client.simGetObjectPose(li.strip('\n')).position
        res.append(pos)
    return res

def dist(vector1, vector2):
    x1 = vector1.x_val
    y1 = vector1.y_val
    x2 = vector2.x_val
    y2 = vector2.y_val
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def avg(num1, num2):
    return (num1 + num2) / 2

def offset(num) :
    num += random.randint(-5, 5)
    return num

def takePic(client, count):
    print("getting image...")
    png_image = client.simGetImage("0", airsim.ImageType.Scene)
    file = 'images/image' + str(count) + '.png'
    with open(file, 'wb') as f:
        f.write(png_image)

client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

# load in pole data
poles = load_poles(client, "pole_data/poles.txt")

# construct pole visiting order
order = []
start = client.getGpsData().gnss.velocity
order.append(start)
while len(poles) > 1 :
    origin = order[len(order) - 1]
    min = 999999
    min_index = 0
    for i in range(len(poles)):
        d = dist(origin, poles[i])
        if d < min :
            min = d
            min_index = i
    order.append(poles[min_index])
    poles.pop(min_index)
order.append(poles[0])
poles.pop(0)

# move drone to each location
z = -14.3
client.takeoffAsync().join()
client.moveToZAsync(z, 1).join()
for i in range(1, len(order)) :
    pos = order[i]
    origin = order[i - 1]

    print("Going to:")
    print(pos)
    client.moveToPositionAsync(avg(origin.x_val, pos.x_val), avg(origin.y_val, pos.y_val), z*5/6, 3, drivetrain = airsim.DrivetrainType.ForwardOnly, yaw_mode =  airsim.YawMode(False,0)).join()
    time.sleep(2)
    takePic(client, i)
    client.moveToPositionAsync(pos.x_val, pos.y_val, z, 3, drivetrain = airsim.DrivetrainType.ForwardOnly, yaw_mode =  airsim.YawMode(False,0)).join()
    time.sleep(3)
client.moveToPositionAsync(order[0].x_val, order[0].y_val, z, 3, drivetrain = airsim.DrivetrainType.ForwardOnly, yaw_mode =  airsim.YawMode(False,0)).join()
client.landAsync().join()

