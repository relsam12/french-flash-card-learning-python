from tkinter import *
import pandas as pd
import random as r

BACKGROUND_COLOR = "#B1DDC6"
random_vocab = {}
languages_dict = {}
try:
    languages_data = pd.read_csv("./data/vocabulary_you_must_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("./data/french_words.csv")
    languages_dict = original_data.to_dict(orient="records")
else:
    # pakai argument 'orient="records"' menghasilkan dict yang berisi nilai tiap kolom.
    # Cth; [{'French': 'partie', 'English': 'part'}] 👇
    languages_dict = languages_data.to_dict(orient="records")


def next_card():
    global random_vocab, flipping_card_with_timer
    # membuat timer berhenti sejenak untuk flip card ketika tombol ❌ atau ✅ di klik
    window.after_cancel(flipping_card_with_timer)

    random_vocab = r.choice(languages_dict)
    canvas.itemconfig(title_card, text="French", fill="black")
    canvas.itemconfig(word_card, text=random_vocab['French'], fill="black")
    canvas.itemconfig(cards, image=card_front_img)
    # update countdownd ketika tombol ❌ atau ✅ di klik kembali
    flipping_card_with_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(title_card, text="English", fill="white")
    canvas.itemconfig(word_card, text=random_vocab["English"], fill="white")
    canvas.itemconfig(cards, image=card_back_img)


#
def is_known():
    """membuat function untuk remove vocabulary yang diketahui oleh user dari languages_dict. jadi, sisa vocab yang ada
     di languages_dict menjadi vocab yang tidak di ketahui oleh user, lalu di passing ke file .csv yang baru
     untuk dipelajari"""
    languages_dict.remove(random_vocab)
    print(random_vocab)
    print(len(languages_dict))
    vaocab_to_learn = pd.DataFrame(languages_dict)
    vaocab_to_learn.to_csv("./data/vocabulary_you_must_learn.csv", index=False)
    next_card()


window = Tk()
window.title("French to English Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
# variable countdown millisecond, tanpa menunggu variable dipanggil, window.after akan langsung ter-trigger
flipping_card_with_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=562, bg=BACKGROUND_COLOR, highlightthickness=0)
card_back_img = PhotoImage(file="./images/card_back.png")
card_front_img = PhotoImage(file="./images/card_front.png")
cards = canvas.create_image(400, 263, image=card_front_img)
canvas.grid(column=0, row=0, columnspan=2)
# 400 dan 150 adalah posisi x dan y dari text 👇
title_card = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
word_card = canvas.create_text(400, 320, text="", font=("Ariel", 50, "bold"))

yes_button = PhotoImage(file="./images/right.png")
button_yes = Button(image=yes_button, relief="flat", bg=BACKGROUND_COLOR, highlightthickness=0, command=is_known)
button_yes.grid(column=1, row=1)
no_button = PhotoImage(file="./images/wrong.png")
button_no = Button(image=no_button, relief="flat", bg=BACKGROUND_COLOR, highlightthickness=0, command=next_card)
button_no.grid(column=0, row=1)

next_card()

window.mainloop()
