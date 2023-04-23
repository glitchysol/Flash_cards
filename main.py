from tkinter import *
import random
import pandas
# ---------------------------------------- Save Progress --------------------------------------- #
# if check mark is clicked remove words from to_learn dictionary

# ---------------------------------------- Shuffle words --------------------------------------- #
random_word = {}
to_learn = {}

try:
    words_file = pandas.read_csv("data/words_to_learn.csv")

except FileNotFoundError:
    original_file = pandas.read_csv("data/Spanish 1k frequency list - Sheet1.csv")
    to_learn = original_file.to_dict(orient="records")

else:
    to_learn = words_file.to_dict(orient="records")


def shuffle_word():
    global word
    global random_word, flip_timer
    window.after_cancel(flip_timer)
    random_word = random.choice(to_learn)
    canvas.delete(word)
    word = canvas.create_text(450, 275, text=f"{random_word['Spanish']}", font=("Comic Sans", 60, "bold"), fill="black")
    canvas.itemconfig(language, text="Spanish", fill="black")
    canvas.itemconfig(card_bg, image=front_flash_card)
    flip_timer = window.after(3000, func=flip_card)


# ---------------------------------------- Flip Card --------------------------------------- #
def flip_card():
    canvas.itemconfig(language, text="English", fill="white")
    canvas.itemconfig(word, text=random_word["English"], fill="white")
    canvas.itemconfig(card_bg, image=back_flash_card)

def is_known():
    to_learn.remove(random_word)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    shuffle_word()

# ------------------------------------------ UI Setup ------------------------------------------ #
BACKGROUND_COLOR = "#B1DDC6"

window = Tk()
window.title("Flashy")
window.config(padx=20, pady=20, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=900, height=550, bg=BACKGROUND_COLOR, highlightthickness=0)
front_flash_card = PhotoImage(file="images/card_front.png")
back_flash_card = PhotoImage(file="images/card_back.png")

card_bg = canvas.create_image(450, 275, image=front_flash_card)
canvas.grid(column=0, row=0, columnspan=2)
language = canvas.create_text(450, 175, text="Spanish", font=("Ariel", 35, "italic"))
word = canvas.create_text(450, 275, text=" ", font=("Comic Sans", 60, "bold"))

# Buttons

yes_img = PhotoImage(file="images/right.png")
yes_button = Button(image=yes_img, highlightthickness=0, command=is_known)
yes_button.grid(column=0, row=1)

no_img = PhotoImage(file="images/wrong.png")
no_button = Button(image=no_img, highlightthickness=0, command=shuffle_word)
no_button.grid(column=1, row=1)

shuffle_word()

window.mainloop()


