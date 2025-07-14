from flask import Blueprint, request, jsonify
from models import phoBert_model,phoBert_tokenizer
from utils.classificate import classificate


phoBert_route = Blueprint('phoBert_route', __name__)

@phoBert_route.route('/phoBert', methods=['POST'])
def predict_phoBert():
    try:
        data = request.json
        result = classificate(phoBert_tokenizer,phoBert_model,data)
       
        return jsonify({
            "success": True,
            "data": result,
            "message": "Dự đoán thành công"
        }), 200
       
    except Exception as e:
            return jsonify({
                "success": False,
                "data": None,
                "message": str(e)
            }), 400
