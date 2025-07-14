def sumary_text(tokenize_sumary,model_sumary ,text):
  # Thêm tiền tố 'summarize:' giống T5
  input_text = "summarize: " + text
  input_ids = tokenize_sumary.encode(input_text, return_tensors="pt", max_length=512, truncation=True)

  summary_ids = model_sumary.generate(
      input_ids,
      max_length=100,
      min_length=40,
      num_beams=4,
      early_stopping=True
  )


  summary = tokenize_sumary.decode(summary_ids[0], skip_special_tokens=True)
  return summary