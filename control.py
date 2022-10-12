from pymodbus.client.sync import ModbusTcpClient
import time
import socket

EV_IP = '192.168.4.70'

# TCP/IP EV connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5000)
s.connect((EV_IP, 5025))

# Modbus server connection
server_ip_address = '192.168.4.18'
server_port = 10502

client = ModbusTcpClient(server_ip_address, server_port)

print("[+]Info : Connection : " + str(client.connect()))

UNIT = 2


def checkCommands():
    option_request = client.read_holding_registers(0, 1, unit=UNIT)
    option = option_request.registers[0]

    value_request = client.read_holding_registers(1, 1, unit=UNIT)
    value = value_request.registers[0]

    if option == 0:
        return

    elif option == 1:
        changeValue('current', value/100)

    elif option == 2:
        changeValue('true_power', value/1000)

    elif option == 3:
        changeValue('PF', value/100)

    elif option == 4:
        changeValue('CF', value/10000)

    elif option == 5:
        changeMode('load_mode', value)

    elif option == 6:
        changeMode('bid_mode', value)

    elif option == 7:
        changeMode('factor_priority', value)

    elif option == 8:
        changeValue('currentA', value/100)

    elif option == 9:
        changeValue('currentB', value/100)

    elif option == 10:
        changeValue('currentC', value/100)

    elif option == 11:
        changeValue('PF_A', value/100)

    elif option == 12:
        changeValue('PF_B', value/100)

    elif option == 13:
        changeValue('PF_C', value/100)

    elif option == 14:
        changeValue('CF_A', value/10000)

    elif option == 15:
        changeValue('CF_B', value/10000)

    elif option == 16:
        changeValue('CF_C', value/10000)

    elif option == 17:
        changeValue('true_powerA', value/1000)

    elif option == 18:
        changeValue('true_powerB', value/1000)

    elif option == 19:
        changeValue('true_powerC', value/1000)


def changeValue(prop, value):
    # Lock out the touch screen
    s.send("SYST:RWL\n")

    # Select instrument
    s.send("INST:NSEL 1\n")

    # Turn on the output
    s.send("OUTP:ON\n")

    if prop == 'current':
        # Change current
        s.send("SOUR:CURRENT " + str(value) + "\n")

    if prop == 'currentA':
        # Change current phase 1
        s.send("SOUR:CURRENT:APH " + str(value) + "\n")

    if prop == 'currentB':
        # Change current phase 2
        s.send("SOUR:CURRENT:BPH " + str(value) + "\n")

    if prop == 'currentC':
        # Change current phase 3
        s.send("SOUR:CURRENT:CPH " + str(value) + "\n")

    if prop == 'true_power':
        # Change true power
        s.send("SOUR:POW " + str(value) + "\n")

    if prop == 'true_powerA':
        # Change true power phase 1
        s.send("SOUR:POW:APH " + str(value) + "\n")

    if prop == 'true_powerB':
        # Change true power phase 2
        s.send("SOUR:POW:BPH " + str(value) + "\n")

    if prop == 'true_powerC':
        # Change true power phase 3
        s.send("SOUR:POW:CPH " + str(value) + "\n")

    if prop == 'PF':
        # Change power factor
        s.send("SOUR:CURR:PF " + str(value) + "\n")

    if prop == 'PF_A':
        # Change power factor phase 1
        s.send("SOUR:CURR:PF:APH " + str(value) + "\n")

    if prop == 'PF_B':
        # Change power factor phase 2
        s.send("SOUR:CURR:PF:BPH " + str(value) + "\n")

    if prop == 'PF_C':
        # Change power factor phase 3
        s.send("SOUR:CURR:PF:CPH " + str(value) + "\n")

    if prop == 'CF':
        # Change crest factor
        s.send("SOUR:CURR:CF " + str(value) + "\n")

    if prop == 'CF_A':
        # Change crest factor phase 1
        s.send("SOUR:CURR:CF:APH " + str(value) + "\n")

    if prop == 'CF_B':
        # Change crest factor phase 2
        s.send("SOUR:CURR:CF:BPH " + str(value) + "\n")

    if prop == 'CF_C':
        # Change crest factor phase 3
        s.send("SOUR:CURR:CF:CPH " + str(value) + "\n")

    # Query for any existing errors
    s.send("SYST:ERR?\n")
    print(s.recv(1024))

    # Unlock out the touch screen
    s.send("SYST:LOC\n")

    s.close()

    client.write_register(0, 0, unit=UNIT)

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
        s.send("CONF:INST:BID " + str(value) + "\n")

    if factor == 'load_mode':
        # Change load mode
        s.send("CONF:INST:LOAD:MODE " + str(value) + "\n")

    if factor == 'factor_priority':
        # Change CF/PF priority
        s.send("SOUR:CURR:PRIO " + str(value) + "\n")

    # Turn on the output
    s.send("OUTP:ON\n")

    # Query for any existing errors
    s.send("SYST:ERR?\n")
    print(s.recv(1024))

    # Unlock out the touch screen
    s.send("SYST:LOC\n")

    #s.close()

    client.write_register(0, 0, unit=UNIT)

    return


def checkMeasurements():
    print("CHECKING MEASUREMENTS!")
    #s.connect((EV_IP, 5025))

    # Lock out the touch screen
    s.send("SYST:RWL\n")

    # Select instrument
    s.send("INST:NSEL 1\n")

    # Query load mode
    s.send("CONF:INST:LOAD:MODE?\n")
    response = s.recv(1024)
    load_mode_str = response.split('\n')

    if load_mode_str == 'NORM':
        load_mode = 0
    elif load_mode_str == 'CR':
        load_mode = 1
    elif load_mode_str == 'RL':
        load_mode = 2

    print("Load mode: ", load_mode_str)
    time.sleep(2)
    client.write_register(6, load_mode, UNIT)

    # Query BID mode
    s.send("CONF:INST:BID?\n")
    response = s.recv(1024)
    bid_mode = response.split('\n')
    print("BID mode: ", int(bid_mode[0]))
    time.sleep(2)
    client.write_register(7, int(bid_mode[0]), unit=UNIT)

    # Query CF/PF priority
    s.send("SOUR:CURR:PRIO?\n")
    response = s.recv(1024)
    priority = response.split('\n')
    print("CF/PF priority: ", int(priority[0]))
    time.sleep(2)
    client.write_register(8, int(priority[0]), unit=UNIT)

    # Query voltage level
    s.send("FETC:VOLT?\n")
    response = s.recv(1024)
    voltage = response.split('\n')
    scaled_value = int(voltage) * 1000
    print("Voltage: ", scaled_value)
    time.sleep(2)
    client.write_register(12, scaled_value, unit=UNIT)

    # Query current level
    s.send("SOUR:CURR?\n")
    response = s.recv(1024)
    current = response.split('\n')
    scaled_value = int(current) * 100
    print("Current: ", scaled_value)
    time.sleep(2)
    client.write_register(2, scaled_value, unit=UNIT)

    # Query current level phase 1
    s.send("SOUR:CURR:APH?\n")
    response = s.recv(1024)
    current_a = response.split('\n')
    scaled_value = int(current_a) * 100
    print("Current APH: ", scaled_value)
    time.sleep(2)
    client.write_register(9, scaled_value, unit=UNIT)

    # Query current level phase 2
    s.send("SOUR:CURR:BPH?\n")
    response = s.recv(1024)
    current_b = response.split('\n')
    scaled_value = int(current_b) * 100
    print("Current BPH: ", scaled_value)
    time.sleep(2)
    client.write_register(10, scaled_value, unit=UNIT)

    # Query current level phase 3
    s.send("SOUR:CURR:CPH?\n")
    response = s.recv(1024)
    current_c = response.split('\n')
    scaled_value = int(current_c) * 100
    print("Current CPH: ", scaled_value)
    time.sleep(2)
    client.write_register(11, scaled_value, unit=UNIT)

    # Query true power
    s.send("FETC:POW:TRUE?\n")
    response = s.recv(1024)
    true_power = response.split('\n')
    scaled_value = int(true_power) * 1000
    print("True power: ", scaled_value)
    client.write_register(3, scaled_value, unit=UNIT)

    # Query true power phase 1
    s.send("FETC:POW:TRUE:APH?\n")
    response = s.recv(1024)
    true_power_a = response.split('\n')
    scaled_value = int(true_power_a) * 1000
    print("True power APH: ", scaled_value)
    time.sleep(2)
    client.write_register(16, scaled_value, unit=UNIT)

    # Query true power phase 2
    s.send("FETC:POW:TRUE:BPH?\n")
    response = s.recv(1024)
    true_power_b = response.split('\n')
    scaled_value = int(true_power_b) * 1000
    print("True power BPH: ", scaled_value)
    time.sleep(2)
    client.write_register(17, scaled_value, unit=UNIT)

    # Query true power phase 3
    s.send("FETC:POW:TRUE:CPH?\n")
    response = s.recv(1024)
    true_power_c = response.split('\n')
    scaled_value = int(true_power_c) * 1000
    print("True power CPH: ", scaled_value)
    time.sleep(2)
    client.write_register(18, scaled_value, unit=UNIT)

    # Query apparent power
    s.send("FETC:POW:APP?\n")
    response = s.recv(1024)
    apparent_power = response.split('\n')
    scaled_value = int(apparent_power) * 1000
    print("Apparent power: ", scaled_value)
    time.sleep(2)
    client.write_register(15, scaled_value, unit=UNIT)

    # Query apparent power phase 1
    s.send("FETC:POW:APP:APH?\n")
    response = s.recv(1024)
    apparent_power_a = response.split('\n')
    scaled_value = int(apparent_power_a) * 1000
    print("Apparent power APH: ", scaled_value)
    time.sleep(2)
    client.write_register(25, scaled_value, unit=UNIT)

    # Query apparent power phase 2
    s.send("FETC:POW:APP:BPH?\n")
    response = s.recv(1024)
    apparent_power = response.split('\n')
    scaled_value = int(apparent_power_b) * 1000
    print("Apparent power BPH: ", scaled_value)
    time.sleep(2)
    client.write_register(26, scaled_value, unit=UNIT)

    # Query apparent power phase 3
    s.send("FETC:POW:APP:CPH?\n")
    response = s.recv(1024)
    apparent_power_c = response.split('\n')
    scaled_value = int(apparent_power_c) * 1000
    print("Apparent power: ", scaled_value)
    time.sleep(2)
    client.write_register(27, scaled_value, unit=UNIT)

    # Query power factor
    s.send("SOUR:CURR:PF?\n")
    response = s.recv(1024)
    power_factor = response.split('\n')
    scaled_value = int(power_factor) * 100
    print("Power factor: ", scaled_value)
    time.sleep(2)
    client.write_register(4, scaled_value, unit=UNIT)

    # Query power factor phase 1
    s.send("SOUR:CURR:PF:APH?\n")
    response = s.recv(1024)
    power_factor_a = response.split('\n')
    scaled_value = int(power_factor_a) * 100
    print("Power factor APH: ", scaled_value)
    time.sleep(2)
    client.write_register(19, scaled_value, unit=UNIT)

    # Query power factor phase 2
    s.send("SOUR:CURR:PF:BPH?\n")
    response = s.recv(1024)
    power_factor_b = response.split('\n')
    scaled_value = int(power_factor_b) * 100
    print("Power factor BPH: ", scaled_value)
    time.sleep(2)
    client.write_register(20, scaled_value, unit=UNIT)

    # Query power factor phase 3
    s.send("SOUR:CURR:PF:CPH?\n")
    response = s.recv(1024)
    power_factor_c = response.split('\n')
    scaled_value = int(power_factor_c) * 100
    print("Power factor CPH: ", scaled_value)
    time.sleep(2)
    client.write_register(21, scaled_value, unit=UNIT)

    # Query crest factor
    s.send("SOUR:CURR:CF?\n")
    response = s.recv(1024)
    crest_factor = response.split('\n')
    scaled_value = int(crest_factor) * 10000
    print("Crest factor: ", scaled_value)
    time.sleep(2)
    client.write_register(5, scaled_value, unit=UNIT)

    # Query crest factor phase 1
    s.send("SOUR:CURR:CF:APH?\n")
    response = s.recv(1024)
    crest_factor_a = response.split('\n')
    scaled_value = int(crest_factor_a) * 10000
    print("Crest factor APH: ", scaled_value)
    time.sleep(2)
    client.write_register(22, scaled_value, unit=UNIT)

    # Query crest factor phase 2
    s.send("SOUR:CURR:CF:BPH?\n")
    response = s.recv(1024)
    crest_factor_b = response.split('\n')
    scaled_value = int(crest_factor_b) * 10000
    print("Crest factor BPH: ", scaled_value)
    time.sleep(2)
    client.write_register(23, scaled_value, unit=UNIT)

    # Query crest factor phase 3
    s.send("SOUR:CURR:CF:CPH?\n")
    response = s.recv(1024)
    crest_factor_c = response.split('\n')
    scaled_value = int(crest_factor_c) * 10000
    print("Crest factor CPH: ", scaled_value)
    time.sleep(2)
    client.write_register(24, scaled_value, unit=UNIT)

    # Query frequency
    s.send("SOUR:FREQ?\n")
    response = s.recv(1024)
    frequency = response.split('\n')
    print("Frequency: ", int(frequency[0]))
    time.sleep(2)
    client.write_register(13, int(frequency[0]), unit=UNIT)

    # Query for any existing errors
    s.send("SYST:ERR?\n")
    print(s.recv(1024))

    # Unlock out the touch screen
    s.send("SYST:LOC\n")

    # s.close()

    return


while True:
    control_state = client.read_coils(0, 1, unit=UNIT)
    print("coil zero", control_state.bits[0])
    if control_state.bits[0] == True:
        checkCommands()
    # time.sleep(10)

    checkMeasurements()
