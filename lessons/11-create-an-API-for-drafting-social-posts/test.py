import requests
import threading

# Dictionary to store responses from threads
responses = {}

def test_generate_posts(article, num_posts, key, platform="LinkedIn"):
    """
    Sends a POST request to generate social media posts for the given article.
    Stores the response in the shared `responses` dictionary.
    """
    url = "http://127.0.0.1:8000/generate-posts"
    payload = {"article_text": article, "num_posts": num_posts, "platform": platform}
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        responses[key] = response.json().get("drafts", [])
    else:
        responses[key] = f"Error: {response.status_code}, {response.text}"

def main():
    # Define articles
    article_1 = "Dogs are wonderful pets that bring joy."
    article_2 = "Quantum computing is the future of technology."

    num_posts = 3  # Number of social media posts to generate per article

    # Start two threads for concurrent requests with different platforms
    t_1 = threading.Thread(target=test_generate_posts, args=(article_1, num_posts, "article_1", "LinkedIn"))
    t_2 = threading.Thread(target=test_generate_posts, args=(article_2, num_posts, "article_2", "Facebook"))

    t_1.start()
    t_2.start()

    t_1.join()
    t_2.join()

    # Print generated drafts from both threads
    print("\nGenerated drafts for article 1:")
    print(responses.get("article_1", "No response received"))

    print("\nGenerated drafts for article 2:")
    print(responses.get("article_2", "No response received"))

    # Retrieve and print all stored posts
    url = "http://127.0.0.1:8000/posts"
    response = requests.get(url)
    
    if response.status_code == 200:
        print("\nAll generated posts stored in data.json:")
        print(response.json())
    else:
        print("\nError retrieving posts:", response.status_code, response.text)

    # Retrieve and print summary information
    summary_url = "http://127.0.0.1:8000/summary"
    summary_response = requests.get(summary_url)
    if summary_response.status_code == 200:
        print("\nSummary:")
        print(summary_response.json())
    else:
        print("\nError retrieving summary:", summary_response.status_code, summary_response.text)

if __name__ == "__main__":
    main()
