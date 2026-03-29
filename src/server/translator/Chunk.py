from pathlib import Path
from PIL import Image
import numpy as np

class Chunk:
    def __init__(self):
        self.path = None
        self.label = None
        self.spec = None

    def load_chunk_from_path(self, input_path):
        self.path = input_path
        self.spec = Image.open(self.path).convert('L')
        self.spec = np.array(self.spec, dtype=np.float32) / 255.0
        # self.spec = self.spec.flatten()

        return self.spec

        
    