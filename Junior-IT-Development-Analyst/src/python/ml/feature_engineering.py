import pandas as pd
import numpy as np
from typing import Optional


class FeatureEngineer:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def create_time_features(self, date_column: str) -> "FeatureEngineer":
        self.df[date_column] = pd.to_datetime(self.df[date_column])
        self.df["ano"] = self.df[date_column].dt.year
        self.df["mes"] = self.df[date_column].dt.month
        self.df["dia"] = self.df[date_column].dt.day
        self.df["dia_semana"] = self.df[date_column].dt.dayofweek
        self.df["hora"] = self.df[date_column].dt.hour
        self.df["fim_semana"] = self.df["dia_semana"].isin([5, 6]).astype(int)
        self.df["trimestre"] = self.df[date_column].dt.quarter
        self.df["safra"] = self.df["mes"].apply(
            lambda m: 1 if m in [3, 4, 5, 6, 7] else 0
        )
        return self

    def create_lag_features(self, target_column: str, lags: list[int]) -> "FeatureEngineer":
        for lag in lags:
            self.df[f"{target_column}_lag_{lag}"] = self.df[target_column].shift(lag)
        return self

    def create_rolling_features(self, target_column: str, windows: list[int]) -> "FeatureEngineer":
        for w in windows:
            self.df[f"{target_column}_rolling_mean_{w}"] = (
                self.df[target_column].rolling(w).mean()
            )
            self.df[f"{target_column}_rolling_std_{w}"] = (
                self.df[target_column].rolling(w).std()
            )
        return self

    def create_aggregate_features(
        self, group_column: str, target_column: str, aggs: Optional[list[str]] = None
    ) -> "FeatureEngineer":
        if aggs is None:
            aggs = ["mean", "std", "min", "max", "count"]
        group_stats = self.df.groupby(group_column)[target_column].agg(aggs)
        group_stats.columns = [f"{target_column}_group_{agg}" for agg in aggs]
        self.df = self.df.merge(group_stats, on=group_column, how="left")
        return self

    def encode_categorical(self, columns: list[str], method: str = "onehot") -> "FeatureEngineer":
        if method == "onehot":
            self.df = pd.get_dummies(self.df, columns=columns, drop_first=True)
        elif method == "label":
            for col in columns:
                self.df[f"{col}_encoded"] = pd.factorize(self.df[col])[0]
        return self

    def create_interaction(self, col1: str, col2: str) -> "FeatureEngineer":
        self.df[f"{col1}_x_{col2}"] = self.df[col1] * self.df[col2]
        return self

    def get_features(self) -> pd.DataFrame:
        return self.df


def example_pipeline():
    rng = np.random.default_rng(42)
    df = pd.DataFrame({
        "data": pd.date_range("2024-01-01", periods=365, freq="D"),
        "producao": rng.integers(80, 120, 365) + rng.normal(0, 5, 365).round(),
        "turno": rng.choice(["manha", "tarde", "noite"], 365),
        "maquina": rng.choice(["M-A", "M-B", "M-C"], 365),
        "temperatura": rng.normal(75, 10, 365).round(1),
    })

    fe = FeatureEngineer(df)
    fe.create_time_features("data")
    fe.create_lag_features("producao", [1, 7, 30])
    fe.create_rolling_features("producao", [7, 30])
    fe.create_aggregate_features("maquina", "producao")
    fe.encode_categorical(["turno"], "onehot")
    fe.create_interaction("temperatura", "producao_lag_1")

    return fe.get_features()


if __name__ == "__main__":
    result = example_pipeline()
    print(f"Features geradas: {result.shape[1]}")
    print(f"Linhas: {result.shape[0]}")
    print("Colunas:", list(result.columns))
