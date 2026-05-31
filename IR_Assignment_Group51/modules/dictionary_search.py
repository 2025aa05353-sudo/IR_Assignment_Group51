import streamlit as st
import time
import pandas as pd
import re
from collections import defaultdict
from nltk.corpus import stopwords

# ==================================================
# 1. Binary Search Tree (BST) Implementation
# ==================================================
class BSTNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value  
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key, value):
        new_node = BSTNode(key, value)
        if self.root is None:
            self.root = new_node
            return
        
        current = self.root
        while True:
            if key < current.key:
                if current.left is None:
                    current.left = new_node
                    break
                current = current.left
            elif key > current.key:
                if current.right is None:
                    current.right = new_node
                    break
                current = current.right
            else:
                current.value = value  
                break

    def search(self, key):
        current = self.root
        while current:
            if key == current.key:
                return current.value
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        return None

# ==================================================
# 2. B-Tree Implementation (Order/Degree t=3)
# ==================================================
class BTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []      
        self.values = []    
        self.child = []     

class BTree:
    def __init__(self, t=3):
        self.root = BTreeNode(True)
        self.t = t  

    def insert(self, key, value):
        root = self.root
        if len(root.keys) == (2 * self.t) - 1:
            temp = BTreeNode()
            self.root = temp
            temp.child.insert(0, root)
            self._split_child(temp, 0, root)
            self._insert_non_full(temp, key, value)
        else:
            self._insert_non_full(root, key, value)

    def _insert_non_full(self, x, key, value):
        i = len(x.keys) - 1
        if x.leaf:
            x.keys.append(None)
            x.values.append(None)
            while i >= 0 and key < x.keys[i]:
                x.keys[i + 1] = x.keys[i]
                x.values[i + 1] = x.values[i]
                i -= 1
            x.keys[i + 1] = key
            x.values[i + 1] = value
        else:
            while i >= 0 and key < x.keys[i]:
                i -= 1
            i += 1
            if len(x.child[i].keys) == (2 * self.t) - 1:
                self._split_child(x, i, x.child[i])
                if key > x.keys[i]:
                    i += 1
            self._insert_non_full(x.child[i], key, value)

    def _split_child(self, x, i, y):
        t = self.t
        z = BTreeNode(leaf=y.leaf)
        x.child.insert(i + 1, z)
        x.keys.insert(i, y.keys[t - 1])
        x.values.insert(i, y.values[t - 1])
        
        z.keys = y.keys[t:(2 * t) - 1]
        z.values = y.values[t:(2 * t) - 1]
        y.keys = y.keys[0:t - 1]
        y.values = y.values[0:t - 1]
        
        if not y.leaf:
            z.child = y.child[t:2 * t]
            y.child = y.child[0:t]

    def search(self, key, x=None):
        if x is None:
            x = self.root
        
        i = 0
        while i < len(x.keys) and key > x.keys[i]:
            i += 1
            
        if i < len(x.keys) and key == x.keys[i]:
            return x.values[i]
        elif x.leaf:
            return None
        else:
            return self.search(key, x.child[i])

# ==================================================
# Main Function Route
# ==================================================
def show_dictionary_search_page():

    st.title(
        "🌳 Part D : Dictionary Search : Binary Search Tree and B-Tree"
    )

    st.markdown("""
    ### Part D : Dictionary Search using Binary Search Tree and B-Tree

    This part demonstrates:

    • Dictionary Construction

    • Binary Search Tree (BST)

    • B-Tree

    • Query Search Time Comparison

    • Retrieval Time Comparison

    • Performance Analysis and Inference
    """)

    st.info(
        "Implementation and comparison results will be displayed below."
    )

    # ==================================================
    # Base Document Verification Guardrail
    # ==================================================
    if "documents" not in st.session_state:
        st.warning("⚠️ Please load a dataset from the Home page first.")
        return

    documents = st.session_state["documents"]
    if len(documents) == 0:
        st.warning("⚠️ No documents available to index.")
        return

    # ==================================================
    # AUTOMATED JIT STATE SYNCHRONIZATION BRIDGE
    # ==================================================
    if "inverted_index" not in st.session_state:
        # Silently build the inverted index if the user jumped straight to Part D
        stop_words = set(stopwords.words("english"))
        fallback_index = defaultdict(list)
        
        for doc_name, doc_text in documents.items():
            doc_hyphenated = re.sub(r"-", " ", doc_text.lower())
            doc_toks = re.findall(r"\b\w+\b", doc_hyphenated)
            doc_fil = [t for t in doc_toks if t.isalpha() and t not in stop_words]
            
            for term in sorted(set(doc_fil)):
                fallback_index[term].append(doc_name)
                
        st.session_state["inverted_index"] = dict(fallback_index)

    raw_index = st.session_state["inverted_index"]

    # Bulk load vocabulary sets into tree nodes
    bst = BinarySearchTree()
    btree = BTree(t=3)

    for term, postings in raw_index.items():
        bst.insert(term, postings)
        btree.insert(term, postings)

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



    # ==================================================
    # Live Search Interaction Section
    # ==================================================
    st.header("🔍 Direct Dictionary Key Search")
    
    search_term = st.text_input("Enter target word to search in dictionary indices:", "learning").strip().lower()

    if search_term:
        t_bst_start = time.perf_counter_ns()
        bst_result = bst.search(search_term)
        t_bst_end = time.perf_counter_ns()
        bst_time = (t_bst_end - t_bst_start) / 1000.0  

        t_btree_start = time.perf_counter_ns()
        btree_result = btree.search(search_term)
        t_btree_end = time.perf_counter_ns()
        btree_time = (t_btree_end - t_btree_start) / 1000.0  

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Binary Search Tree (BST)")
            st.metric("BST Search Latency", f"{bst_time:.4f} μs")
            st.write("Postings Extracted:", bst_result if bst_result else "Key not located.")
            
        with col2:
            st.subheader("B-Tree Index Structure")
            st.metric("B-Tree Search Latency", f"{btree_time:.4f} μs")
            st.write("Postings Extracted:", btree_result if btree_result else "Key not located.")

        st.divider()

        # ==================================================
        # Performance Evaluation Metrics Table
        # ==================================================
        st.header("📊 Query & Retrieval Time Comparison")
        
        perf_metrics = {
            "Algorithmic Data Layer": ["Binary Search Tree (BST)", "B-Tree Architecture"],
            "Evaluated Term": [search_term, search_term],
            "Execution Latency (Microseconds)": [f"{bst_time:.4f} μs", f"{btree_time:.4f} μs"],
            "Hits Status": ["Found" if bst_result else "Miss", "Found" if btree_result else "Miss"]
        }
        
        comp_df = pd.DataFrame(perf_metrics)
        comp_df.index = ["1", "2"]  
        st.dataframe(comp_df, use_container_width=True)

    st.divider()

    # ==================================================
    # Technical Inferences and Structural Discussion
    # ==================================================
    st.header("📈 Performance Analysis and Inference")
    
    st.table(pd.DataFrame({
        "Performance Parameters": [
            "Search Time Complexity (Average)",
            "Search Time Complexity (Worst-Case)",
            "Disk Input/Output Operational Block Cost",
            "Node Layout Geometry"
        ],
        "Binary Search Tree (BST)": [
            "O(log₂ V)",
            "O(V) - Occurs if vocabulary terms are fed in sorted order, creating an unbalanced line tree.",
            "High cost due to deep pointer paths spread randomly across systemic memory allocations.",
            "Strictly limited to a maximum of 2 children per node structure."
        ],
        "B-Tree Architecture": [
            "O(log_t V)",
            "O(log_t V) - Stays completely balanced because nodes split and merge dynamically.",
            "Extremely low cost, loading multiple key-value sets into a single sequential page read.",
            "Can handle multiple keys and child pointers simultaneously."
        ]
    }).set_index(pd.Index(["1", "2", "3", "4"]))) 

    st.caption("ℹ️ **Notation Note:** **O** denotes Big-O notation (growth rate complexity framework), while **V** represents the size of the unique Preprocessed Vocabulary.")

    st.subheader("📌 Inferences & Database Architecture Insights")
    st.markdown("""
    * **Dynamic Speed Observations:** In an isolated simulation running purely within local RAM memory (like this small data array context), a **BST** can occasionally execute marginally faster than a B-Tree for basic lookups. This happens because a BST relies on simple binary pointer steps, skipping the secondary internal loops that a B-Tree node has to use to search through its inner bucket of sorted keys.
    * **Worst-Case Robustness:** If vocabulary terms are processed in perfect alphabetical order, an unbalanced BST degrades into a linear single line with a slow search complexity of **O(V)**. A **B-Tree** completely avoids this degradation; its node splitting guidelines guarantee structural stability with a consistent, balanced complexity curve.
    * **Real-World Scale Factor (Disk I/O):** In large-scale setups, system indices are saved directly to physical disk storage rather than volatile RAM. A BST node requires a slow disk-page lookup for every individual step down its pointer pathway. A B-Tree functions as a flat, broad hierarchy that bundles hundreds of keys into single block arrangements. This configuration optimizes disk access efficiency, making it the foundational standard for production database engines.
    """)