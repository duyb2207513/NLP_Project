from utils.preprocess import preprocess
import torch
import torch as nn
import torch.nn.functional as F

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
def classificate(tokenizer, model, text):
    inputs = preprocess(str(text))
    inputs = tokenizer(inputs, return_tensors="pt", truncation=True, padding=True, max_length=128)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = F.softmax(logits, dim=1)

        pred = torch.argmax(probs, dim=1).item()
        confidence = probs[0][pred].item()
        all_probs = probs[0].tolist()  # List xác suất cho tất cả các class

    return {
        "label": pred,
        "confidence": confidence,
        "all_probs": all_probs,
        "logits": logits[0].tolist(),
        "tokenized_input": inputs['input_ids'][0].tolist()
    }