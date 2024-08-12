import streamlit as st
import requests
from gemini_summarizer import summarize_with_gemini
import logging
import json

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
    if 'jina_response' not in st.session_state:
        st.session_state.jina_response = None

    url = st.text_input("Enter the URL of the webpage you want to extract text from:")

    if st.button("Extract Text"):
        if url and jina_api_key:
            try:
                logger.info(f"Extracting text from URL: {url}")
                jina_url = f'https://r.jina.ai/{url}'
                headers = {
                    'Authorization': f'Bearer {jina_api_key}',
                    'X-With-Images-Summary': 'true',
                    'X-With-Links-Summary': 'true'
                }
                response = requests.get(jina_url, headers=headers)
                
                logger.info(f"Jina API response status code: {response.status_code}")
                logger.info(f"Jina API response headers: {response.headers}")
                logger.info(f"Jina API response content type: {response.headers.get('Content-Type')}")
                
                if response.status_code == 200:
                    content_type = response.headers.get('Content-Type', '')
                    if 'application/json' in content_type:
                        try:
                            st.session_state.jina_response = response.json()
                            st.session_state.extracted_text = st.session_state.jina_response.get('text', '')
                            st.success("Text extracted successfully!")
                            logger.info("Text extraction successful (JSON response)")
                        except json.JSONDecodeError as json_err:
                            st.error(f"Error decoding JSON from Jina API: {str(json_err)}")
                            logger.error(f"JSON decode error. Response content: {response.text[:1000]}")  # Log first 1000 characters
                    else:
                        st.session_state.extracted_text = response.text
                        st.success("Text extracted successfully (non-JSON response)!")
                        logger.info("Text extraction successful (non-JSON response)")
                else:
                    st.error(f"Error: Unable to extract text. Status code: {response.status_code}")
                    logger.error(f"Jina API error: Status code {response.status_code}")
                    logger.error(f"Jina API error response: {response.text[:1000]}")  # Log first 1000 characters
            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred during the request to Jina API: {str(e)}")
                logger.exception("Exception during Jina API request")
            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")
                logger.exception("Unexpected exception during text extraction")
        else:
            st.warning("Please enter a URL and make sure you've entered your Jina.AI API key in the sidebar.")

    # Display extracted text and related information
    if st.session_state.extracted_text:
        with st.expander("View Extracted Text"):
            st.markdown(st.session_state.extracted_text)
        
        st.download_button(
            label="Download Extracted Text",
            data=st.session_state.extracted_text,
            file_name="extracted_text.md",
            mime="text/markdown"
        )

        # Display image and link summaries if available
        if isinstance(st.session_state.jina_response, dict):
            if 'images_summary' in st.session_state.jina_response:
                with st.expander("Image Summary"):
                    st.markdown(st.session_state.jina_response['images_summary'])
            
            if 'links_summary' in st.session_state.jina_response:
                with st.expander("Links Summary"):
                    st.markdown(st.session_state.jina_response['links_summary'])

        # Summarize with Gemini button
        if st.button("Summarize with Gemini"):
            if gemini_api_key:
                try:
                    logger.info("Starting Gemini summarization")
                    with st.spinner("Generating summary..."):
                        st.session_state.summary = summarize_with_gemini(st.session_state.extracted_text, gemini_api_key)
                    logger.info("Gemini summarization completed")
                except Exception as e:
                    st.error(f"An error occurred during summarization: {str(e)}")
                    logger.exception("Exception during Gemini summarization")
            else:
                st.warning("Please enter your Google Gemini LLM API key in the sidebar.")

    # Display summary if available
    if st.session_state.summary:
        st.subheader("Gemini Summary")
        st.markdown(st.session_state.summary)
        
        st.download_button(
            label="Download Summary",
            data=st.session_state.summary,
            file_name="gemini_summary.md",
            mime="text/markdown"
        )
