
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
from flask import Flask, request, jsonify
import threading
import time

# --- CONFIGURATION ---
BASE_MODEL = "microsoft/phi-2"
ADAPTER_PATH = "c:/NeuroSys_Phoenix_Clean_v7/AURORA_PHOENIX_TRAINING_LAB/Tier10-Specialist-v1"
PORT = 11434 # Ollama default port

app = Flask(__name__)
model = None
tokenizer = None

def load_model():
    global model, tokenizer
    print("🚀 Loading Tier 10 Specialist Model...")
    
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    
    base_model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        torch_dtype=torch.float16,
        device_map="auto",
        trust_remote_code=True
    )
    
    print(f"🔗 Attaching Adapter: {ADAPTER_PATH}")
    model = PeftModel.from_pretrained(base_model, ADAPTER_PATH)
    model.eval()
    print("✅ Model Ready!")

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    messages = data.get('messages', [])
    
    if not messages:
        return jsonify({"error": "No messages provided"}), 400
        
    # Extract the user prompt (usually the last message)
    user_prompt = messages[-1]['content']
    
    # Construct the prompt using the MASTER PROMPT structure we found
    # Note: The user_prompt from Tier 10 ALREADY contains the Master Prompt instructions!
    # So we just need to wrap it in the format our model expects.
    
    formatted_prompt = f"""### System:
You are Tier 10, a strict code governance engine.
RULES:
1. OPTIMIZE: Replace slow algorithms.
2. SECURE: Remove os.system/exec/eval.
3. OUTPUT: Return ONLY the optimized Python code.

### Instruction:
Analyze and optimize the following code.

### Input:
{user_prompt}

### Response:
"""
    
    print(f"📩 Received request. Generating response...")
    
    inputs = tokenizer(formatted_prompt, return_tensors="pt").to("cuda")
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs, 
            max_new_tokens=1024, 
            temperature=0.01,
            do_sample=True,
            repetition_penalty=1.1
        )
    
    response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Extract just the response part
    if "### Response:" in response_text:
        response_text = response_text.split("### Response:")[-1].strip()
    
    # Ollama API format response
    return jsonify({
        "model": "tier10-specialist",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S.000000Z", time.gmtime()),
        "message": {
            "role": "assistant",
            "content": response_text
        },
        "done": True
    })

@app.route('/api/tags', methods=['GET'])
def tags():
    # Mock response for 'ollama list'
    return jsonify({
        "models": [
            {
                "name": "llama3.1:8b", # Pretend to be the model Tier 10 expects
                "modified_at": "2025-12-18T00:00:00.000000Z",
                "size": 0,
                "digest": "sha256:fake"
            }
        ]
    })

if __name__ == "__main__":
    load_model()
    print(f"🌐 Starting Bridge Server on port {PORT}...")
    app.run(host='0.0.0.0', port=PORT)
