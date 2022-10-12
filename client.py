from pymodbus.client.sync import ModbusTcpClient

UNIT = 3

client = ModbusTcpClient('192.168.4.72', 10502)

client.write_coil(0, True)  # turn control on/off
client.write_register(0, 5)  # option
client.write_register(1, 5000)  # value to set

value_request = client.read_holding_registers(2, 26, unit=UNIT)
value = value_request.registers[0]

print("Current", value_request.registers[0])  # HR2
print("True Power", value_request.registers[1])  # HR3
print("Power Factor", value_request.registers[2])  # HR4
print("Crest Factor", value_request.registers[3])  # HR5
print("Load Mode", value_request.registers[4])  # HR6
print("Bidirectional Mode", value_request.registers[5])  # HR7
print("CF/PF priority", value_request.registers[6])  # HR8
print("Phase 1 Current", value_request.registers[7])  # HR9
print("Phase 2 Current", value_request.registers[8])  # HR10
print("Phase 3 Current", value_request.registers[9])  # HR11
print("Voltage", value_request.registers[10])  # HR12
print("Frequency", value_request.registers[11])  # HR13
#print("Reactive Power", value_request.registers[12])  # HR14
print("Apparent Power", value_request.registers[13])  # HR15
print("Phase 1 True Power", value_request.registers[14])  # HR16
print("Phase 2 True Power", value_request.registers[15])  # HR17
print("Phase 3 True Power", value_request.registers[16])  # HR18
print("Phase 1 PF", value_request.registers[17])  # HR19
print("Phase 2 PF", value_request.registers[18])  # HR20
print("Phase 3 PF", value_request.registers[19])  # HR21
print("Phase 1 CF", value_request.registers[20])  # HR22
print("Phase 2 CF", value_request.registers[21])  # HR23
print("Phase 3 CF", value_request.registers[22])  # HR24
print("Phase 1 Apparent Power", value_request.registers[23])  # HR25
print("Phase 2 Apparent Power", value_request.registers[24])  # HR26
print("Phase 3 Apparent Power", value_request.registers[25])  # HR27

client.close()
