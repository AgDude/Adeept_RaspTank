#!/usr/bin/python3
# File name   : setup.py
# Author      : Adeept
# Date        : 2020/3/14

import os
import time

curpath = os.path.realpath(__file__)
thisPath = "/" + os.path.dirname(curpath)

def replace_num(file,initial,new_num):
    newline=""
    str_num=str(new_num)
    with open(file,"r") as f:
        for line in f.readlines():
            if(line.find(initial) == 0):
                line = (str_num+'\n')
            newline += line
    with open(file,"w") as f:
        f.writelines(newline)

errors = set()
def run_command(command):
    result = os.system(command)
    if result == 0 and command in errors:
        errors.remove(command)
    elif result != 0:
        errors.add(command)
    return result

commands_1 = [
    "sudo apt-get update",
    # "sudo apt-get purge -y wolfram-engine",
    # "sudo apt-get purge -y libreoffice*",
    # "sudo apt-get -y clean",
    # "sudo apt-get -y autoremove",
    "sudo apt install -y python3-pip",
    "sudo pip3 install -U pip",
    "sudo apt-get install -y python-dev libfreetype6-dev libjpeg-dev build-essential",
    "sudo apt-get install -y i2c-tools",
    "sudo -H pip3 install --upgrade luma.oled",
    "sudo pip3 install adafruit-pca9685",
    "sudo pip3 install rpi_ws281x",
    "sudo apt-get install -y python3-smbus",
    "sudo pip3 install mpu6050-raspberrypi",
    "sudo pip3 install flask",
    "sudo pip3 install flask_cors",
    "sudo pip3 install websockets",
    "sudo apt-get install -y libjasper-dev",
    "sudo apt-get install -y libatlas-base-dev",
    "sudo apt-get install -y libgstreamer1.0-0"
]

mark_1 = 0
for x in range(3):
    for command in commands_1:
        if run_command(command) != 0:
            print("Error running installation step 1")
            mark_1 = 1
    if mark_1 == 0:
        break


commands_2 = [
    "sudo pip3 install RPi.GPIO",
    # "sudo apt-get -y install libqtgui4 libqt4-test",
    "sudo apt-get -y install libhdf5-dev libhdf5-serial-dev libatlas-base-dev libjasper-dev python3-h5py",
    "sudo pip3 install -r server/requirements.txt",
    "sudo git clone https://github.com/oblique/create_ap",
    "cd " + thisPath + "../create_ap && sudo make install",
    "cd //home/pi/create_ap && sudo make install",
    "sudo apt-get install -y util-linux procps hostapd iproute2 iw haveged dnsmasq"
]

mark_2 = 0
for x in range(3):
    for command in commands_2:
        if os.system(command) != 0:
            print("Error running installation step 2")
            mark_2 = 1
    if mark_2 == 0:
        break

try:
    replace_num("/boot/config.txt", '#dtparam=i2c_arm=on','dtparam=i2c_arm=on\nstart_x=1\n')
except:
    print('Error updating boot config to enable i2c. Please try again.')



try:
    os.system('sudo touch //home/pi/startup.sh')
    with open("/home/pi/startup.sh",'w') as file_to_write:
        #you can choose how to control the robot
        file_to_write.write("#!/bin/sh\nsudo python3 " + thisPath + "/server/webServer.py")
#       file_to_write.write("#!/bin/sh\nsudo python3 " + thisPath + "/server/server.py")
except:
    pass


os.system('sudo chmod 777 //home/pi/startup.sh')

replace_num('/etc/rc.local','fi','fi\n//home/pi/startup.sh start')

try: #fix conflict with onboard Raspberry Pi audio
    os.system('sudo touch /etc/modprobe.d/snd-blacklist.conf')
    with open("/etc/modprobe.d/snd-blacklist.conf",'w') as file_to_write:
        file_to_write.write("blacklist snd_bcm2835")
except:
    pass

os.system("sudo cp -f //home/pi/Adeept_RaspTank/server/config.txt //etc/config.txt")


print('The program in Raspberry Pi has been installed, disconnected and restarted. \nYou can now power off the Raspberry Pi to install the camera and driver board (Robot HAT). \nAfter turning on again, the Raspberry Pi will automatically run the program to set the servos port signal to turn the servos to the middle position, which is convenient for mechanical assembly.')

if len(errors):
    print('errors encountered during install. The following commands exited non-zero\n')
    for error in errors:
        print(f'{error}\n')
    print('Restart required for some installations to take effect. Manually restart like "sudo reboot"')
else:
    print('restarting...')
    os.system("sudo reboot")
