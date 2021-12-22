#code Written by Engr. Din Muhammad
#----------------------------------
# To install dependencies: 
# pip install modbus-tk
# pip install pyserial
#-------------------------------
#find usb serial device
#dmesg | grep tty
#------------------------------
import time
import json
import serial
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu

if __name__ == "__main__":
    try:
        # Connect to the slave
        serial = serial.Serial(
                               port='/dev/ttyUSB0',   
                               baudrate=9600,
                               bytesize=8,
                               parity='N',
                               stopbits=1,
                               xonxoff=0
                              )

        master = modbus_rtu.RtuMaster(serial)
        master.set_timeout(2.0)
        master.set_verbose(True)
        # Changing power alarm value to 100 W 
        # master.execute(1, cst.WRITE_SINGLE_REGISTER, 1, output_value=100)
        dict_payload = dict()

        while True:
            data = master.execute(1, cst.READ_INPUT_REGISTERS, 0, 10)
            
            voltage = data[0] / 10.0 # [V]
            current = (data[1] + (data[2] << 16)) / 1000.0 # [A]
            power = (data[3] + (data[4] << 16)) / 10.0 # [W]
            energy = data[5] + (data[6] << 16) # [Wh]
            frequency = data[7] / 10.0 # [Hz]
            powerFactor = data[8] / 100.0
#            alarm = data[9] # 0 = no alarm

            print('Voltage [V]: ', voltage)
            print('Current [A]: ', current)
            print('Power [W]: ', power) # active power (V * I * power factor)
            print('Energy [Wh]: ', energy)
            print('Frequency [Hz]: ', frequency)
            print('Power factor []: ', powerFactor)
#            print('Alarm : ', alarm)
            
            time.sleep(1)
        
    except KeyboardInterrupt:
        print('exiting pzem script')
    except Exception as e:
        print(e)
    finally:
        master.close()
