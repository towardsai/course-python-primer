import os
from openai import OpenAI
import gradio as gr
import json

client = OpenAI(
    api_key= "Your_OpenAI_API_Key"
    # api_key=os.environ.get("OPENAI_API_KEY")
)

# Function that communicates with an LLM to generate the summary, sentiment analysis, and tags
def analyze_news_article(article_text):
    """
    This function sends the article text to the LLM and expects a JSON output with:
      - "summary"
      - "sentiment"
      - "sentiment_confidence"
      - "tags"
      - "language"
    """
    system_message = {
        "role": "system",
        "content": "You are helpful assistant for Article Analysis and Response in JSON Format"
    }
    user_message = {
        "role": "user",
        "content": f""" You are an assistant that reads and analyzes a news article. You must return your answer in valid JSON format. Specifically, you will generate:
1) "summary": A concise, 2-3 sentence overview of the key points in the article.
2) "sentiment": One of the following strings: "positive", "negative", or "neutral".
3) "sentiment_confidence": A numeric value between 0 and 1 indicating your confidence in the sentiment.
4) "tags": A short list (3-5 items) of relevant keywords or topics from the article. These should be all lowercase, each word or short phrase separated by commas.
5) "language": The language of the article, e.g., "English" or "Spanish".

Other Important instructions you must follow:
1. You must give only a JSON response – no additional prefix or suffix text.
2. You are not allowed to include any explanations, apologies, or disclaimers.
3. You must not output any JSON keys other than "summary", "sentiment", "sentiment_confidence", "tags", and "language".
4. You must not include code fences (e.g., ```json ... ```).

The response MUST be valid JSON and look like this:

{{
  "summary": "...",
  "sentiment": "...",
  "sentiment_confidence": 0.0,
  "tags": ["...", "..."],
  "language": "..."
}}

For example:

{{
  "summary": "This article discusses the recent improvements in local education funding...",
  "sentiment": "positive",
  "sentiment_confidence": 0.85,
  "tags": ["education", "funding", "local news", "policy"],
  "language": "english"
}}

Now, here is the text of the news article you should analyze:

\"\"\" {article_text} \"\"\" """
    }
    try:
        response = client.responses.create(
            model="gpt-5-mini",  # Update the Model you want
            input=[system_message, user_message],
        )
        llm_response = response.output_text
        parsed = json.loads(llm_response)
        summary = parsed.get("summary", "No summary found.")
        sentiment = parsed.get("sentiment", "No sentiment found.")
        confidence = parsed.get("sentiment_confidence", 0)
        tags = parsed.get("tags", [])
        language = parsed.get("language", "Unknown")
        return summary, f"{sentiment} (confidence: {confidence})", tags, language
    except Exception as e:
        error_msg = f"Error during LLM analysis: {str(e)}"
        return error_msg, "N/A", [], "Unknown"

# Function to update the Gradio UI with the results from the LLM
def gradio_interface(article_text):
    if len(article_text) > 20000: # 10000
        return "Error: Article is too long.", "N/A", "N/A", "N/A"
    summary, sentiment, tags, language = analyze_news_article(article_text)
    with open("analysis_history.txt", "a") as f:
        f.write(f"Summary: {summary}\nSentiment: {sentiment}\nTags: {tags}\nLanguage: {language}\n---\n")
    return f"Summary:\n{summary}", f"Sentiment: {sentiment}", f"Tags: {tags}", f"Language: {language}"

# Build the Gradio app
with gr.Blocks() as demo:
    gr.Markdown("# News Analyzer (Summarize, Sentiment, and Tags)")
    article_input = gr.Textbox(
        label="Paste your news article here",
        placeholder="Type or paste the text of a news article..."
    )
    analyze_button = gr.Button("Analyze")
    summary_output = gr.Textbox(label="Summary")
    sentiment_output = gr.Textbox(label="Sentiment")
    tags_output = gr.Textbox(label="Tags")
    language_output = gr.Textbox(label="Language")
    analyze_button.click(
        fn=gradio_interface,
        inputs=article_input,
        outputs=[summary_output, sentiment_output, tags_output, language_output]
    )

if __name__ == "__main__":
    demo.launch()
