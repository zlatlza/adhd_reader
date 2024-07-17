import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
from PyPDF2 import PdfReader

# Function to read sentences from a PDF file
def read_sentences_from_pdf(file_path):
    try:
        pdf_reader = PdfReader(open(file_path, 'rb'))
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
        sentences = text.split('. ')
        sentences = [sentence.strip() + '.' for sentence in sentences if sentence.strip()]
        return sentences
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read the PDF file: {e}")
        return []

# Function to show the next sentence
def show_next_sentence(event=None):
    global current_sentence_index, sentences
    if current_sentence_index < len(sentences):
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, sentences[current_sentence_index])
        current_sentence_index += 1

# Function to load a PDF file
def load_file():
    global sentences, current_sentence_index
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        sentences = read_sentences_from_pdf(file_path)
        current_sentence_index = 0
        if sentences:
            show_next_sentence()

# Initialize the main window
root = tk.Tk()
root.title("Sentence Reader")

# Add a scrolled text widget
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=10)
text_area.pack(padx=10, pady=10)

# Add a button to load a PDF file
load_button = tk.Button(root, text="Load File", command=load_file)
load_button.pack(pady=10)

# Bind the space bar to show the next sentence
root.bind('<space>', show_next_sentence)

# Initialize variables
sentences = []
current_sentence_index = 0

# Run the application
root.mainloop()
