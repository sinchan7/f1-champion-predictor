# ============================================
# Phase 3 & 4 - Model Code
# File: src/model.py
# ============================================

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# ------------------------------
# Phase 3: Training & Evaluation
# ------------------------------

def train_model(X_train, y_train):
    """
    Trains a RandomForestClassifier model.
    """
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    """
    Evaluates the model and prints performance metrics.
    """
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"✅ Accuracy: {acc:.2f}")
    print("📊 Classification Report:")
    print(classification_report(y_test, y_pred))

# ------------------------------
# Phase 4: Champion Prediction
# ------------------------------

def predict_champions(model, future_df, entity="driver"):
    """
    Predicts champions for future seasons using the trained model.
    Selects the entity with the highest predicted probability for each season.

    Parameters:
        model      : Trained sklearn model.
        future_df  : DataFrame with future season features.
        entity     : "driver" or "constructor" — the entity to predict.

    Returns:
        DataFrame with champion predictions per season.
    """
    df = future_df.copy()

    identity_cols = ["season", entity]

    # Ensure only the features used during training are included
    model_features = model.feature_names_in_
    X = df[model_features]

    # Predict probabilities
    df["champion_prob"] = model.predict_proba(X)[:, 1]

    # Select top candidate per season
    predictions = df.loc[df.groupby("season")["champion_prob"].idxmax()][["season", entity, "champion_prob"]]
    predictions = predictions.sort_values("season").reset_index(drop=True)

    return predictions
