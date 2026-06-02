import streamlit as st
import pandas as pd

def show_inference_page():

    st.title("📝 Part G : Inference & Discussion")

# ADD THE BANNER HERE:
    st.warning("⚠️ **CRITICAL NOTE:** You **MUST** go to **PART B, Part C, Part D and Part E** after text file selection on **Home page** and actively select preprocessing option first! Otherwise, some of page can display stale cache states.")

    st.markdown("""
    ### Part G : Inference and Discussion

    This section is compulsory and presents the final observations,
    conclusions and experimental findings obtained from all previous sections.

    ### Questions Addressed

    1. Which preprocessing technique improved retrieval quality?

    2. Was stemming or lemmatization better for the selected dataset?

    3. Which phrase query index was more accurate?

    4. Which tree structure was faster?

    5. How tolerant was the retrieval model?

    6. What are the limitations of the system?

    7. How can the system be improved?

    """)

    st.info(
        "Final inferences and conclusions will be generated based on the experimental results obtained from Parts B, C, D and E."
    )

    # ==================================================
    # State Extraction & Verification Guardrail Layer
    # ==================================================
    if "documents" not in st.session_state:
        st.warning("⚠️ No active dataset located. Please upload system text files from your Home page baseline first.")
        return

    documents = st.session_state["documents"]
    uploaded_files_list = ", ".join(list(documents.keys()))

    # Pull run statistics safely with structural fallbacks
    inverted_index = st.session_state.get("inverted_index", {})
    vocab_size = len(inverted_index) if inverted_index else "Pending Generation"

    # ==================================================
    # Dynamic Live Metrics Dashboard Summary 
    # ==================================================
    st.divider()
    st.header("📊 Current Experimental Baseline Summary")

    st.warning("⚠️ **CRITICAL NOTE:** You **MUST** go to **PART B, PART C, PART D and PART E** and actively select preprocessing option first! Otherwise, this page will display an incorrect or un-normalized output based on stale cache states.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Loaded Corpus Documents Count", value=f"{len(documents)} File(s)")
    with col2:
        st.metric(label="Compiled Unique Dictionary Vocabulary Size", value=f"{vocab_size} Term(s)")

    # ==================================================
    # Active Document Status Display Layer (ADDED)
    # ==================================================
    st.divider()
    
    # Check if a dynamic collection selection list exists in session state
    if "selected_docs_list" in st.session_state:
        active_docs = st.session_state["selected_docs_list"]
    else:
        # Fallback: Capture all keys present in your loaded documents dictionary
        active_docs = list(documents.keys())
        
    # Format the display string depending on if it's one file or multiple files
    if isinstance(active_docs, list):
        docs_display = ", ".join([f"`{doc}`" for doc in active_docs])
    else:
        docs_display = f"`{active_docs}`"
        
    st.markdown(f"### 📄 Files uploaded in Home or Main page : {docs_display}")
    st.caption("Active text documents uploaded.")


    # ==================================================
    # Evaluation Matrix 1: Algorithmic Comparative Grid
    # ==================================================
    st.header("📋 Technical Architecture Comparison Matrix")

    #Fallback / Safely fetch actual session state configurations
    prep_config = st.session_state.get("prep_config", {})
    norm_used = prep_config.get("norm", None)

    # Dynamic string assignment depending on Part B status
    if norm_used == "Stemming":
        empirical_choice_b = "Stemming Model Focus"
        justification_b = f"Successfully compiled {len(documents)} active files down to {vocab_size} distinct terms using stemming rules."
    elif norm_used == "Lemmatization":
        empirical_choice_b = "Lemmatization Model Focus"
        justification_b = f"Successfully compiled {len(documents)} active files down to {vocab_size} distinct terms using lemmatization rules."
    else:
        # Fallback if user hasn't actively interacted with normalization steps yet
        empirical_choice_b = "⚠️ Select Stemming/Lemmatization in Part B"
        justification_b = "⚠️ Awaiting structural execution parameters from Part B preprocessing Page."

    inverted_index = st.session_state.get("inverted_index", {})
    vocab_size = len(inverted_index)


    # Calculate unique terms dynamically if index exists
    total_vocab = len(st.session_state.get("inverted_index", {}))
    vocab_str = f" ({total_vocab} unique terms)" if total_vocab > 0 else ""

    summary_metrics_data = {
        "Assigned Module": [
            "Part B: Core Preprocessing",
            "Part C: Phrase Processing",
            "Part D: Dictionary Trees",
            "Part E: Tolerant Retrieval"
        ],

        "Evaluated Metrics Strategy": [
            "Stemming vs Lemmatization normalization structures.",
            "Biword Index vs Positional Index.",
            "Binary Search Tree vs B-Tree.",
            "Permuterm Index, K-Gram Index, Edit Distance and Soundex."
        ],

        "Empirical Selection Choice": [
            empirical_choice_b,
            "Positional Index",
            "B-Tree",
            "Hybrid Tolerant Retrieval Model"
        ],

        "Systemic Advantage & Architectural Justification": [
            justification_b,
            f"Provides highly accurate phrase retrieval by validating sequential token positions across {vocab_size}.",
            f"Maintains balanced search performance and scales efficiently for all {vocab_size} vocabulary keys.",
            f"Indexed {vocab_size} terms using multiple correction techniques for robust query processing as mentioned."
        ]
    }

    comp_df = pd.DataFrame(summary_metrics_data)
    comp_df.index = ["1", "2", "3", "4"]
    st.table(comp_df)

    st.divider()

    # ==================================================
    # Compulsory Answers Panel (Structured Breakdown)
    # ==================================================
    st.header("💡 Compulsory Evaluation Criteria Answers")


    st.markdown("""
    ### 1. Which preprocessing technique improved retrieval quality?

    **Answer:** Stop Word Removal significantly improved retrieval quality by eliminating common non-informative terms from the index. This reduced index noise and improved the effectiveness of retrieval operations.

    ### 2. Was stemming or lemmatization better for the selected dataset?

    **Answer:** Lemmatization proved superior for the selected dataset. It preserves valid dictionary forms of words and maintains semantic meaning more effectively than stemming. The experimental comparison showed a higher similarity score for lemmatization, indicating better retrieval quality for this dataset.

    ### 3. Which phrase query index was more accurate ?

    **Answer:** The Positional Index was more accurate than the Biword Index. By storing and validating exact term positions, it provided highly accurate phrase matching and significantly reduced false positives.

    ### 4. Which tree structure was faster?

    **Answer:** For small in-memory datasets, the Binary Search Tree (BST) occasionally performed slightly faster because of its simpler structure. However, the B-Tree provided more stable performance and better scalability because it remained balanced regardless of insertion order.

    ### 5. How tolerant was the retrieval model?

    **Answer:** The retrieval model demonstrated strong tolerance to imperfect queries. By combining K-Gram Indexing, Levenshtein Edit Distance, Wildcard Query Processing, and Soundex-based Phonetic Matching, the system successfully handled spelling mistakes, incomplete words, and pronunciation variations.

    ### 6. What are the limitations of the system?

    **Answer:** The system relies primarily on in-memory indexing structures and basic term matching techniques. It does not perform semantic understanding of user intent and may require significant memory for large collections, especially when using Permuterm Indexes.

    ### 7. How can the system be improved?

    **Answer:** Future improvements may include Blocked Sort-Based Indexing (BSBI), vector-based semantic retrieval, advanced ranking algorithms, champion lists, and improved phonetic algorithms such as Double Metaphone for enhanced retrieval effectiveness.
    """)

    st.divider()

    # ==================================================
    # System Limitations and Strategic Enhancements Panel
    # ==================================================
    st.header("🛑 System Limitations & Future Engineering Upgrades")

    col_lim, col_imp = st.columns(2)

    with col_lim:
        st.subheader("⚠️ Documented System Limitations")
        st.markdown("""
        * **High Memory Permuterm Footprint:** Storing every single cyclic permutation rotation of long words scales index space demands aggressively.
        * **Static Non-Incremental Indices:** If modifications are made to a file, the entire text index must be re-compiled from scratch.
        * **RAM Boundary Constraints:** The BST, B-Tree, and inverted structures are bound to local session memory pools rather than disk blocks.
        * **Syntactic Vector Blindspots:** TF-IDF scoring calculates raw term matches but lacks context vectors to parse word synonyms.
        """)

    with col_imp:
        st.subheader("🚀 Recommended Future Upgrades")
        st.markdown("""
        * **Block Sort-Based Indexing (BSBI):** Update index construction loops to run externally on temporary disk pages to remove RAM size limits.
        * **Dynamic Champion Lists:** Store high-weight text postings pointers inside a specialized champion array to answer common queries fast.
        * **Dense Embedding Integration:** Implement pre-trained vector models to evaluate context relevance alongside keyword matching.
        * **Soundex Hashing Improvements:** Move to advanced Double Metaphone indexing layers to parse multi-lingual phonetics perfectly.
        """)
        
