# Steel_Oxidation_Analysis

Antony Morales-Cervantes [![ORCID](https://img.shields.io/badge/ORCID-0000--0003--3669--2638-green)](https://orcid.org/0000-0003-3669-2638); Héctor Javier Vergara-Hernández [![ORCID](https://img.shields.io/badge/ORCID-0000--0001--6224--1027-green)](https://orcid.org/0000-0001-6224-1027); Edgar Guevara [![ORCID](https://img.shields.io/badge/ORCID-0000--0002--2313--2810-green)](https://orcid.org/0000-0002-2313-2810); Jorge Sergio Téllez-Martínez [![ORCID](https://img.shields.io/badge/ORCID-0000--0003--0587--0059-green)](https://orcid.org/0000-0003-0587-0059); Gerardo Marx Chávez-Campos [![ORCID](https://img.shields.io/badge/ORCID-0000--0003--3945--9903-green)](https://orcid.org/0000-0003-3945-9903)

This repository contains the dataset used in the study titled "Real-Time Detection and Monitoring of Oxide Layer Formation in 1045 Steel Using Infrared Thermography and Advanced Image Processing Algorithms." The research focuses on real-time monitoring of oxide layer formation in AISI 1045 steel using infrared thermography.

## Contents

- **Dataset**: The thermographic data captured during the heating of 1045 steel specimens, including annotated images used for analysis. The data is organized into folders corresponding to different experimental conditions.

  - **Folder Structure**:
    - The `Thermographic_Data` folder contains two subfolders named `Barilla_1` and `Barilla_2`, representing the two steel bars from which the specimens were prepared.
    - Inside each of these subfolders, you will find additional subfolders, each corresponding to an individual experiment conducted on a specific specimen.
    - Within each experiment's folder, you will find the thermograms captured during that experiment. The file names of the thermograms include the acquisition time, which varies between 2 seconds and 5 seconds, depending on the experiment.

- **Scripts**: The Python scripts used for processing and analyzing the thermographic data.
  - **`segment_colors.py`**: Script for segmenting colors in thermographic images to highlight regions of interest.
  - **`limites_probeta.py`**: Identifies the edges of the specimens in the thermographic images for accurate region of interest analysis.
  - **`main.py`**: Main script that coordinates the entire analysis and processing workflow.
  - **`metricasdelmain_correrenvezdelmain.py`**: Alternative script focused on calculating specific metrics rather than running the full analysis.
  - **`oxidation.py`**: Script for analyzing the oxidation process based on the segmented thermographic data.

## Methodology

The dataset comprises thermal images of 1045 steel specimens heated in a controlled environment. The images were annotated to identify regions of oxide layer formation. These annotations were used to evaluate the performance of the image processing algorithms discussed in the study.

## Purpose

This dataset is provided to support further research in the field of infrared thermography and material science. It offers a valuable resource for developing and testing algorithms aimed at detecting and monitoring oxide layer formation in metals.

## How to Use

1. **Clone the Repository**: Download the repository to your local machine.
2. **Explore the Dataset**: Browse through the `Thermographic_Data` folder to access the thermal images and annotations. The dataset is structured to facilitate easy navigation and understanding. Each experiment is documented within its respective folder, making it easy to locate specific sets of thermograms.
3. **Run the Scripts**: Navigate to the `code_scripts` folder and run the provided Python scripts to process and analyze the thermographic data.

## Data availability statement

The thermographic dataset used for monitoring oxide layer formation in 1045 steel is available via [OneDrive](https://1drv.ms/f/s!Ap8bec7rYt6ijOplQ5MLm-zfeX8hXg?e=fhVQMh).

## Authors' contributions

Antony Morales-Cervantes led the data collection. All authors contributed to data analysis and interpretation. All authors approved the final version of the manuscript for publication.

