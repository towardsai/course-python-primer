import os
import json
import math
from typing import List, Dict
import gradio as gr

from openai import OpenAI

#######################################################
# Sample documents with titles
#######################################################
SAMPLE_DOCUMENTS = [
    {"title": "Doc1: DeepSeek R1", "content": """Doc1: 1. Introduction: We introduce our first-generation reasoning models, DeepSeek-R1-Zero and DeepSeek-R1. DeepSeek-R1-Zero, a model trained via large-scale reinforcement learning (RL) without supervised fine-tuning (SFT) as a preliminary step, demonstrated remarkable performance on reasoning. With RL, DeepSeek-R1-Zero naturally emerged with numerous powerful and interesting reasoning behaviors. However, DeepSeek-R1-Zero encounters challenges such as endless repetition, poor readability, and language mixing. To address these issues and further enhance reasoning performance, we introduce DeepSeek-R1, which incorporates cold-start data before RL. DeepSeek-R1 achieves performance comparable to OpenAI-o1 across math, code, and reasoning tasks. To support the research community, we have open-sourced DeepSeek-R1-Zero, DeepSeek-R1, and six dense models distilled from DeepSeek-R1 based on Llama and Qwen. DeepSeek-R1-Distill-Qwen-32B outperforms OpenAI-o1-mini across various benchmarks, achieving new state-of-the-art results for dense models.
        NOTE: Before running DeepSeek-R1 series models locally, we kindly recommend reviewing the Usage Recommendation section. 2. Model Summary: Post-Training: Large-Scale Reinforcement Learning on the Base Model. We directly apply reinforcement learning (RL) to the base model without relying on supervised fine-tuning (SFT) as a preliminary step. This approach allows the model to explore chain-of-thought (CoT) for solving complex problems, resulting in the development of DeepSeek-R1-Zero. DeepSeek-R1-Zero demonstrates capabilities such as self-verification, reflection, and generating long CoTs, marking a significant milestone for the research community. Notably, it is the first open research to validate that reasoning capabilities of LLMs can be incentivized purely through RL, without the need for SFT. This breakthrough paves the way for future advancements in this area. We introduce our pipeline to develop DeepSeek-R1. The pipeline incorporates two RL stages aimed at discovering improved reasoning patterns and aligning with human preferences, as well as two SFT stages that serve as the seed for the model's reasoning and non-reasoning capabilities. We believe the pipeline will benefit the industry by creating better models."""},
    {"title": "Doc2: OpenAI o1", "content": """Doc2: OpenAI o1 is a generative pre-trained transformer (GPT). A preview of o1 was released by OpenAI on September 12, 2024. o1 spends time "thinking" before it 
      answers, making it better at complex reasoning tasks, science and programming than GPT-4o.[1] The full version was released to ChatGPT users on December 5, 2024"""},
    {"title": "Doc3: Python Programming", "content": """Doc3: The Python programming language emphasizes readability and simplicity.
    It is widely used for data analysis, web development, and artificial intelligence.
    Python's ecosystem includes many libraries for scientific computing."""},
    {"title": "Doc4: Healthy Lifestyle", "content": """Doc4: A balanced diet contains fruits, vegetables, protein sources, and whole grains.
    Consistent exercise can help maintain healthy body weight.
    Both nutrition and exercise are vital components of a healthy lifestyle."""},
    {"title": "Doc5: Photosynthesis", "content": """Doc5: The process of photosynthesis converts light energy into chemical energy in plants.
    Chlorophyll molecules absorb sunlight.
    Water, carbon dioxide, and sunlight are used to produce glucose and oxygen."""}
]

#######################################################
# Our OOP class for Document-based QA (RAG)
#######################################################
class RAGChatBot:
    """
    RAGChatBot manages:
    - Document text, titles, & embeddings
    - A method to compute similarity
    - A method to retrieve top docs
    - A method to query the LLM with a custom prompt
    """
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.documents = []
        self.embeddings = []

    def embed_documents(self, docs: List[Dict[str, str]]) -> None:
        """
        Embeds each document's content using OpenAI embeddings and stores results.
        """
        self.documents = docs
        self.embeddings = []
        for doc in docs:
            response = self.client.embeddings.create(
                input=doc["content"],
                model="text-embedding-3-small"
            )
            embedding_vector = response.data[0].embedding
            self.embeddings.append(embedding_vector)

    def save_embeddings_to_json(self, filepath: str) -> None:
        """
        Saves documents and their embeddings to a JSON file.
        """
        data_to_save = []
        for doc, embedding in zip(self.documents, self.embeddings):
            data_to_save.append({
                "title": doc["title"],
                "content": doc["content"],
                "embedding": embedding
            })
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data_to_save, f)

    def load_embeddings_from_json(self, filepath: str) -> None:
        """
        Loads documents and embeddings from a JSON file.
        """
        with open(filepath, "r", encoding="utf-8") as f:
            loaded_data = json.load(f)
        self.documents = []
        self.embeddings = []
        for item in loaded_data:
            self.documents.append({"title": item["title"], "content": item["content"]})
            self.embeddings.append(item["embedding"])

    def cosine_similarity(self, vec_a: List[float], vec_b: List[float]) -> float:
        """
        Computes cosine similarity between two vectors.
        """
        dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = math.sqrt(sum(a * a for a in vec_a))
        norm_b = math.sqrt(sum(b * b for b in vec_b))
        if norm_a == 0 or norm_b == 0:
            return 0
        return dot_product / (norm_a * norm_b)

    def retrieve_top_documents(self, query: str, top_k: int = 2) -> List[Dict[str, str]]:
        """
        Embeds the query, compares with document embeddings, returns top_k documents.
        """
        response = self.client.embeddings.create(
            input=query,
            model="text-embedding-3-small"
        )
        query_vec = response.data[0].embedding
        sims = []
        for idx, emb in enumerate(self.embeddings):
            sim_score = self.cosine_similarity(query_vec, emb)
            sims.append((sim_score, idx))
        sims.sort(key=lambda x: x[0], reverse=True)
        top_docs = [self.documents[i[1]] for i in sims[:top_k]]
        return top_docs

    def summarize_doc(self, doc_text: str) -> str:
        """
        Generates a one-sentence summary for the given document text.
        """
        summary_prompt = f"Summarize this document in one short sentence:\n\n{doc_text}"
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": summary_prompt}],
        )
        return response.choices[0].message.content.strip()

    def answer_query(self, query: str, top_k: int = 2) -> str:
        """
        Creates a prompt using top documents as context, calls the LLM, and returns the final answer.
        """
        top_docs = self.retrieve_top_documents(query, top_k=top_k)
        context_str = "\n\n---\n\n".join(f"{doc['title']}\n{doc['content']}" for doc in top_docs)
        prompt = f"""
You are a helpful assistant. Use ONLY the following documents to answer the user query:
-----
{context_str}
-----

If the answer is not found in the documents, say: "I can't find the answer in the documents."

User query: {query}
Answer:
        """.strip()
        chat_response = self.client.responses.create(
            model="gpt-5-mini",
            input=[{"role": "user", "content": prompt}],
        )
        answer = chat_response.output_text
        used_titles = [doc["title"] for doc in top_docs]
        doc_summaries = [self.summarize_doc(doc["content"]) for doc in top_docs]
        summary_str = "\n\nDocument Summaries:\n" + "\n".join(f"{title}: {summary}" for title, summary in zip(used_titles, doc_summaries))
        final_answer = answer + f"\n\n(Used documents: {', '.join(used_titles)})" + summary_str
        return final_answer

#######################################################
# Building the Gradio Interface
#######################################################
def main():
    EMBEDDINGS_JSON = "doc_embeddings.json"
    api_key = "YOUR_OPENAI_API_KEY"
    rag_bot = RAGChatBot(api_key=api_key)
    if not os.path.exists(EMBEDDINGS_JSON):
        rag_bot.embed_documents(SAMPLE_DOCUMENTS)
        rag_bot.save_embeddings_to_json(EMBEDDINGS_JSON)
    else:
        rag_bot.load_embeddings_from_json(EMBEDDINGS_JSON)

    def ask_question(user_query, k):
        return rag_bot.answer_query(user_query, top_k=k)

    with gr.Blocks() as demo:
        gr.Markdown("## Chat with Your Documents - RAG Demo")
        user_input = gr.Textbox(label="Enter your query about the documents here:")
        num_docs_slider = gr.Slider(minimum=1, maximum=5, step=1, value=2, label="Number of documents to retrieve")
        answer_output = gr.Textbox(label="Answer:")
        submit_button = gr.Button("Submit")
        submit_button.click(
            fn=ask_question,
            inputs=[user_input, num_docs_slider],
            outputs=answer_output
        )
    demo.launch()

if __name__ == "__main__":
    main()
