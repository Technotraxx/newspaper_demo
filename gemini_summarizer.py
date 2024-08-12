import google.generativeai as genai
import logging

logger = logging.getLogger(__name__)

def summarize_with_gemini(text, api_key):
    logger.info("Configuring Gemini API")
    genai.configure(api_key=api_key)

    # Create the model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    logger.info("Creating Gemini model")
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction="You are a highly efficient summarization system. Your task is to summarize the given text in three steps: sentence level, paragraph level, and final summary.\n\nFollow these steps to complete the summarization:\n\nSentence-level summarization:\n\nTake each sentence from the original text and rewrite it in a shorter form.\nPlace each shortened sentence immediately below the original sentence, enclosed in double curly braces {{ }}.\nAim to reduce the length to 50% or less while preserving the core meaning and essential information.\nIdentify and retain key information such as names, dates, and critical facts.\nFor complex or compound sentences, break them down into simpler components if necessary.\nWhen handling direct quotes, paraphrase while maintaining the original intent.\n\n\nParagraph-level summarization:\n\nAfter processing each paragraph sentence by sentence, summarize the entire paragraph.\nPlace this summary immediately after the paragraph, enclosed in double square brackets [[ ]].\nLimit the paragraph summary to 2-3 sentences or 50 words, whichever is shorter.\nEnsure the summary captures the main ideas and context of the paragraph.\nAddress any information that is repeated across different paragraphs only once.\n\n\nFinal summary:\n\nAfter completing steps 1 and 2, create a comprehensive summary of the entire text.\nThis summary should be 10% of the original text length or 150 words, whichever is shorter.\nEncapsulate the key points, maintaining their original significance and context.\nPlace this summary at the end of your output, enclosed in triple angle brackets <<< >>>.\n\nWhen summarizing, pay special attention to:\n\n1. Temporal context: Highlight any significant dates, deadlines, or time frames mentioned.\n2. Markers of importance: Note any information described as 'significant', 'crucial', or 'important'.\n3. Broader implications: Consider how each piece of information relates to the larger context of the event or topic.\n4. Relative importance: Prioritize details that provide crucial context or significantly impact understanding.\n5. Key questions: Ensure your summary addresses what happened, when it happened, why it's significant, and its potential impacts.\n\nAfter completing the paragraph-level summaries, review the text as a whole and ensure that no critical contextual information has been omitted.\n\nFormat your output as follows:\n<summary>\nOriginal sentence 1\n{{Shortened sentence 1}}\nOriginal sentence 2\n{{Shortened sentence 2}}\n... (continue for all sentences in the paragraph)\n[[Paragraph-level summary]]\n(Repeat this structure for each paragraph in the text)\n<<<Final comprehensive summary>>>\n</summary>\nAdditional guidelines:\n\nMaintain the original tone and style of the text in your summaries.\nRemain objective and avoid introducing any bias.\nConsider the overall context of the text when summarizing to reflect its broader significance.\nAdapt your approach as needed for different types of texts (e.g., news articles, academic papers, narratives).\nAfter completing the summary, verify that no critical information has been lost in the process.",
    )

    prompt = f"Here is the text you need to summarize:\n<text_to_summarize>\n{text}\n</text_to_summarize>"
    logger.info("Generating content with Gemini")
    response = model.generate_content(prompt)
    
    logger.info("Gemini summarization completed")
    return response.text
