import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel, PeftConfig
import sys
from pathlib import Path

def test_specialist():
    print("🤖 INICIANDO CARGA DEL ESPECIALISTA TIER 10 (Phi-2 + LoRA) 🤖")
    print("=============================================================")

    # Rutas
    base_model_id = "microsoft/phi-2"
    # Ajustar ruta absoluta
    adapter_path = Path(r"c:\Users\Cruz Sanchez\DEBUGGING\DEBUGGING_GODTIER\external_modules\Tier_10_Clean\TIER10_UPDATE_PACKAGE\Tier10-Specialist-v1")

    if not adapter_path.exists():
        print(f"❌ Error: No se encuentra el adaptador en {adapter_path}")
        return

    print(f"📂 Cargando adaptador desde: {adapter_path}")

    try:
        # 1. Cargar Tokenizer
        print("⏳ Cargando Tokenizer...")
        # Intentar cargar tokenizer local si existe en la carpeta del adaptador, sino del base
        try:
            tokenizer = AutoTokenizer.from_pretrained(str(adapter_path), trust_remote_code=True)
        except:
            print("   (Usando tokenizer del modelo base)")
            tokenizer = AutoTokenizer.from_pretrained(base_model_id, trust_remote_code=True)
            
        tokenizer.pad_token = tokenizer.eos_token

        # 2. Cargar Modelo Base (Phi-2)
        print(f"⏳ Cargando Modelo Base ({base_model_id})...")
        # Usamos float16 para ahorrar memoria si hay GPU, si no float32
        device = "cuda" if torch.cuda.is_available() else "cpu"
        torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        
        print(f"   Device: {device}")
        print(f"   Dtype: {torch_dtype}")

        model = AutoModelForCausalLM.from_pretrained(
            base_model_id,
            torch_dtype=torch_dtype,
            trust_remote_code=True,
            device_map="auto" if device == "cuda" else None
        )
        
        if device == "cpu":
            model = model.to(device)

        # 3. Cargar Adaptador LoRA
        print("⏳ Fusionando Adaptador LoRA Tier-10...")
        model = PeftModel.from_pretrained(model, str(adapter_path))
        
        print("✅ ¡MODELO HÍBRIDO CARGADO EXITOSAMENTE!")

        # 4. Prueba de Inferencia
        # Prompt estilo instruccion
        prompt = "Instruct: Explain the purpose of AuroraMemory in the Tier 10 system.\nOutput:"
        print(f"\n🧪 Probando inferencia:\nPrompt: {prompt}\n")
        
        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs, 
                max_new_tokens=150, 
                do_sample=True, 
                temperature=0.7,
                pad_token_id=tokenizer.eos_token_id
            )
            
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print("-" * 50)
        print(response)
        print("-" * 50)

    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_specialist()
