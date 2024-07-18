import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
from PyPDF2 import PdfReader
from docx import Document
import os
import json

def read_sentences_from_file(file_path):
    try:
        if file_path.endswith('.pdf'):
            pdf_reader = PdfReader(open(file_path, 'rb'))
            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text()
        elif file_path.endswith('.txt'):
            with open(file_path, 'r') as file:
                text = file.read()
        elif file_path.endswith('.docx'):
            doc = Document(file_path)
            text = '\n'.join([para.text for para in doc.paragraphs])
        else:
            raise ValueError("Unsupported file type")
        
        sentences = text.split('. ')
        sentences = [sentence.strip() + '.' for sentence in sentences if sentence.strip()]
        return sentences
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read the file: {e}")
        return []

def show_sentence():
    global current_sentence_index, sentences
    if 0 <= current_sentence_index < len(sentences):
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, sentences[current_sentence_index])
        save_state()

def show_next_sentence(event=None):
    global current_sentence_index
    if current_sentence_index < len(sentences) - 1:
        current_sentence_index += 1
        show_sentence()

def show_previous_sentence(event=None):
    global current_sentence_index
    if current_sentence_index > 0:
        current_sentence_index -= 1
        show_sentence()

def save_state(file_path=None):
    if file_path is None:
        file_path = os.path.join(SAVE_DIR, f"{os.path.basename(current_file_path)}.json")
    state = {
        "file_path": current_file_path,
        "current_sentence_index": current_sentence_index,
        "notes": notes_area.get(1.0, tk.END)
    }
    with open(file_path, 'w') as file:
        json.dump(state, file)

def load_state(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            state = json.load(file)
            return state
    return None

def load_file():
    global sentences, current_sentence_index, current_file_path
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("Text files", "*.txt"), ("Word files", "*.docx")])
    if file_path:
        sentences = read_sentences_from_file(file_path)
        current_file_path = file_path
        current_sentence_index = 0
        state = load_state(os.path.join(SAVE_DIR, f"{os.path.basename(file_path)}.json"))
        if state:
            current_sentence_index = state["current_sentence_index"]
            notes_area.delete(1.0, tk.END)
            notes_area.insert(tk.END, state["notes"])
        if sentences:
            show_sentence()

def load_last_session():
    global sentences, current_sentence_index, current_file_path
    json_file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if json_file_path:
        state = load_state(json_file_path)
        if state:
            current_file_path = state["file_path"]
            sentences = read_sentences_from_file(current_file_path)
            current_sentence_index = state["current_sentence_index"]
            notes_area.delete(1.0, tk.END)
            notes_area.insert(tk.END, state["notes"])
            if sentences:
                show_sentence()
        else:
            messagebox.showinfo("Info", "No saved session found in the selected file.")

def save_notes():
    note_file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if note_file_path:
        with open(note_file_path, 'w') as note_file:
            note_file.write(notes_area.get(1.0, tk.END))

def save_current_position():
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if file_path:
        save_state(file_path)
        messagebox.showinfo("Info", "Current position saved.")

root = tk.Tk()
root.title("ADHD_Reader v1.2")

reader_frame = tk.Frame(root)
reader_frame.pack(padx=10, pady=10)

text_area = scrolledtext.ScrolledText(reader_frame, wrap=tk.WORD, width=50, height=10)
text_area.pack()

button_frame = tk.Frame(reader_frame)
button_frame.pack(pady=10)

load_button = tk.Button(button_frame, text="Load File", command=load_file)
load_button.pack(side=tk.LEFT, padx=5)

load_last_button = tk.Button(button_frame, text="Load Last Session", command=load_last_session)
load_last_button.pack(side=tk.LEFT, padx=5)

save_position_button = tk.Button(button_frame, text="Save Current Position", command=save_current_position)
save_position_button.pack(side=tk.LEFT, padx=5)

root.bind('<Right>', show_next_sentence)
root.bind('<Left>', show_previous_sentence)

notes_frame = tk.Frame(root)
notes_frame.pack(padx=10, pady=10)

notes_label = tk.Label(notes_frame, text="Notes:")
notes_label.pack()

notes_area = scrolledtext.ScrolledText(notes_frame, wrap=tk.WORD, width=50, height=10)
notes_area.pack()

save_button = tk.Button(notes_frame, text="Save Notes", command=save_notes)
save_button.pack(pady=10)

sentences = []
current_sentence_index = 0
current_file_path = ""
SAVE_DIR = "save_states"

root.mainloop()
