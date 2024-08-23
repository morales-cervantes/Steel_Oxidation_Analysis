# Code Scripts for Oxide Layer Segmentation

This directory contains all the Python scripts developed and used for the **Oxide Layer Segmentation** project. These scripts are designed to process, analyze, and evaluate thermographic images captured during the oxidation experiments of 1045 steel specimens. Each script serves a specific role in the overall workflow, as described below.

## Contents

1. **`main.py`**: The central script that integrates all the steps in the workflow, from loading data to producing final analysis results.
2. **`limites.py`**: Script for identifying the boundaries of the regions of interest (ROIs) within the thermographic images.
3. **`segment_colors.py`**: Script for background removal and segmentation of the area of interest in the thermographic images.
4. **`oxidation.py`**: Script for analyzing the oxidation process by detecting areas of non-uniform oxide growth.
5. **`matrix.py`**: Script for extracting and saving the temperature matrix from the thermographic images.

## How to Use

### 1. Run the Main Script (`main.py`)

- **Purpose**: The `main.py` script coordinates the entire workflow. It calls other scripts in sequence to process thermographic images, perform segmentation, and analyze the results.
- **Usage**:
  1. Ensure all necessary dependencies are installed (`numpy`, `pandas`, `matplotlib`, `opencv-python`, `flirimageextractor`).
  2. Place your thermographic image files in the correct directory.
  3. Run the script using Python:
     ```bash
     python main.py
     ```
  4. The script will process the images, detect ROIs, segment the oxide layers, and calculate metrics such as precision, recall, F1-Score, and Dice Coefficient.

### 2. Determine the Boundaries (`limites.py`)

- **Purpose**: This script is responsible for detecting the upper, lower, left, and right limits of the regions of interest in the thermographic images.
- **Usage**:
  1. This script is invoked by `main.py` and does not need to be run independently.
  2. It identifies the boundaries of the specimen within the thermal image, which is crucial for accurate segmentation.

### 3. Segment the Background (`segment_colors.py`)

- **Purpose**: The `segment_colors.py` script isolates the area of interest by removing the background from the thermographic images.
- **Usage**:
  1. This script is called by `main.py`.
  2. It utilizes color space transformations and masking techniques to differentiate the oxide layer from the background.

### 4. Analyze Oxidation (`oxidation.py`)

- **Purpose**: This script detects and analyzes the growth of oxide layers on the steel specimen by evaluating the temperature gradients and differences in the segmented areas.
- **Usage**:
  1. This script is also called by `main.py`.
  2. It outputs key metrics related to the oxidation process, helping to assess the uniformity and extent of oxidation.

### 5. Extract the Temperature Matrix (`matrix.py`)

- **Purpose**: The `matrix.py` script extracts the temperature matrix from the thermographic images using the FLIR image extractor and saves it as a CSV or Excel file.
- **Usage**:
  1. This script is called by `main.py`.
  2. It processes the thermographic image files to extract accurate temperature data, which is essential for further analysis.

## Dependencies

Ensure the following Python libraries are installed:

```bash
pip install numpy pandas matplotlib opencv-python flirimageextractor


