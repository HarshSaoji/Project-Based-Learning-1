import streamlit
from getters.prompts import get_drug, get_diagnosis, q_n_a
from utils.predict_utils import predict_sentence
from utils.pdf_extraction import extract_from_pdf, extract_from_pdfs

# Function to display search results for the query in uploaded or input text
def show_results(container, query, text_docs):
    cnt = 1
    for i in get_matches(query, text_docs):
        cnt += 1        # Matches found are counted (logic of displaying not implemented here)

# Formats and returns sorted cancer type matches based on prediction confidence
def get_cancer_matches(results):
    matches = sorted(results, key=results.get, reverse=True)  # Sort by prediction confidence
    match = ""
    for j in range(len(matches)):
        match += "<br>" + acc_cancer.format(matches[j], f"{results[matches[j]] * 100:.2f} %")
    return match

# Reading static about information
about = open("about.txt", "r")
info = about.read()

# Titles and display constants
title = "Oncology Document Analyzer System"
acc_cancer = "<i>{}</i>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<code style='font-size:15px'>{}</code><br>"
footer = f"""<footer style="left: 0;
                            bottom: 0;
                            width: 100%;
                            padding-top: 120px;
                            font-size: medium;
                            text-align: center;">
                Copyright © ODAS | <a style="text-decoration: none;" href={}> GitHub</a>
            </footer>"""

# Initialize session states for data persistence across user interactions
if 'home' not in st.session_state:
    st.session_state.home = True
if 'text_prompt' not in st.session_state:
    st.session_state.text_prompt = ""
if 'cancer' not in st.session_state:
    st.session_state.cancer = ""
if 'file_input' not in st.session_state:
    st.session_state.file_input = None
if 'file_content' not in st.session_state:
    st.session_state.file_content = ""

# Main title display
st.markdown('<h1 style="text-align:center; font-family:Verdana;">O D A S</h1>', unsafe_allow_html=True)
st.markdown(f'<p style="text-align:center; font-family:Verdana;">{title}</p>', unsafe_allow_html=True)

# Three main tabs for functionality: classification, search, and chat
text, search, chat = st.tabs(["Oncology Classification", "Search", "ONCObot"])

about.close()  # Close the file after reading

# --- Oncology Classification Tab ---
with text:
    if st.session_state.home:
        # User input via text or PDF file
        st.session_state.text_prompt = st.text_area(label="Enter any text")
        st.markdown('<h5 style="text-align:center;">or</h5>', unsafe_allow_html=True)
        st.session_state.file_input = st.file_uploader("Upload PDF(s)", accept_multiple_files=True)
        st.markdown(footer, unsafe_allow_html=True)

        # Trigger prediction if text or file is uploaded
        if (st.session_state.text_prompt or st.session_state.file_input):
            if st.session_state.text_prompt != "":
                # Predict from input text
                st.session_state.cancer = get_cancer_matches(predict_sentence(st.session_state.text_prompt))
            elif st.session_state.file_input is not None:
                # Predict from uploaded file(s)
                if str(type(st.session_state.file_input).__name__) == 'list':
                    st.session_state.file_content = extract_from_pdfs(st.session_state.file_input)
                else:
                    st.session_state.file_content = extract_from_pdf(st.session_state.file_input)
                st.session_state.cancer = get_cancer_matches(predict_sentence(st.session_state.file_content))

    # Show prediction results and AI-generated drug/diagnosis information
    if not st.session_state.home:
        st.markdown(f'<h3><b>Cancer \tMatches<b> :</h3><h5>{st.session_state.cancer}</h5>', unsafe_allow_html=True)

        st.markdown('<h2 style="font-style:italic;">Drug Use Advisory</h2>', unsafe_allow_html=True)
        st.markdown(get_drug(st.session_state.text_prompt, st.session_state.cancer).choices[0].message.content)

        st.markdown('<h2 style="font-style:italic;">Diagnosis</h2>', unsafe_allow_html=True)
        time.sleep(0.5)
        st.markdown(get_diagnosis(st.session_state.text_prompt, st.session_state.cancer).choices[0].message.content)

# --- Search Tab ---
with search:
    results = """<i style="font-family:Verdana;">{}</i>"""

    with qtr1:
        query = st.text_input("Enter Keywords")
    with qtr2:
        st.write("\n")
        st.write("\n")
        find = st.button("Search")

    # Perform document search if button is clicked or input is detected
    if find or query:
        with st.spinner("Searching the document(s) for matches"):
            st.markdown("Relevant matches")
            container = st.container(border=True)

            # Error handling if required input is missing
            if (st.session_state.text_prompt or st.session_state.file_content) == "":
                container.write("Please provide text in the classification section. ")
            elif query == "":
                container.write("Please enter a keyword to search")
            else:
                time.sleep(5)  # Simulated loading

                # Perform search in either user text or extracted file content
                if st.session_state.text_prompt != "":
                    show_results(container, query, st.session_state.text_prompt)
                elif st.session_state.file_input is not None:
                    if str(type(st.session_state.file_input).__name__) == 'list':
                        st.session_state.file_content = extract_from_pdfs(st.session_state.file_input)
                    else:
                        st.session_state.file_content = extract_from_pdf(st.session_state.file_input)
                    show_results(container, query, st.session_state.file_content)

    st.markdown(footer, unsafe_allow_html=True)

# --- ONCObot Chat Tab ---
with chat:
    # Setup for message history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if st.session_state.messages != []:
        st.markdown("Chat History")
        for message in st.session_state.messages:
            with st.chat_message(message['role']):
                st.markdown(message["content"])

    # Take new input from user
    if prompt := st.chat_input("Summarize this is 50 words..."):
        st.session_state.messages.append({'role': 'user', 'content': prompt})
        with st.chat_message('user'):
            st.markdown(prompt)

        # Use extracted file or input text to answer the query
        if st.session_state.file_input is not None:
            if str(type(st.session_state.file_input).__name__) == 'list':
                st.session_state.file_content = extract_from_pdfs(st.session_state.file_input)
            else:
                st.session_state.file_content = extract_from_pdf(st.session_state.file_input)
            response = q_n_a(st.session_state.file_content, prompt)
        elif st.session_state.text_prompt != "":
            response = q_n_a(st.session_state.text_prompt, prompt)

        # Save and display assistant's response
        st.session_state.messages.append({'role': 'assistant',
                                          'content': response.choices[0].message.content})
        with st.chat_message("assistant"):
            st.markdown(response.choices[0].message.content)
