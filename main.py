# import streamlit as st
# import langchain_helper as lch
# import textwrap
# import os

# st.title("Youtube Assistant")

# with st.sidebar:
#     with st.form(key='my_form'):
#         youtube_url=st.sidebar.text_area(
#             label="What is the YouTube video URL?",
#             max_chars=50
#         )
#         query=st.sidebar.text_area(
#            label="Ask me about the video?",
#            max_chars=50,
#            key="query" 
#         )
#         google_api_key = os.getenv('GOOGLE_API_KEY')

#         #openai_api_key= os.getenv('OPENAI_API_KEY')
#         submit_button=st.form_submit_button(label='Submit')

# if query and youtube_url:
#     # if not openai_api_key:
#     #     st.info("Please add your OpenAI API Key to continue")
#     #     st.stop()
#     # else:
#     db=lch.create_vectordb_from_yt_url(youtube_url)
#     response = lch.get_response_from_query(db, query)

#     #response,docs=lch.get_response_from_query(db,query)
#     st.subheader("Answer:")
#     st.text(textwrap.fill(response,width=80))

import streamlit as st
import langchain_helper as lch
import textwrap
import os

# Set up the app title and layout
st.set_page_config(layout="wide")

# Add custom CSS to change the background color
st.markdown(
    """
    <style>
    body {
    background-color: #f0f2f6;
    }
    .block-container {
    padding:1rem;
    }
    .block-container .markdown {
    background-color: #ffffff;
    padding:1rem;
    border-radius:10px;
    box-shadow:0 0 10px rgba(0,0,0,0.1);
    }
    </style>
    """,
    unsafe_allow_html=True,
)
st.title(f"**YouTube Assistant** 🤖📹")


# Create a sidebar with input fields
with st.sidebar:
    st.header("**Input** :speech_balloon:")
    st.markdown("### Enter the YouTube video URL and your query")

    col1, col2 = st.columns([4, 1])

    with col1:
        youtube_url = st.text_input(
            label="**YouTube Video URL**",
            placeholder="Enter the YouTube video URL",
            help="Enter the URL of the YouTube video you want to ask about",
        )

    with col2:
        st.write("🤖")

    query = st.text_input(
        label="**Query**",
        placeholder="Ask me about the video?",
        help="Enter your question about the video",
    )

    submit_button = st.button(label="**Submit** :rocket:")

# Check if the submit button is clicked
if submit_button and youtube_url and query:
    # Create a vector database from the YouTube URL
    db = lch.create_vectordb_from_yt_url(youtube_url)

    # Get the response from the query
    response = lch.get_response_from_query(db, query)

    # Display the response
    st.subheader("**Summary:** :thinking_face:")
    st.markdown(
        f"""
        <div style="background-color: #f7f7f7; padding:1rem; border-radius:10px; box-shadow:0 0 10px rgba(0,0,0,0.1);">
        {textwrap.fill(response, width=80)}
        </div>
        """,
        unsafe_allow_html=True,
    )

# Display a loading animation if the submit button is clicked but inputs are not ready
elif submit_button and (not youtube_url or not query):
    st.spinner("**Please fill in both fields and try again** :hourglass_flowing_sand:")

# Display a warning if GOOGLE_API_KEY is not set
if not os.getenv('GOOGLE_API_KEY'):
    st.warning("**Please set your GOOGLE_API_KEY environment variable** :warning:")


