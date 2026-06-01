import pytest
import numpy as np


class TestClassifier:
    def test_train_and_predict(self):
        from src.python.ml.classifier import train, predict_classification

        metrics = train()
        assert "accuracy" in metrics
        assert metrics["accuracy"] > 0
        assert "feature_importance" in metrics

        pred, prob, importance = predict_classification([1.0, -0.5, 0.3, 2.0, -1.0])
        assert pred in (0, 1)
        assert 0 <= prob <= 1
        assert len(importance) == 5

    def test_feature_count_match(self):
        from src.python.ml.classifier import generate_sample_data

        X, y, feature_names = generate_sample_data()
        assert X.shape[1] == len(feature_names)


class TestRegressor:
    def test_train_and_predict(self):
        from src.python.ml.regressor import train, predict_regression

        metrics = train()
        assert "r2" in metrics
        assert metrics["r2"] > -1

        pred, importance = predict_regression([25.0, 60.0, 80.0, 7.5])
        assert isinstance(pred, float)
        assert len(importance) == 4


class TestClustering:
    def test_train_and_predict(self):
        from src.python.ml.clustering import train, predict_cluster

        metrics = train(n_clusters=3)
        assert metrics["n_clusters"] == 3
        assert metrics["silhouette_score"] > -1

        cluster_id, similarity = predict_cluster([15.0, 20.0, 25.0])
        assert isinstance(cluster_id, int)
        assert 0 <= similarity <= 1


class TestFeatureEngineering:
    def test_pipeline(self):
        from src.python.ml.feature_engineering import example_pipeline

        result = example_pipeline()
        assert result.shape[0] == 365
        assert "ano" in result.columns
        assert "fim_semana" in result.columns
        assert "producao_lag_1" in result.columns
        assert "producao_rolling_mean_7" in result.columns
