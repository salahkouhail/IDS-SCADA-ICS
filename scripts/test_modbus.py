from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient('127.0.0.1', port=502)
client.connect()

print("Connexion établie, envoi de la requête...")

# Lecture de 8 registers à partir de l'adresse 40001, sur le device ID 2
result = client.read_holding_registers(address=40001, count=8, device_id=2)

if result.isError():
    print("Erreur:", result)
else:
    print("Réponse reçue !")
    print("Valeurs des registers:", result.registers)

client.close()
