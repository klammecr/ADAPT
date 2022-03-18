from webots.controller import Robot

class DroneInterface(object):
    def __init__(self):
        # create the Robot instance.
        self.robot = Robot()

        # get the time step of the current world. Time step is 64 ms for each physics step
        self.timestep = int(self.robot.getBasicTimeStep())

        # Initialize camera
        self.camera = self.robot.getDevice("camera")
        self.camera.enable(self.timestep)

        # Initialize the IMU
        self.imu = self.robot.getDevice("inertial unit")
        self.imu.enable(self.timestep)

        # Initialize the GPS
        self.gps = self.robot.getDevice("gps")
        self.gps.enable(self.timestep)

        # Initialize the Gyro
        self.gyro = self.robot.getDevice("gyro")
        self.gyro.enable(self.timestep)

        # Camera YPR (Camera Movement)
        self.camera_roll_motor  = self.robot.getDevice("camera roll")
        self.camera_pitch_motor = self.robot.getDevice("camera pitch")
        self.camera_yaw_motor   = self.robot.getDevice("camera yaw")

        # PID Constants:
        self.k_vertical_thrust = 68.5 
        self.k_vertical_offset = 0.60
        self.k_vertical_p      = 3.0
        self.k_roll_p          = 50.0
        self.k_pitch_p         = 30.0

        # Get the propeller motors, for a FW, we may need to move this into a subclass
        fl_propeller = self.robot.getDevice("front left propeller")
        fr_propeller = self.robot.getDevice("front right propeller")
        rl_propeller = self.robot.getDevice("rear left propeller")
        rr_propeller = self.robot.getDevice("rear right propeller")
        self.propellers = [fl_propeller, fr_propeller, rl_propeller, rr_propeller]

    @staticmethod
    def clamp(val, min_val, max_val):
        return min(max(val, min_val), max_val)

    def start_drone(self, starting_vel = 1.0):
        """
        Start up the motors for the propellers
        """
        for propeller in self.propellers:
            propeller.setPosition(float('inf'))
            propeller.setVelocity(starting_vel)

    def _calc_motor_input(self, yaw_disturbance, pitch_disturbance, roll_disturbance, target_altitude = 1.0):
        """
        Calculate the motor inputs

        :param yaw_disturbance   The imparted yaw input for the time step
        :param pitch_disturbance The imparted pitch input for the time step
        :param roll_disturbance  The imparted roll input for the time step

        Returns:
        fl_motor_input  Motor input for the front left
        fr_motor_input  Motor input for the front right
        bl_motor_input  Motor input for the back left
        br_motor_input  Motor input for the back right
        """
        # Calculate the inputs into the motor equations
        roll_input             = self.k_roll_p * self.clamp(self.get_roll(), -1.0, 1.0) + self.get_roll_acceleration() + roll_disturbance
        pitch_input            = self.k_pitch_p * self.clamp(self.get_pitch(), -1.0, 1.0) + self.get_pitch_acceleration() + pitch_disturbance
        yaw_input              = yaw_disturbance
        altitude               = self.gps.getValues()[2]
        clamped_difference_alt = self.clamp(target_altitude - altitude + self.k_vertical_offset, -1.0, 1.0)
        vertical_input         = self.k_vertical_p * (clamped_difference_alt ** 3)

        # Calculate the motor inputs
        # These two are diagonal, so, they must rotate the same direction, make it clockwise
        fl_motor_input = self.k_vertical_thrust + vertical_input - roll_input + pitch_input - yaw_input
        rr_motor_input = self.k_vertical_thrust + vertical_input + roll_input - pitch_input - yaw_input
        # These two are diagonal, so, they must rotate the same direction, but opposite of the other two make it counter-clockwise
        fr_motor_input = - 1 * (self.k_vertical_thrust + vertical_input + roll_input + pitch_input + yaw_input) 
        rl_motor_input = -1 * (self.k_vertical_thrust + vertical_input - roll_input - pitch_input + yaw_input) #
       
        return [fl_motor_input, fr_motor_input, rl_motor_input, rr_motor_input]

    def actuate_motors(self, yaw_disturbance, pitch_disturbance, roll_disturbance, target_alt = 1.0):
        """
        Actuate the motors to move the drone

        :param  fl_motor_input  Motor input for the front left
        :param  fr_motor_input  Motor input for the front right
        :param  bl_motor_input  Motor input for the back left
        :param  br_motor_input  Motor input for the back right
        """
        # Grab the inputs
        motor_inputs = self._calc_motor_input(yaw_disturbance, pitch_disturbance, roll_disturbance, target_alt)
        
        # Actuate those motors
        for i in range(0, len(motor_inputs)):
            self.propellers[i].setVelocity(motor_inputs[i])

    # Getters Section
    def get_roll(self):
        return self.imu.getRollPitchYaw()[0]
    def get_roll_acceleration(self):
        return self.gyro.getValues()[0]
    def get_pitch(self):
        return self.imu.getRollPitchYaw()[1]
    def get_pitch_acceleration(self):
        return self.gyro.getValues()[1]
    def get_yaw(self):
        return self.imu.getRollPitchYaw()[2]
    def get_yaw_acceleration(self):
        return self.gyro.getValues()[2]
    def get_robot(self):
        """
        Return the robot object
        """
        return self.robot