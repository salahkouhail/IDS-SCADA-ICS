import pandas as pd

# Charger les trois fichiers
normal = pd.read_csv('normal_traffic.csv')
malicious = pd.read_csv('malicious_traffic.csv')
replay = pd.read_csv('replay_traffic.csv')

# Ajouter une colonne "label" : 0 = normal, 1 = malicious (write + replay)
normal['label'] = 0
malicious['label'] = 1
replay['label'] = 1

# Renommer 'values' en 'value' dans normal pour correspondre
normal = normal.rename(columns={'values': 'value'})

# Garder seulement les colonnes communes utiles
normal_clean = normal[['timestamp', 'function_code', 'address', 'device_id', 'label']]
malicious_clean = malicious[['timestamp', 'function_code', 'address', 'device_id', 'label']]
replay_clean = replay[['timestamp', 'function_code', 'address', 'device_id', 'label']]

# Fusionner les trois datasets
combined = pd.concat([normal_clean, malicious_clean, replay_clean], ignore_index=True)

# Convertir le timestamp en datetime
combined['timestamp'] = pd.to_datetime(combined['timestamp'])

# Afficher un résumé
print("Aperçu du dataset combiné :")
print(combined.head(10))
print(f"\nTotal de lignes : {len(combined)}")
print(f"Normal (label=0) : {len(combined[combined['label']==0])}")
print(f"Malicious (label=1) : {len(combined[combined['label']==1])}")

# Sauvegarder
combined.to_csv('combined_dataset.csv', index=False)
print("\nFichier 'combined_dataset.csv' créé avec succès !")
