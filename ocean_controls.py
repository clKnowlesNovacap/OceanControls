import serial
import time

class Ocean_Controls(object):

    def __init__ (self):
        self.port = 0
        self.port_default = 'COM7'
        self.ACCF = 3000
        self.ACCI = 10
        self.ACCS = 100
        self.vel = 0
        self.pos = 0
        self.si_factor = 1
        self.gear_ratio = 1
        self.trash = 0
    
    def set_default(self):
        self.ACCF = 3000
        self.ACCI = 10
        self.ACCS = 100
        self.si_factor = 1
        self.gear_ratio = 1

    def set_port(self,port_val):
        ''' sets the serial port for the controller
            returns 1 if successful 0 if not '''

        try:
            self.port = serial.Serial(port_val)
            self.port.baudrate = 57600
            self.port.timeout = 0
            print("Successful")
            print(self.port)
            return 1

        except:
            print("Couldn't Connect to Ocean Controller")
            print("Try a different port?")
            return 0
    
    def set_velocity(self,speed):
        speed_frequency = speed * self.si_factor
        return speed_frequency

    def set_distance(self,distance):
        pulses = distance * self.gear_ratio * self.si_factor
        return pulses

    def accf(self, motor, value):
        # Sets the Maximum Frequency for an Axis [Hz]
        # Default is 3000
        
        self.ACCI = value
        string = '@' + str(motor) + ' ACCF ' + str(self.ACCI) + '\r\n'
        self.port.write(string.encode('utf_8'))
        self.trash = self.port.readline()
        return self.trash
  

    def acci(self, motor, value):
        # Sets the Frequency increment for an axis [Hz/Step]
        # Default is 10

        self.ACCI = value
        string = '@' + str(motor) + ' ACCI ' + str(self.ACCI) + '\r\n'
        self.port.write(string.encode('utf_8'))
        self.trash = self.port.readline()
        return self.trash
    
    def accs(self, motor, value):
        # Sets the initial Frequency for an Axis [Hz]
        # Default is 100

        self.ACCS = value
        string = '@' + str(motor) + ' ACCS ' + str(self.ACCI) + '\r\n'
        self.port.write(string.encode('utf_8'))
        self.trash = self.port.readline()
        return self.trash 

    def amov(self, motor, vel, pos):
        # Move to a Position [Steps]
        # Use default values for steps
        # Otherwise use a si_factor to change
        # Velocity from [pulses/s] to [dist/s]
        # Position from [pulses] to [dist]

        vel = self.set_velocity(vel)
        pos = self.set_distance(pos)
        string ='@' + str(motor) +' AMOV ' + str(pos) + '\r\n'
        self.port.write(string.encode('utf_8'))
        self.trash = self.port.readline()


    def rmov(self, motor, pos):
        # Move to a Position [Steps]
        # Use default values to send steps
        # Otherwise use a si_factor to change
        # Velocity from [pulses/s] to [dist/s]
        # Position from [pulses] to [dist]

        string = '@' + str(motor) +' RMOV ' + str(pos) + '\r\n'
        self.port.write(string.encode('utf_8'))
        self.waitfor(1)

    def waitfor(self,motors):
        while True:
            a = self.port.readline().decode('utf_8')
            string = "Reply = " + str(a) + "<<"
            print(string)
            if "!" in a:
                break
            time.sleep(0.001)

    def baud(self, value):
        # Set the communication Baudrate
        # Valid Values from 10 to 230400 bps
        # 1 - 9 common baud rates 9600 ect...

        string ='@' + str(1) +' BAUD ' + str(value) + '\r\n'
        self.port.write(string.encode('utf_8'))
        self.trash = self.port.readline().decode('utf_8')
        return self.trash

    def drof(self,channel):
        # Sets an output channel off
        # DRON,DROF,DRST are output channel commands 

        string ='@' + str(channel) +' DROF' + '\r\n'
        self.port.write(string.encode('utf_8'))
        self.trash = self.port.readline()
        return self.trash
    
    def dron(self,channel, output):
        # Sets an output channel on
        # If output is set to -1 stays on until switched off with DROF
        # When value is positive, causes the output to switch on for 100ms multiplied by the given value 
        # DRON,DROF,DRST are output channel commands 

        string ='@' + str(channel) +' DRON ' + str(output) + '\r\n'
        self.port.write(string.encode('utf_8'))
        self.trash = self.port.readline()
        return self.trash

    def drst(self, motor, channel):
        # Returns the number of of tenths of seconds left on the output timer for an axis
        # DRON,DROF,DRST are output channel commands 

        string ='@' + str(motor) +' DRST ' + str(channel) + '\r\n'
        self.port.write(string.encode('utf_8'))
        self.trash = self.port.readline()
        return self.trash

    def optn(self, motor, mode):
        # Set checksum mode and configure how the controller reasponds to axis commands
        # Value Verbose_Mode Checksum_Mode Individual_Response

        string ='@' + str(motor) +' OPTN ' + str(mode) + '\r\n'
        self.port.write(string.encode('utf_8'))
        self.trash = self.port.readline()
        return self.trash

    def posn(self, axis, pos):
        # Sets the current position for one or more axes
        # Can only be used to set an axis positon while idle

        string = '@' + str(axis) + 'POSN ' + str(pos) + '\r\n'
        self.port.write(string.encode('utf_8'))
        self.trash = self.port.readline()
        return self.trash

    def pstt(self):
        # Responds with the positions of the four controlled axes

        string = '@' + str(1) + ' PSTT' + '\r\n'
        self.port.write(string.encode('utf_8'))
        self.trash = self.port.readline()
        return self.trash
    
    def racc(self):
        # Responds with the inital frequency, frequency increment, and maximum frequency

        string = '@' + str(1) + ' RACC' + '\r\n'
        self.port.write(string.encode('utf_8'))
        self.trash = self.port.readline()
        return self.trash

    def rdan(self,io):
        # The rdan command reads the voltages at AN1,AN2,IO1,IO2 or the suppoy voltage to the controller
        # With no parameter, the command returns all voltages in milivolts

        string = '@' + str(1) + ' RDAN ' + str(io) + '\r\n'
        self.port.write(string.encode('utf_8'))
        self.trash = self.port.readline()
        return self.trash

    def rdio(self,io):
        # Returns the state of IO ports 0, 1, 2, 3...

        string = '@' + str(1) + ' RDIO ' + str(io) + '\r\n'
        self.port.write(string.encode('utf_8'))
        self.trash = self.port.readline()
        return self.trash

    def rset(self):
        # RSET command cases the controller to reset, simulating a 
        # removal and reapplication of power

        string = '@' + str(1) + ' RSET\r\n'
        self.port.write(string.encode('utf_8'))
        self.trash = self.port.readline()
        return self.trash


    def save(self):
        # Save records the controller's current configureations
        # Save baud rate, checksum ect...

        string = '@' + str(1) + 'SAVE' + '\r\n'
        self.port.write(string.encode('utf_8'))
        self.trash = self.port.readline()
        return self.trash



    def stat(self):
        string ='@' + str(1) +' STAT' + '\r\n'
        self.port.write(string.encode('utf_8'))
        self.trash = self.port.readline().decode('utf_8')
        return self.trash
    

    def stop(self):
        # Immediately stop all axes

        string = '@' + str(1) + ' STOP\r\n'
        self.port.write(string.enocde('utf_8'))
        self.trash = self.port.readline()
        return self.trash

    def wdio(self, io):
        # Sets IO1 and IO2 as digital outputs
        # Command can be addressed to any axis of the controller

        string = '@' + str(io) + ' WDIO\r\n'
        self.port.write(string.encode('utf_8'))
        self.trash  = self.port.readline()
        return self.trash 
    
    def custom(self,custom_string):
        string = str(custom_string) + '\r\n'
        self.port.write(string.encode('utf_8'))
        self.trash = self.port.readlines(128)
        return self.trash

    def close_port(self):
        self.port.close()