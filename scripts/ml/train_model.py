import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

# Charger le dataset
df = pd.read_csv('final_dataset.csv')

# Features (X) et Label (y)
X = df[['function_code', 'address', 'device_id', 'time_delta']]
y = df['label']

# Split 80% train / 20% test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42,stratify=y)

print(f"Training set: {len(X_train)} lignes")
print(f"Test set: {len(X_test)} lignes\n")

# Créer et entraîner le modèle
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Prédictions sur le test set
y_pred = model.predict(X_test)

# Évaluation
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy*100:.2f}%\n")
print("Rapport de classification :")
print(classification_report(y_test,y_pred,labels=[0, 1],target_names=['Normal', 'Malicious']))
print("Matrice de confusion :")
print(confusion_matrix(y_test, y_pred))

# Sauvegarder le modèle
joblib.dump(model, 'ids_model.pkl')
print("\nModèle sauvegardé sous 'ids_model.pkl'")
