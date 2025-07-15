from flask import Blueprint, request, jsonify
from models import roberta_model,roberta_tokenizer, model_sumary, tokenize_sumary
from utils.classificate import classificate
from utils.sumarize import sumary_text
from utils.find_related import find_related_links

roberta_route = Blueprint('roberta_route', __name__)

@roberta_route.route('/roberta', methods=['POST'])
def predict_roberta():
    try:
        data = request.json
        result = classificate(roberta_tokenizer,roberta_model,data['text'])
        sumaried_text = sumary_text(tokenize_sumary,model_sumary,data['text'])
        find_related_link= find_related_links(data['text'])
        
        return jsonify({
            "success": True,
            "data": {
                "label": result,
                "summary": sumaried_text,
                "links": find_related_link
            },
            "message": "Dự đoán thành công"
        }), 200
        
    except Exception as e:
            return jsonify({
                "success": False,
                "data": None,
                "message": str(e)
            }), 400
