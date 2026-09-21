from pymodbus.client import ModbusTcpClient
import time
import csv
from datetime import datetime

csv_file = 'normal_traffic.csv'

with open(csv_file, mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['timestamp', 'function_code', 'address', 'device_id', 'values', 'status'])
print("Début de la collecte de trafic normal...")
print("Appuie sur Ctrl+C pour arrêter.\n")

count = 0
try:
    while True:
        client = ModbusTcpClient('127.0.0.1', port=502)
        client.connect()

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        result = client.read_holding_registers(address=40001, count=8, device_id=2)

        if result.isError():
            status = 'error'
            values = []
        else:
            status = 'success'
            values = result.registers

        with open(csv_file, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, 3, 40001, 2, values, status])

        count += 1
        print(f"[{count}] {timestamp} - Requête envoyée - Status: {status}")

        client.close()
        time.sleep(2)

except KeyboardInterrupt:
    print(f"\nCollecte arrêtée. {count} requêtes enregistrées dans '{csv_file}'.")
