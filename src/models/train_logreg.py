import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from src.config import TRAIN_PARQUET
from src.evaluation.metrics import compute_metrics

def main() -> None:
    df = pd.read_parquet(TRAIN_PARQUET)
    y = df["label"].astype(int).values
    X = df.drop(columns=["customer_id", "label"])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = Pipeline([
        ("scaler", StandardScaler(with_mean=True, with_std=True)),
        ("clf", LogisticRegression(max_iter=2000, n_jobs=None))
    ])

    model.fit(X_train, y_train)
    y_prob = model.predict_proba(X_test)[:, 1]

    metrics = compute_metrics(y_test, y_prob)
    print("Logistic Regression metrics:", metrics)

    # top coefficients
    clf = model.named_steps["clf"]
    coefs = pd.Series(clf.coef_[0], index=X.columns).sort_values(key=abs, ascending=False)
    print("\nTop coefficients (by abs value):")
    print(coefs.head(15))

if __name__ == "__main__":
    main()
