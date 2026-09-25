import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

# 1. Load your dataset
df = pd.read_csv("Loan_default.csv")

# 2. Separate features and target
X = df.drop("Default", axis=1)
y = df["Default"]

# 3. Convert categorical columns exactly like the notebook
categorical_cols = X.select_dtypes(include="object").columns.tolist()
X = pd.get_dummies(
    X,
    columns=categorical_cols,
    drop_first=True,
    dtype=int
)

# 4. Same train/test split used in the notebook
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# 5. Create the scaler used by the notebook
sc = StandardScaler()
sc.fit(X_train)

# 6. Train the tuned Random Forest from the notebook
best_model = RandomForestClassifier(
    n_estimators=100,
    max_depth=20,
    min_samples_split=5,
    random_state=42,
    n_jobs=-1
)

best_model.fit(X_train, y_train)

# 7. Save the three artifacts
joblib.dump(best_model, "loan_default_model.pkl")
joblib.dump(sc, "loan_default_scaler.pkl")
joblib.dump(X_train.columns.tolist(), "loan_default_features.pkl")

print("SUCCESS!")
print("Created:")
print("  loan_default_model.pkl")
print("  loan_default_scaler.pkl")
print("  loan_default_features.pkl")
print()
print("Feature count:", len(X_train.columns))
print("Model:", best_model)
