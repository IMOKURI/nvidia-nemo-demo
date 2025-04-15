import argparse
from nemo.export.vllm_hf_exporter import vLLMHFExporter


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, type=str, help="Local path of the base model")
    parser.add_argument("--lora-model", required=True, type=str, help="Local path of the lora model")
    # parser.add_argument('--triton-model-name', required=True, type=str, help="Name for the service")
    args = parser.parse_args()

    lora_model_name = "lora_model"

    exporter = vLLMHFExporter()
    exporter.export(model=args.model, enable_lora=True)
    exporter.add_lora_models(lora_model_name=lora_model_name, lora_model=args.lora_model)

    print("vLLM Output: ", exporter.forward(input_texts=["How are you doing?"], lora_model_name=lora_model_name))
