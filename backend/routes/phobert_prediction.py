from flask import Blueprint, request, jsonify
from models import phoBert_model,phoBert_tokenizer, model_sumary, tokenize_sumary
from utils.classificate import classificate
from utils.sumarize import sumary_text
from utils.find_related import find_related_links
from utils.crawl_data import extract_main_text

phoBert_route = Blueprint('phoBert_route', __name__)

@phoBert_route.route('/phoBert', methods=['POST'])
def predict_phoBert():
    try:
        data = request.json
        result = classificate(phoBert_tokenizer,phoBert_model,data['text'])
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

@phoBert_route.route('/withlink/phoBert', methods=['POST'])
def predict_phoBert_withlink():
    try:
        
        data = request.json
        text = extract_main_text(data['text'])
        result = classificate(phoBert_tokenizer,phoBert_model,text)
        sumaried_text = sumary_text(tokenize_sumary,model_sumary,text)
        find_related_link= find_related_links(text)
        
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