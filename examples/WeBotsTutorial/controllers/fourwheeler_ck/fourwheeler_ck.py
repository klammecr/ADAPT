"""fourwheeler_ck controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
from controller import Motor
from controller import DistanceSensor

# initialize motors
wheels = []
wheelsNames = ['wheel1', 'wheel2', 'wheel3', 'wheel4']
for name in wheelsNames:
    wheels.append(robot.getDevice(name))
for i in range(4):
    wheels.append(robot.getDevice(wheelsNames[i]))
    wheels[i].setPosition(float('inf'))
    wheels[i].setVelocity(0.0)

# init distance sensors
ds_names = ["ds_left", "ds_right"]
ds_list  = []
for name in ds_names:
    ds = robot.getDevice(name)
    ds.enable(timestep)
    ds_list.append(ds)

# Set some default values:
angular_vel = 1 # rad/sec

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    # Read the sensors:
    ds_left_val  = ds_list[0].getValue()
    ds_right_val = ds_list[1].getValue()

    # Default is Drive Forward
    left_vel  = angular_vel
    right_vel = angular_vel

    # Process sensor data here.
    # Note, for this ds: 0 cm = 0 and .01m = 10 cm = 1000.
    obstacle_left  = (ds_left_val <= 1000)
    obstacle_right = (ds_right_val <= 1000)
    """
    CK:
    The below is not elif because if there is an obstacle left and right, 
    we want to go straight backwards. We have no backwards sensors so we can't
    consider that case yet.
    """
    if obstacle_left:
        # Turn Right, Left Wheels Back (1,3), Right Wheels Forward (2,4)
        print("OBSTACLE LEFT")
        left_vel= -angular_vel
    elif obstacle_right:
        # Turn Left, Left Wheels Back (2,4), Right Wheels Forward (1,3)
        print("OBSTACLE RIGHT")
        right_vel = -angular_vel

    # Set the wheel velocities
    wheels[0].setVelocity(left_vel)
    wheels[1].setVelocity(right_vel)
    wheels[2].setVelocity(left_vel)
    wheels[3].setVelocity(right_vel)

    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)

# Enter here exit cleanup code.
