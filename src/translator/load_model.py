
import os
import torch
import torch.nn as nn
import torchvision
import torchvision.models as models
import torchvision.transforms as transforms
#import wandb
from torch.optim import lr_scheduler
from torch.utils.data import DataLoader

from PIL import Image
import numpy as np
from Signal import Signal
from Chunk import Chunk
import random
from pathlib import Path

def load_model(path="best_resnet18.pth"):
    num_classes = 94
    class_names = list(range(num_classes)) 
    
    # resnet18 = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    resnet18 = models.resnet18()

    # Replace the last fully connected layer for class number
    num_classes = len(class_names)
    num_ftrs = resnet18.fc.in_features
    resnet18.fc = nn.Linear(num_ftrs, num_classes)

    resnet18.load_state_dict(torch.load(path, map_location="cpu"))

    return resnet18





def classify(model, path):
    sig = Signal(path)
    sig.chunk_up_the_wav(1)
    sig.chunks_to_specs()
    temp_dir = "src/translator/temp"
    temp_path = Path(temp_dir)
    

    sig.save_chunks(folder=temp_dir)

    chunks = []
    chunk_files = temp_path.rglob('*')

    # for chunk_file in chunk_files:
    #     chunk = Chunk()
    #     chunk.load_chunk_from_path(chunk_file)
    #     chunks.append(chunk)
    transform = transforms.Compose(
        [transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))])
    tensors = []

    device = (
        "cuda"
        if torch.cuda.is_available()
        else "mps"
        if torch.backends.mps.is_available()
        else "cpu"
    )
    device = "cpu"
    print(f"Using {device} device")


    for chunk_file in chunk_files:
        img = Image.open(chunk_file).convert("RGB")
        img = transform(img)
        img = img.unsqueeze(0)  
        img.to(device)  
        tensors.append(img)

    # Move model to the device
    model.to(device)

    model.eval()


    labels = []
    for tensor in tensors:
        with torch.no_grad():
            outputs = model(tensor)
            _, pred = torch.max(outputs, 1)


        class_names = list(range(94))

        print("Predicted class: ", str(class_names[pred.item()]))
        labels.append(class_names[pred.item()])

def temp_classify(path):
    sig = Signal(path)
    sig.chunk_up_the_wav(1)

    return [random.randint(0, 94) for _ in range(len(sig.chunks))]


if __name__ == "__main__":
    # rizzy = load_model()
    # classify(rizzy, path="data/audioFiles/XC717918.mp3")

    print(temp_classify(path="data/audioFiles/XC717918.mp3"))