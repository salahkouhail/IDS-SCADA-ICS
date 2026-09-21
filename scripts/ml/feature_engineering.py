import pandas as pd

# Charger séparément les trois fichiers
normal = pd.read_csv('normal_traffic.csv')
malicious = pd.read_csv('malicious_traffic.csv')
replay = pd.read_csv('replay_traffic.csv')

normal['timestamp'] = pd.to_datetime(normal['timestamp'])
malicious['timestamp'] = pd.to_datetime(malicious['timestamp'])
replay['timestamp'] = pd.to_datetime(replay['timestamp'])

# Trier chacun individuellement
normal = normal.sort_values('timestamp').reset_index(drop=True)
malicious = malicious.sort_values('timestamp').reset_index(drop=True)
replay = replay.sort_values('timestamp').reset_index(drop=True)

# Calculer time_delta SÉPARÉMENT pour chaque dataset
normal['time_delta'] = normal['timestamp'].diff().dt.total_seconds().fillna(0)
normal.loc[normal['time_delta'] > 10, 'time_delta'] = 2.0
malicious['time_delta'] = malicious['timestamp'].diff().dt.total_seconds().fillna(0)
replay['time_delta'] = replay['timestamp'].diff().dt.total_seconds().fillna(0)

# Ajouter les labels
normal['label'] = 0
malicious['label'] = 1
replay['label'] = 1

# Renommer 'values' en 'value' dans normal pour cohérence
normal = normal.rename(columns={'values': 'value'})

# Garder les colonnes communes utiles
normal_clean = normal[['timestamp', 'function_code', 'address', 'device_id', 'time_delta', 'label']]
malicious_clean = malicious[['timestamp', 'function_code', 'address', 'device_id', 'time_delta', 'label']]
replay_clean = replay[['timestamp', 'function_code', 'address', 'device_id', 'time_delta', 'label']]

# Fusionner (SANS re-trier par timestamp global)
combined = pd.concat([normal_clean, malicious_clean, replay_clean], ignore_index=True)

print(combined.head(10))
print(f"\nStatistiques time_delta :")
print(combined.groupby('label')['time_delta'].describe())

combined.to_csv('final_dataset.csv', index=False)
print("\nFichier 'final_dataset.csv' créé avec succès !")
