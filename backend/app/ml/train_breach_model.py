import joblib
import pandas as pd

from sklearn.ensemble import (
    RandomForestClassifier
)

from sklearn.preprocessing import (
    LabelEncoder
)


def train_model():

    df = pd.read_csv(
        "app/ml/training_data.csv"
    )

    lens_encoder = LabelEncoder()
    status_encoder = LabelEncoder()

    df["lens_type"] = (
        lens_encoder.fit_transform(
            df["lens_type"]
        )
    )

    df["status"] = (
        status_encoder.fit_transform(
            df["status"]
        )
    )

    X = df[
        [
            "lens_type",
            "status",
            "elapsed_hours"
        ]
    ]

    y = df["breached"]

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X, y)

    joblib.dump(
        model,
        "app/ml/breach_model.pkl"
    )

    joblib.dump(
        lens_encoder,
        "app/ml/lens_encoder.pkl"
    )

    joblib.dump(
        status_encoder,
        "app/ml/status_encoder.pkl"
    )

    return {
        "rows": len(df)
    }


if __name__ == "__main__":
    print(
        train_model()
    )