import pandas as pd
import re
from typing import Optional


class DataValidator:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.errors: list[dict] = []
        self.warnings: list[dict] = []

    def check_missing(self, columns: Optional[list[str]] = None) -> "DataValidator":
        cols = columns or self.df.columns.tolist()
        for col in cols:
            missing = self.df[col].isna().sum()
            if missing > 0:
                self.warnings.append({
                    "type": "missing_values",
                    "column": col,
                    "count": int(missing),
                    "pct": round(float(missing / len(self.df) * 100), 2),
                })
        return self

    def check_duplicates(self, subset: Optional[list[str]] = None) -> "DataValidator":
        dups = self.df.duplicated(subset=subset).sum()
        if dups > 0:
            self.warnings.append({
                "type": "duplicates",
                "columns": subset or "all",
                "count": int(dups),
            })
        return self

    def check_outliers_iqr(self, columns: list[str], multiplier: float = 1.5) -> "DataValidator":
        for col in columns:
            if col not in self.df.select_dtypes(include=["number"]).columns:
                continue
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - multiplier * IQR
            upper = Q3 + multiplier * IQR
            outliers = ((self.df[col] < lower) | (self.df[col] > upper)).sum()
            if outliers > 0:
                self.warnings.append({
                    "type": "outliers",
                    "column": col,
                    "count": int(outliers),
                    "pct": round(float(outliers / len(self.df) * 100), 2),
                })
        return self

    def check_data_types(self, schema: dict[str, type]) -> "DataValidator":
        for col, expected_type in schema.items():
            if col not in self.df.columns:
                self.errors.append({
                    "type": "missing_column",
                    "column": col,
                })
                continue
            actual = self.df[col].dtype
            if not self._type_matches(actual, expected_type):
                self.errors.append({
                    "type": "type_mismatch",
                    "column": col,
                    "expected": str(expected_type),
                    "actual": str(actual),
                })
        return self

    def check_email_format(self, columns: list[str]) -> "DataValidator":
        pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
        for col in columns:
            if col in self.df.columns:
                invalid = ~self.df[col].astype(str).str.match(pattern, na=False)
                count = int(invalid.sum())
                if count > 0:
                    self.errors.append({
                        "type": "invalid_email",
                        "column": col,
                        "count": count,
                    })
        return self

    def check_range(self, column: str, min_val: Optional[float] = None, max_val: Optional[float] = None) -> "DataValidator":
        if column not in self.df.columns:
            return self
        if min_val is not None:
            below = (self.df[column] < min_val).sum()
            if below > 0:
                self.errors.append({
                    "type": "below_minimum",
                    "column": column,
                    "count": int(below),
                    "min_expected": min_val,
                })
        if max_val is not None:
            above = (self.df[column] > max_val).sum()
            if above > 0:
                self.errors.append({
                    "type": "above_maximum",
                    "column": column,
                    "count": int(above),
                    "max_expected": max_val,
                })
        return self

    def report(self) -> dict:
        return {
            "total_rows": len(self.df),
            "total_columns": len(self.df.columns),
            "errors": self.errors,
            "warnings": self.warnings,
            "is_valid": len(self.errors) == 0,
        }

    def _type_matches(self, actual, expected) -> bool:
        type_map = {
            int: ["int64", "int32"],
            float: ["float64", "float32"],
            str: ["object", "string"],
            bool: ["bool"],
            pd.Timestamp: ["datetime64[ns]"],
        }
        return str(actual) in type_map.get(expected, [str(expected)])
