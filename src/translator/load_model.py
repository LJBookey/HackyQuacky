
import os
import torch
import torch.nn as nn
import torchvision
import torchvision.models as models
import torchvision.transforms as transforms
#import wandb
from torch.optim import lr_scheduler
from torch.utils.data import DataLoader

def main():
    num_classes = 4
    class_names = list(range(num_classes)) 
    
    resnet18 = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)

    # Replace the last fully connected layer for class number
    num_classes = len(class_names)
    num_ftrs = resnet18.fc.in_features
    resnet18.fc = nn.Linear(num_ftrs, num_classes)

    resnet18.load_state_dict(torch.load("best_resnet18.pth"))
    resnet18.eval()


if __name__ == "__main__":
    main()