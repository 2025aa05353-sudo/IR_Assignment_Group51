import streamlit as st
import re
import pandas as pd
from modules.preprocessing import tokenize

# ==================================================
# Index Construction Utilities
# ==================================================

def build_biword_index(documents, stop_words):
    """
    Constructs a Biword Index by creating continuous structural token pairs 
    from the lowercased, hyphen-handled text of each document.
    """
    biword_idx = {}
    for doc_name, content in documents.items():
        clean_text = re.sub(r"-", " ", content.lower())
        doc_tokens = [t for t in tokenize(clean_text) if t.isalpha() and t not in stop_words]
        
        # Form biwords: w1_w2
        for i in range(len(doc_tokens) - 1):
            biword = f"{doc_tokens[i]}_{doc_tokens[i+1]}"
            if biword not in biword_idx:
                biword_idx[biword] = set()
            biword_idx[biword].add(doc_name)
            
    return {k: sorted(list(v)) for k, v in sorted(biword_idx.items())}


def build_positional_index(documents, stop_words):
    """
    Constructs a Positional Index tracking { term: { doc_id: [position1, position2] } }
    to preserve exact physical spatial coordinates.
    """
    pos_idx = {}
    for doc_name, content in documents.items():
        clean_text = re.sub(r"-", " ", content.lower())
        doc_tokens = [t for t in tokenize(clean_text) if t.isalpha() and t not in stop_words]
        
        for position, term in enumerate(doc_tokens):
            if term not in pos_idx:
                pos_idx[term] = {}
            if doc_name not in pos_idx[term]:
                pos_idx[term][doc_name] = []
            pos_idx[term][doc_name].append(position)
            
    return pos_idx

# ==================================================
# Retrieval Engines (Strict Phrase Logic Configured)
# ==================================================

def search_biword(query_tokens, biword_index):
    # Reject single-word lookups for pure phrase processing
    if len(query_tokens) < 2:
        return []
    
    # Generate biwords for the query phrase
    needed_biwords = [f"{query_tokens[i]}_{query_tokens[i+1]}" for i in range(len(query_tokens) - 1)]
    
    # Intersect the matching postings lists
    hits = None
    for bw in needed_biwords:
        current_docs = set(biword_index.get(bw, []))
        if hits is None:
            hits = current_docs
        else:
            hits = hits.intersection(current_docs)
        if not hits:
            return []
            
    return sorted(list(hits)) if hits else []


def search_positional(query_tokens, pos_index):
    # Reject single-word lookups for pure phrase processing
    if len(query_tokens) < 2:
        return []
    
    first_term = query_tokens[0]
    if first_term not in pos_index:
        return []
    
    # Find documents containing all words in the phrase query
    candidate_docs = set(pos_index[first_term].keys())
    for term in query_tokens[1:]:
        if term not in pos_index:
            return []
        candidate_docs = candidate_docs.intersection(set(pos_index[term].keys()))
        
    matching_docs = []
    
    # Verify strict, sequential positioning within candidate documents
    for doc in candidate_docs:
        possible_starts = pos_index[first_term][doc]
        for start_pos in possible_starts:
            phrase_valid = True
            for offset, next_term in enumerate(query_tokens[1:], start=1):
                target_pos = start_pos + offset
                if target_pos not in pos_index[next_term][doc]:
                    phrase_valid = False
                    break
            if phrase_valid:
                matching_docs.append(doc)
                break  
                
    return sorted(matching_docs)


# ==================================================
# Main Function
# ==================================================

def show_phrase_query_page():

    st.title("📌 Part C : Phrase Query Processing Implementation")

    st.warning("⚠️ **CRITICAL NOTE:** You **MUST** go to **PART B, Part C, Part D and Part E** after text file selection on **Home page** and actively select preprocessing option first! Otherwise, some of page can display stale cache states.")

    st.markdown("""
    ### Part C : Phrase Query Processing

    This section implements and compares phrase query search using:

    • Biword Index

    • Positional Index

    ### Features Covered

    ✅ Biword Index Representation

    ✅ Positional Index Representation

    ✅ Query Result using Biword Index

    ✅ Query Result using Positional Index

    ✅ Cases where Biword Index may give False Positives

    ✅ Why Positional Index provides more Accurate Phrase Query Results

    """)

    st.info(
        "Implementation and comparison results will be displayed below."
    )

    # ==================================================
    # Guard Rails & Background Initialization
    # ==================================================
    if "documents" not in st.session_state:
        st.warning("⚠️ Please load a dataset from the Home page first.")
        return

    documents = st.session_state["documents"]
    if len(documents) == 0:
        st.warning("⚠️ No documents available to index.")
        return

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
    st.caption("The phrase queries run across the global token index space generated by loaded txt files")



    # Extract NLTK stop words to ensure preprocessing alignment
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words("english"))

    # Compute structures behind the scenes
    biword_index = build_biword_index(documents, stop_words)
    pos_index = build_positional_index(documents, stop_words)

    st.subheader("📈 Index Statistics")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total Biwords",
            len(biword_index)
        )

    with col2:
        st.metric(
            "Total Positional Terms",
            len(pos_index)
        )



    # ==================================================
    # Execution Interface (Query Entry & Processing)
    # ==================================================
    st.header("🔍 Execute Phrase Queries")
    
    phrase_query = st.text_input("Enter your multi-word search phrase query here:", "machine learning")
    
    # Generate query tokens matching the exact text processing constraints
    q_tokens = [t.lower() for t in tokenize(phrase_query) if t.isalpha() and t.lower() not in stop_words]
    st.caption(f"⚙️ Active Query Tokens Extracted: `{q_tokens}`")

    if len(q_tokens) >= 2:

        query_biwords = [

            f"{q_tokens[i]}_{q_tokens[i+1]}"

            for i in range(len(q_tokens)-1)

        ]

        st.write(
            "Generated Query Biwords:",
            query_biwords
        )

    # Flag check for single words or empty inputs
    if len(q_tokens) < 2:
        st.warning("Please enter at least two words for phrase query processing.")
        res_biword = []
        res_pos = []
    else:
        # Run queries against both indexing layers
        res_biword = search_biword(q_tokens, biword_index)
        res_pos = search_positional(q_tokens, pos_index)

    # Side-by-side metric display
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Query Result using Biword Index")
        st.metric("Total Document Matches", f"{len(res_biword)} Doc(s)")
        st.write("Matching Postings:", res_biword if res_biword else "No matches found.")

    with col2:
        st.subheader("Query Result using Positional Index")
        st.metric("Total Document Matches", f"{len(res_pos)} Doc(s)")
        st.write("Matching Postings:", res_pos if res_pos else "No matches found.")

    st.divider()

    # ==================================================
    # Structural Presentations (Safe Preview Modes)
    # ==================================================
    st.header("🗂️ Structural Representation Previews")
    
    view_selection = st.radio(
        "Choose Structural Representation Snapshot to View:",
        ["Biword Index representation", "Positional Index representation"]
    )

    if view_selection == "Biword Index representation":
        st.subheader("Biword Index Representation")
        bw_display = [{"Biword String": k, "Postings List Matches": ", ".join(v)} for k, v in list(biword_index.items())[:100]]
        bw_df = pd.DataFrame(bw_display)
        bw_df.index = [str(i) for i in range(1, len(bw_df) + 1)]
        st.dataframe(bw_df, use_container_width=True)
        st.info(f"💡 UI Safe Mode: Showing a snapshot preview of the first 100 out of {len(biword_index)} unique biwords.")

    elif view_selection == "Positional Index representation":
        st.subheader("Positional Index Representation")
        pos_display = []
        for term, doc_map in list(pos_index.items())[:100]:
            repr_str = " | ".join([f"{doc}: {positions}" for doc, positions in doc_map.items()])
            pos_display.append({"Dictionary Term": term, "Document Mappings with Positional Coordinates": repr_str})
        pos_df = pd.DataFrame(pos_display)
        pos_df.index = [str(i) for i in range(1, len(pos_df) + 1)]
        st.dataframe(pos_df, use_container_width=True)
        st.info(f"💡 UI Safe Mode: Showing a snapshot preview of the first 100 unique dictionary terms with coordinate arrays.")

    st.divider()

    # ==================================================
    # Analytical Verification Tables for Part G Rubrics
    # ==================================================
    st.header("📊 Analytical Observations and Inferences")

    comparison_data = {
        "Structural Parameters": [
            "Positional Sequencing Accuracy", 
            "Index Footprint Memory Scaling", 
            "Handling Phrases of Arbitrary Length",
            "Reliability Metrics"
        ],
        "Biword Index Strategy": [
            "Fails to verify relative distance constraints across word pairs.",
            "Scales quadratically O(V²) as document vocabulary size expands.",
            "Decomposes long phrases into combinations of overlapping pairs, increasing risk profiles.",
            "Susceptible to False Positives"
        ],
        "Positional Index Strategy": [
            "Guarantees exact positioning matches using integer token coordinates.",
            "Requires larger memory footprints due to storing full sequence position arrays.",
            "Instantly handles multi-token phrases via continuous linear tracking lookups.",
            "Provides exact phrase matching by validating term positions."
        ]
    }
    
    st.table(pd.DataFrame(comparison_data))

    st.caption("ℹ️ **Notation Note:** **O** denotes Big-O notation (growth rate complexity framework), while **V** represents the size of the unique Preprocessed Vocabulary.")


    st.subheader("📌 Inference")

    st.success(
        """
    • Positional Index produced more accurate phrase query results.

    • Biword Index is simpler and faster to construct but may generate
    false positives because it does not verify exact word positions.

    • Positional Index explicitly stores token positions and validates
    their sequence during phrase matching.

    • Positional Index provides more reliable phrase retrieval,
    especially for multi-word queries.

    • Therefore, Positional Index is preferred when accurate phrase
    retrieval is required.
    """
    )


    st.subheader("💡 Deep Dive Theory Explanations")

    st.markdown("""
    ### Cases where Biword Index may give False Positives

    A Biword Index stores pairs of consecutive words (biwords) and retrieves
    documents by matching overlapping word pairs.

    For a phrase query such as **"machine learning algorithms"**, the system
    generates the biwords:

    • machine_learning

    • learning_algorithms

    and intersects their posting lists.

    Although this approach is efficient and requires simpler query processing,
    it does not explicitly verify the exact positions of all words in the
    document.

    Consequently, certain phrase queries may produce false positives when
    matching biwords are present but the complete phrase does not occur in
    the exact required sequence.

    ### Why Positional Index Provides More Accurate Phrase Query Results

    A Positional Index stores the exact position of every term occurrence
    within each document.

    **Example:**

    doc1 → machine: [5], learning: [6], algorithms: [7]

    When processing a phrase query such as **"machine learning algorithms"**,
    the retrieval algorithm verifies that the positions are consecutive.

    That is:

    • learning occurs at position n + 1

    • algorithms occurs at position n + 2

    relative to machine.

    By validating the exact sequence and positions of terms, the Positional
    Index provides highly accurate phrase matching and minimizes false
    positives during retrieval.

    Therefore, Positional Indexing is generally preferred for phrase query
    processing because it provides more accurate retrieval results and better
    supports exact phrase matching.
    """)
