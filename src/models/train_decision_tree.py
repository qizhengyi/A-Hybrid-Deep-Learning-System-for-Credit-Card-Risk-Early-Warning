import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from src.config import TRAIN_PARQUET
from src.evaluation.metrics import compute_metrics

def main() -> None:
    df = pd.read_parquet(TRAIN_PARQUET)
    y = df["label"].astype(int).values
    X = df.drop(columns=["customer_id", "label"])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    clf = DecisionTreeClassifier(
        max_depth=6,
        min_samples_leaf=200,
        random_state=42
    )
    clf.fit(X_train, y_train)
    y_prob = clf.predict_proba(X_test)[:, 1]

    metrics = compute_metrics(y_test, y_prob)
    print("Decision Tree metrics:", metrics)

    importances = pd.Series(clf.feature_importances_, index=X.columns).sort_values(ascending=False)
    print("\nTop feature importances:")
    print(importances.head(15))

if __name__ == "__main__":
    main()
