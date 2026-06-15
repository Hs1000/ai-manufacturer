import joblib
import pandas as pd

from sklearn.ensemble import (
    RandomForestRegressor
)

from sklearn.preprocessing import (
    LabelEncoder
)


def train_forecast_model():

    df = pd.read_csv(
        "app/ml/forecast_training.csv"
    )

    lens_encoder = LabelEncoder()
    power_encoder = LabelEncoder()
    index_encoder = LabelEncoder()
    coating_encoder = LabelEncoder()

    df["lens_type"] = (
        lens_encoder.fit_transform(
            df["lens_type"]
        )
    )

    df["power"] = (
        power_encoder.fit_transform(
            df["power"]
        )
    )

    df["lens_index"] = (
        index_encoder.fit_transform(
            df["lens_index"]
        )
    )

    df["coating"] = (
        coating_encoder.fit_transform(
            df["coating"]
        )
    )

    X = df[
        [
            "lens_type",
            "power",
            "lens_index",
            "coating"
        ]
    ]

    y = df["quantity_used"]

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    model.fit(X, y)

    joblib.dump(
        model,
        "app/ml/forecast_model.pkl"
    )

    joblib.dump(
        lens_encoder,
        "app/ml/forecast_lens_encoder.pkl"
    )

    joblib.dump(
        power_encoder,
        "app/ml/forecast_power_encoder.pkl"
    )

    joblib.dump(
        index_encoder,
        "app/ml/forecast_index_encoder.pkl"
    )

    joblib.dump(
        coating_encoder,
        "app/ml/forecast_coating_encoder.pkl"
    )

    return len(df)


if __name__ == "__main__":

    print(
        train_forecast_model()
    )