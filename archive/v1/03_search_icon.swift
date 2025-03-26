import Foundation
import ONNXRuntime

// Helper function to compute cosine similarity
func cosineSimilarity(_ a: [Float], _ b: [Float]) -> Float {
    let dotProduct = zip(a, b).map(*).reduce(0, +)
    let normA = sqrt(a.map { $0 * $0 }.reduce(0, +))
    let normB = sqrt(b.map { $0 * $0 }.reduce(0, +))
    return dotProduct / (normA * normB)
}

// Load precomputed icon embeddings and metadata from JSON
func loadData() -> ([[Float]], [[String: String]]) {
    guard let embeddingsURL = Bundle.main.url(forResource: "icon_embeddings", withExtension: "json"),
          let metadataURL = Bundle.main.url(forResource: "icons_index", withExtension: "json"),
          let embeddingsData = try? Data(contentsOf: embeddingsURL),
          let metadataData = try? Data(contentsOf: metadataURL),
          let embeddings = try? JSONDecoder().decode([[Float]].self, from: embeddingsData),
          let metadata = try? JSONDecoder().decode([[String: String]].self, from: metadataData) else {
        fatalError("Failed to load data")
    }
    return (embeddings, metadata)
}

// Simple pre-tokenized input (for demo; replace with actual tokenization if needed)
func getTokenizedInput(query: String) -> (inputIds: [Int64], attentionMask: [Int64]) {
    // Placeholder: In practice, use a tokenizer or precomputed tokens
    // Here, we simulate tokenized input with dummy values
    let inputIds = Array(repeating: Int64(query.count % 1000), count: 128) // Simplified
    let attentionMask = Array(repeating: Int64(1), count: 128)
    return (inputIds, attentionMask)
}

// Load and run the ONNX model
func getEmbedding(inputIds: [Int64], attentionMask: [Int64]) -> [Float] {
    guard let modelPath = Bundle.main.path(forResource: "embedder", ofType: "onnx") else {
        fatalError("Model file not found")
    }

    let session = try! ORTSession(modelPath: modelPath)
    let inputIdsTensor = try! ORTTensor(int64Values: inputIds, dimensions: [1, 128])
    let attentionMaskTensor = try! ORTTensor(int64Values: attentionMask, dimensions: [1, 128])

    let inputs: [String: ORTTensor] = [
        "input_ids": inputIdsTensor,
        "attention_mask": attentionMaskTensor
    ]

    let outputs = try! session.run(withInputs: inputs)
    return outputs["output"] as! [Float]  // Adjust "output" to match your model’s output name
}

// Search function
func searchIcons(query: String, topK: Int = 5) -> [[String: String]] {
    let (iconEmbeddings, iconMetadata) = loadData()
    let (inputIds, attentionMask) = getTokenizedInput(query: query)
    let queryEmbedding = getEmbedding(inputIds: inputIds, attentionMask: attentionMask)

    var similarities: [(Int, Float)] = []
    for (index, iconEmb) in iconEmbeddings.enumerated() {
        let sim = cosineSimilarity(queryEmbedding, iconEmb)
        similarities.append((index, sim))
    }

    let topIndices = similarities
        .sorted { $0.1 > $1.1 }
        .prefix(topK)
        .map { $0.0 }

    return topIndices.map { iconMetadata[$0] }
}

// Example usage
let query = "star"
let results = searchIcons(query: query)
for icon in results {
    print("Icon ID: \(icon["id"] ?? ""), Tags: \(icon["tags"] ?? "")")
}