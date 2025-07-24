# def sumary_text(tokenize_sumary,model_sumary ,text):
#   # Thêm tiền tố 'summarize:' giống T5
#   input_text = "summarize: " + text
#   print(input_text)
#   input_ids = tokenize_sumary.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
#   summary_ids = model_sumary.generate(
#       input_ids,
#       max_length=150,
#       min_length=100,
#       num_beams=5,
#       early_stopping=True
#   )


#   summary = tokenize_sumary.decode(summary_ids[0], skip_special_tokens=True)
#   return summary
def sumary_text(model_bundle, text, max_length=150, min_length=100, num_beams=5):
    tokenizer = model_bundle["tokenizer"]
    model = model_bundle["model"]

    input_text = "summarize: " + text
    input_ids = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)

    summary_ids = model.generate(
        input_ids,
        max_length=max_length,
        min_length=min_length,
        num_beams=num_beams,
        early_stopping=True
    )

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary
