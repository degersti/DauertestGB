from datetime import datetime
import time
import RPi.GPIO as GPIO

#--------------- SET-UP------------------------------
K1_pin = 17     #Forward / Backward
K2_pin = 27     #Set speed 2   m/s
K3_pin = 22     #Set speed 2.2 m/s
K4_pin = 10     #Set speed 2.3 m/s
K5_pin = 9      #Quittierung
K6_pin = 26     #Testausl.
Vorab_pin = 2   #Vorabschaltung ausgeloest?
Ueber_pin = 3   #Uebergeschw. ausgeloest?

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(K1_pin,GPIO.OUT)
GPIO.setup(K2_pin,GPIO.OUT)
GPIO.setup(K3_pin,GPIO.OUT)
GPIO.setup(K4_pin,GPIO.OUT)
GPIO.setup(K5_pin,GPIO.OUT)
GPIO.setup(K6_pin,GPIO.OUT)
GPIO.setup(Vorab_pin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(Ueber_pin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

K1_arr = [1,1,0,0,0,0,1,1,1,1,1,1,1]
K2_arr = [1,1,0,0,0,1,1,0,0,0,1,1,1]
K3_arr = [1,1,1,0,0,1,1,1,0,0,1,1,1]
K4_arr = [1,1,1,1,0,1,1,1,1,0,1,1,1]
K5_arr = [1,0,1,1,1,1,0,1,1,1,1,0,1]
K6_arr = [1,1,1,1,1,1,1,1,1,1,1,1,0]

delay_1 = [1 ,1,10,10,10,10,1,10,10,10,10,1,1]
delay_2 = [10,1,1 ,1 ,1 ,1 ,1,1 ,1 ,1 ,1 ,1,1]

now = datetime.now()
fileName = "protocol_" +  now.strftime("%Y%d%m_%H%M%S") + ".txt"
file = open(fileName, "w")
file.close
#--------------- CHECK STATUS OF GB
def survailance(strOut):
        #STATUS: "State of K1-K6"
        strOut = strOut + str(GPIO.input(K1_pin)) + ";"
        strOut = strOut + str(GPIO.input(K2_pin)) + ";"
        strOut = strOut + str(GPIO.input(K3_pin)) + ";"
        strOut = strOut + str(GPIO.input(K4_pin)) + ";"
        strOut = strOut + str(GPIO.input(K5_pin)) + ";"
        strOut = strOut + str(GPIO.input(K6_pin)) + ";"
        #STATUS: "Vorabschaltung"
        strOut = strOut + str(GPIO.input(Vorab_pin)) + ";"
        #STATUS: "Uebergeschwindigkeit"
        strOut = strOut + str(GPIO.input(Ueber_pin)) + ";"
        return strOut
#--------------- MAIN LOOP -------------------------
while 1:
        for i in range(13):
                # Set  outputs
                GPIO.output(K1_pin,K1_arr[i])
                GPIO.output(K2_pin,K2_arr[i])
                GPIO.output(K3_pin,K3_arr[i])
                GPIO.output(K4_pin,K4_arr[i])
                GPIO.output(K5_pin,K5_arr[i])
                GPIO.output(K6_pin,K6_arr[i])
                # Wait for the system to get to idle state
 # Wait for the system to get to idle state
                time.sleep(delay_1[i])
                # Check the state of the system
                now = datetime.now()
                strOut = now.strftime("%Y/%d/%m_%H:%M:%S") + ";"
                strOut = survailance(strOut)
                print (strOut)
                # Write the state to the logfile
                file = open(fileName, "a")
                file.write(strOut + "\n")
                file.close
                # Wait for next cycle
                time.sleep(delay_1[i])

# --------------- END PROGRAMM  ----------------------------
