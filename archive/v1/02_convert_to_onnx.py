from sentence_transformers import SentenceTransformer
import torch
import os
import dotenv

dotenv.load_dotenv()


# Define a wrapper module for ONNX compatibility
class ONNXWrapper(torch.nn.Module):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def forward(self, input_ids, attention_mask):
        features = {'input_ids': input_ids, 'attention_mask': attention_mask}
        output = self.model(features)
        return output['sentence_embedding']


def main():
    # Model name
    model_name = 'distilled_student_model'
    print(f"Loading model '{model_name}'...")

    # Load the SentenceTransformer model
    model = SentenceTransformer(model_name, trust_remote_code=True)
    print("Model loaded successfully.")

    # Move the model to CPU and set to evaluation mode
    model = model.to('cpu')
    model.eval()

    # Wrap the model for ONNX export
    wrapper = ONNXWrapper(model)
    wrapper = wrapper.to('cpu')
    wrapper.eval()

    # Create dummy inputs on CPU
    dummy_input_ids = torch.randint(0, 1000, (1, 128), dtype=torch.long).to('cpu')
    dummy_attention_mask = torch.ones(1, 128, dtype=torch.long).to('cpu')

    # Export to ONNX with updated opset version
    print("Exporting to ONNX...")
    torch.onnx.export(
        wrapper,
        (dummy_input_ids, dummy_attention_mask),
        "data/embedder.onnx",
        input_names=["input_ids", "attention_mask"],
        output_names=["output"],
        opset_version=14,  # Updated to version 14
        dynamic_axes={
            'input_ids': {0: 'batch_size', 1: 'sequence_length'},
            'attention_mask': {0: 'batch_size', 1: 'sequence_length'},
            'output': {0: 'batch_size'}
        }
    )
    print("Model exported to 'data/embedder.onnx'.")


if __name__ == "__main__":
    main()