from sentence_transformers import SentenceTransformer
import torch
import os
import dotenv
import onnx
from onnxconverter_common import convert_float_to_float16

dotenv.load_dotenv()

# Configuration paths and dimensions.
STUDENT_BASE_MODEL = "distiluse-base-multilingual-cased-v2"  # base student model
STUDENT_STATE_DICT = "distilled_student_model/student_model_fp16.pth"
PROJECTION_STATE_DICT = "distilled_student_model/projection_fp16.pth"
OUTPUT_ONNX_PATH_FP32 = "data/embedder_fp32.onnx"
OUTPUT_ONNX_PATH_FP16 = "../../data/embedder_fp16.onnx"

# Known dimensions: teacher=384, student=512
TEACHER_DIM = 384
STUDENT_DIM = 512


# Define a wrapper that combines the student model and projection layer.
class ONNXWrapper(torch.nn.Module):
    def __init__(self, student_model, projection):
        super().__init__()
        self.student_model = student_model
        self.projection = projection

    def forward(self, input_ids, attention_mask):
        # The student model expects a dict with input_ids and attention_mask.
        features = {'input_ids': input_ids, 'attention_mask': attention_mask}
        output = self.student_model(features)
        # Use the sentence embedding from the student model and apply projection.
        sentence_embedding = output['sentence_embedding']
        return self.projection(sentence_embedding)


def main():
    print("Loading base student model...")
    # Load the base student model.
    student_model = SentenceTransformer(STUDENT_BASE_MODEL, trust_remote_code=True)
    student_model = student_model.cpu().half()  # move to CPU and convert to FP16.

    print("Loading saved student state dict...")
    # Load the saved FP16 state dict for the student model.
    student_state = torch.load(STUDENT_STATE_DICT, map_location="cpu")
    student_model.load_state_dict(student_state, strict=False)

    print("Rebuilding projection layer...")
    # Recreate the projection layer and load its state dict.
    projection = torch.nn.Linear(STUDENT_DIM, TEACHER_DIM).cpu().half()
    projection_state = torch.load(PROJECTION_STATE_DICT, map_location="cpu")
    projection.load_state_dict(projection_state)

    # Wrap the student model and projection together.
    wrapper = ONNXWrapper(student_model, projection)
    wrapper = wrapper.cpu().half()
    wrapper.eval()

    # Create dummy inputs.
    dummy_input_ids = torch.randint(0, 1000, (1, 128), dtype=torch.long)
    dummy_attention_mask = torch.ones(1, 128, dtype=torch.long)

    # Export the FP32 ONNX model first.
    print("Exporting to ONNX (FP32)...")
    torch.onnx.export(
        wrapper,
        (dummy_input_ids, dummy_attention_mask),
        OUTPUT_ONNX_PATH_FP32,
        input_names=["input_ids", "attention_mask"],
        output_names=["output"],
        opset_version=14,
        dynamic_axes={
            "input_ids": {0: "batch_size", 1: "sequence_length"},
            "attention_mask": {0: "batch_size", 1: "sequence_length"},
            "output": {0: "batch_size"}
        }
    )
    print(f"FP32 ONNX model saved to {OUTPUT_ONNX_PATH_FP32}")

    # Convert the FP32 ONNX model to FP16.
    print("Converting ONNX model to FP16...")
    model_fp32 = onnx.load(OUTPUT_ONNX_PATH_FP32)
    model_fp16 = convert_float_to_float16(model_fp32, keep_io_types=True)
    onnx.save(model_fp16, OUTPUT_ONNX_PATH_FP16)
    print(f"FP16 ONNX model saved to {OUTPUT_ONNX_PATH_FP16}")


if __name__ == "__main__":
    main()
