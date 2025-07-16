from utils.preprocess import preprocess
from tensorflow.keras.preprocessing.sequence import pad_sequences
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
def classificate_lstm(tokenizer, model, text):
    if not text:
        return {"error": "Text input is empty or None"}

    processed_text = preprocess(str(text))
    sequences = tokenizer.texts_to_sequences([processed_text])

    # Check for empty or invalid sequences
    if not sequences or sequences[0] is None or sequences[0] == []:
        return {"error": "Tokenizer failed to produce valid sequence from input."}

    # Remove None values from sequences
    sequences = [[token for token in seq if token is not None] for seq in sequences]

    try:
        # Pad sequences
        padded = pad_sequences(sequences, maxlen=512, padding='post', truncating='post')
        input_tensor = torch.tensor(padded, dtype=torch.long).to(device)
    except Exception as e:
        return {"error": f"Padding or tensor conversion failed: {str(e)}"}

    try:
        model.eval()
        with torch.no_grad():
            logits = model(input_tensor)
            print(f"Logits shape: {logits.shape}")  # Debugging line

            # Handle scalar output (logits shape: [])
            if logits.dim() == 0:
                probs = logits
                confidence = probs.item()
                pred = int(confidence >= 0.5)
                all_probs = [1 - confidence, confidence]
                logits_out = logits.item()

            # Output shape [batch_size, 1]
            elif logits.dim() == 2 and logits.size(1) == 1:
                probs = logits.squeeze(1)  # shape: [batch_size]
                confidence = probs[0].item()
                pred = int(confidence >= 0.5)
                all_probs = [1 - confidence, confidence]
                logits_out = logits[0][0].item()

            else:
                return {"error": f"Unexpected logits shape: {logits.shape}"}

        return {
            "label": pred,
            "confidence": confidence,
            "all_probs": all_probs,
            "logits": logits_out,
            "tokenized_input": input_tensor[0].tolist()
        }

    except Exception as e:
        return {"error": f"Model inference failed: {str(e)}"}
