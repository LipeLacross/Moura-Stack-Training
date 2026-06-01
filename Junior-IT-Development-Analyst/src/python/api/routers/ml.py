from fastapi import APIRouter, HTTPException
from ..models import MLPredictionRequest, MLPredictionResponse

router = APIRouter()


@router.post("/predict", response_model=MLPredictionResponse)
def predict(request: MLPredictionRequest):
    features = request.features
    model_type = request.model_type

    try:
        if model_type == "classifier":
            from ...ml.classifier import predict_classification
            pred, prob, importance = predict_classification(features)
            return MLPredictionResponse(
                prediction=pred, probability=prob,
                model_used="RandomForestClassifier", feature_importance=importance
            )
        elif model_type == "regressor":
            from ...ml.regressor import predict_regression
            pred, importance = predict_regression(features)
            return MLPredictionResponse(
                prediction=pred, model_used="RandomForestRegressor",
                feature_importance=importance
            )
        elif model_type == "cluster":
            from ...ml.clustering import predict_cluster
            cluster_id, similarity = predict_cluster(features)
            return MLPredictionResponse(
                prediction=int(cluster_id), probability=similarity,
                model_used="KMeans"
            )
        else:
            raise HTTPException(400, f"Modelo inválido: {model_type}")
    except ImportError:
        raise HTTPException(503, "Modelos ML não carregados. Execute o treinamento primeiro.")
    except Exception as e:
        raise HTTPException(500, f"Erro na predição: {str(e)}")


@router.post("/train")
def train_models():
    try:
        from ...ml.train_pipeline import train_all
        results = train_all()
        return {"status": "ok", "results": results}
    except Exception as e:
        raise HTTPException(500, f"Erro no treinamento: {str(e)}")
