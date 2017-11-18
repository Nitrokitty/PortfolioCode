# -*- coding: utf-8 -*-
"""
This file contains the class for all interactions with the i-create robot
and raspberry pi. To ensure optimal functionality, please call it with in
a "with" statement.

Written for CSCE-374 @ UofSC

@authors: Audrey "Danielle" Talley, Zackery Slater, & Thomas Kenner
@date: 9/21/2016
"""

#----------------------------Imports----------------------------
import serial
import time
import struct
import threading

class Robot:
    #----------------------------Variables----------------------------
    #Opcodes    
    __START = chr(128);
    __RESET = chr(7);
    __STOP = chr(173);
    __SAFE_MODE = chr(131)
    __POWER_DOWN = chr(133)
    __DRIVE = chr(137)
    __BUTTONS = chr(165)
    __QUERY = chr(149)
    __SIMPLE_QUERY = chr(142)
    #Packets
    __BUTTONS_PKT = chr(18)
    __DISTANCE_PKT = chr(19)
    __ANGLE_PKT = chr(20)
    #Button Codes
    CLOCK_CODE = 1 << 7
    SCHEDULE_CODE = 1 << 6
    DAY_CODE = 1 << 5
    HOUR_CODE = 1 << 4
    MINUTE_CODE = 1 << 3
    DOCK_CODE = 1 << 2
    SPOT_CODE = 1 << 1
    CLEAN_CODE = 1 << 0
    #Other
    __is_connected = False
    __connection = None
    __automate_on_off = True
    __PUSH_BUTTON = 1
    __RELEASE_BUTTON = 0
    __LAST_GET_REQUEST = None
    __REQUEST_WAIT_TIME = .015 #Can only request information every 15 miliseconds
    
    #----------------------------Con/Destructors----------------------------
    def __init__(self, auto_start_and_shut_down = True):
        """

        """
        self.automate_on_off = auto_start_and_shut_down

    def __exit__(self, exception_type, exception_value, exception_traceback):
        """
        This function is called at the end of a "with" statement. This will show any exceptions
        that were thrown if some were thrown and shudown the robot.

        Parameters:
            exception_type: Type of exception thrown
            exception_value: The exception message
            exception_tracebock: Where the exception was thrown (memory address)
        """
        if exception_type is not None:
            print exception_type, exception_value, exception_traceback
            self.__disconnect()
        if self.automate_on_off:
            self.shut_down()
        return self

    def __enter__(self):
        """
        This function is called at the beginning of a "with" statement. It will
        start up and connect to the robot. Note a double startup is needed or there
        will be issues recieving packets from the robot
        """
        if self.automate_on_off:
            self.start_up(True)
        else:
            self.__connect()
        return self

    #----------------------------Private Methods----------------------------
    def __int_to_hex(self, val, num_of_bits = 4, start_index = 0, end_index = -1, use_thirty_two_bits = True): 
        """
        Converts a signed integer into a signed hexadecimal number.
        
        Parameters:
            val: The integer that will be converted.
            num_of_bits: The number of bits to keep in the hexadecimal result.
            start_index: The starting index of the bits you want to retrieve.
            end_index: The ending index of the bits you want to retrieve.
            use_thirty_two_bits: If true, will convert the val into a 32bit hexadecimal value,
                otherwise it will be converted to a 64bit hexadecimal value.
        Returns:
            (str) hexadecimal representation of val
        """
        bits = 32;
        if not use_thirty_two_bits:
            bits = 64;
        answer = hex(val & (2**bits-1))[2:-1] #removing the "0x" and "L": "0xf5f6L" -> "f5f6"
        while(len(answer) < num_of_bits): #padding
            answer = "0" + answer;
        return answer[:num_of_bits][start_index:end_index]
    
    def __hex_to_int(self, val):
        """
        Converts a signed hexadecimal number into an unsigned integer

        Parameters:
            val: The hexadecimal number that will be converted.
        """
        return int(val, 16)
    
    def __convert_integer(self, val, num_of_hex_bits = 4, start_index = 0, end_index = -1, return_character = True):
        """
        Converts a signed integer into an unsigned integer by converting it into abs
        signed hexadecimal value intermediately.
        
        Parameters:
            val: The hexadecimal number that will be converted.
            num_of_hex_bits: The number of hex bits to keep in the intermediate
                hexadecimal number. This will effect all positive numbers
            start_index: The start index of the bits you wish to keep in the intermediate
                hexadecimal number. This will effect the translation from a signed hexadecimal
                value to an unsigned integer.
            end_index: The end index of the bits you wish to keep in the intermediate
                hexadecimal number. This will effect the translation from a signed hexadecimal
                value to an unsigned integer.
            return_character: If true, will return the result as a character instead of an
                integer

        Returns:
            (int) interger representation of hexadecimal value
        """
        result = self.__hex_to_int(self.__int_to_hex(val, num_of_hex_bits, start_index, end_index))
        if return_character:
            return chr(result)
        return result
    
    def __send(self, message):
        """
        Sends a command to the robot

        Parameter:
            message: command to send
        """
        t = threading.Thread(target = self.__connection.write, args = (message, ))
        t.start()
        t.join()
        
    def __start(self):
        """
        Starts the robot. The robot will start in Passive Mode
        """
        self.__send(self.__START)
    
    def __safe_mode(self):
        """
        Sets the robot into safe mode. The robot must be started before changing modes
        """
        self.__send(self.__SAFE_MODE)
        
    def __power_down(self):
        """
        Powers down the robot
        """
        print "Powering Down."
        self.__send(self.__POWER_DOWN)
    
    def __disconnect(self):
        """
        Closes the connection with the raspberry pi.
        """
        if not self.__is_connected:
            return
        t = threading.Thread(target = self.__connection.close)
        t.start()
        t.join()
        
    def __connect(self):
        """
        Opens a new connection to the raspberry pi
        """
        if not self.__is_connected:
            self.__connection = serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=1)
        
    def __request(self, request, expected_message_bytes = 1):
        """
        This will send a request to the robot for information and return the information as a tupple.

        Parameters:
            request: op-code with any necessary parameters for the request.
            expected_message_bytes: the number of bytes we are expected to recieve from the robot

        Returns:
            int tupple (x,x): the requested information from the robot in the form of a touple
                (0,) for one byte and (0,0) for two
        """
        self.__send(request)
        msg = self.__connection.read(expected_message_bytes)
        if len(msg) > 0: #If it did not have any information to return, the message will be empty
            unpacked_msg = ""
            for character in msg:
                unpacked_msg = self.__unpack(character)
        self.wait(self.__REQUEST_WAIT_TIME)
        return unpacked_msg
    
    def __get_buttons(self, return_raw_data = False):
        """
        This function will send a request to the robot to get the buttons that are currently pressed.

        Returns:
            (int) button that was pressed or zero if no button was pressed
        """
        msg = self.__request(self.__SIMPLE_QUERY + self.__BUTTONS_PKT)
        if return_raw_data:
            return msg
        if len(msg) > 0:
            return msg[0]
        return 0

    def __get_distance(self):
        """
        This function will send a request to the robot to get the distance that it has traveled since
        it's last request

        Returns:
            (int tupple) distance traveled (x,y) where x is the high value
        """
        return self.__request(self.__SIMPLE_QUERY + self.__DISTANCE_PKT, 2)

    def __get_angle(self):
        """
        This function will send a request to the robot to get the angle that it has turned since
        it's last request

        Returns:
            (int tupple) angle turned (x,y) where x is the high value
        """
        return self.__request(self.__SIMPLE_QUERY + self.__ANGLE_PKT, 2)

    def __unpack(self, packet):
        """
        This function will unpack a packet recieved from the robot.

        Parameters:
            packed: The packet from the robot in ascii

        Returns:
            (int tupple) unpacked packet
        """
        return struct.unpack('b', packet)
        
    #----------------------------Public Methods----------------------------
    def reset(self):
        """
        Resets the robot. The state is changed to off.
        """
        print "Resetting..."
        self.__send(self.__RESET)

     def shut_down(self):
        """
        Stops the robot's current action and powers it down. It then disconnects
        from the robot.
        """
        print "Shutting Down..."
        self.stop()
        self.__disconnect()
        print "Shutdown Complete"

     def start_up(self, initial_start = True):
        """
        Connects to and starts up the robot. Then puts it in safe mode.

        Parameters:
            inital_start: Some functions will return garbage data if the connection
                is nt attempted twice
        """
        if initial_start:
            print "Starting Up..."
        self.__connect()
        self.__start()
        if initial_start:
            self.__disconnect()
            #self.wait(1) #TODO: Try with and without waiting
            self.__connect()
            self.__start()
        self.__safe_mode()
        if initial_start:
            print "Start Up Complete"
        
    def pressed_button(self, loop_until_true = False):
        """
        This function will check to see if any buttons are pressed with an option to loop until a button is pressed until the given timeout

        Parameters:
            loop_until_true: This parameter will enable the funtion to continuously loop until a button is pressed
            timeout: If loop until true is enabled, this is how long in seconds the function will try to recieve input from the robot. If this is
                set to 0 then it will loop infinately

        Returns:
            (int) button code
        """
        if loop_until_true:
            button = self.__get_buttons()
            while(button == 0):
                button = self.__get_buttons()
            return button
        return self.__get_buttons()

    def pressed_button_raw(self, loop_until_true = False):
        """
        This function will check to see if any buttons are pressed with an option to loop until a button is pressed until the given timeout.
        Will return the raw tupple

        Parameters:
            loop_until_true: This parameter will enable the funtion to continuously loop until a button is pressed
            timeout: If loop until true is enabled, this is how long in seconds the function will try to recieve input from the robot. If this is
                set to 0 then it will loop infinately

        Returns:
            (int tupple) button code
        """
        if loop_until_true:
            button = self.__get_buttons(True)
            while(button[0] == 0):
                button = self.__get_buttons()
            return button
        return self.__get_buttons()
    
    def pressed_clock(self):
        """
        This function will check if the clock button is pressed.

        Parameters:
            print_check: If enabled, the function will print that it's checking the button.

        Returns:
            (bool) if button was pressed
        """
        if(self.pressed_button() == self.CLOCK_CODE):
            print "Clock was pressed"
            return True
        return False
        
    def pressed_day(self):
        """
        This function will check if the day button is pressed.

        Parameters:
            print_check: If enabled, the function will print that it's checking the button.

        Returns:
            (bool) if button was pressed
        """
        if self.pressed_button() == self.DAY_CODE:
            print "Day was pressed"
            return True
        return False
        
    def pressed_hour(self):
        """
        This function will check if the hour button is pressed.

        Parameters:
            print_check: If enabled, the function will print that it's checking the button.

        Returns:
            (bool) if button was pressed
        """
        if self.pressed_button() == self.HOUR_CODE:
            print "Hour was pressed"
            return True
        return False
    
    def pressed_minute(self):
        """
        This function will check if the minute button is pressed.

        Parameters:
            print_check: If enabled, the function will print that it's checking the button.

        Returns:
            (bool) if button was pressed
        """
        if self.pressed_button() == self.MINUTE_CODE:
            print "Minute was pressed"
            return True
        return False
        
    def pressed_dock(self):
        """
        This function will check if the dock button is pressed.

        Parameters:
            print_check: If enabled, the function will print that it's checking the button.

        Returns:
            (bool) if button was pressed
        """
        if self.pressed_button() == self.DOCK_CODE:
            print "Dock was pressed"
            return True
        return False
        
    def pressed_spot(self):
        """
        This function will check if the spot button is pressed.

        Parameters:
            print_check: If enabled, the function will print that it's checking the button.

        Returns:
            (bool) if button was pressed
        """
        if self.pressed_button() == self.SPOT_CODE:
            print "Spot was pressed"
            return True
        return False
        
    def pressed_clean(self):
        """
        This function will check if the clean button is pressed.

        Parameters:
            print_check: If enabled, the function will print that it's checking the button.

        Returns:
            (bool) if button was pressed
        """
        if self.pressed_button() == self.CLEAN_CODE:
            print "Clean button was pressed"
            return True
        return False
        
    def stop(self):
        """
        Stops the robot's current behavior
        """
        print "Stopping"
        self.__send(self.__STOP)
        self.start_up(False)
        self.wait(.1)
    
    def drive(self, velocity, angle):
        """
        Commands the robot to drive givent the velocity and rotation.
        
        Parameters:
            velocity: The speed and direction as to which the robot will drive. The speed
                can be between 0 and 255 and the direction is the sign. For example, 
                -50 would move the robot backward at a speed of 50.
            angle: The angle at which the robot will rotate. The rotation can be between
                0 and 255 and a positive angle will result in a clockwise rotation. 
        """
        velocity_first_half = self.__convert_integer(velocity, 4, 0, 2) #first two velocity bits
        velocity_second_half = self.__convert_integer(velocity, 4, 2, 4) #second two velocity bits
        angle_first_half = self.__convert_integer(angle, 4, 0, 2) #first two angle bits
        angle_second_half = self.__convert_integer(angle, 4, 2, 4) #second two angle bits
        if not angle == 0:
            self.__get_angle() #reseting it before it starts turning
        if not velocity == 0:
            self.__get_distance() #reseting it before it starts going
        self.__send(self.__DRIVE + velocity_first_half +velocity_second_half + angle_first_half + angle_second_half)

    def wait_for_interrupt(self, interrupt_code, timeout = 5):
        """
        This function will wait for a specified period of time but will stop waiting if
        the given interrupt code is given.

        Parameters:
            interrupt_code: The button code of the button that will be used to interrupt
                the wait
            timeout: The number of seconds we should wait for an interrupt

        Returns:
            (int) button code of interrupt or zero if it was not interrupted
        """
        if not type(interrupt_code) == list:
            interrupt_code = [interrupt_code]
        self.wait(.1)
        stop_time = time.time() + timeout - .1
        button = 0
        while (time.time() < stop_time and not(button in interrupt_code)):
            button = self.pressed_button()
        if button not in interrupt_code:
            return 0
        return button

    def drive_until_interrupt(self, interrupt_code, distance = 1000, timeout = 5):
        """
        This function will wait for the robot to drive a certain distance but will stop waiting if
        the given interrupt code is given.

        Parameters:
            interrupt_code: The button code of the button that will be used to interrupt
                the wait. This can also be a list of codes
            distance: How far in milimeters the robot should travel before stopping
            timeout: How long the robot has to reach it's goal

        Returns:
            (int) button code of interrupt or zero if it was not interrupted
        """
        print "Driving for " + str(distance) + "mm..."
        distance = abs(distance)
        stop_time = time.time() + timeout - .1
        button = 0
        distance_traveled = 0;
        percent_complete = .2;
        if not type(interrupt_code) == list:
            interrupt_code = [interrupt_code]
        self.wait(.1)
        while (time.time() < stop_time and not(button in interrupt_code) and distance_traveled < distance):
            button = self.pressed_button()
            distance_traveled += abs(self.__get_distance()[0])
            if distance_traveled > percent_complete * distance:
                print str(distance_traveled) + "mm (" + str(percent_complete * 100) + ")%..."
                percent_complete += .2
        print "Distance Traveled: " + str(distance_traveled) + "mm"
        if button not in interrupt_code:
            return 0
        return button

    def turn_until_interrupt(self, interrupt_code, angle = 90, timeout = 5):
        """
        This function will wait for the robot to turn a certain angle but will stop waiting if
        the given interrupt code is given.

        Parameters:
            interrupt_code: The button code of the button that will be used to interrupt
                the wait. This can also be a list of codes
            angle: How much in degrees the robot should turn before stopping
            timeout: How long the robot has to reach it's goal

        Returns:
            (int) button code of interrupt or zero if it was not interrupted
        """
        print "Turning for " + str(angle) + "deg..."
        angle = abs(angle)
        stop_time = time.time() + timeout - .1
        button = 0
        angle_turned = 0;
        percent_complete = .2;
        if not type(interrupt_code) == list:
            interrupt_code = [interrupt_code]
        self.wait(.1)
        while (time.time() < stop_time and not(button in interrupt_code) and angle_turned < angle):
            button = self.pressed_button()
            angle_turned += abs(self.__get_angle()[0])
            if angle_turned > angle * percent_complete:
                print str(angle_turned) + "deg (" + str(percent_complete * 100) + ")%..."
                percent_complete += .2
        print "Total Amount Turned: " + str(angle_turned) + "deg"
        if button not in interrupt_code:
            return 0
        return button
            

    def forward(self, speed):
        """
        This function will drive the robot foward

        Parameters:
            speed: The speed at which the robot will travel
        """
        print "Driving Forward"
        return self.drive(abs(speed), 0)
        
    def backward(self, speed):
        """
        This function will drive the robot backward

        Parameters:
            speed: The speed at which the robot will travel
        """
        print "Driving Backward"
        return self.drive(-abs(speed), 0)

    def turn_left(self, velocity, angle):
        """
        This function will turn the robot to the right in place.

        Parameters:
            angle: The speed as to which the robot will turn
        """
        print "Turning Left"
        return self.drive(abs(velocity), abs(angle))

    def turn_right(self, velocity, angle):
        """
        This function will turn the robot to the left in place.

        Parameters:
            angle: The speed as to which the robot will turn
        """
        print "Turning Right"
        self.drive(abs(velocity), -abs(angle))
    
    def wait(self, seconds, stop_at_end = False):
        """
        Instructs the interpreter to wait for the specified number of seconds.

        Parameters:
            seconds: number of seconds the interpreter should wait
        """
        t = threading.Thread(target = time.sleep, args = (seconds, ))
        t.start()
        t.join()
        if stop_at_end:
            self.stop()
            
        
    #----------------------------End Robot Class----------------------------


