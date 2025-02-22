from sentence_transformers import SentenceTransformer
import faiss
import pandas as pd
import numpy as np
import os
from transformers import T5Tokenizer, T5ForConditionalGeneration


def text_to_df(self, file_name):
    '''
    returns a df of text
    '''
    df = None
    try:

        if not os.path.exists(file_name):
            raise FileNotFoundError(f"File not found: {file_name}")

        sentences = ''

        # read all lines
        with open(file_name, 'r') as file:
            sentences = file.readlines()

        # strip them
        sentences = [sentence.strip() for sentence in sentences]

        #assign df to return
        df = pd.DataFrame(sentences, columns=["text"])

    except FileNotFoundError as e:
        print(e)
    
    except Exception as e:
        print(f"An error occurred while reading the file '{file_name}': {e}")
    
    return df


def embed_data(self, path):
    #CALLED WHEN DATA IS SCRAPED
    file_name = path + "scrapped_data.txt"
    index_file_name = path + 'VectorDB.index'
    
    df = text_to_df(file_name)
    if df is None:
        print("Error: Failed to read the text file.")
        return

    try:
        #ENCODE TEXT 
        text = df['text'].tolist() # FIX THIS, it doesnt do full text for each string (convert to array?)
        encoder = SentenceTransformer("paraphrase-mpnet-base-v2", batch_size = 32, show_progress_bar=True) # pre trained model

        embeddings = encoder.encode(text) # for improvement try batch encoding


        #INDEX FILE WRITING
        vector_dimensions = embeddings.shape[1]
        index = faiss.IndexFlatL2(vector_dimensions) # malloc based on dimensions

        # write to index
        index.add(embeddings)

        # write index to vectorDB file
        faiss.write_index(index, index_file_name)

        #possibly try writing meta data file?

    except Exception as e:
        print(f"An error occurred during embedding or indexing: {e}")

    
    return





def get_info(self, path, query, get_x_texts):
    '''RETURNS INFORMATION TO SUMMARIZE'''

    file_name = path + "scrapped_data.txt"
    index_file_name = path + "VectorDB.index"
    index = None
    try:
        # MAKE SURE INDEX DB exists
        if not os.path.exists(index_file_name):
            raise FileNotFoundError(f"FAISS index file not found at: {index_file_name}")
        
        index = faiss.read_index(index_file_name)

        # MAKE SURE META DATA EXISTS IF WE USE IT

        #define encoder
        encoder = SentenceTransformer("paraphrase-mpnet-base-v2", batch_size = 32, show_progress_bar=True) # pre trained model


        #make query into vector
        vectorized_query = encoder.encode(query) 
        vectorized_query_2d = np.array([vectorized_query]) #needs to be 2d to normalize

        #normalize query vector
        faiss.normalize_L2(vectorized_query_2d)

        #find distances and ann
        distances,ann = index.search(vectorized_query_2d,k=4)

        #combine our df's to see closest text pairs
        text_df = text_to_df(file_name)
        if (text_df is None):
            return ''

        nearest_vectors = pd.DataFrame({'distances': distances[0], 'ann':ann[0]})

        text_distance_df = pd.merge(nearest_vectors,text_df,left_on='ann',right_index=True)

        #find X closest texts
        x = get_x_texts
        if(text_distance_df.shape[1] < x):
            x = text_distance_df.shape[1]

        text_list = text_distance_df[0:x]['text'].to_list()
        full_text  = '\n'.join(text_list) # JOIN BASED ON WHATEVER DELIMITER IS BEST FOR SUMMARY OF ENTIRE TEXT

    except FileNotFoundError as e:
        print(e)
        return ''
    except Error as e:
        print(f"An error occurred: {e}")
        return ''

    return full_text





def summarize_query(self, path, query):
    # called when user asks a question,
    get_x_texts = 10 
    #get relevent text using vector db
    relevant_text  = get_info(path, query, get_x_texts)
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



