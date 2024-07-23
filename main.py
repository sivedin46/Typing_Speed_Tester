from tkinter import *
from tkinter import filedialog

timer = None
sample_words = []
user_words = []
char_counter = 0
counter = 0
cwpm = 0
wpm = 0
record = 0


def count_down(count):
    global timer, cwpm, wpm, record
    if count > 0:
        timer = window.after(1000, count_down, count - 1)
    else:
        check_record()
        update_display()
    time_text.delete(1.0, END)
    time_text.insert(END, count)


def update_display():
    global cwpm, wpm
    cwpm_text.delete(1.0, END)
    cwpm_text.insert(END, str(cwpm))
    wpm_text.delete(1.0, END)
    wpm_text.insert(END, str(wpm))

    user_text.unbind("<space>")
    user_text.unbind("<Return>")


def check_record():
    global record
    if cwpm > record:
        record = cwpm
        with open("records.txt", 'w', encoding='utf-8') as file:
            file.write(f"{record}")
        best_text.delete(1.0, END)
        best_text.insert(END, str(record))


def start_timer():
    global timer
    if timer is not None:
        window.after_cancel(timer)
    read_record()
    initialize_all()
    user_text.bind("<space>", compare)
    user_text.bind("<Return>", compare)
    count_down(60)


def read_record():
    global record
    try:
        with open("records.txt", 'r', encoding='utf-8') as file:
            record = file.readline().strip()
            record = int(record) if record else 0
    except FileNotFoundError:
        record = 0


def initialize_all():
    global cwpm, wpm, char_counter, counter, user_words, record
    best_text.delete(1.0, END)
    best_text.insert(END, str(record))
    sample_text.tag_remove("correct", 1.0, END)
    sample_text.tag_remove("incorrect", 1.0, END)
    user_words = []
    char_counter = 0
    counter = 0
    cwpm = 0
    wpm = 0
    user_text.config(state="normal")
    user_text.focus_set()
    user_text.delete("1.0", "end-1c")


def open_sample_text():
    global sample_words
    file_path = filedialog.askopenfilename(title="Open Text File",
                                           filetypes=[("Text", "*.txt")])
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            combined_text = ' '.join(line.strip() for line in file)
            sample_words = combined_text.split()
            sample_text.config(state="normal")
            sample_text.delete(1.0, END)  # clear entry
            sample_text.insert(END, ' '.join(sample_words))
            sample_text.config(state="disabled")


def compare(event):
    global user_words, sample_words, char_counter, counter, cwpm, wpm
    last_word = user_text.get("1.0", "end-1c").strip()
    user_text.delete("1.0", "end-1c")
    if last_word:
        user_words.append(last_word)
        wpm += 1
        if counter < len(sample_words):
            if user_words[counter] == sample_words[counter]:
                state = "correct"
                cwpm += 1
            else:
                state = "incorrect"
            start_index = f"1.{char_counter}"
            end_index = f"1.{char_counter + len(sample_words[counter])}"
            sample_text.tag_add(state, start_index, end_index)
            char_counter += len(sample_words[counter]) + 1  # +1 for the space
            counter += 1


#        ----------------------------------------------user gui------------------------------------------
# GUI
window = Tk()
window.title("Type Speed Tester")
window.config(padx=20, pady=20, bg="salmon3")
window.geometry("800x500")
window.resizable(None)

# Frames
info_frame = Frame(window, bg="salmon2")
info_frame.pack(side="right", padx=10, fill=BOTH, anchor="w")
sample_text_frame = Frame(window, bg="white")
sample_text_frame.pack(side="top", pady=10, )
entry_frame = Frame(window, bg="white")
entry_frame.pack(side="top", pady=10)
button_frame = Frame(window, bg="white")
button_frame.pack(side="top", pady=10)

# Information Frames
time_frame = Frame(info_frame, bg="salmon2")
time_frame.pack(side="top", pady=2, anchor="w")
cpm_frame = Frame(info_frame, bg="salmon2")
cpm_frame.pack(side="top", pady=2, anchor="w")
words_frame = Frame(info_frame, bg="salmon2")
words_frame.pack(side="top", pady=2, anchor="w")
best_frame = Frame(info_frame, bg="salmon2")
best_frame.pack(side="top", pady=2, anchor="w")

# Labels and Entries
sample_text = Text(sample_text_frame, width=590, height=15, font=("Arial", "14"), bg="white", wrap=WORD)
sample_text.insert(END, "Please load a text file for typing exercise. \n"
                        "When you will feel ready click start button for typing")
sample_text.config(state="disabled")
sample_text.pack(side="top", expand=True)
sample_text.propagate(False)
sample_text.tag_configure("correct", foreground="green")
sample_text.tag_configure("incorrect", foreground="red")

user_text = Text(entry_frame, width=20, height=1, font=("Arial", "18"), bg="white", wrap=WORD, )
user_text.insert(END, "Type Here", "center")
user_text.config(state="disabled")
user_text.pack(side="top")

time_label = Label(time_frame, text="Time Left:                ", width=20, height=1, font=("Arial", "12"),
                   bg="salmon2")
time_label.pack(side="left")
time_text = Text(time_frame, width=3, height=1, font=("Arial", "12"), bg="salmon2")
time_text.insert(END, "")
time_text.pack(side="left")

cwpm_label = Label(cpm_frame, text="Correct Words Per Minute:", width=20, height=1, font=("Arial", "12"),
                   bg="salmon2")
cwpm_label.pack(side="left")
cwpm_text = Text(cpm_frame, width=3, height=1, font=("Arial", "12"), bg="salmon2")
cwpm_text.pack(side="left")

words_label = Label(words_frame, text="Words Per Minute:", width=20, height=1, font=("Arial", "12"), bg="salmon2")
words_label.pack(side="left")
wpm_text = Text(words_frame, width=3, height=1, font=("Arial", "12"), bg="salmon2")
wpm_text.pack(side="left")

best_label = Label(best_frame, text="Your Best Result:   ", width=20, height=1, font=("Arial", "12"), bg="salmon2")
best_label.pack(side="left")
best_text = Text(best_frame, width=3, height=1, font=("Arial", "12"), bg="salmon2")
best_text.pack(side="left")

# Buttons
open_tex_button = Button(button_frame, width=33, text="Open Text File", command=open_sample_text)
open_tex_button.pack(side="left", )

start_button = Button(button_frame, width=33, text="Start", command=start_timer)
start_button.pack(side="left", )

window.mainloop()
