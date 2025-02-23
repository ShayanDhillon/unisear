import google.generativeai as genai
import os
from dotenv import load_dotenv;

def gemini_txt_wrapper(context):
    """
    Wraps the Gemini API to process text content from a file and answer a user's question.

    Args:
        file_path (str): Path to the text file.
        user_question (str): The question the user wants to ask about the text file.

    Returns:
        str: Gemini API response text, or None if there was an error.
    """
    load_dotenv();
    try:
        api_key = os.getenv("GOOGLE_API_KEY") # get api from env
        if not api_key:
            return "Error: GOOGLE_API_KEY environment variable not set. Please set it." # incase wrong api key
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro') # get the model

        # Improved prompt for better accuracy and formatting
        prompt_text = f"Summarize: {context}"

        response = model.generate_content(prompt_text) # response

        return response.text # return the response
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":

    user_question = input("Enter your question about the text file: ")
    file_path = "related_rows.txt"
    with open(file_path, 'r', encoding='utf-8') as file:
        context = file.read() # read file
    gemini_response = gemini_txt_wrapper(context, user_question)
    if gemini_response and gemini_response.startswith("Error"):
        print(gemini_response) # Print error message
    elif gemini_response:
        print("\nQuestion:\n", user_question) # Print the question asked
        print("\nGemini Answer:\n")
        print(gemini_response)
    else:
        print("No response from Gemini or an unexpected error occurred.")
