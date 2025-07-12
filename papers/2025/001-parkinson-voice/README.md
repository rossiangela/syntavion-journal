---
title: "Diagnosing Parkinson's Disease from Voice Using Random Forest and Conversion in TensorFlow Lite"
authors:
  - name: "Angela Rossi"
    affiliation: "Syntavion Publishing"
    email: "angela.rossi393@gmail.com"
    orcid: "0009-0001-8485-8666"
abstract: |
  This project presents a machine learning system for diagnosing Parkinson's disease 
  through voice analysis using Random Forest classification. The model achieved 92% 
  overall accuracy and 97% recall for Parkinson's patients, with an AUC-ROC of 0.96.
keywords: ["Parkinson's disease", "voice analysis", "machine learning", "Random Forest", "TensorFlow Lite", "medical diagnosis", "mobile health", "biomedical engineering"]
---

# Summary

This research presents a machine learning approach for diagnosing Parkinson's disease through voice analysis. Using a Random Forest classifier optimized with GridSearchCV, the system analyzes 22 voice features to distinguish between healthy individuals and those with Parkinson's disease. The model was successfully converted to TensorFlow Lite for deployment on mobile devices, achieving 92% accuracy with 97% recall for Parkinson's patients.

# Statement of Need

Parkinson's disease affects millions worldwide, and early detection is crucial for effective treatment. Traditional diagnostic methods rely heavily on clinical observation and may miss early-stage symptoms. Voice analysis offers a non-invasive, accessible approach for Parkinson's screening, as vocal impairments are among the earliest symptoms. This work addresses the need for automated, mobile-ready diagnostic tools that can support healthcare professionals in clinical settings.

# Methods

## Dataset Overview

The study utilized a dataset containing:
- **Size**: 195 samples with 24 features
- **Class distribution**: 147 Parkinson's patients, 48 healthy controls
- **Features**: Voice characteristics including jitter, shimmer, harmonics, and noise ratios

## Machine Learning Model

A **Random Forest Classifier** was selected for its robustness to noise and effectiveness with small, unbalanced datasets. The model was optimized using GridSearchCV with the following hyperparameters:

- `n_estimators = 100`: Optimal balance between accuracy and computational efficiency
- `max_depth = None`: Allows trees to grow until minimum samples per leaf
- `min_samples_split = 5`: Prevents overfitting on small sample groups

## Voice Features Analyzed

The system analyzes 22 key voice characteristics:

**Frequency Measures:**
- MDVP:Fo(Hz) - Average fundamental frequency
- MDVP:Fhi(Hz) - Maximum frequency  
- MDVP:Flo(Hz) - Minimum frequency

**Jitter Measures (frequency variation):**
- MDVP:Jitter(%), MDVP:Jitter(Abs), MDVP:RAP, MDVP:PPQ, Jitter:DDP

**Shimmer Measures (amplitude variation):**
- MDVP:Shimmer, MDVP:Shimmer(dB), Shimmer:APQ3, Shimmer:APQ5, MDVP:APQ, Shimmer:DDA

**Noise Measures:**
- NHR - Noise-harmonic ratio
- HNR - Harmonic-to-noise ratio

**Nonlinear Measures:**
- RPDE - Entropy of voice signal
- DFA - Detrended Fluctuation Analysis
- spread1, spread2 - Nonlinear voice measurements
- D2 - Vocal dynamics dimension
- PPE - Prediction entropy

## TensorFlow Lite Conversion

The trained Random Forest model was converted to TensorFlow Lite for mobile deployment:

- **Input shape**: (None, 22) - Variable batch size with 22 features
- **Output**: Probability distribution for two classes
- **Example inference**: [0.0118, 0.9881] → Parkinson's diagnosis (98.8% confidence)

# Results

## Model Performance

The Random Forest classifier demonstrated excellent performance:

- **Overall Accuracy**: 92%
- **Precision**: 0.93 (Parkinson's class)
- **Recall**: 0.97 (Parkinson's class) 
- **F1-Score**: 0.95 (Parkinson's class)
- **AUC-ROC**: 0.96

## Confusion Matrix Analysis

Out of 39 test samples, the model made only 3 errors:
- **True Negatives**: 8 (correctly identified healthy)
- **False Positives**: 2 (healthy misclassified as Parkinson's)
- **False Negatives**: 1 (Parkinson's misclassified as healthy)
- **True Positives**: 28 (correctly identified Parkinson's)

The high recall (97%) for Parkinson's detection is particularly important in medical applications, as missing positive cases has more serious consequences than false alarms.

## Mobile Deployment

The TensorFlow Lite conversion enables:
- Real-time inference on smartphones and embedded devices
- Lightweight model suitable for resource-constrained environments
- Potential for field deployment in clinical and home settings

# Discussion

## Clinical Implications

The 97% recall rate suggests this system could effectively identify most Parkinson's patients, making it valuable for screening programs. The non-invasive nature of voice analysis makes it particularly suitable for:

- Early detection programs
- Remote monitoring of disease progression
- Screening in underserved areas with limited access to specialists

## Technical Advantages

Random Forest was chosen for several key advantages:
- Robust performance with small, unbalanced datasets
- No requirement for extensive data preprocessing
- Built-in feature importance estimation
- Resistance to overfitting

## Limitations and Future Work

**Current Limitations:**
- Dataset size (195 samples) limits generalizability
- Class imbalance may affect performance on larger populations
- Limited to English-speaking populations

**Future Improvements:**
- **Dataset Balancing**: Implement SMOTE (Synthetic Minority Over-sampling Technique) to address class imbalance
- **Feature Analysis**: Utilize Random Forest feature importance to identify most discriminative voice characteristics
- **Expanded Datasets**: Include multilingual and larger patient populations
- **Longitudinal Studies**: Track disease progression over time

# Conclusion

This work demonstrates the feasibility of automated Parkinson's disease detection through voice analysis using machine learning. The Random Forest classifier achieved excellent performance with 92% accuracy and 97% recall, successfully converted to TensorFlow Lite for mobile deployment.

The system's high recall rate makes it particularly valuable for clinical screening, while the mobile-ready format enables deployment in diverse healthcare settings. This research contributes to the growing field of digital health tools and demonstrates the potential for AI-assisted medical diagnosis.

**Code Availability:** Complete implementation available at [Google Colab](https://colab.research.google.com/drive/1qGACQUX93sNMQaCItZWpgJcER7USNs5y?usp=sharing)

# References

1. Sakar, C.O. et al. (2013). Collection and analysis of a Parkinson speech dataset with multiple types of sound recordings. *IEEE Journal of Biomedical and Health Informatics*, 17(4), 828-834.

2. Tsanas, A. et al. (2012). Novel speech signal processing algorithms for high-accuracy classification of Parkinson's disease. *IEEE Transactions on Biomedical Engineering*, 59(5), 1264-1271.

3. Breiman, L. (2001). Random forests. *Machine Learning*, 45(1), 5-32.

4. Little, M.A. et al. (2009). Exploiting nonlinear recurrence and fractal scaling properties for voice disorder detection. *Biomedical Engineering Online*, 8, 23.

5. Abadi, M. et al. (2016). TensorFlow: Large-scale machine learning on heterogeneous systems. *12th USENIX Symposium on Operating Systems Design and Implementation*, 265-283.
