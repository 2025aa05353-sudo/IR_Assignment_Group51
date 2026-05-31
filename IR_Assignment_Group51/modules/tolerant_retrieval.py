import streamlit as st
import re
import time
import pandas as pd
from collections import defaultdict

# ==================================================
# 1. Core Tolerant Retrieval Algorithms
# ==================================================

def build_kgram_index(vocab_terms, k=3):
    """Builds a non-positional k-gram index from the unique vocabulary."""
    kgram_idx = defaultdict(set)
    for term in vocab_terms:
        padded = "$" + term + "$"
        if len(padded) < k:
            kgram_idx[padded].add(term)
            continue
        for i in range(len(padded) - k + 1):
            gram = padded[i:i+k]
            kgram_idx[gram].add(term)
    return kgram_idx

def build_permuterm_index(vocab_terms):
    """Maps every rotated variation of a term back to its root term key."""
    permuterm_idx = {}
    for term in vocab_terms:
        anchored = term + "$"
        for i in range(len(anchored)):
            rotation = anchored[i:] + anchored[:i]
            permuterm_idx[rotation] = term
    return {k: permuterm_idx[k] for k in sorted(permuterm_idx.keys())}

def search_permuterm(query, permuterm_idx):
    """Processes trailing (w*), leading (*w), and infix (w*w) wildcard expressions."""
    query = query.strip().lower()
    if "*" not in query:
        return [query] if query in permuterm_idx.values() else []
    
    parts = query.split("*")
    if len(parts) > 2:  # Regex fallback handle for multiple complex wildcards
        pattern = "^" + query.replace("*", ".*") + "$"
        return [t for t in set(permuterm_idx.values()) if re.match(pattern, t)]
        
    if query.endswith("*"):
        target = parts[0]
    elif query.startswith("*"):
        target = parts[1] + "$"
    else:
        target = parts[1] + "$" + parts[0]
        
    return sorted(list(set([t for rot, t in permuterm_idx.items() if rot.startswith(target)])))

def get_levenshtein_distance(s1, s2):
    """Calculates minimal edit distance operations between two string terms."""
    if len(s1) < len(s2):
        return get_levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
        
    prev_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        curr_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = prev_row[j + 1] + 1
            deletions = curr_row[j] + 1
            substitutions = prev_row[j] + (c1 != c2)
            curr_row.append(min(insertions, deletions, substitutions))
        prev_row = curr_row
    return prev_row[-1]

def get_soundex_code(term):
    """Converts a word to its 4-character phonetic hashing code structure."""
    term = term.upper()
    if not term:
        return "0000"
    
    mapping = {
        "B": "1", "F": "1", "P": "1", "V": "1",
        "C": "2", "G": "2", "J": "2", "K": "2", "Q": "2", "S": "2", "X": "2", "Z": "2",
        "D": "3", "T": "3",
        "L": "4",
        "M": "5", "N": "5",
        "R": "6"
    }
    
    first_char = term[0]
    tail = term[1:]
    
    encoded_tail = ""
    for char in tail:
        encoded_tail += mapping.get(char, "0")
        
    collapsed_tail = ""
    prev = ""
    for char in encoded_tail:
        if char != prev:
            collapsed_tail += char
            prev = char
            
    cleaned_tail = collapsed_tail.replace("0", "")
    res = first_char + cleaned_tail
    return res[:4].ljust(4, "0")

# ==================================================
# Main Layout Code
# ==================================================

def show_tolerant_retrieval_page():

    st.title("🛠 Part E : Tolerant Retrieval")

    st.markdown("""
    ### Part E : Tolerant Retrieval

    This section experimentally demonstrates how the retrieval system handles imperfect queries.

    ### Techniques Covered

    ✅ Wildcard Queries

    ✅ Spelling Correction

    ✅ Edit Distance Correction

    ✅ K-Gram Index

    ✅ Phonetic Correction

    """)

    st.info(
        "Implementation results and experimental observations will be displayed below."
    )

    # ==================================================
    # State Guardrails & Setup Sync
    # ==================================================
    if "documents" not in st.session_state or "inverted_index" not in st.session_state:
        st.warning("⚠️ Please load a dataset and execute standard Inverted Index Creation in Part B first.")
        return

    documents = st.session_state["documents"]
    raw_index = st.session_state["inverted_index"]
    
    if len(raw_index) == 0 or len(documents) == 0:
        st.warning("⚠️ Index structures appear empty. Please verify data preprocessing pipeline states.")
        return

    # Extract global distinct vocabulary keys from inverted index
    vocab_terms = list(raw_index.keys())

    st.subheader("📈 Retrieval Index Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Vocabulary Size",
            len(vocab_terms)
        )

    with col2:
        st.metric(
            "Documents Indexed",
            len(documents)
        )

    with col3:
        st.metric(
            "Techniques Implemented",
            "5"
        )

    st.caption("""
        1. Wildcard Queries
        2. Spelling Correction
        3. Edit Distance Correction
        4. K-Gram Index
        5. Phonetic Correction
    """)

    # Build internal index matrices once for runtime lookups
    kgram_index = build_kgram_index(vocab_terms, k=3)
    permuterm_index = build_permuterm_index(vocab_terms)
    
    # Pre-calculate phonetic indices for Soundex search matching
    soundex_index = defaultdict(list)
    for term in vocab_terms:
        soundex_index[get_soundex_code(term)].append(term)

   
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
    st.caption("TThe tolerant retrieval techniques operate on the global vocabulary generated from the loaded text documents.")


    # ==================================================
    # Live Technical Demonstration Workspace UI
    # ==================================================
    st.header("🔍 Imperfect Query Parsing Playground")
    
    # 1. Wildcard Module UI Box
    st.subheader("1. Wildcard Query Execution (Permuterm Index)")
    wildcard_in = st.text_input("Enter a wildcard term expression (use *):", "learn*").strip().lower()
    
    if wildcard_in:
        t0 = time.perf_counter_ns()
        wildcard_matches = search_permuterm(wildcard_in, permuterm_index)
        t_wildcard = (time.perf_counter_ns() - t0) / 1000.0
        
        st.caption(f"⏱️ Retrieval Latency: `{t_wildcard:.2f} μs` | Resolved Words: `{len(wildcard_matches)}`")
        st.write("**Resolved Terms:**", wildcard_matches if wildcard_matches else "No matching keys found.")
    
    st.markdown("---")

    # 2. Spelling / Edit Distance / K-Gram Module UI Box
    st.subheader("2. Spelling Correction, K-Grams, & Edit Distance Processing")
    misspelled_in = st.text_input("Type a misspelled search word to run correction pipelines:", "machne").strip().lower()
    
    if misspelled_in:
        t0_corr = time.perf_counter_ns()
        
        # A. Resolve K-Grams for input to narrow down candidates quickly
        input_padded = "$" + misspelled_in + "$"
        input_grams = [input_padded[i:i+3] for i in range(len(input_padded) - 3 + 1)] if len(input_padded) >= 3 else [input_padded]
        
        candidate_counts = defaultdict(int)
        for g in input_grams:
            for term in kgram_index.get(g, []):
                candidate_counts[term] += 1
                
        # Calculate Jaccard similarity coefficients over matching grams
        jaccard_results = []
        input_gram_set = set(input_grams)
        
        for term, count in candidate_counts.items():
            t_padded = "$" + term + "$"
            t_grams = set([t_padded[i:i+3] for i in range(len(t_padded) - 3 + 1)]) if len(t_padded) >= 3 else {t_padded}
            union_len = len(input_gram_set.union(t_grams))
            jaccard_score = count / union_len if union_len > 0 else 0
            jaccard_results.append((term, jaccard_score))
            
        # Take the top 10 candidates by K-gram match to pass to edit distance loops
        jaccard_results = sorted(jaccard_results, key=lambda x: x[1], reverse=True)[:10]
        
        # B. Run Levenshtein Edit Distance metrics over selected candidate tokens
        correction_records = []
        for term, j_score in jaccard_results:
            ed_dist = get_levenshtein_distance(misspelled_in, term)
            correction_records.append({
                "Vocabulary Candidate": term,
                "Overlapping K-Grams": candidate_counts[term],
                "Jaccard Coefficient": f"{j_score:.4f}",
                "Edit Distance (Levenshtein)": ed_dist
            })
            
        t_corr = (time.perf_counter_ns() - t0_corr) / 1000.0
        st.caption(f"⏱️ Correction Pipeline Latency: `{t_corr:.2f} μs`")
        
        if correction_records:
            corr_df = pd.DataFrame(correction_records).sort_values(by=["Edit Distance (Levenshtein)", "Jaccard Coefficient"], ascending=[True, False])
            corr_df.index = [str(i) for i in range(1, len(corr_df) + 1)]
            st.dataframe(corr_df, use_container_width=True)
            st.success(f"💡 Optimal System Suggestion: **{corr_df.iloc[0]['Vocabulary Candidate']}**")
            
            best_term = corr_df.iloc[0]['Vocabulary Candidate']

            st.info(
                f"""
                Original Query : {misspelled_in}

                Suggested Query : {best_term}

                Edit Distance : {corr_df.iloc[0]['Edit Distance (Levenshtein)']}
                """
            )
        else:
            st.write("No correction candidates found in system index layers.")

    st.markdown("---")

    # 3. Phonetic Search / Soundex Module UI Box
    st.subheader("3. Phonetic Matching Analysis (Soundex Hashing)")
    phonetic_in = st.text_input("Enter a phonetically skewed word (sounds like target):", "learnin").strip().lower()
    
    if phonetic_in:
        t0_soundex = time.perf_counter_ns()
        input_code = get_soundex_code(phonetic_in)
        phonetic_matches = soundex_index.get(input_code, [])
        t_soundex = (time.perf_counter_ns() - t0_soundex) / 1000.0
        
        st.caption(f"⏱️ Soundex Hash Lookup Latency: `{t_soundex:.2f} μs`")
        
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.metric("Generated Soundex Hash String", input_code)
        with col_s2:
            st.metric("Phonetic Vocabulary Matches", f"{len(phonetic_matches)} Word(s)")
            
        st.write("**Soundex Matching Words:**", phonetic_matches if phonetic_matches else "No phonetic matches found.")

    st.divider()

    # ==================================================
    # Analytical Inferences & Evaluation Criteria
    # ==================================================
    st.header("📊 Analytical Observations and Inferences")

    comparison_data = {
        "Tolerant Retrieval Sub-System": [
            "Wildcard Query Processing (Permuterm Index)",
            "K-Gram / Jaccard Pipeline",
            "Levenshtein Edit Distance",
            "Phonetic Matching (Soundex)"
        ],
        "Algorithmic Core Strategy": [
            "Generates cyclic string shifts appended with boundary indicators to resolve internal/infix variations.",
            "Deconstructs continuous text sub-sequences to execute quick vocabulary pruning lookup selections.",
            "Calculates the minimum single-character insertions, deletions, or swaps needed to fix typos.",
            "Transforms variable word spellings into static alphanumeric sound fingerprints."
        ],
        "Operational Complexity Profile": [
            "O(K) - Dependent on search rotation prefix length constraints.",
            "O(V) worst-case, reduced to minor subsets when checking intersecting token sets.",
            "O(M * N) - Evaluates string matrices dynamically between text pairs.",
            "O(1) constant runtime bucket extraction after building structural code keys."
        ]
    }
    
    comp_df = pd.DataFrame(comparison_data)
    comp_df.index = ["1", "2", "3", "4"]
    st.table(comp_df)

    st.caption("ℹ️ **Notation Note:** **O** denotes Big-O complexity scale values, **V** is total unique Vocabulary size, and **M, N, K** represent internal word lengths.")

    st.subheader("📌 Inference")
    st.success(
        """
        • **Wildcard Scaling Resolution:** Using a Permuterm Index turns expensive word scans into predictable prefix lookups, optimizing string search latency.
        
        • **Multi-Stage Error Pipelines:** Combining K-Gram Jaccard indexing with Edit Distance filtering prevents system slowdowns. The K-Gram index filters thousands of unrelated words out instantly, allowing the Levenshtein calculator to check only the top candidate words in fractions of a millisecond.
        
        • **Phonetic vs Textual Constraints:** Phonetic algorithms like Soundex bridge errors where text distances fail (e.g., matching words that look different but sound identical, like 'Smith' vs 'Smyth').
        
        • **Conclusion:** A robust, tolerant retrieval system must combine text alignment models with sound hashing strategies to catch both typographic slip-ups and conversational spelling variations.
        """
    )


    st.subheader("📌 Retrieval Quality Summary")

    st.success(
        """
        • Wildcard Queries effectively handle partial term searches.

        • K-Gram Indexing reduces the search space by identifying likely candidate words.

        • Edit Distance correction resolves typographical errors.

        • Soundex supports phonetic matching for words with similar pronunciation.

        • Combining multiple tolerant retrieval techniques improves the robustness of the retrieval system.

        • The system successfully retrieves relevant terms even when user queries contain spelling mistakes or incomplete words.
        """
    )