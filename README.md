# Age and Gender Prediction using CNN and ResNet50

A deep learning-based computer vision project that predicts a person's **age** and **gender** from facial images using a **multi-output Convolutional Neural Network (CNN)** built with **Keras** and **ResNet50 transfer learning**.

---

## Overview

Built a multi-output CNN model for simultaneous age and gender prediction from facial images using the UTKFace dataset. The project uses transfer learning with pretrained ResNet50 for deep facial feature extraction and fine-tuning for task-specific learning. Images were preprocessed and augmented using ImageDataGenerator to improve generalization and reduce overfitting. The architecture consists of a shared CNN backbone with two separate output branches: one for age prediction using regression and another for gender classification using sigmoid activation. The model was trained using the Adam optimizer along with EarlyStopping and ReduceLROnPlateau callbacks for stable convergence and improved validation performance.

---

## Features

* Multi-output CNN architecture
* Transfer Learning using ResNet50
* Fine-tuning of pretrained layers
* Real-time image preprocessing and augmentation
* Simultaneous age and gender prediction
* Early stopping and adaptive learning rate scheduling
* Batch-wise memory-efficient training pipeline

---

## Dataset

Dataset used: UTKFace Dataset(https://www.kaggle.com/datasets/jangedoo/utkface-new) 

The dataset contains facial images with labels embedded directly in filenames.

Example:

```text
25_0_2_20170116174525125.jpg
```

Where:

* `25` → Age
* `0` → Gender (Male)
* `2` → Ethnicity

---

## Tech Stack

### Languages & Libraries

* Python
* Keras
* NumPy
* Pandas
* Matplotlib

### Deep Learning Concepts Used

* CNN (Convolutional Neural Networks)
* Transfer Learning
* Fine-Tuning
* Multi-Task Learning
* Data Augmentation

---

## Project Workflow

### 1. Dataset Preparation

* Downloaded dataset from Kaggle
* Extracted image files
* Parsed filenames to extract labels
* Created structured dataframe

### 2. Data Preprocessing

* Image resizing
* Pixel normalization
* Data augmentation using `ImageDataGenerator`

### 3. Model Architecture

* Used pretrained ResNet50 as feature extractor
* Removed original classification head
* Added custom dense layers
* Created separate branches for:

  * Age Prediction
  * Gender Prediction

### 4. Model Training

* Adam Optimizer
* MAE Loss for age prediction
* Binary Crossentropy Loss for gender prediction
* EarlyStopping and ReduceLROnPlateau callbacks

### 5. Evaluation

* Evaluated model on unseen validation images
* Measured:

  * Age MAE
  * Gender Accuracy

---

## Why ResNet50?

ResNet50 was selected because:

* It is pretrained on ImageNet
* Provides powerful feature extraction
* Uses residual connections to avoid vanishing gradients
* Improves accuracy and convergence speed

---

## Data Augmentation Techniques

The following augmentations were applied during training:

* Rotation
* Width Shift
* Height Shift
* Zoom
* Shear Transformation
* Horizontal Flip

This improves generalization and reduces overfitting.

---

## Training Strategy

* Transfer Learning with Fine-Tuning
* Low Learning Rate (`0.0001`)
* Multi-output loss balancing
* Batch-wise training pipeline
* Adaptive learning rate reduction

---

## Key Learnings

Through this project, the following concepts were implemented practically:

* Transfer Learning
* CNN-based Feature Extraction
* Fine-Tuning
* Multi-output Neural Networks
* Image Augmentation

---

