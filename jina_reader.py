import streamlit as st
import requests
from gemini_summarizer import summarize_with_gemini
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def jina_reader_option(jina_api_key, gemini_api_key):
    st.header("Jina.AI Reader")
    
    # Initialize session state variables
    if 'extracted_text' not in st.session_state:
        st.session_state.extracted_text = None
    if 'summary' not in st.session_state:
        st.session_state.summary = None

    url = st.text_input("Enter the URL of the webpage you want to extract text from:")

    if st.button("Extract Text"):
        if url and jina_api_key:
            try:
                logger.info(f"Extracting text from URL: {url}")
                jina_url = f'https://r.jina.ai/{url}'
                headers = {
                    'Authorization': f'Bearer {jina_api_key}',
                    'X-Return-Format': 'markdown'
                }

                response = requests.get(jina_url, headers=headers)
                
                if response.status_code == 200:
                    st.success("Text extracted successfully!")
                    st.session_state.extracted_text = response.text
                    logger.info("Text extraction successful")
                else:
                    st.error(f"Error: Unable to extract text. Status code: {response.status_code}")
                    logger.error(f"Jina API error: Status code {response.status_code}")
            except Exception as e:
                st.error(f"An error occurred during text extraction: {str(e)}")
                logger.exception("Exception during text extraction")
        else:
            st.warning("Please enter a URL and make sure you've entered your Jina.AI API key in the sidebar.")

    # Display extracted text and download button if available
    if st.session_state.extracted_text:
        with st.expander("View Extracted Text"):
            st.markdown(st.session_state.extracted_text)
        
        st.download_button(
            label="Download Extracted Text",
            data=st.session_state.extracted_text,
            file_name="extracted_text.md",
            mime="text/markdown"
        )

        # Summarize with Gemini button
        if st.button("Summarize with Gemini"):
            if gemini_api_key:
                try:
                    logger.info("Starting Gemini summarization")
                    st.session_state.summary = summarize_with_gemini(st.session_state.extracted_text, gemini_api_key)
                    logger.info("Gemini summarization completed")
                except Exception as e:
                    st.error(f"An error occurred during summarization: {str(e)}")
                    logger.exception("Exception during Gemini summarization")
            else:
                st.warning("Please enter your Google Gemini LLM API key in the sidebar.")

    # Display summary and download button if available
    if st.session_state.summary:
        st.subheader("Gemini Summary")
        st.markdown(st.session_state.summary)
        
        st.download_button(
            label="Download Summary",
            data=st.session_state.summary,
            file_name="gemini_summary.md",
            mime="text/markdown"
        )
