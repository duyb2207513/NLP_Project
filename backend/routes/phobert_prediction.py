from flask import Blueprint, request, jsonify
from models import phoBert_model,phoBert_tokenizer, model_sumary, tokenize_sumary
from utils.classificate import classificate
from utils.sumarize import sumary_text


phoBert_route = Blueprint('phoBert_route', __name__)

@phoBert_route.route('/phoBert', methods=['POST'])
def predict_phoBert():
    try:
        data = request.json
        result = classificate(phoBert_tokenizer,phoBert_model,data['text'])
        sumaried_text = sumary_text(tokenize_sumary,model_sumary,data['text'])
        return jsonify({
            "success": True,
            "data": result,
            "sumary":sumaried_text,
            "message": "Dự đoán thành công"
        }), 200
       
    except Exception as e:
            return jsonify({
                "success": False,
                "data": None,
                "message": str(e)
            }), 400
