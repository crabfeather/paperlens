# PaperLens AI

### Description:
PaperLens AI is a tool developed for summarizing and doing topic modelling completely free on a large number of research paper PDFs using the Groq API -- mainly beneficial for literature reviews.
### How to use:
1. Install the script by running one of two below commands in a terminal:
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
4. Edit the script to include a free Groq API key gotten from https://console.groq.com/keys
5. Modify the prompts and AI query paramters in the script to your liking. If needed edit the rate limits and chunk size accordingly.
6. Run the script with Python for your folder of PDFs:
```
python PaperLensAI.py <input-folder>
```

### Contact:
Allan Edh
Research Intern, *Stockholm School of Economics (SSE)*
allan.edh@gmail.com
