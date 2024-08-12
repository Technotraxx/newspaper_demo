import streamlit as st
import requests

def jina_reader_option(api_key):
    st.header("Jina.AI Reader")
    url = st.text_input("Enter the URL of the webpage you want to extract text from:")

    if st.button("Extract Text"):
        if url and api_key:
            try:
                jina_url = f'https://r.jina.ai/{url}'
                headers = {
                    'Authorization': f'Bearer {api_key}',
                    'X-Return-Format': 'markdown'
                }

                response = requests.get(jina_url, headers=headers)
                
                if response.status_code == 200:
                    st.success("Text extracted successfully!")
                    
                    with st.expander("View Extracted Text"):
                        st.markdown(response.text)
                    
                    # Add a download button for the extracted text
                    st.download_button(
                        label="Download Extracted Text",
                        data=response.text,
                        file_name="extracted_text.md",
                        mime="text/markdown"
                    )
                else:
                    st.error(f"Error: Unable to extract text. Status code: {response.status_code}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a URL and make sure you've entered your Jina.AI API key in the sidebar.")
