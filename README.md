# 🛡️ IDS Intelligent pour Protocoles Industriels (SCADA/ICS)

Système de détection d'intrusion combinant Machine Learning et IA Générative
pour la détection et l'explication d'anomalies sur le protocole Modbus.

**Projet de Stage** — Groupe OCP, Complexe de Jorf Lasfar (2025/2026)

## ⚠️ Avertissement

Ce projet est réalisé dans un cadre strictement académique et pédagogique.
Les scripts d'attaque inclus ciblent exclusivement un environnement de
simulation isolé (Conpot, machines virtuelles locales) et ne doivent en
aucun cas être utilisés contre des systèmes réels sans autorisation
explicite. L'auteur décline toute responsabilité en cas d'usage détourné.

## Architecture

1. **Simulation** : Conpot (PLC virtualisé) via Docker
2. **Génération de trafic** : SCADA légitime + attaques (Kali Linux)
3. **Capture** : Wireshark, pymodbus
4. **Détection** : Random Forest (scikit-learn) — 100% accuracy
5. **Explication** : Ollama (llama3.2, local)
6. **Supervision** : Dashboard Streamlit (style SOC)

## 📊 Résultats

- 3 432 requêtes collectées (508 normales, 2 924 malveillantes)
- 2 scénarios d'attaque : écriture non autorisée + rejeu
- Précision du modèle : 100%

## 🛠️ Stack technique

Docker · Python · pymodbus · scikit-learn · Ollama · Streamlit · Wireshark


## 🔧 Reproduction complète de l'expérience

Pour reproduire l'ensemble du pipeline (Conpot, attaques, entraînement, IA générative) :

\`\`\`bash
# 1. Environnement de simulation
docker pull honeynet/conpot
docker run -d --name conpot_ics -p 502:5020 -p 161:161/udp honeynet/conpot

# 2. Dépendances
pip install -r requirements.txt

# 3. Collecte des données
python3 scripts/collection/collect_normal_traffic.py
python3 scripts/attacks/attack_write.py      # depuis une machine attaquante (Kali)
python3 scripts/collection/collect_attack_traffic.py
python3 scripts/attacks/attack_replay.py

# 4. Entraînement du modèle
python3 scripts/ml/prepare_data.py
python3 scripts/ml/feature_engineering.py
python3 scripts/ml/train_model.py

# 5. IA Générative (nécessite Ollama installé localement)
# https://ollama.com
ollama pull llama3.2
python3 scripts/ai/generate_alert.py

# 6. Dashboard
streamlit run dashboard/dashboard.py
\`\`\`

## 👤 Auteur

**Salah-Eddine Kouhail** — Informatique et Réseaux, option Cybersécurité et Infrastructures Réseaux — 
École Marocaine des Sciences de l'Ingénieur (EMSI)

[LinkedIn](https://www.linkedin.com/in/salah-eddine-kouhail-64126328a/)
