import streamlit as st
import pandas as pd
import nltk
import re

from collections import defaultdict
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

# --------------------------------------------------
# NLTK Downloads
# --------------------------------------------------

try:
    nltk.data.find("corpora/stopwords")
except:
    nltk.download("stopwords", quiet=True)

try:
    nltk.data.find("corpora/wordnet")
except:
    nltk.download("wordnet", quiet=True)


# --------------------------------------------------
# Simple Tokenizer
# --------------------------------------------------

def tokenize(text):
    return re.findall(r"\b\w+\b", text)


# --------------------------------------------------
# Jaccard Similarity
# --------------------------------------------------

def jaccard_similarity(set1, set2):

    if len(set1.union(set2)) == 0:
        return 0

    return len(set1.intersection(set2)) / len(set1.union(set2))


# --------------------------------------------------
# Main Function
# --------------------------------------------------

def show_preprocessing_page():

    st.title("⚙️ Part B : Text Preprocessing")

    st.warning("⚠️ **CRITICAL NOTE:** You **MUST** go to **PART B, Part C, Part D and Part E** after text file selection on **Home page** and actively select preprocessing option first! Otherwise, some of page can display stale cache states.")

    st.markdown("""
    ### Part B : Text Preprocessing

    Select a document and preprocessing technique to view results.
    """)

    if "documents" not in st.session_state:

        st.warning(
            "Please load a dataset from the Home page first."
        )
        return

    documents = st.session_state["documents"]

    if len(documents) == 0:

        st.warning(
            "No documents available."
        )
        return

    # ==================================================
    # Select Document
    # ==================================================

    selected_doc = st.selectbox(
        "📄 Select Document",
        list(documents.keys())
    )

    text = documents[selected_doc]

    st.subheader("Document View")

    st.text_area(
        "Document Content",
        value=text,
        height=250
    )

    # ==================================================
    # Select Preprocessing Technique 
    # ==================================================

    preprocessing_option = st.radio(
        "Select Preprocessing Technique",
        [
            "Tokenization",
            "Lowercasing",
            "Stop Words List",
            "Stop Word Removal",
            "Hyphen Handling",
            "Stemming",
            "Lemmatization",
            "Stemming vs Lemmatization Comparison",
            "Inverted Index Creation"
        ]
    )

    # ==================================================
    # Common Processing
    # ==================================================

    tokens = tokenize(text)

    lower_tokens = [
        token.lower()
        for token in tokens
    ]

    stop_words = set(
        stopwords.words("english")
    )

    filtered_tokens = [
        token
        for token in lower_tokens
        if token.isalpha()
        and token not in stop_words
    ]

    hyphen_text = re.sub(
        r"-",
        " ",
        text.lower()
    )

    hyphen_tokens = tokenize(
        hyphen_text
    )

    stemmer = PorterStemmer()

    stemmed_tokens = [
        stemmer.stem(token)
        for token in filtered_tokens
    ]

    lemmatizer = WordNetLemmatizer()

    lemmatized_tokens = [
        lemmatizer.lemmatize(token)
        for token in filtered_tokens
    ]

    # ==================================================
    # Background Index Synchronization
    # ==================================================
    
    global_inverted_index = defaultdict(list)
    
    for doc_name, doc_text in documents.items():
        doc_hyphenated = re.sub(r"-", " ", doc_text.lower())
        doc_toks = tokenize(doc_hyphenated)
        doc_fil = [t for t in doc_toks if t.isalpha() and t not in stop_words]
        
        if preprocessing_option == "Stemming":
            doc_final = [stemmer.stem(t) for t in doc_fil]
        elif preprocessing_option == "Lemmatization":
            doc_final = [lemmatizer.lemmatize(t) for t in doc_fil]
        else:
            doc_final = doc_fil
            
        for term in sorted(set(doc_final)):
            global_inverted_index[term].append(doc_name)
            
    st.session_state["inverted_index"] = dict(global_inverted_index)
    st.session_state["prep_config"] = {
        "lower": True,
        "stop": True,
        "hyphen": True,
        "norm": "Stemming" if preprocessing_option == "Stemming" else ("Lemmatization" if preprocessing_option == "Lemmatization" else None)
    }

    # ==================================================
    # Tokenization
    # ==================================================

    if preprocessing_option == "Tokenization":

        st.subheader("Tokenization")

        st.metric(
            "Total Tokens",
            len(tokens)
        )

        st.write(tokens[:100])

        st.info(
            f"💡 UI Safe Mode: Displaying first 100 tokens out of {len(tokens)} total tokens."
        )

    # ==================================================
    # Lowercasing
    # ==================================================

    elif preprocessing_option == "Lowercasing":

        st.subheader("Lowercasing")

        st.metric(
            "Total Lowercased Tokens",
            len(lower_tokens)
        )

        st.write(lower_tokens[:100])

        st.info(
            f"💡 UI Safe Mode: Displaying first 100 lowercased tokens out of {len(lower_tokens)} total tokens."
        )

    # ==================================================
    # Stop Words List 
    # ==================================================

    elif preprocessing_option == "Stop Words List":

        st.subheader("🗂️ Document-Specific Stop Words Analysis")

        # Extract stop words localized inside the specific active text target
        words_in_doc = [t.lower() for t in tokens if t.isalpha()]
        stop_words_found_in_doc = [w for w in words_in_doc if w in stop_words]
        
        from collections import Counter
        stop_word_counts = Counter(stop_words_found_in_doc)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                label="Total Stop Word Occurrences in File",
                value=len(stop_words_found_in_doc)
            )
        with col2:
            st.metric(
                label="Unique Stop Word Types Identified",
                value=len(stop_word_counts)
            )

        if stop_word_counts:
            stop_breakdown = pd.DataFrame({
                "Intercepted Stop Word": list(stop_word_counts.keys()),
                "Frequency in This Document": list(stop_word_counts.values())
            }).sort_values(by="Frequency in This Document", ascending=False)
            
            stop_breakdown.index = [str(i) for i in range(1, len(stop_breakdown) + 1)]

            st.dataframe(stop_breakdown, use_container_width=True)
        else:
            st.info("No standard English stop words were detected in this specific document text.")
            
        st.caption(f"ℹ️ Analysis run against the global vocabulary filter set across: `{selected_doc}`")

    # ==================================================
    # Stop Word Removal
    # ==================================================

    elif preprocessing_option == "Stop Word Removal":

        st.subheader("Stop Word Removal")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Before (Lowercased)",
                len(lower_tokens)
            )

        with col2:
            st.metric(
                "After (Cleaned)",
                len(filtered_tokens)
            )

        st.write(filtered_tokens[:100])

        st.info(
            f"💡 UI Safe Mode: Displaying first 100 cleaned tokens out of {len(filtered_tokens)} total filtered tokens."
        )

    # ==================================================
    # Hyphen Handling
    # ==================================================

    elif preprocessing_option == "Hyphen Handling":

        st.subheader("Hyphen Handling")

        st.metric(
            "Total Tokens (After Hyphen Split)",
            len(hyphen_tokens)
        )

        st.write("After replacing hyphens with spaces:")

        st.write(hyphen_tokens[:100])

        st.info(
            f"💡 UI Safe Mode: Displaying first 100 tokens out of {len(hyphen_tokens)} total handled tokens."
        )

    # ==================================================
    # Stemming
    # ==================================================

    elif preprocessing_option == "Stemming":

        st.subheader("Stemming")

        st.metric(
            "Total Stemmed Corpus Vocabulary Size",
            len(set(stemmed_tokens))
        )

        skinny_df = pd.DataFrame({
            "Original": filtered_tokens[:30],
            "Stemmed": stemmed_tokens[:30]
        })
        skinny_df.index = [str(i) for i in range(1, len(skinny_df) + 1)]

        st.dataframe(
            skinny_df,
            use_container_width=True
        )
        
        st.info("💡 Snapshot view displaying the first 30 pipeline transformations.")

    # ==================================================
    # Lemmatization
    # ==================================================

    elif preprocessing_option == "Lemmatization":

        st.subheader("Lemmatization")

        st.metric(
            "Total Lemmatized Corpus Vocabulary Size",
            len(set(lemmatized_tokens))
        )

        skinny_df = pd.DataFrame({
            "Original": filtered_tokens[:30],
            "Lemmatized": lemmatized_tokens[:30]
        })
        skinny_df.index = [str(i) for i in range(1, len(skinny_df) + 1)]

        st.dataframe(
            skinny_df,
            use_container_width=True
        )
        
        st.info("💡 Snapshot view displaying the first 30 pipeline transformations.")

    # ==================================================
    # Stemming vs Lemmatization
    # ==================================================

    elif preprocessing_option == "Stemming vs Lemmatization Comparison":

        st.subheader(
            "📊 Stemming vs Lemmatization Comparison"
        )

        comparison_size = min(
            25,
            len(filtered_tokens)
        )

        comparison_df = pd.DataFrame({

            "Original":
            filtered_tokens[:comparison_size],

            "Stemmed":
            stemmed_tokens[:comparison_size],

            "Lemmatized":
            lemmatized_tokens[:comparison_size]

        })
        comparison_df.index = [str(i) for i in range(1, len(comparison_df) + 1)]

        st.dataframe(
            comparison_df,
            use_container_width=True
        )

        # ------------------------------------------
        # Similarity Calculation
        # ------------------------------------------

        original_set = set(filtered_tokens)

        stem_set = set(stemmed_tokens)

        lemma_set = set(lemmatized_tokens)

        stem_similarity = jaccard_similarity(
            original_set,
            stem_set
        )

        lemma_similarity = jaccard_similarity(
            original_set,
            lemma_set
        )

        # ------------------------------------------
        # Retrieval Quality Comparison
        # ------------------------------------------

        stem_unique_terms = len(stem_set)

        lemma_unique_terms = len(lemma_set)

        metrics_df = pd.DataFrame({

            "Metric": [
                "Unique Terms",
                "Jaccard Similarity"
            ],

            "Stemming": [
                stem_unique_terms,
                round(stem_similarity, 4)
            ],

            "Lemmatization": [
                lemma_unique_terms,
                round(lemma_similarity, 4)
            ]

        })

        st.subheader(
            "📈 Retrieval Quality Comparison"
        )

        st.dataframe(
            metrics_df,
            hide_index=True,
            use_container_width=True
        )

        # ------------------------------------------
        # Inference
        # ------------------------------------------

        st.subheader("📌 Inference")

        if lemma_similarity >= stem_similarity:

            st.success(
                f"""
Lemmatization is more suitable for the selected dataset.

Unique Terms:
{lemma_unique_terms} (Lemmatization)
vs
{stem_unique_terms} (Stemming)

Jaccard Similarity:
{round(lemma_similarity,4)}
vs
{round(stem_similarity,4)}

Conclusion:
Lemmatization preserves meaningful dictionary words and
retains semantic information while reducing word variations.
Therefore, it provides better retrieval quality for this dataset.
"""
            )

        else:

            st.success(
                f"""
Stemming is more suitable for the selected dataset.

Unique Terms:
{stem_unique_terms} (Stemming)
vs
{lemma_unique_terms} (Lemmatization)

Jaccard Similarity:
{round(stem_similarity,4)}
vs
{round(lemma_similarity,4)}

Conclusion:
Stemming reduces vocabulary size more aggressively,
which may improve retrieval efficiency for this dataset.
"""
            )

    # ==================================================
    # Inverted Index Creation
    # ==================================================

    elif preprocessing_option == "Inverted Index Creation":

        st.subheader("Inverted Index Creation")

        inverted_df = pd.DataFrame(
            [
                [term, ", ".join(postings)] 
                for term, postings 
                in list(st.session_state["inverted_index"].items())[:100]
            ],
            columns=[
                "Term",
                "Posting List"
            ]
        )
        inverted_df.index = [str(i) for i in range(1, len(inverted_df) + 1)]

        st.metric(
            "Unique Terms",
            len(st.session_state["inverted_index"])
        )

        st.dataframe(
            inverted_df,
            use_container_width=True
        )

        st.success(
            f"Inverted Index created successfully with {len(st.session_state['inverted_index'])} unique terms."
        )
        st.info("💡 Displaying first 100 dictionary entries in alphabetical order.")
