# from flask import Blueprint, request, jsonify
# from models import roberta_model,roberta_tokenizer
# from utils.classificate import classificate


# roberta_route = Blueprint('roberta_route', __name__)

# @roberta_route.route('/roberta', methods=['POST'])
# def predict_roberta():
#     try:
#         data = request.json
#         result = classificate(roberta_tokenizer,roberta_model,data)
       
#         return jsonify({
#             "success": True,
#             "data": result,
#             "message": "Dự đoán thành công"
#         }), 200
       
#     except Exception as e:
#             return jsonify({
#                 "success": False,
#                 "data": None,
#                 "message": str(e)
#             }), 400
