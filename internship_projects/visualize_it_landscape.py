import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans 
import matplotlib.pyplot as plt

# Charger les données
data = pd.read_csv('./application_export.csv')

label_encoder = LabelEncoder()
data['application_encoded'] = label_encoder.fit_transform(data['application'])

# Construire un nouveau DataFrame avec les colonnes encodées
new_frame = data[['application_encoded', 'user_count']]

scaler = StandardScaler()
scaled_features = scaler.fit_transform(new_frame)

kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(scaled_features)

data['cluster'] = kmeans.labels_
print(data.head())

# Visualiser les clusters avec des labels
plt.figure(figsize=(12, 8))
scatter = plt.scatter(data['application_encoded'], data['user_count'], c=data['cluster'], cmap='viridis')
plt.xlabel('Application (encodée)')
plt.ylabel('Nombre d\'utilisateurs')
plt.title('Global view of software - Boxine GmbH')

# Ajouter des labels sur chaque point
for i, txt in enumerate(data['application']):
    plt.annotate(txt, (data['application_encoded'][i], data['user_count'][i]), fontsize=8, alpha=0.7)

# Extraire les valeurs numériques des labels
handles, labels = scatter.legend_elements()
numeric_labels = [label.replace('$\\mathdefault{', '').replace('}$', '') for label in labels]
plt.legend(handles, [f'Cluster {label}' for label in numeric_labels], title="Clusters")

plt.show()