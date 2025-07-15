from flask import Blueprint

# from .roberta_prediction import roberta_route
from .phobert_prediction import phoBert_route
from .roberta_prediction import roberta_route
from .BiLSTM_prediction import bilstm_route

def register_app(app):
    api_v1 = Blueprint("api_v1", __name__, url_prefix="/api/v1")
    api_v1.register_blueprint(roberta_route, url_prefix="/predict")
    api_v1.register_blueprint(phoBert_route, url_prefix="/predict")
    api_v1.register_blueprint(bilstm_route, url_prefix="/predict")
    app.register_blueprint(api_v1)