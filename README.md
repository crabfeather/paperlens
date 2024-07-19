# PaperLens AI

### Description:
PaperLens AI is a Python tool for summarizing and performing topic modelling on a large number of research paper PDFs completely free using the Groq API. It is mainly beneficial for topic modelling and quick literature reviews, and was developed as my time as a research intern at Stockholm School of Economics. Using the default settings it can process ca 4 papers/minute using the *Llama3 8B* model.<br/> 
Note: The tool is not equivalent to manual work but instead serves as a faster method for making a selection from many articles or applying a certain topic model.

### How to use:
1. Install the script by running one of two below commands in a terminal depending on your OS:

Windows PowerShell:
```
iwr https://github.com/crabfeather/paperlens/blob/main/PaperLensAI.py -O PaperLensAI.py
```
Linux/MacOS:
```
curl -O https://github.com/crabfeather/paperlens/blob/main/PaperLensAI.py
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
