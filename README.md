# Information Retrieval System - Assignment

## Group Information

**Group Number:** 51

| Student ID  | Student Name             | Contribution (%) |
| ----------- | ------------------------ | ---------------- |
| 2025AA05350 | AKANKSHA PARMAR          | 100%             |
| 2025AA05359 | ROHIT GUPTA              | 100%             |
| 2025AA05353 | SHEETAL PRAKASH BARANWAL | 100%             |

---

## Prerequisites

* Python 3.8 or higher
* pip package manager

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

* **Part A** – Streamlit Workflow (Home Page)
* **Part B** – Text Preprocessing (Part B: Text Preprocessing Page)
* **Part C** – Phrase Query Processing (Part C: Phrase Query Processing Page)
* **Part D** – Dictionary Search (Binary Search Tree and B-Tree) (Part D: Dictionary Search: Binary Search Tree and B-Tree Page)
* **Part E** – Tolerant Retrieval (Part E: Tolerant Retrieval Page)
* **Part G** – Inference and Discussion (Part G – Inference and Discussion Page)

---

## Usage

1. Launch the application using one of the commands above.
2. Upload one or more `.txt` files or use the provided sample dataset in the Home Page.
3. Navigate through Parts A–G using the sidebar menu.
4. Execute experiments and observe the retrieval results.
5. Review the final conclusions in Part G.

---

## Assignment Requirements and Implementation Mapping

### Part A: Streamlit-Based End-to-End Workflow

#### Implemented Features

1. **Upload a text dataset or document collection** – Implemented in Home Page.
2. **View uploaded documents** – Implemented in Home Page.
3. **Enter search queries from the front end** – Implemented in Part C, Part D and Part E.

##### Query Types

* In Part C, users enter multi-word phrases (e.g., `"machine learning"`).
* In Part D, users type individual target vocabulary words to probe the structural indices.
* In Part E, users can enter imperfect inputs, such as:

  * Wildcard expressions (e.g., `learn*`)
  * Typographical errors (e.g., `machne`)
  * Phonetic inputs (e.g., `learnin`)

4. **Select preprocessing and retrieval options from the Streamlit interface** – Implemented in Home, Part B, and Part C.

##### Home Page

* Users select the dataset source.
* Users dynamically choose all files or a subset of files.

##### Part B: Text Preprocessing

Users can select:

* Tokenization
* Lowercasing
* Stop Word Removal
* Hyphen Handling
* Stemming
* Lemmatization
* Stemming vs Lemmatization Comparison
* Inverted Index Creation

using the provided radio button interface.

##### Part C: Phrase Query Processing

Users can switch dynamically between:

* Biword Index Representation
* Positional Index Representation

using the radio button interface.

5. **Display intermediate and final outputs on the front end** – Implemented throughout all modules.

##### Intermediate Outputs

* Part B displays dynamic preprocessing metrics.

##### Final Retrieval Outputs

* Part C displays phrase query results.
* Part D displays BST and B-Tree search results.
* Part E displays tolerant retrieval and correction outputs.

Streamlite Page Link : https://irassignmentgroup51-zj6epdhd5kk8jufezqypem.streamlit.app/
---

## Authors

### Group 51

* AKANKSHA PARMAR (2025AA05350)
* ROHIT GUPTA (2025AA05359)
* SHEETAL PRAKASH BARANWAL (2025AA05353)
