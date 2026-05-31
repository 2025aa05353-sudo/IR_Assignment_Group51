  
Work Integrated Learning Programmes Division
Information Retrieval (Merged - AIMLCZG537/DSECLZG537)(S2-25)
Assignment - 1 
Marks = 10
Objective
The objective of this assignment is to design and implement an end-to-end Information Retrieval system using Streamlit.
Students must build an interactive front-end application where the user can upload a dataset/document collection, enter queries, select different retrieval techniques, and observe outputs for preprocessing, indexing, querying, and tolerant retrieval.
Dataset 
Documents of your choice
1.	Task Breakdown
Executing the Assignment on BITS Lab portal - 1 Mark
A. Streamlit-Based End-to-End Workflow
1.	Upload a text dataset or document collection. 
2.	View the uploaded documents. 
3.	Enter search queries from the front end. 
4.	Select preprocessing and retrieval options from the Streamlit interface. 
5.	Display intermediate and final outputs on the front end. 
The complete workflow must be executable through the Streamlit front end only. Students should not show provide backend code or static notebook outputs.
B. Text Preprocessing
Apply and display the effect of the following preprocessing steps:
•	Tokenization, Inverse index creation
•	Lowercasing
•	Stop word removal
•	Hyphen handling
•	Stemming and/or Lemmatization
Compare stemming vs lemmatization using any suitable semantic similarity or retrieval quality measure and conclude whether stemming or lemmatization is more suitable for the selected dataset and justify your decision.
C. Phrase Query Processing
Implement and compare phrase query search using: Biword Index, Positional Index 
•	Biword index representation 
•	Positional index representation 
•	Query result using biword index 
•	Query result using positional index 
•	Cases where biword index may give false positives 
•	Why positional index gives more accurate phrase query results 
The comparison must be visible on the Streamlit front end and you shall be providing your inferences
D. Dictionary Search using Binary Search Tree and B-Tree
Create a dictionary of terms from the document collection. Implement, Binary Search Tree, B-Tree 
Compare their performance for: Query search time, Retrieval time 
Students must run multiple queries and report experimental results in a table and also provide inference based on the results.
E. Tolerant Retrieval
Students must experimentally demonstrate how their retrieval system handles imperfect queries. You may use one or more of the following:
1.	Wildcard queries 
2.	Spelling correction 
3.	Edit distance correction 
4.	K-gram index 
5.	Phonetic correction 
G. Inference and Discussion *** This section is compulsory.***
Students must provide clear inferences in the report for every task. You should answer:
1.	Which preprocessing technique improved retrieval quality? 
2.	Was stemming or lemmatization better for their dataset? 
3.	Which phrase query index was more accurate? 
4.	Which tree structure was faster? 
5.	How tolerant was their retrieval model? 
6.	What are the limitations of their system? 
7.	How can the system be improved? 
2.	Submission Components
Students must submit:
1.	Streamlit application code 
o	.py file 
o	Supporting files, if any 
2.	Dataset used 
o	Text documents, CSV, or any document collection 
3.	Report 
o	Explanation of implementation in the Virtual lab
o	Screenshots of Streamlit front end (that you have worked in Virtual lab)
o	Experimental results 
o	Tables and inferences 
4.	Demo evidence 
o	Screenshots or short screen recording of the application running 
5.	README file 
o	Steps to install dependencies 
o	Command to run the app
Example: streamlit run app.py
3.	Rubric: 10 Marks
Component	Marks
Streamlit end-to-end workflow	1
Text preprocessing	1.5
Stemming vs lemmatization 	1
Phrase query using biword and positional index	1.5
Binary Tree and B-Tree comparison	1.5
Tolerant retrieval	1.5
Experimental evidence and inference	1
Virtual lab usage	1
Total	10

For any other queries/ clarifications related to the assignment, please write on the Taxila Discussion Forum, after checking existing queries and their answers. 
Submission Deadline – 15th June 23:59 PM
This is a Hard Deadline - No extensions will be provided. 
All the Best !!
