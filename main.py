import os
from PIL import Image, ImageDraw, ImageFont
from docx import Document
import textwrap
import tkinter as tk
from tkinter import filedialog, messagebox

# Konfiguracja
WATCH_WIDTH = 368  # Szerokość obrazu
WATCH_HEIGHT = 448  # Wysokość obrazu
DEFAULT_OUTPUT_FOLDER = "CheatMaster"
output_folder = DEFAULT_OUTPUT_FOLDER  # Domyślny folder zapisu

# Ustawienia fontu
FONT_PATH = "arial.ttf"  # Podaj ścieżkę do fontu, jeśli używasz innego
FONT_SIZE = 24

# Tworzenie folderu na wyjściowe obrazy, jeśli nie został jeszcze utworzony
if not os.path.exists(DEFAULT_OUTPUT_FOLDER):
    os.makedirs(DEFAULT_OUTPUT_FOLDER)



def create_image_from_text(text, image_name_base):
    text_parts = [text[i:i + 300] for i in range(0, len(text), 300)]
    part_number = 1

    for text_part in text_parts:
        image = Image.new('RGB', (WATCH_WIDTH, WATCH_HEIGHT), color='white')
        draw = ImageDraw.Draw(image)

        try:
            font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
        except IOError:
            font = ImageFont.load_default()
            print("Błąd wczytania fontu, używam domyślnej czcionki")

        if part_number == 1 and ":" in text_part:
            question_part, answer_part = text_part.split(":", 1)
            question_part = question_part.strip() + ":"
            answer_part = answer_part.strip()
        else:
            question_part = ""
            answer_part = text_part.strip()

        max_line_width = WATCH_WIDTH - 20
        wrapped_question = textwrap.fill(question_part, width=int(max_line_width / (FONT_SIZE * 0.6)))
        wrapped_answer = textwrap.fill(answer_part, width=int(max_line_width / (FONT_SIZE * 0.6)))

        text_lines = wrapped_question.splitlines() + wrapped_answer.splitlines()
        total_text_height = len(text_lines) * FONT_SIZE
        y_offset = (WATCH_HEIGHT - total_text_height) // 2

        if part_number == 1:
            for line in wrapped_question.splitlines():
                text_bbox = draw.textbbox((0, 0), line, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                x = (WATCH_WIDTH - text_width) // 2
                for dx, dy in [(0, 0), (1, 0), (0, 1), (1, 1)]:
                    draw.text((x + dx, y_offset + dy), line, fill="black", font=font)
                y_offset += FONT_SIZE

        for line in wrapped_answer.splitlines():
            text_bbox = draw.textbbox((0, 0), line, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            x = (WATCH_WIDTH - text_width) // 2
            draw.text((x, y_offset), line, fill="black", font=font)
            y_offset += FONT_SIZE

        image_name = f"{image_name_base}_part{part_number}.jpg"
        image.save(os.path.join(output_folder, image_name), "JPEG", quality=95)
        print(f"Utworzono obraz: {image_name}")
        part_number += 1


def process_word_file(file_path):
    doc = Document(file_path)
    question_number = 1
    question_text = ""

    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()

        if text:
            question_text += text + "\n"
        else:
            if question_text.strip():
                image_name_base = f"pytanie{question_number}"
                create_image_from_text(question_text.strip(), image_name_base)
                question_number += 1
                question_text = ""

    if question_text.strip():
        image_name_base = f"pytanie{question_number}"
        create_image_from_text(question_text.strip(), image_name_base)

    messagebox.showinfo("Gotowe", f"Zdjęcia zostały zapisane w folderze:\n{output_folder}")


def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Word Documents", "*.docx")])
    if file_path:
        process_word_file(file_path)


def select_output_folder():
    global output_folder
    selected_folder = filedialog.askdirectory()
    if selected_folder:
        output_folder = selected_folder
        messagebox.showinfo("Folder zapisu", f"Folder zapisu ustawiono na:\n{output_folder}")


# Tworzenie GUI
root = tk.Tk()
root.title("CheatMaster")
root.geometry("300x200")

label = tk.Label(root, text="Wybierz plik DOCX do konwersji:")
label.pack(pady=10)

select_file_button = tk.Button(root, text="Wybierz plik", command=select_file)
select_file_button.pack(pady=5)

select_folder_button = tk.Button(root, text="Wybierz folder zapisu", command=select_output_folder)
select_folder_button.pack(pady=5)

root.mainloop()

#Grodzix :) + CHATGPT
