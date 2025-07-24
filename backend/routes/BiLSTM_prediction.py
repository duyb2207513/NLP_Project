from flask import Blueprint, request, jsonify
from models import bilstm_model,bilstm_tokenizer, model_sumary, tokenize_sumary
from models.summarization_model import summarization_models
from utils.classificate import classificate_lstm
from utils.sumarize import sumary_text
from utils.find_related import find_related_links
from utils.crawl_data import extract_main_text


bilstm_route = Blueprint('bilstm_route', __name__)

@bilstm_route.route('/bilstm', methods=['POST'])
def predict_BiLSTM():
    try:
        
        data = request.json
        text = data['text']
        model_name = data.get("summary_model", "vit5")  # Mặc định dùng vit5 nếu không có

        if model_name not in summarization_models:
            raise ValueError(f"Không hỗ trợ mô hình tóm tắt: {model_name}")
        
        summary_model = summarization_models[model_name]
        
        result = classificate_lstm(bilstm_tokenizer,bilstm_model,text)
        sumaried_text = sumary_text(summary_model, text)
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

@bilstm_route.route('/withlink/bilstm', methods=['POST'])
def predict_BiLSTM_withlink():
    try:
        
        # data = request.json
        # text = extract_main_text(data['text'])
        data = request.json
        text = extract_main_text(data['text'])

        model_name = data.get("summary_model", "vit5")  # Mặc định dùng vit5 nếu không có

        if model_name not in summarization_models:
            raise ValueError(f"Không hỗ trợ mô hình tóm tắt: {model_name}")
        

        summary_model = summarization_models[model_name]
        result = classificate_lstm(bilstm_tokenizer,bilstm_model,text)
        sumaried_text = sumary_text(summary_model, text)
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