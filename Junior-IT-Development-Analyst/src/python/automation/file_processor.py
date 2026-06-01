from pathlib import Path
import pandas as pd
import csv
from typing import Literal


class FileProcessor:
    SUPPORTED_FORMATS = ("csv", "xlsx", "json", "parquet")

    def __init__(self, source_dir: Path, output_dir: Path):
        self.source_dir = source_dir
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def read_file(self, filepath: Path) -> pd.DataFrame:
        ext = filepath.suffix.lower()
        if ext == ".csv":
            return pd.read_csv(filepath, encoding="utf-8-sig")
        elif ext == ".xlsx":
            return pd.read_excel(filepath, engine="openpyxl")
        elif ext == ".json":
            return pd.read_json(filepath)
        elif ext == ".parquet":
            return pd.read_parquet(filepath)
        else:
            raise ValueError(f"Formato não suportado: {ext}")

    def export(self, df: pd.DataFrame, filename: str, fmt: Literal["csv", "xlsx", "parquet"]):
        path = self.output_dir / f"{filename}.{fmt}"
        if fmt == "csv":
            df.to_csv(path, index=False, encoding="utf-8-sig")
        elif fmt == "xlsx":
            df.to_excel(path, index=False, engine="openpyxl")
        elif fmt == "parquet":
            df.to_parquet(path, index=False)
        return path

    def consolidate_files(self, pattern: str = "*.csv") -> pd.DataFrame:
        files = list(self.source_dir.glob(pattern))
        if not files:
            raise FileNotFoundError(f"Nenhum arquivo encontrado: {pattern}")
        return pd.concat([self.read_file(f) for f in files], ignore_index=True)

    def split_csv(self, filepath: Path, chunk_size: int = 10000):
        df = self.read_file(filepath)
        stem = filepath.stem
        parts = []
        for i, start in enumerate(range(0, len(df), chunk_size)):
            chunk = df.iloc[start : start + chunk_size]
            part_path = self.output_dir / f"{stem}_part_{i+1:03d}.csv"
            chunk.to_csv(part_path, index=False, encoding="utf-8-sig")
            parts.append(part_path)
        return parts
