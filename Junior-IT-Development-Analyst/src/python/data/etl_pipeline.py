import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Literal, Optional


class ETLPipeline:
    def __init__(self, source_dir: Path, staging_dir: Optional[Path] = None):
        self.source_dir = Path(source_dir)
        self.staging_dir = Path(staging_dir) if staging_dir else source_dir / "staging"
        self.staging_dir.mkdir(parents=True, exist_ok=True)

    def extract(self, file_pattern: str = "*.csv") -> pd.DataFrame:
        files = list(self.source_dir.glob(file_pattern))
        if not files:
            raise FileNotFoundError(f"Nenhum arquivo {file_pattern} em {self.source_dir}")

        dfs = []
        for f in files:
            df = pd.read_csv(f, encoding="utf-8-sig")
            df["_source_file"] = f.name
            df["_extracted_at"] = datetime.now()
            dfs.append(df)

        return pd.concat(dfs, ignore_index=True)

    def transform(self, df: pd.DataFrame, operations: Optional[list[dict]] = None) -> pd.DataFrame:
        if operations is None:
            df = self._default_transform(df)
        else:
            for op in operations:
                op_type = op.get("type")
                if op_type == "drop_columns":
                    df = df.drop(columns=op["columns"], errors="ignore")
                elif op_type == "fill_na":
                    df = df.fillna(op.get("value", 0))
                elif op_type == "rename":
                    df = df.rename(columns=op["mapping"])
                elif op_type == "filter":
                    df = df.query(op["condition"])
                elif op_type == "type_cast":
                    for col, dtype in op["mapping"].items():
                        df[col] = df[col].astype(dtype)
                elif op_type == "add_column":
                    df[op["name"]] = op["value"]
        return df

    def _default_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        for col in df.select_dtypes(include=["object"]):
            df[col] = df[col].str.strip() if df[col].dtype == "object" else df[col]

        for col in df.select_dtypes(include=["float64", "int64"]):
            df[col] = df[col].fillna(df[col].median())

        return df

    def load(self, df: pd.DataFrame, target: str, fmt: Literal["csv", "parquet", "json"] = "parquet"):
        path = self.staging_dir / f"{target}.{fmt}"
        if fmt == "csv":
            df.to_csv(path, index=False, encoding="utf-8-sig")
        elif fmt == "parquet":
            df.to_parquet(path, index=False)
        elif fmt == "json":
            df.to_json(path, orient="records", indent=2, force_ascii=False)
        return path

    def run(self, file_pattern: str = "*.csv", target: str = "gold_layer") -> dict:
        start = datetime.now()

        df = self.extract(file_pattern)
        raw_count = len(df)

        df = self.transform(df)
        transformed_count = len(df)

        path = self.load(df, target)
        duration = (datetime.now() - start).total_seconds()

        return {
            "status": "success",
            "raw_rows": raw_count,
            "transformed_rows": transformed_count,
            "output_path": str(path),
            "duration_seconds": round(duration, 2),
        }


def generate_sample_data(output_dir: Path):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(42)
    n = 5000

    for batch in range(3):
        df = pd.DataFrame({
            "id": range(batch * n + 1, (batch + 1) * n + 1),
            "data_registro": pd.date_range(
                f"2024-0{batch+1}-01", periods=n, freq="h"
            ).strftime("%Y-%m-%d %H:%M:%S"),
            "produto": rng.choice(["Bateria Automotiva", "Bateria Estacionária", "Bateria Industrial"], n),
            "quantidade": rng.integers(1, 100, n),
            "valor_unitario": rng.uniform(50, 500, n).round(2),
            "regiao": rng.choice(["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"], n),
            "canal_venda": rng.choice(["Direta", "Distribuidor", "E-commerce"], n),
        })
        path = output_dir / f"vendas_2024_batch_{batch+1}.csv"
        df.to_csv(path, index=False, encoding="utf-8-sig")
        print(f"  Criado: {path.name} ({len(df)} linhas)")


if __name__ == "__main__":
    data_dir = Path(__file__).parent.parent.parent.parent / "data" / "sample"
    print("Gerando dados de exemplo...")
    generate_sample_data(data_dir)

    print("\nExecutando ETL...")
    pipeline = ETLPipeline(source_dir=data_dir)
    result = pipeline.run()
    for k, v in result.items():
        print(f"  {k}: {v}")
