import setup_path 
import airsim
import pprint

client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)

client.armDisarm(True)




pose1 = client.simGetObjectPose("Power_Line_604");
print("Power_Line - Position: %s, Orientation: %s" % (pprint.pformat(pose1.position),
    pprint.pformat(pose1.orientation)))

client.takeoffAsync().join()

client.moveToPositionAsync(pose1.position.x_val, pose1.position.y_val, -50, 5).join();
