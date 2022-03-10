"""epuck_collisionavoidance_ck controller."""
"""
In the usual case, the update delay is chosen to be similar to the control step (TIME_STEP) 
and hence the sensor will be updated at every wb_robot_step function call. If, for example, 
the update delay is chosen to be twice the control step then the sensor data will be updated 
every two wb_robot_step function calls: this can be used to simulate a slow device. 
Note that a larger update delay can also speed up the simulation, especially for CPU intensive devices like the Camera.
"""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, DistanceSensor, Motor

# Time step is 64 ms for each physics step
TIME_STEP = 64

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# initialize devices, the 8 distance sensors
ps = []
psNames = [
    'ps0', 'ps1', 'ps2', 'ps3',
    'ps4', 'ps5', 'ps6', 'ps7'
]

for i in range(8):
    ps.append(robot.getDevice(psNames[i]))
    ps[i].enable(TIME_STEP)
    

# Get the left and the right motor for locomotion
# Actuators don't need to be explicitly enabled
leftMotor = robot.getDevice('left wheel motor')
rightMotor = robot.getDevice('right wheel motor')

# Set the default position and velocity
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(0.0)
rightMotor.setVelocity(0.0)


# Main loop:
# - perform simulation steps until Webots is stopping the controller
    # Enter here functions to send actuator commands, like:

while robot.step(timestep) != -1:
    # Read the sensors:
    # read sensors outputs
    psValues = []
    for i in range(8):
        psValues.append(ps[i].getValue())

    # Process sensor data here.
    # Detect obstacles
    # This will check the distance at pi/6, pi/4, and pi/2
    right_obstacle = psValues[0] > 80.0 or psValues[1] > 80.0 or psValues[2] > 80.0
    # This will check the distance at -pi/6, -pi/4, and -pi/2
    left_obstacle = psValues[5] > 80.0 or psValues[6] > 80.0 or psValues[7] > 80.0

    # modify speeds according to obstacles
    MAX_SPEED = 6.28

    # initialize motor speeds at 50% of MAX_SPEED.
    leftSpeed  = 0.5 * MAX_SPEED
    rightSpeed = 0.5 * MAX_SPEED
    if left_obstacle:
        # turn right
        leftSpeed  = 0.5 * MAX_SPEED
        rightSpeed = -0.5 * MAX_SPEED
    elif right_obstacle:
        # turn left
        leftSpeed  = -0.5 * MAX_SPEED
        rightSpeed = 0.5 * MAX_SPEED
   
    # write actuators inputs
    leftMotor.setVelocity(leftSpeed)
    rightMotor.setVelocity(rightSpeed)

# Enter here exit cleanup code.
