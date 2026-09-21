from pymodbus.client import ModbusTcpClient
import time
import csv
from datetime import datetime
import random

target_ip = '192.168.37.137'
csv_file = 'malicious_traffic.csv'

with open(csv_file, mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['timestamp', 'function_code', 'address', 'device_id', 'value', 'status'])

print("Début de la collecte de trafic malveillant...")
print("Ctrl+C pour arrêter.\n")

count = 0
try:
    while True:
        client = ModbusTcpClient(target_ip, port=502)
        client.connect()

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        random_value = random.randint(1000, 9999)

        result = client.write_register(address=40001, value=random_value, device_id=2)

        status = 'error' if result.isError() else 'success'

        with open(csv_file, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, 6, 40001, 2, random_value, status])

        count += 1
        print(f"[{count}] {timestamp} - Write value={random_value} - Status: {status}")

        client.close()
        time.sleep(0.5)

except KeyboardInterrupt:
    print(f"\nCollecte arrêtée. {count} requêtes enregistrées dans '{csv_file}'.")
