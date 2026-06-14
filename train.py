import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import pickle

print("Initializing Optimized 7-Feature Pipeline...")

# 1. Load the dataset file
df = pd.read_csv('DrDoS_DNS.csv')

# 2. FEATURE SELECTION: The exact 7 columns you requested + the label
optimized_columns = [
    'flow_duration', 
    'total_forward_packets', 
    'total_backward_packets',
    'forward_iat_mean',
    'backward_iat_mean',
    'flow_packets_per_seconds',
    'flow_bytes_per_seconds',
    'label'
]

# Filter the dataframe to just these 8 columns (7 features + 1 label)
df = df[optimized_columns]
df.columns = df.columns.str.strip()

# 3. Clean the data
df = df.replace([np.inf, -np.inf], np.nan).dropna()

# 4. Encode label (0 = Benign/Safe, 1 = Attack)
df['label'] = df['label'].apply(lambda x: 0 if 'benign' in str(x).lower() else 1)

X = df.drop('label', axis=1)
y = df['label']

# 5. Split and Scale
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# 6. Train the Model on the 7 selected features
model = RandomForestClassifier(n_estimators=50, random_state=42, n_jobs=-1)
model.fit(X_train_scaled, y_train)

# 7. Save components
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

with open('features.pkl', 'wb') as f:
    pickle.dump(list(X.columns), f)

print("Success! model.pkl and scaler.pkl are now optimized for your 7 specific inputs.")