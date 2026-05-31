# Information Retrieval System Assignment

## Group Information

**Group Number:** 51

| Student ID | Student Name | Contribution (%) |
|------------|--------------|------------------|
| 2025AA05350 | AKANKSHA PARMAR | 100% |
| 2025AA05359 | ROHIT GUPTA | 100% |
| 2025AA05353 | SHEETAL PRAKASH BARANWAL | 100% |

---

## Overview

This project implements an end-to-end Information Retrieval (IR) System using Python and Streamlit. The system demonstrates text preprocessing, phrase query processing, dictionary search structures, tolerant retrieval techniques, and experimental analysis as required in the assignment.

---

## Prerequisites

- Python 3.8 or higher
- pip package manager

---

## Install Dependencies

Open a terminal in the project folder and run:

```bash
pip install -r requirements.txt
```

If a `requirements.txt` file is not available, install the required libraries manually:

```bash
pip install streamlit pandas nltk
```

---

## Download NLTK Resources

Run Python and execute:

```python
import nltk

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
```

---

## Run the Application

Open a terminal in the project directory and execute one of the following commands:

### Option 1

```bash
streamlit run app.py
```

### Option 2 (Recommended if Streamlit command is not recognized)

```bash
python -m streamlit run app.py
```

After execution, the Streamlit application will automatically open in your default web browser.

---

## Project Modules

- Part A – Streamlit Workflow (Home Page)
- Part B – Text Preprocessing
- Part C – Phrase Query Processing
- Part D – Dictionary Search (Binary Search Tree and B-Tree)
- Part E – Tolerant Retrieval
- Part G – Inference and Discussion

---

## Usage

1. Launch the application using one of the commands above.
2. Upload one or more `.txt` files or use the provided sample dataset.
3. Navigate through Parts A–G using the sidebar menu.
4. Execute experiments and observe the retrieval results.
5. Review the final conclusions in Part G.

---

## Assignment Implementation Mapping

### Part A: Streamlit-Based End-to-End Workflow

1. Upload a text dataset or document collection – Implemented in Home Page
2. View uploaded documents – Implemented in Home Page
3. Enter search queries from the front end – Implemented in Parts C, D and E
4. Select preprocessing and retrieval options from the Streamlit interface
5. Display intermediate and final outputs on the front end

### Part B: Text Preprocessing

Implemented Features:

- Tokenization
- Lowercasing
- Stop Word Removal
- Hyphen Handling
- Stemming
- Lemmatization
- Stemming vs Lemmatization Comparison
- Inverted Index Creation

### Part C: Phrase Query Processing

Implemented Features:

- Biword Index Representation
- Positional Index Representation
- Query Result using Biword Index
- Query Result using Positional Index
- False Positive Analysis
- Phrase Retrieval Accuracy Comparison

### Part D: Dictionary Search

Implemented Features:

- Binary Search Tree (BST)
- B-Tree
- Dictionary Search Operations
- Search Time Comparison
- Performance Analysis

### Part E: Tolerant Retrieval

Implemented Features:

- Wildcard Queries (Permuterm Index)
- Spelling Correction
- Edit Distance Correction
- K-Gram Index
- Phonetic Correction (Soundex)

### Part G: Inference and Discussion

Implemented Features:

- Retrieval Quality Analysis
- Stemming vs Lemmatization Evaluation
- Phrase Query Accuracy Comparison
- BST vs B-Tree Analysis
- Retrieval Tolerance Evaluation
- System Limitations
- Future Improvements

---

## Project Structure

```text
IR_Assignment_Group51/
│
├── app.py
├── README.md
├── requirements.txt
│
├── modules/
│   ├── preprocessing.py
│   ├── phrase_query.py
│   ├── dictionary_search.py
│   ├── tolerant_retrieval.py
│   └── inference.py
│
└── sample_docs/
```

---

## Contribution Summary

All group members actively participated in the design, implementation, testing, evaluation, and documentation of the Information Retrieval System.

### Areas of Contribution

- Streamlit Application Development
- Text Preprocessing and Inverted Index Construction
- Phrase Query Processing using Biword and Positional Indexes
- Dictionary Search using BST and B-Tree
- Tolerant Retrieval using Permuterm Index, K-Gram Index, Edit Distance, and Soundex
- Experimental Analysis and Performance Evaluation
- Project Documentation and Report Preparation

---

## Authors

**Group 51**

- AKANKSHA PARMAR (2025AA05350)
- ROHIT GUPTA (2025AA05359)
- SHEETAL PRAKASH BARANWAL (2025AA05353)

Academic Year: 2025–26
