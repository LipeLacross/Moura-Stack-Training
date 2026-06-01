from . import classifier, regressor, clustering


def train_all() -> dict:
    return {
        "classifier": classifier.train(),
        "regressor": regressor.train(),
        "clustering": clustering.train(),
    }


if __name__ == "__main__":
    results = train_all()
    for model_name, metrics in results.items():
        print(f"\n=== {model_name.upper()} ===")
        for k, v in metrics.items():
            print(f"  {k}: {v}")
