from pymodbus.client.sync import ModbusTcpClient
import time
import socket

EV_IP = '192.168.4.70'

# TCP/IP EV connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5000)

# Modbus server connection
server_ip_address = '127.0.0.1'
server_port = 10502

client = ModbusTcpClient(server_ip_address, server_port)

print("[+]Info : Connection : " + str(client.connect()))

UNIT = 2

def checkCommands(option, value):
    if option == 0:
        return

    elif option == 1:
        changeValue('current', value)

    elif option == 2:
        changeValue('true_power', value)

    elif option == 3:
        changeValue('PF', value)

    elif option == 4:
        changeValue('CF', value)

    elif option == 5:
        changeMode('load_mode', value)

    elif option == 6:
        changeMode('bid_mode', value)

    elif option == 7:
        changeMode('factor_priority', value)

    elif option == 8:
        changeValue('currentA', value)

    elif option == 9:
        changeValue('currentB', value)

    elif option == 10:
        changeValue('currentC', value)

    elif option == 11:
        changeValue('PF_A', value)

    elif option == 12:
        changeValue('PF_B', value)

    elif option == 13:
        changeValue('PF_C', value)

    elif option == 14:
        changeValue('CF_A', value)

    elif option == 15:
        changeValue('CF_B', value)

    elif option == 16:
        changeValue('CF_C', value)

    elif option == 17:
        changeValue('true_powerA', value)

    elif option == 18:
        changeValue('true_powerB', value)

    elif option == 19:
        changeValue('true_powerC', value)

def changeValue(prop, value):
    # Lock out the touch screen
    s.send("SYST:RWL\n")

    # Select instrument
    s.send("INST:NSEL 1\n")

    # Turn on the output
    s.send("OUTP:ON\n")

    if prop == 'current':
        # Change current
        s.send("SOUR:CURRENT " + value + "\n")

    if prop == 'currentA':
        # Change current phase 1
        s.send("SOUR:CURRENT:APH " + value + "\n")

    if prop == 'currentB':
        # Change current phase 2
        s.send("SOUR:CURRENT:BPH " + value + "\n")

    if prop == 'currentC':
        # Change current phase 3
        s.send("SOUR:CURRENT:CPH " + value + "\n")

    if prop == 'true_power':
        # Change true power
        s.send("SOUR:POW " + value + "\n")

    if prop == 'true_powerA':
        # Change true power phase 1
        s.send("SOUR:POW:APH " + value + "\n")

    if prop == 'true_powerB':
        # Change true power phase 2
        s.send("SOUR:POW:BPH " + value + "\n")

    if prop == 'true_powerC':
        # Change true power phase 3
        s.send("SOUR:POW:CPH " + value + "\n")

    if prop == 'PF':
        # Change power factor
        s.send("SOUR:CURR:PF " + value + "\n")

    if prop == 'PF_A':
        # Change power factor phase 1
        s.send("SOUR:CURR:PF:APH " + value + "\n")

    if prop == 'PF_B':
        # Change power factor phase 2
        s.send("SOUR:CURR:PF:BPH " + value + "\n")

    if prop == 'PF_C':
        # Change power factor phase 3
        s.send("SOUR:CURR:PF:CPH " + value + "\n")

    if prop == 'CF':
        # Change crest factor
        s.send("SOUR:CURR:CF " + value + "\n")

    if prop == 'CF_A':
        # Change crest factor phase 1
        s.send("SOUR:CURR:CF:APH " + value + "\n")

    if prop == 'CF_B':
        # Change crest factor phase 2
        s.send("SOUR:CURR:CF:BPH " + value + "\n")

    if prop == 'CF_C':
        # Change crest factor phase 3
        s.send("SOUR:CURR:CF:CPH " + value + "\n")

    # Query for any existing errors
    s.send("SYST:ERR?\n")
    print(s.recv(1024))

    # Unlock out the touch screen
    s.send("SYST:LOC\n")

    s.close()

    client.write_register(0, 0, UNIT)

    return

def changeMode(factor, value):
    # Lock out the touch screen
    s.send("SYST:RWL\n")

    # Select instrument
    s.send("INST:NSEL 1\n")

    # Turn off the output
    s.send("OUTP:OFF\n")

    if factor == 'bid_mode':
        # Change bidirectional mode
        s.send("CONF:INST:BID " + value + "\n")

    if factor == 'load_mode':
        # Change load mode
        s.send("CONF:INST:LOAD:MODE " + value + "\n")

    if factor == 'factor_priority':
        # Change CF/PF priority
        s.send("SOUR:CURR:PRIO " + value + "\n")

    # Turn on the output
    s.send("OUTP:ON\n")

    # Query for any existing errors
    s.send("SYST:ERR?\n")
    print(s.recv(1024))

    # Unlock out the touch screen
    s.send("SYST:LOC\n")

    s.close()

    client.write_register(0, 0, UNIT)

    return
def checkMeasurements():
    s.connect((EV_IP, 5025))

    # Lock out the touch screen
    s.send("SYST:RWL\n")

    # Select instrument
    s.send("INST:NSEL 1\n")

    # Query load mode
    s.send("CONF:INST:LOAD:MODE?\n")
    load_mode = s.recv(1024).split("\n")
    print("Load mode: ", load_mode[0])
    time.sleep(2)
    client.write_register(6, load_mode[0], UNIT)

    # Query BID mode
    s.send("CONF:INST:BID?\n")
    bid_mode = s.recv(1024).split("\n")
    print("BID mode: ", bid_mode[0])
    time.sleep(2)
    client.write_register(7, bid_mode[0], UNIT)

    # Query CF/PF priority
    s.send("SOUR:CURR:PRIO?\n")
    priority = s.recv(1024).split("\n")
    print("CF/PF priority: ", priority[0])
    time.sleep(2)
    client.write_register(8, priority[0], UNIT)

    # Query voltage level
    s.send("VOLT?\n")
    voltage = s.recv(1024).split("\n")
    print("Voltage: ", voltage[0])
    time.sleep(2)
    client.write_register(12, voltage[0], UNIT)

    # Query current level
    s.send("SOUR:CURR?\n")
    current = s.recv(1024).split("\n")
    print("Current: ", current[0])
    time.sleep(2)
    client.write_register(2, current[0], UNIT)

    # Query current level phase 1
    s.send("SOUR:CURR:APH?\n")
    current_a = s.recv(1024).split("\n")
    print("Current APH: ", current_a[0])
    time.sleep(2)
    client.write_register(9, current_a[0], UNIT)

    # Query current level phase 2
    s.send("SOUR:CURR:BPH?\n")
    current_b = s.recv(1024).split("\n")
    print("Current BPH: ", current_b[0])
    time.sleep(2)
    client.write_register(10, current_b[0], UNIT)

    # Query current level phase 3
    s.send("SOUR:CURR:CPH?\n")
    current_c = s.recv(1024).split("\n")
    print("Current CPH: ", current_c[0])
    time.sleep(2)
    client.write_register(11, current_c[0], UNIT)

    # Query true power
    s.send("FETC:POW:TRUE?\n")
    true_power = s.recv(1024).split("\n")
    print("True power: ", true_power[0])
    client.write_register(3, true_power[0], UNIT)

    # Query true power phase 1
    s.send("FETC:POW:TRUE:APH?\n")
    true_power_a = s.recv(1024).split("\n")
    print("True power APH: ", true_power_a[0])
    time.sleep(2)
    client.write_register(16, true_power_a[0], UNIT)

    # Query true power phase 2
    s.send("FETC:POW:TRUE:BPH?\n")
    true_power_b = s.recv(1024).split("\n")
    print("True power BPH: ", true_power_b[0])
    time.sleep(2)
    client.write_register(17, true_power_b[0], UNIT)

    # Query true power phase 3
    s.send("FETC:POW:TRUE:CPH?\n")
    true_power_c = s.recv(1024).split("\n")
    print("True power CPH: ", true_power_c[0])
    time.sleep(2)
    client.write_register(18, true_power_c[0], UNIT)

    # Query apparent power
    s.send("FETC:POW:APP?\n")
    apparent_power = s.recv(1024).split("\n")
    print("Apparent power: ", apparent_power[0])
    time.sleep(2)
    client.write_register(15, apparent_power[0], UNIT)

    # Query apparent power phase 1
    s.send("FETC:POW:APP:APH?\n")
    apparent_power_a = s.recv(1024).split("\n")
    print("Apparent power APH: ", apparent_power_a[0])
    time.sleep(2)
    client.write_register(25, apparent_power_a[0], UNIT)

    # Query apparent power phase 2
    s.send("FETC:POW:APP:BPH?\n")
    apparent_power_b = s.recv(1024).split("\n")
    print("Apparent power BPH: ", apparent_power_b[0])
    time.sleep(2)
    client.write_register(26, apparent_power_b[0], UNIT)

    # Query apparent power phase 3
    s.send("FETC:POW:APP:CPH?\n")
    apparent_power_c = s.recv(1024).split("\n")
    print("Apparent power CPH: ", apparent_power_c[0])
    time.sleep(2)
    client.write_register(27, apparent_power_c[0], UNIT)

    # Query power factor
    s.send("SOUR:CURR:PF?\n")
    power_factor = s.recv(1024).split("\n")
    print("Power factor: ", power_factor[0])
    time.sleep(2)
    client.write_register(4, power_factor[0], UNIT)

    # Query power factor phase 1
    s.send("SOUR:CURR:PF:APH?\n")
    power_factor_a = s.recv(1024).split("\n")
    print("Power factor APH: ", power_factor_a[0])
    time.sleep(2)
    client.write_register(19, power_factor_a[0], UNIT)

    # Query power factor phase 2
    s.send("SOUR:CURR:PF:BPH?\n")
    power_factor_b = s.recv(1024).split("\n")
    print("Power factor BPH: ", power_factor_b[0])
    time.sleep(2)
    client.write_register(20, power_factor_b[0], UNIT)

    # Query power factor phase 3
    s.send("SOUR:CURR:PF:CPH?\n")
    power_factor_c = s.recv(1024).split("\n")
    print("Power factor CPH: ", power_factor_c[0])
    time.sleep(2)
    client.write_register(21, power_factor_c[0], UNIT)

    # Query crest factor
    s.send("SOUR:CURR:CF?\n")
    crest_factor = s.recv(1024).split("\n")
    print("Crest factor: ", crest_factor[0])
    time.sleep(2)
    client.write_register(5, crest_factor[0], UNIT)

    # Query crest factor phase 1
    s.send("SOUR:CURR:CF:APH?\n")
    crest_factor_a = s.recv(1024).split("\n")
    print("Crest factor APH: ", crest_factor_a[0])
    time.sleep(2)
    client.write_register(22, crest_factor_a[0], UNIT)

    # Query crest factor phase 2
    s.send("SOUR:CURR:CF:BPH?\n")
    crest_factor_b = s.recv(1024).split("\n")
    print("Crest factor BPH: ", crest_factor_b[0])
    time.sleep(2)
    client.write_register(23, crest_factor_b[0], UNIT)

    # Query crest factor phase 3
    s.send("SOUR:CURR:CF:CPH?\n")
    crest_factor_c = s.recv(1024).split("\n")
    print("Crest factor CPH: ", crest_factor_c[0])
    time.sleep(2)
    client.write_register(24, crest_factor_c[0], UNIT)

    # Query frequency
    s.send("SOUR:FREQ?\n")
    frequency = s.recv(1024).split("\n")
    print("Frequency: ", frequency[0])
    time.sleep(2)
    client.write_register(13, frequency[0], UNIT)

    # Query for any existing errors
    s.send("SYST:ERR?\n")
    print(s.recv(1024))

    # Unlock out the touch screen
    s.send("SYST:LOC\n")

    s.close()

    return

while True:
    checkCommands()
    time.sleep(10)
    checkMeasurements()

