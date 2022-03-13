from Webots.DroneInterface import DroneInterface
from webots.controller import Keyboard

# Init Keyboard
keyboard  = Keyboard()

# Constants, empirically found.
# Lift the drone with thrust
# g_vertical_thrust = 68.5
# g_vertical_offset = 0.6
# # PID constants
# g_vertical_p = 3.0    
# g_roll_p     = 50.0      
# g_pitch_p    = 30.0
g_target_altitude = 1.0

# Start up the drone
print("Starting Drone\n")
drone = DroneInterface()
time_step = drone.timestep
drone.start_drone()

# Tutorial
print("You can control the drone with your computer keyboard:\n");
print("- 'up': move forward.\n");
print("- 'down': move backward.\n");
print("- 'right': turn right.\n");
print("- 'left': turn left.\n");
print("- 'shift + up': increase the target altitude.\n");
print("- 'shift + down': decrease the target altitude.\n");
print("- 'shift + right': strafe right.\n");
print("- 'shift + left': strafe left.\n");

# Perform simulation steps until Webots is stopping the controller
robot = drone.get_robot()
keyboard.enable(time_step)
while robot.step(time_step) != -1:
    if robot.getTime() > 1.0:
        # Default Values
        yaw_disturbance   = 0.0
        pitch_disturbance = 0.0
        roll_disturbance  = 0.0
        # Get the keyboard input
        key = keyboard.getKey()
        while (key > 0):
            if key == Keyboard.UP:
                pitch_disturbance = -2.0;
                break
            if key == Keyboard.DOWN:
                pitch_disturbance = 2.0;
                break
            if key == Keyboard.RIGHT:
                yaw_disturbance = -1.3;
                break
            if key == Keyboard.LEFT:
                yaw_disturbance = 1.3;
                break;
            if key == (Keyboard.SHIFT + Keyboard.RIGHT):
                roll_disturbance = -1.0;
                break;
            if key == (Keyboard.SHIFT + Keyboard.LEFT):
                roll_disturbance = 1.0;
                break;
            if key == (Keyboard.SHIFT + Keyboard.UP):
                g_target_altitude += 0.05;
                print("target altitude: %f [m]\n", g_target_altitude);
                break;
            if key == (Keyboard.SHIFT + Keyboard.DOWN):
                g_target_altitude -= 0.05;
                print("target altitude: %f [m]\n", g_target_altitude);
                break;

            # Get the next key input
            key = keyboard.getKey()

        # Deliver inputs into the drone and have it move by actuating the motors
        drone.actuate_motors(yaw_disturbance, pitch_disturbance, roll_disturbance, g_target_altitude)