# Flirtbot
A RAG Enhanced Chatbot for Romantic Conversations. The goal of this project was simply to get a feel for how RAG systems work and develop a simple RAG system capable of retrieving information from an external source. 

## How to use the flirtbot
In order to test the flirtbot, first clone the repo and save it on your local computer. Get an OpenAI API key and enter it in flirtbot.py (where it currently says 'Enter your own API key here'). Next, open up a new terminal shell and run python3 flirtbot.py. You should be prompted to enter some background information and the flirtbot should return some flirtacious sentences to choose from. 

## The Database
For the RAG system, I utilized Love is Blind transcripts available online at: https://tvshowtranscripts.ourboard.org/viewforum.php?f=1243

Each episode has a separate link, so the data of each episode has to be extracted separately (a script was written to perform this). 

## Brief File Description
Below is a brief description of the repository and how to replicate the results shown.
**Building the text database**
1. create_texts.py
This file is used to extract the text of each episode. To use this file, simply change the url and name to the desired one in the main function. The script will then create a text file of all of the dialogue in the episode in the "texts" folder.
2. combine_text.py
This file combines all of the files in the "texts" folder into one text file to be turned into a vector database.
3. transcipts.txt
This file contains all of the dialogue from the texts folder into one file. This file is the result of combine_text.py
**Creating the Vector Database (ChromaDB)**
1. create_chromadb.py
This file utilizes ChromaDB to build a persistent vector database. It takes the transcripts.txt file and chunks the file into separate sentences. Each sentence is then embedded in order to be compared via semantic similarity for the RAG system.
2. DB_info.py
This file is a helper function used to peak into the ChromaDB database. This file was mainly used to verify the information within the database during development. (only a very simple one is present currently for this repository)
**Developing the RAG system**
1. flirtbot.py
This is the main file in the repository and handles the logic for the RAG system. This file utilizes a retriever that retrieves semantically similar sentences to the prompt and a generator that uses the prompt with the retrieved sentences to generate a response. Some prompt engineering was used to align the model with the primary task of the project.
## Future Work
1. Add a larger variety of data so the model, enlarging the background database and allowing the model to pull better contextual sentences.
2. Compare the OpenAI API based model to a custom LLM that does not require an API key (or credits to use properly).
3. Create a simple web-based interface to make the flirtbot more accessible and easier for users to utilize. 