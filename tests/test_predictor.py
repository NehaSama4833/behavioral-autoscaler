import sys, os, torch
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from predictor.model import LoadPredictor

def test_output_shape():
    m = LoadPredictor()
    assert m(torch.rand(8, 20, 4)).shape == (8, 1)
    print("PASS: output shape (8,1)")

def test_output_dtype():
    m = LoadPredictor()
    assert m(torch.rand(1, 20, 4)).dtype == torch.float32
    print("PASS: output dtype float32")

if __name__ == "__main__":
    test_output_shape(); test_output_dtype()
    print("\nAll predictor tests passed.")
