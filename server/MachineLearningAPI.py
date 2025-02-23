import faiss
import json;
import os;

import pandas as pd
import numpy as np

from sentence_transformers import SentenceTransformer;
from transformers import pipeline;

# Time needed to auto update scrapper information
SCRAPED_DATA_FILE_NAME = "scraped_data.csv";
EMBEDDINGS_DATA_FILE_NAME = "embeddings.npy";

class MachineLearningAPI():
    def __init__(self, file_path : str):
        # Initialize file_path
        self.file_path = file_path;
        # Load the encoding model
        self.model = SentenceTransformer("all-MiniLM-L6-v2");
        # Load the summarizer model
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        # Load Q and A model
        self.qa_model = pipeline("question-answering", model="deepset/roberta-base-squad2")
        # First load the data frame
        self.df = self.loadScrapedDataFrameData();

        # The embeddings
        self.embeddings_file = self.loadOrCreateEmbeddings();

        # Creates an index for faiss
        self.index = self.createFaissIndex();
        pass;

    def loadScrapedDataFrameData(self):
        try: 
            self.df = pd.read_csv(f"{self.file_path}/{SCRAPED_DATA_FILE_NAME}");
        except Exception as e:
            print(f"Failed to {SCRAPED_DATA_FILE_NAME} at {self.file_path}: {e}");
        return self.df;

    def loadOrCreateEmbeddings(self):
        # First check if embeddings path exists
        file_dir = f"{self.file_path}/{EMBEDDINGS_DATA_FILE_NAME}";

        # Before creating embeddings load the prompts
        self.df["Prompt"] = self.df["Header"] + ": " + self.df["Content"];

        if os.path.exists(file_dir):
            print(f"Loading precomputed embeddings file: {self.file_path}/{EMBEDDINGS_DATA_FILE_NAME}");
            self.embeddings_file = np.load(file_dir);
            return self.embeddings_file;
        else:
            # If it doesn't exist load it
            print(f"Creating embeddings for: {self.file_path}");
            # Create the embeddings
            embeddings = self.model.encode(self.df["Prompt"].to_list(), show_progress_bar=True);
            self.embeddings_file = embeddings;

            # Save embeddings to the file_directory
            np.save(file_dir, embeddings);

            return self.embeddings_file;

        self.encoder = SentenceTransformer("paraphrase-mpnet-base-v2");
        return self.encoder;
    def createFaissIndex(self):
        dimension = self.embeddings_file.shape[1];
        self.index = faiss.IndexFlatL2(dimension);
        self.index.add(self.embeddings_file.astype(np.float32));
        return self.index;

    def findSimilarPrompts(self, query, top_k):
        # Encode the query;
        query_embedding = self.model.encode([query]).astype(np.float32);

        # Find similarities
        distances, top_indices = self.index.search(query_embedding, top_k);

        # Gets the top similarities
        top_indices = top_indices.flatten();

        # Convert FAISS L2 distances to similarity scores (1 / (1 + distance))
        similarity_scores = 1 / (1 + distances.flatten())
    
        # Return the top-k prompts 
        return [(self.df.iloc[idx]["Prompt"], similarity_scores[i]) for i, idx in enumerate(top_indices)]

    def answerQuestion(self, query):
        print(f"Answering question for query: {query}");
        # Find similar prompts;
        similar_prompts = self.findSimilarPrompts(query, 5);
        if not similar_prompts:
            return {
                "query": query,
                "error": "No similar prompts found.",
            }
        
        combined_context = " ".join([prompt for prompt, _ in similar_prompts]);
        
        tokens = self.summarizer.tokenizer(combined_context, return_tensors="pt", truncation=True, max_length=1024)
        
        truncated_text = self.summarizer.tokenizer.decode(tokens['input_ids'][0], skip_special_tokens=True);
        
        answer = self.qa_model(question=query, context=truncated_text, max_answer_length=200);
        return {
            "query": query,
            "answer": answer["answer"],
            "confidence": answer['score'],
        }

    def summarize(self, query):
        print(f"Summarizing for query: {query}");
        # Find similar prompts
        similar_prompts = self.findSimilarPrompts(query, 5);
        if not similar_prompts:
            return {
                "query": query,
                "error": "No similar prompts found.",
            }

        combined_content = " ".join([prompt for prompt, _ in similar_prompts]);
        
        # Truncate the input text if necessary
        tokens = self.summarizer.tokenizer(combined_content, return_tensors="pt", truncation=True, max_length=1024)
        
        truncated_text = self.summarizer.tokenizer.decode(tokens['input_ids'][0], skip_special_tokens=True);
        
        summary_text = self.summarizer(truncated_text, max_length=300, min_length=100, do_sample=False)[0]["summary_text"];

        return {
            "query" : query,
            "top_prompts": similar_prompts,
            "combined_content": combined_content,
            "answer" : summary_text,
        }

    def query(self, query : str):
        if query[-1] == "?":
            return self.answerQuestion(query);  
        else:
            return self.summarize(query);

