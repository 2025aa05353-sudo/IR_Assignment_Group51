import streamlit as st
import pandas as pd
import os
import re

# ==================================================
# PAGE CONFIG
# ==================================================

from modules.preprocessing import show_preprocessing_page
from modules.phrase_query import show_phrase_query_page
from modules.dictionary_search import show_dictionary_search_page
from modules.tolerant_retrieval import show_tolerant_retrieval_page
from modules.inference import show_inference_page

st.set_page_config(
    page_title="Information Retrieval System",
    page_icon="🔍",
    layout="wide"
)

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title("📚 Navigation")

page = st.sidebar.radio(
    "Select Module",
    [
        "🏠 Home",
        "⚙️ Part B : Text Preprocessing",
        "📌 Part C : Phrase Query Processing",
        "🌳 Part D : Dictionary Search : Binary Search Tree and B-Tree",
        "🛠 Part E : Tolerant Retrieval",
        "📝 Part G : Inference & Discussion"
    ]
)
# ==================================================
# HOME PAGE
# ==================================================

if page == "🏠 Home":

    st.title("🔍 Information Retrieval - upload text file")
    st.warning("⚠️ **CRITICAL NOTE:** You **MUST** go to **PART B, Part C, Part D and Part E** after text file selection on **Home page** and actively select preprocessing option first! Otherwise, some of page can display stale cache states.")
    st.subheader("Group Number : 51")
    st.subheader("Scroll down to end to Upload text files")

    team_df = pd.DataFrame({
        "Student ID": [
            "2025AA05350",
            "2025AA05359",
            "2025AA05353"
        ],
        "Student Name": [
            "AKANKSHA PARMAR",
            "ROHIT GUPTA",
            "SHEETAL PRAKASH BARANWAL"
        ],
        "Contribution (%)": [
            "100%",
            "100%",
            "100%"
        ]
    })

    st.dataframe(
        team_df,
        hide_index=True,
        use_container_width=True
    )

    st.markdown("""
    ### Part A : Streamlit-Based End-to-End Workflow
    •  Upload a text dataset or document collection
                
    •  View uploaded documents
                
    •  Select datasets through the Streamlit interface
                
    •  Execute the Information Retrieval workflow from the Streamlit front end only
    """)
    st.divider()

    # ==================================================
    # DATASET SOURCE
    # ==================================================

    st.header("📂 Dataset Source")

    dataset_option = st.radio(
        "Choose Dataset",
        [
            "Upload My Documents",
            "Use Built-in Sample Dataset"
        ],
        horizontal=True
    )

    # ==================================================
    # OPTION 1 : UPLOAD DOCUMENTS
    # ==================================================

    if dataset_option == "Upload My Documents":

        uploaded_files = st.file_uploader(
            "Upload one or more .txt files",
            type=["txt"],
            accept_multiple_files=True
        )

        if uploaded_files:

            st.success(
                "✅ document(s) uploaded successfully."
            )

            # Store documents for other modules
            st.session_state["documents"] = {}
            st.session_state["selected_docs_list"] = [f.name for f in uploaded_files]
            
            file_names = []
            total_characters = 0

            for file in uploaded_files:

                file.seek(0)

                content = file.read().decode("utf-8")

                # Store documents for other modules
                st.session_state["documents"][file.name] = content

                total_characters += len(content)

                file_names.append(file.name)

            st.subheader("📊 Dataset Summary")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Total Documents",
                    len(uploaded_files)
                )

            with col2:
                st.metric(
                    "Total Characters",
                    total_characters
                )

            st.subheader("📄 Uploaded Documents")

            st.dataframe(
                pd.DataFrame({
                    "Document Name": file_names
                }),
                hide_index=True,
                use_container_width=True
            )

            st.subheader("👁️ View Uploaded Documents")

            selected_doc = st.radio(
                "Select Document",
                uploaded_files,
                format_func=lambda x: x.name
            )

            selected_doc.seek(0)

            content = selected_doc.read().decode("utf-8")

            st.text_area(
                "Document Content",
                value=content,
                height=550
            )

    # ==================================================
    # OPTION 2 : SAMPLE DATASET (WITH ACTIVE DOCUMENT SELECTOR)
    # ==================================================

    else:

        dataset_folder = "dataset"
        
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        dataset_folder = os.path.join(BASE_DIR, "dataset")

        sample_docs = sorted(
            [
            file
            for file in os.listdir(dataset_folder)
            if file.endswith(".txt")
            ],
            key=lambda x: int(
                re.search(r"doc(\d+)", x).group(1)
            )
         )

        # FRONT-END CHIP FILTER SELECTOR HUB
        st.subheader("🗂️ Active Target File System Filter")
        
        chosen_sample_files = st.multiselect(
            "Select target database baseline files (Choose all or at least 1 file component):",
            options=sample_docs,
            default=sample_docs,
            format_func=lambda x: x.replace(".txt", "")
        )

        # Force structural system selection safety guardrails 
        if not chosen_sample_files:
            st.error("⚠️ System alert: You must choose at least one active text file baseline. Defaulting back to complete file collection matrix.")
            chosen_sample_files = sample_docs

        st.success(
            f"✅ Active System Working Context: Loaded {len(chosen_sample_files)} out of {len(sample_docs)} total files."
        )

        # Store filtered text arrays cleanly into systemic storage states
        st.session_state["documents"] = {}
        st.session_state["selected_docs_list"] = chosen_sample_files

        total_characters = 0

        for file in chosen_sample_files:

            with open(
                os.path.join(dataset_folder, file),
                "r",
                encoding="utf-8"
            ) as f:
                
                content = f.read()

                st.session_state["documents"][file] = content

                total_characters += len(content)

        st.subheader("📊 Dataset Summary")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Total Active Documents",
                len(chosen_sample_files)
            )

        with col2:
            st.metric(
                "Total Characters",
                total_characters
            )

        st.subheader("👁️ View Uploaded Documents")

        selected_doc = st.radio(
            "Select Document to Preview:",
            chosen_sample_files,
            format_func=lambda x: x.replace(".txt", "")
        )

        file_path = os.path.join(
            dataset_folder,
            selected_doc
        )

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            content = f.read()

        st.text_area(
            "Document Content Preview Workspace",
            value=content,
            height=550
        )

# ==================================================
# PREPROCESSING PAGE
# ==================================================

elif page == "⚙️ Part B : Text Preprocessing":

    show_preprocessing_page()


# ==================================================
# PHRASE QUERY PAGE
# ==================================================

elif page == "📌 Part C : Phrase Query Processing":

    show_phrase_query_page()

# ==================================================
# Dictionary Search
# ==================================================

elif page == "🌳 Part D : Dictionary Search : Binary Search Tree and B-Tree":

    show_dictionary_search_page()

# ==================================================
# TOLERANT RETRIEVAL PAGE
# ==================================================

elif page == "🛠 Part E : Tolerant Retrieval":

    show_tolerant_retrieval_page()

# ==================================================
# INFERENCE PAGE
# ==================================================

elif page == "📝 Part G : Inference & Discussion":

    show_inference_page()
