import streamlit as st
import requests
from gemini_summarizer import summarize_with_gemini

def jina_reader_option(jina_api_key, gemini_api_key):
    st.header("Jina.AI Reader")
    url = st.text_input("Enter the URL of the webpage you want to extract text from:")

    if st.button("Extract Text"):
        if url and jina_api_key:
            try:
                jina_url = f'https://r.jina.ai/{url}'
                headers = {
                    'Authorization': f'Bearer {jina_api_key}',
                    'X-With-Images-Summary': 'true',
                    'X-With-Links-Summary': 'true'
                }

                response = requests.get(jina_url, headers=headers)
                
                if response.status_code == 200:
                    st.success("Text extracted successfully!")
                    extracted_text = response.text
                    
                    with st.expander("View Extracted Text"):
                        st.markdown(extracted_text)
                    
                    # Add a download button for the extracted text
                    st.download_button(
                        label="Download Extracted Text",
                        data=extracted_text,
                        file_name="extracted_text.md",
                        mime="text/markdown"
                    )

                    # Add a button for Gemini summarization
                    if st.button("Summarize with Gemini"):
                        if gemini_api_key:
                            summary = summarize_with_gemini(extracted_text, gemini_api_key)
                            st.subheader("Gemini Summary")
                            st.markdown(summary)
                            
                            # Add a download button for the summary
                            st.download_button(
                                label="Download Summary",
                                data=summary,
                                file_name="gemini_summary.md",
                                mime="text/markdown"
                            )
                        else:
                            st.warning("Please enter your Google Gemini LLM API key in the sidebar.")
                else:
                    st.error(f"Error: Unable to extract text. Status code: {response.status_code}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a URL and make sure you've entered your Jina.AI API key in the sidebar.")
