#    ____                        __                       ___    ____
#   / __ \____ _____  ___  _____/ /   ___  ____  _____   /   |  /  _/
#  / /_/ / __ `/ __ \/ _ \/ ___/ /   / _ \/ __ \/ ___/  / /| |  / /  
# / ____/ /_/ / /_/ /  __/ /  / /___/  __/ / / (__  )  / ___ |_/ /   
#/_/    \__,_/ .___/\___/_/  /_____/\___/_/ /_/____/  /_/  |_/___/   
#           /_/                                                      
#   By: Allan Edh (allan.edh@gmail.com)
#
# Description:
# PaperLens AI is a tool developed for summarizing and doing topic modelling completely free on a large number of research paper PDFs -- mainly beneficial for litterature reviews.
# Instrucions:
# Install the required libraries in your terminal of choice: 'PyPDF2' & 'groq'
# Edit this script to (1)Include a free Groq API token, (2)Substitute the default prompts to your liking, (3)Modify AI query parameters for your use, (4)Edit rate limits and chunk size accordingly.
# Run the script with Python3 for your folder of PDFs like so: 'python PaperLensAI.py <input-folder>'

import os
import sys
import time
import PyPDF2
import groq
from groq import Groq

# Record time to process
start_time = time.time()

# Load Groq API key
client = Groq(
    api_key="<API-KEY-GOES-HERE>" # <-- ENTER API KEY HERE
)

# Groq query (change accordingly)
def groq_query(context, prompt):
    chat_completion = client.chat.completions.create(
        messages=[
        {
            "role": "system",
            # EDIT SYSTEM/CONTEXT PROMPT:
            "content": context,
        },
        {
            "role": "user",
            "content": prompt, 
        },
        ],
        # CHOOSE LLM MODEL:
        model="llama3-8b-8192",
        # INCREASE LIKELIHOOD TO TALK ABOUT NEW TOPICS (-2.0 -- 2.0):  
        presence_penalty=0,
        # LOWER TO INCREASE DETERMINISM & DECREASE HALLUCINATION (-2.0 -- 2.0):
        temperature=0.3,
        # SET SEED FOR LESS RANDOMNESS BETWEEN DIFFERENT USES:
        seed=10,
    )
    return chat_completion

# Extract text from PDF
def extract_text_from_pdf(pdf_path, txt_path):
    try:
        # Open PDF
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""

            # Iterate through pages
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
            # If PDF contains not text prompt error
                if text == "":
                    print(pdf_path + " contains no text!")

        # Write output text to folder
        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)
    except Exception as e:
        print(f"Error while extracting text from {pdf_path}: {e}")

# Iterate through PDFs
def extract_texts_from_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            txt_filename = f"{os.path.splitext(filename)[0]}.txt"
            txt_path = os.path.join(output_folder, txt_filename)
            extract_text_from_pdf(pdf_path, txt_path)

# Split text file into chunks
def read_and_split_file(file_path, max_chunk_size=5000): # <-- EDIT MAX CHARACTER CHUNK SIZE
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        # Split text into chunks and save to list
        chunks = [text[i:i+max_chunk_size] for i in range(0, len(text), max_chunk_size)]
        return chunks
    except Exception as e:
        print(f"Error while splitting text into chunks: {e}")

# Perform chat completion with Groq
def process_folder(folder_path):
    try:
        # Iterate through text files
        for filename in os.listdir(folder_path):
            if filename.endswith('.txt'):
                # Do split for current file
                file_path = os.path.join(folder_path, filename)
                chunks = read_and_split_file(file_path)
                if chunks:
                    num = 0
                    summarize = ""
                    for y in range(len(chunks)):
                        # AI instructions for Groq:
                        context = "You are an expert research assistant in reading through and summarizing research papers in social science and economics. You give answers directly without saying things like 'Here is a summary' before answering. You will be given a part of a research paper. You will summarize the part in the form of a ca 150 words-long single-paragraph coherent text with no bullet points. Focus on the content and try to ignore what looks like footnote references."
                        prompt = ""
                        if num == 0:
                            prompt += "Begin your answer with a separate line containing the title of the research paper beginning like 'Title:' and a separate line with the author(s) beginning like 'Authors:'." + "\n"
                        prompt += chunks[num]
                        if prompt != "":
                            chat_completion = groq_query(context, prompt)
                            summarize += chat_completion.choices[0].message.content + "\n" + "\n"
                            time.sleep(0.5) # <--- EDIT RATE LIMIT BETWEEN API REQUESTS
                        # Loop logic
                        num += 1
                    
                    # Write summary to outfile
                    summarized_filename = f"{os.path.splitext(filename)[0]}_long.txt"
                    summarized_file_path = os.path.join(sum_folder, summarized_filename)
                    with open(summarized_file_path, 'w', encoding='utf-8') as sum_file:
                        sum_file.write(summarize)
                    print("\n" + "'" + filename + "'" + " first round summary done!")

    except Exception as e:
        print(f"Error while querying AI: {e}")

# Final summarizaiton of PDF
def final_summary(folder_path):
    try:
        # Iterate through summarized folder
        for filename in os.listdir(folder_path):
            if filename.endswith('_long.txt'):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    sum_content = file.read()
                
                # AI instructions for Groq
                context = "You are an expert research assistant in reading through and summarizing research papers in social science and economics. You give answers directly without saying things like 'Here is a summary' before answering. You will be given a summary of a research paper. You will summarize it further to a ca 300 words-long coherent text written in passive voice with no bullet points. Begin your answer with a separatate line with the title of the paper beginning with 'Title:', and a separate line with the author(s) as seen in the beginning of the file (in your answer beginning with 'Authors:'), followed by a separate line starting with 'Topics:' stating the ten most important topics discussed in the form of keywords, ranged in the order of most important to least."
                prompt = sum_content
                chat_completion = groq_query(context, prompt)
                final_completion = chat_completion.choices[0].message.content

                # Write summary to outfile
                final_filename = f"{os.path.splitext(filename)[0]}_short.txt"
                final_path = os.path.join(final_folder, final_filename)
                with open(final_path, 'w', encoding='utf-8') as final_file:
                    final_file.write(final_completion)
                print("\n" + "'" + filename + "'" + " second round summary done!")
                time.sleep(0.5) # <--- EDIT RATE LIMIT BETWEEN API REQUESTS

    except Exception as e:
        print(f"Error while performing final summarize: {e}")

# Join together all summaries
def joined_document(folder_path):
    try:
        joined = ""
        joined_filename = "AllSummaries_PaperLensAI.txt"
        # Iterate through final folder
        for filename in os.listdir(folder_path):
            if filename.endswith('_long_short.txt'):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    final_content = file.read()
                    joined += final_content + "\n\n" + "---------------------------------------------------" + "\n\n"
        # Write joined content to outfile   
        with open(joined_filename, 'w', encoding='utf-8') as joined_file:
            joined_file.write(joined)
        print("\n" + "---------------------------------------------------" + "\n" + "'" + joined_filename + "'" + " saved to: " + file_path)

    except Exception as e: 
        print(f"Error creating joined text file: {e}")

# Main
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("\n" + "Usage: python3 PaperLensAI.py <input-folder>")
        sys.exit(1)
    folder_path = sys.argv[1]

    # Create output folders
    parent_folder = os.path.dirname(folder_path)
    output_folder = os.path.join(parent_folder, f"{os.path.basename(folder_path)}_text")
    os.makedirs(output_folder, exist_ok=True)
    sum_folder = os.path.join(parent_folder, f"{os.path.basename(folder_path)}_long")
    os.makedirs(sum_folder, exist_ok=True)
    final_folder = os.path.join(parent_folder, f"{os.path.basename(folder_path)}_short")
    os.makedirs(final_folder, exist_ok=True)

    # Run extraction and summarizer
    print("\n" + "Extracting texts from PDFs...")
    extract_texts_from_folder(folder_path)
    print("\n" + "Processing long summarization...")
    process_folder(output_folder)
    print("\n" + "Processing short summarization...")
    final_summary(sum_folder)
    print("\n" + "Joining short summaries to file...")
    joined_document(final_folder)
    pdf_count = len([entry for entry in os.listdir(folder_path) if entry.lower().endswith('.pdf')])
    print("\n" + str(pdf_count) + " PDFs finished processing in %s seconds." % (time.time() - start_time) + "\n")
    print("Thank you for using PaperLens AI, created by Allan Edh. Feel free to contact allan.edh@gmail.com for questions." + "\n")
