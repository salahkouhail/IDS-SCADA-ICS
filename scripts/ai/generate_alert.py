import joblib
import pandas as pd
import subprocess

# Charger le modèle ML
model = joblib.load('ids_model.pkl')

# Exemple : nouvelle requête détectée (simulée ici, à remplacer par une vraie requête capturée)
new_request = pd.DataFrame([{
    'function_code': 6,
    'address': 40001,
    'device_id': 2,
    'time_delta': 0.5
}])

# Prédiction avec le modèle ML
prediction = model.predict(new_request)[0]

if prediction == 1:
    print("⚠️  ALERTE : Requête suspecte détectée par le modèle ML !\n")

    # Construire le prompt pour Ollama
    prompt = f"""Tu es un expert en cybersécurité industrielle (SCADA/ICS/Modbus).

Une alerte a été détectée par un système IDS basé sur du Machine Learning :

- Function Code : {new_request['function_code'].values[0]} (6 = Write Register, écriture)
- Adresse mémoire ciblée : {new_request['address'].values[0]}
- ID de l'appareil (device_id) : {new_request['device_id'].values[0]}
- Intervalle entre requêtes : {new_request['time_delta'].values[0]} secondes (anormalement rapide)
- Classification du modèle ML : MALICIOUS (comportement suspect)

Explique en langage clair et accessible :
1. Ce qui s'est probablement passé
2. Le niveau de gravité (faible/moyen/élevé)
3. Une action recommandée immédiate

Réponds en français, de façon concise (5-6 lignes maximum)."""

    print("Envoi de l'alerte à Ollama pour analyse...\n")

    # Appeler Ollama avec le prompt
    result = subprocess.run(
        ['ollama', 'run', 'llama3.2', prompt],
        capture_output=True,
        text=True
    )

    print("="*60)
    print("EXPLICATION GÉNÉRÉE PAR L'IA (Ollama) :")
    print("="*60)
    print(result.stdout)
    print("="*60)

else:
    print("✅ Requête normale, aucune alerte.")
