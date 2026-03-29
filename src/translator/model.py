# The following links were used to code the ResNet model:
# (1) https://dev.to/santoshpremi/fine-tuning-a-pre-trained-model-in-pytorch-a-step-by-step-guide-for-beginners-4p6l
# (2) https://www.mathworks.com/help/deeplearning/ref/resnet18.html
# This was particularly used in the 'Implementation of ResNet model' section

# The main training and validation sections were inspired by resource used for CNN model
# https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html 

# The lines of code related to wandB is learnt from:
# https://docs.wandb.ai/quickstart

# To run the file:
# Current Directory: .../PytorchImageClassifier
# Run the following command: python ResNet18ImageClassifier.py

import os
import torch
import torch.nn as nn
import torchvision
import torchvision.models as models
import torchvision.transforms as transforms
#import wandb
from torch.optim import lr_scheduler
from torch.utils.data import DataLoader

# Initialises the next run (NEED TO SPECIFY THE NAME)
#wandb.init(project="duckIt", name="resnet18-run")


def main():
    num_classes = 94

    # List of all classnames
    class_names = [i for i in range(num_classes)]

    # ===================== Print all class names =====================
    def count_images_in_folder(folder_path):
        # List of common image file extensions
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']

        # Count files with image extensions
        image_count = sum(1 for file in os.listdir(folder_path) 
                        if os.path.splitext(file)[1].lower() in image_extensions)
        
        return image_count

    # Print the total number of class names
    for class_name in class_names:
        print(f"Total training images for {class_name}: {count_images_in_folder(f'data/training/{class_name}')}")
        print(f"Total validation images for {class_name}: {count_images_in_folder(f'data/validation/{class_name}')}")


    # ===================== Implentation of ResNet model =====================
    # Main Hyperparameters
    LEARNING_RATE = 0.007
    EPOCH_NUMBER = 20
    BATCH_SIZE = 2
    STEP_SIZE = 7

    # Load in the resnet18 classifier
    resnet18 = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)

    # Replace the last fully connected layer for class number
    num_classes = len(class_names)
    num_ftrs = resnet18.fc.in_features
    resnet18.fc = nn.Linear(num_ftrs, num_classes)

    # Define loss function, optimizer, and learning_rate scheduler
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(resnet18.parameters(), LEARNING_RATE)
    scheduler = lr_scheduler.StepLR(optimizer, step_size=STEP_SIZE, gamma=0.1)

    ## GET ALL THE DATA ##
    # Preprocess grayscale dolphin images for neural network input:
    # 1. Convert to tensor (0-1 range)
    # 2. Normalise using mean=0.5, std=0.5 for better training stability
    transform = transforms.Compose(
        [transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

    trainingImagesDataset = torchvision.datasets.ImageFolder(root='data/training', transform=transform)
    trainingDataLoader = DataLoader(trainingImagesDataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=4)
    validationImagesDataset = torchvision.datasets.ImageFolder(root='data/validation', transform=transform)
    validationDataLoader = DataLoader(validationImagesDataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=4)

    # Get cpu, gpu or mps device for training
    device = (
        "cuda"
        if torch.cuda.is_available()
        else "mps"
        if torch.backends.mps.is_available()
        else "cpu"
    )
    print(f"Using {device} device")

    # Move model to the device
    resnet18.to(device)

    # ===================== Training and Validating ResNet model =====================

    # wandb config
    # wandb.config.update({
    #     "learning_rate":LEARNING_RATE,
    #     "epochs": EPOCH_NUMBER,
    #     "batch_size": BATCH_SIZE,
    #     "model": "ResNet18",
    #     "optimizer": "Adam"
    # })

    best_val_accuracy = 0 # Initialise for early stopping parameters
    log_interval = 50  # Define number of times
    for epoch in range(EPOCH_NUMBER):
        # ===================== Training Phase =====================
        resnet18.train() # Set model to training mode
        running_loss = 0.0 # For tracking loss over 50 batches
        train_loss = 0.0 # For tracking total epoch loss

        # Iterate over batches
        for i, data in enumerate(trainingDataLoader, start=1):
            # Get and prepare data
            inputs, labels = data
            inputs, labels = inputs.to(device), labels.to(device)

            # Reset gradients
            optimizer.zero_grad()

            # Forward pass
            outputs = resnet18(inputs)
            loss = criterion(outputs, labels)

            # Backward pass and optimise
            loss.backward()
            optimizer.step()

            # Update loss trackers
            running_loss += loss.item()
            train_loss += loss.item()

            # Log every 50 batches
            # if i % log_interval == 0:
            #     wandb.log({
            #         "epoch": epoch, 
            #         "batch": i, 
            #         "training_loss": running_loss / log_interval
            #     })
            #     running_loss = 0.0
        
        # Calculate average training loss for the epoch
        avg_train_loss = train_loss / len(trainingDataLoader)

        # ===================== Validation Phase =====================
        resnet18.eval() # Set model to evaluation mode
        correct, total = 0, 0
        val_loss = 0.0

        # Initialise per-class metrics
        class_correct = [0] * len(class_names)
        class_total = [0] * len(class_names)
        confusion_matrix = [[0 for _ in range(num_classes)] for _ in range(num_classes)]

        # No gradient calculation during validation
        with torch.no_grad():
            for data in validationDataLoader:
                images, labels = data
                # Move images and labels to the GPU
                images, labels = images.to(device), labels.to(device)
                
                # Forward pass
                outputs = resnet18(images)
                loss = criterion(outputs, labels)
                val_loss += loss.item()

                # Calculate predictions
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

                # Calculate per-class accuracy
                for class_idx in range(num_classes):
                    mask = (labels == class_idx)
                    class_total[class_idx] += mask.sum().item()
                    class_correct[class_idx] += ((predicted == labels) & mask).sum().item()
                
                # Update confusion matrix
                for true_label, pred_label in zip(labels, predicted):
                    confusion_matrix[true_label.item()][pred_label.item()] += 1

        # Calculate metrics
        accuracy = 100 * correct / total
        avg_val_loss = val_loss / len(validationDataLoader)

        # Calculate per-class accuracies and create list of three values
        class_accuracies = [100 * correct_count / total_count if total_count > 0 else 0 
                        for correct_count, total_count in zip(class_correct, class_total)]
        
        # ===================== Convert Confusion Matrix to Percentages =====================
        # Creates a a confusion matrix
        confusion_matrix_percent = []
        for i in range(num_classes):
            row_total = sum(confusion_matrix[i])  # Total samples for the true class i
            row_percentages = [(100 * count / row_total) if row_total > 0 else 0 for count in confusion_matrix[i]]
            confusion_matrix_percent.append(row_percentages)
        
        # ===================== Logging =====================
        # Log metrics to Weights & Biases
        # wandb.log({
        #     "epoch": epoch,
        #     "train_loss": avg_train_loss,
        #     "validation_loss": avg_val_loss,
        #     "validation_accuracy": accuracy,
        #     "learning_rate": scheduler.get_last_lr()[0],
        #     "bottlenose_accuracy": class_accuracies[0],
        #     "common_accuracy": class_accuracies[1],
        #     "melonheaded_accuracy": class_accuracies[2]
        # })

        # Print epoch summary
        print(f'Epoch {epoch+1}/{EPOCH_NUMBER}:')
        print(f'Training Loss: {avg_train_loss:.3f}')
        print(f'Validation Loss: {avg_val_loss:.3f}')
        print(f'Validation Accuracy: {accuracy:.2f}%')
        print(f'Learning Rate: {scheduler.get_last_lr()[0]:.6f}')
        print('Per-class accuracies:')
        for i in range(len(class_names)):
            print(f'{i}: {class_accuracies[i]:.2f}%')
        
        # Print confusion matrix in percentage form
        print("\nConfusion Matrix (in percentages):")
        for i in range(len(class_names)):
            for j in range(len(class_names)):
                print(f"{class_names[i]}: {confusion_matrix_percent[i][j]:6.2f}% (predicted {j})")

        # ===================== Early stopping =====================
        # Stop the model if the accuracy is not increasing
        if accuracy > best_val_accuracy:
            print(f'Validation accuracy improved from {best_val_accuracy:.2f}% to {accuracy:.2f}%')
            best_val_accuracy = accuracy
            torch.save(resnet18.state_dict(), "best_resnet18_2.pth")
        else:
            print(f'Early stopping triggered after epoch {epoch+1}')
            break
        
        # Step the scheduler after validation
        scheduler.step()

    # ================== Final Summary ==================
    print('Finished Training')
    print(f'\nBest validation accuracy: {best_val_accuracy:.2f}%')

    #wandb.finish()

if __name__ == "__main__":
    main()