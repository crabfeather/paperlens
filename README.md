# PaperLens AI

### Description:
PaperLens AI is a Python tool for summarizing and applying topic model methods on a large number of research paper PDFs completely for free using the *Groq* API. It was developed primarily for doing quick literature reviews during my internship at Stockholm School of Economics, but can also be used for basic Retrieval-Augmented Generation (RAG). Using the default settings it can process ca 4 standard-length papers/minute using the *Llama3 8B* model.<br/>

### How to use:
1. Install the script by running one of below commands in a terminal depending on your OS:

Windows PowerShell:
```
iwr https://raw.githubusercontent.com/crabfeather/paperlens/main/PaperLensAI.py -O PaperLensAI.py
```
Linux/MacOS:
```
curl https://raw.githubusercontent.com/crabfeather/paperlens/main/PaperLensAI.py -o PaperLensAI.py
```
2. Verify the latest version of Python3 and PIP are installed by running:
```
python --version
pip --version
```
3. Install the required libraries:
```
pip install PyPDF2
pip install groq
```
4. Edit the script to include a free Groq API key generated from https://console.groq.com/keys
5. Modify the prompts and AI query parameters in the script to your liking. If needed edit the rate limits and chunk size accordingly.
6. Run the script with Python for your folder of PDFs:
```
python PaperLensAI.py <input-folder>
```

### Contact:
Allan Edh\
Research Intern, *Stockholm School of Economics* (SSE)\
allan.edh@gmail.com
