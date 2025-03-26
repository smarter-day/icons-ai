#!/usr/bin/env python

import os
import torch
import dotenv
from onnxruntime.quantization import quantize_dynamic, QuantType
from sentence_transformers import SentenceTransformer

dotenv.load_dotenv()

class ONNXWrapper(torch.nn.Module):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def forward(self, input_ids, attention_mask):
        with torch.no_grad():
            features = {'input_ids': input_ids, 'attention_mask': attention_mask}
            output = self.model(features)
            return output['sentence_embedding']

def export_onnx(model_name:str, onnx_path:str, seq_length:int=128):
    print(f"Loading base model: {model_name}")
    # 1) Load model
    model = SentenceTransformer(model_name)
    model.to("cpu").eval()

    # 2) Wrap in a Module
    wrapped = ONNXWrapper(model).to("cpu").eval()

    # 3) Dummy CPU tensors
    dummy_input_ids = torch.randint(0, 1000, (1, seq_length), dtype=torch.long, device="cpu")
    dummy_attention_mask = torch.ones((1, seq_length), dtype=torch.long, device="cpu")

    print("Exporting to ONNX...")
    torch.onnx.export(
        wrapped,
        (dummy_input_ids, dummy_attention_mask),
        onnx_path,
        input_names=["input_ids", "attention_mask"],
        output_names=["output"],
        opset_version=14,
        dynamic_axes={
            'input_ids': {0: 'batch_size', 1: 'sequence_length'},
            'attention_mask': {0: 'batch_size', 1: 'sequence_length'},
            'output': {0: 'batch_size'}
        }
    )
    print(f"Exported unquantized ONNX model to: {onnx_path}")

def quantize_onnx(onnx_path:str, quantized_path:str):
    print("Quantizing ONNX model (dynamic int8)...")
    quantize_dynamic(
        model_input=onnx_path,
        model_output=quantized_path,
        per_channel=False,
        reduce_range=False,
        weight_type=QuantType.QUInt8
    )
    print(f"Quantized model saved to: {quantized_path}")

    size_mb = os.path.getsize(quantized_path)/(1024*1024)
    print(f"Final ONNX size: {size_mb:.1f} MB")

def main():
    base_model = os.environ.get("EMBEDDING_MODEL", "intfloat/multilingual-e5-small")
    onnx_out = "data/multilingual_e5_unquantized.onnx"
    onnx_quant = "data/multilingual_e5_quantized.onnx"

    # 1) Export unquantized ONNX on CPU
    export_onnx(base_model, onnx_out, seq_length=128)

    # 2) Quantize
    quantize_onnx(onnx_out, onnx_quant)

if __name__ == "__main__":
    main()
