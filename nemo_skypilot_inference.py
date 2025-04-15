import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer


def main():
    # Load base model and tokenizer
    base_model_name = "rinna/gemma-2-baku-2b-it"
    tokenizer = AutoTokenizer.from_pretrained(base_model_name)
    model = AutoModelForCausalLM.from_pretrained(base_model_name)

    # Load PEFT adapter
    adapter_path = "/checkpoints/gemma2_baku_lora/gemma2_baku_lora/checkpoints/model_name=0--val_loss=0.00-step=100-consumed_samples=0-last/hf_adapter"
    model = PeftModel.from_pretrained(model, adapter_path)

    # Move model to GPU if available
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    # Generate text
    input_text = "東京の観光名所を教えてください。"
    inputs = tokenizer(input_text, return_tensors="pt").to(device)
    output = model.generate(**inputs, max_length=100)

    # Decode and print the output
    print(tokenizer.decode(output[0], skip_special_tokens=True))


if __name__ == "__main__":
    main()
