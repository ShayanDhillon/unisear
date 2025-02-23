import faiss
import json;
import os;
import traceback;
import time;
import threading;

import pandas as pd
import numpy as np

from sentence_transformers import SentenceTransformer
from transformers import T5Tokenizer, T5ForConditionalGeneration
from WebScraperAPI import WebScraperAPI;

# Time needed to auto update scrapper information
AUTO_UPDATE_INTERVAL = 259200; 
SCRAPED_DATA_FILE_NAME = "scrapped_data.txt";
VECTOR_DATA_FILE_NAME = "VectorDB.index";

class MLFlowAPI():
    def __init__(self, file_path : str, web_scraper_api : WebScraperAPI):
        # Initialize file_path
        self.file_path = file_path;
        # Give ourselves the correct web scrapper
        self.web_scraper_api = web_scraper_api;

        # Next load up the encoder
        self.encoder = None;
        self.initializeEncoder();

        # Do we need to rescrape data?
        # Check the time difference
        current_time = int(time.time());
        with open(self.file_path + "/meta_data.json", "r") as file:
            data = json.load(file);
            print(current_time - int(data['scrape_time']));
            if current_time - int(data['scrape_time']) >= AUTO_UPDATE_INTERVAL and not self.web_scraper_api.scraping:
                print("Would update")
                thread = threading.Thread(target=self.web_scraper_api.scrapeAndSave);
                thread.start();
        # First load the data frame
        self.df = None;
        self.scrapedDataToDataFrame();

        # Load the vector db
        # self.storeDataFrameAsVectorDB();

        pass;

    def getScrapedDataFromFile(self):
        try:
            if not os.path.exists(self.file_path):
                raise FileNotFoundError(f"File not found: {self.file_path}");
            
            sentences = [];
            # read all lines
            with open(self.file_path + f"/{SCRAPED_DATA_FILE_NAME}", 'r', encoding='utf-8', errors="replace") as file:
                sentences = file.readlines()
            sentences = [sentence for sentence in sentences];
            return sentences;

        except FileNotFoundError as e:
            print(f"File not found error: {e}");
        except Exception as e:
            print(f"getScrapedDataFromFile exception: {e}");

    def scrapedDataToDataFrame(self):
        try:
            scraped_data = self.getScrapedDataFromFile();
            #assign df to return
            self.df = pd.DataFrame(scraped_data, columns=["text"])
        except Exception as e:
            print(e);
        return self.df

    def initializeEncoder(self):
        self.encoder = SentenceTransformer("paraphrase-mpnet-base-v2");
    
    def storeDataFrameAsVectorDB(self):
        # Called when VectorDB.index needs to be created
        file_name = self.file_path + r"/scrapped_data.txt"
        index_file_name = self.file_path + r'/VectorDB.index'
        
        if self.df is None:
            print("Error: DataFrame is none. Please call scrapedDataToDataFrame.");
            return

        try:
            #ENCODE TEXT 
            text = self.df['text'].tolist() # FIX THIS, it doesnt do full text for each string (convert to array?)
            encoder = self.encoder # pre trained model

            embeddings = encoder.encode(text, batch_size = 32, show_progress_bar=True) # for improvement try batch encoding

            #INDEX FILE WRITING
            vector_dimensions = embeddings.shape[1]
            index = faiss.IndexFlatL2(vector_dimensions) # malloc based on dimensions

            # write to index
            index.add(embeddings)

            # write index to vectorDB file
            faiss.write_index(index, index_file_name)

        except Exception as e:
            print(f"An error occurred during embedding or indexing: {e}")
            traceback.print_exc();
        
        return

    def queryModel(self, query, text_response_size):
        '''RETURNS INFORMATION TO SUMMARIZE'''
        file_name = self.file_path + r"/scrapped_data.txt"
        index_file_name = self.file_path + r"/VectorDB.index"
        index = None
        try:
            # MAKE SURE INDEX DB exists
            if not os.path.exists(index_file_name):
                # Save the dataFrame as vector if the file does not exist;
                self.storeDataFrameAsVectorDB();
            
            index = faiss.read_index(index_file_name)

            #define encoder
            encoder = self.encoder; # pre trained model

            #make query into vector
            vectorized_query = encoder.encode(query, show_progress_bar=True) 
            vectorized_query_2d = np.array([vectorized_query]) #needs to be 2d to normalize

            #normalize query vector
            faiss.normalize_L2(vectorized_query_2d)

            #find distances and ann
            distances,ann = index.search(vectorized_query_2d,k=4)

            #combine our df's to see closest text pairs
            text_df = self.df;
            if (text_df is None):
                return ''

            nearest_vectors = pd.DataFrame({'distances': distances[0], 'ann':ann[0]})

            text_distance_df = pd.merge(nearest_vectors,text_df,left_on='ann',right_index=True)

            #find X closest texts
            x = text_response_size
            if(text_distance_df.shape[1] < x):
                x = text_distance_df.shape[1]

            text_list = text_distance_df[0:x]['text'].to_list()
            full_text  = '\n'.join(text_list) # JOIN BASED ON WHATEVER DELIMITER IS BEST FOR SUMMARY OF ENTIRE TEXT

        except FileNotFoundError as e:
            print(e)
            return ''
        except Exception as e:
            print(f"An error occurred: {e}")
            return ''

        return full_text

    def summarizeQuery(self, query):
        # called when user asks a question,
        get_x_texts = 10 
        #get relevent text using vector db
        relevant_text  = self.queryModel(query, get_x_texts)
        if(relevant_text == ''):
            return "no relevant info found..."

        #load model
        model_name = 't5-small'  # Or 't5-base' or 't5-3b'
        tokenizer = T5Tokenizer.from_pretrained(model_name, legacy=False)
        model = T5ForConditionalGeneration.from_pretrained(model_name)

        #Summarize prompt, could use changing?
        input_text = f"Summarize the following text, focusing on {query}: {relevant_text}"

        # tokenize the input text, could use changing?
        input_ids = tokenizer.encode(input_text, return_tensors="pt", max_length=1024, truncation=True)

        # generate summary :pray:, find out what these parameters are and tune them
        summary_ids = model.generate(input_ids, max_length=200, num_beams=4, early_stopping=True)

        # decode summary
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)


        return summary

