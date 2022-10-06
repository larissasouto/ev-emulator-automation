from pymodbus.client.sync import ModbusTcpClient
import time
import socket

EV_IP = '192.168.4.70'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5000)
# s.connect((EV_IP, 5025))

# Modbus server connection
server_ip_address = '127.0.0.1'
server_port = 10502

client = ModbusTcpClient(server_ip_address, server_port)

print("[+]Info : Connection : " + str(client.connect()))

UNIT = 2

def checkMeasurement():
    s.connect((EV_IP, 5025))

    # Lock out the touch screen
    s.send("SYST:RWL\n")

    # Select instrument
    s.send("INST:NSEL 1\n")

    # Query load mode
    s.send("CONF:INST:LOAD:MODE?\n")
    load_mode = s.recv(1024).split("\n")
    print("Load mode: ", load_mode[0])
    client.write_register(6, load_mode[0], UNIT)

    # Query BID mode
    s.send("CONF:INST:BID?\n")
    bid_mode = s.recv(1024).split("\n")
    print("BID mode: ", bid_mode[0])
    client.write_register(7, bid_mode[0], UNIT)

    # Query CF/PF priority
    s.send("SOUR:CURR:PRIO?\n")
    priority = s.recv(1024).split("\n")
    print("CF/PF priority: ", priority[0])
    client.write_register(8, priority[0], UNIT)

    # Query voltage level
    s.send("VOLT?\n")
    voltage = s.recv(1024).split("\n")
    print("Voltage: ", voltage[0])
    client.write_register(12, voltage[0], UNIT)

    # Query current level
    s.send("SOUR:CURR?\n")
    current = s.recv(1024).split("\n")
    print("Current: ", current[0])
    client.write_register(2, current[0], UNIT)

    # Query current level phase 1
    s.send("SOUR:CURR:APH?\n")
    current_a = s.recv(1024).split("\n")
    print("Current APH: ", current_a[0])
    client.write_register(9, current_a[0], UNIT)

    # Query current level phase 2
    s.send("SOUR:CURR:BPH?\n")
    current_b = s.recv(1024).split("\n")
    print("Current BPH: ", current_b[0])
    client.write_register(10, current_b[0], UNIT)

    # Query current level phase 3
    s.send("SOUR:CURR:CPH?\n")
    current_c = s.recv(1024).split("\n")
    print("Current CPH: ", current_c[0])
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
    client.write_register(16, true_power_a[0], UNIT)

    # Query true power phase 2
    s.send("FETC:POW:TRUE:BPH?\n")
    true_power_b = s.recv(1024).split("\n")
    print("True power BPH: ", true_power_b[0])
    client.write_register(17, true_power_b[0], UNIT)

    # Query true power phase 3
    s.send("FETC:POW:TRUE:CPH?\n")
    true_power_c = s.recv(1024).split("\n")
    print("True power CPH: ", true_power_c[0])
    client.write_register(18, true_power_c[0], UNIT)

    # Query apparent power
    s.send("FETC:POW:APP?\n")
    apparent_power = s.recv(1024).split("\n")
    print("Apparent power: ", apparent_power[0])
    client.write_register(15, apparent_power[0], UNIT)

    # Query apparent power phase 1
    s.send("FETC:POW:APP:APH?\n")
    apparent_power_a = s.recv(1024).split("\n")
    print("Apparent power APH: ", apparent_power_a[0])
    client.write_register(25, apparent_power_a[0], UNIT)

    # Query apparent power phase 2
    s.send("FETC:POW:APP:BPH?\n")
    apparent_power_b = s.recv(1024).split("\n")
    print("Apparent power BPH: ", apparent_power_b[0])
    client.write_register(26, apparent_power_b[0], UNIT)

    # Query apparent power phase 3
    s.send("FETC:POW:APP:CPH?\n")
    apparent_power_c = s.recv(1024).split("\n")
    print("Apparent power CPH: ", apparent_power_c[0])
    client.write_register(27, apparent_power_c[0], UNIT)

    # Query power factor
    s.send("SOUR:CURR:PF?\n")
    power_factor = s.recv(1024).split("\n")
    print("Power factor: ", power_factor[0])
    client.write_register(4, power_factor[0], UNIT)

    # Query power factor phase 1
    s.send("SOUR:CURR:PF:APH?\n")
    power_factor_a = s.recv(1024).split("\n")
    print("Power factor APH: ", power_factor_a[0])
    client.write_register(19, power_factor_a[0], UNIT)

    # Query power factor phase 2
    s.send("SOUR:CURR:PF:BPH?\n")
    power_factor_b = s.recv(1024).split("\n")
    print("Power factor BPH: ", power_factor_b[0])
    client.write_register(20, power_factor_b[0], UNIT)

    # Query power factor phase 3
    s.send("SOUR:CURR:PF:CPH?\n")
    power_factor_c = s.recv(1024).split("\n")
    print("Power factor CPH: ", power_factor_c[0])
    client.write_register(21, power_factor_c[0], UNIT)

    # Query crest factor
    s.send("SOUR:CURR:CF?\n")
    crest_factor = s.recv(1024).split("\n")
    print("Crest factor: ", crest_factor[0])
    client.write_register(5, crest_factor[0], UNIT)

    # Query crest factor phase 1
    s.send("SOUR:CURR:CF:APH?\n")
    crest_factor_a = s.recv(1024).split("\n")
    print("Crest factor APH: ", crest_factor_a[0])
    client.write_register(22, crest_factor_a[0], UNIT)

    # Query crest factor phase 2
    s.send("SOUR:CURR:CF:BPH?\n")
    crest_factor_b = s.recv(1024).split("\n")
    print("Crest factor BPH: ", crest_factor_b[0])
    client.write_register(23, crest_factor_b[0], UNIT)

    # Query crest factor phase 3
    s.send("SOUR:CURR:CF:CPH?\n")
    crest_factor_c = s.recv(1024).split("\n")
    print("Crest factor CPH: ", crest_factor_c[0])
    client.write_register(24, crest_factor_c[0], UNIT)

    # Query frequency
    s.send("SOUR:FREQ?\n")
    frequency = s.recv(1024).split("\n")
    print("Frequency: ", frequency[0])
    client.write_register(13, frequency[0], UNIT)

    # Query for any existing errors
    s.send("SYST:ERR?\n")
    print(s.recv(1024))

    # Unlock out the touch screen
    s.send("SYST:LOC\n")

    s.close()

    return


def getValues():
    print("GETTING MEASUREMENTS")