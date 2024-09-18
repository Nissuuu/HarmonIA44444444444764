from tkinter import *
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
import tkinter.font as font
import random
import pygame
import time

# ----------------------------- funcions ---------------------------------
def on_enter(event, canvas, cursor_type):
    canvas.config(cursor=cursor_type)

def on_leave(event, canvas):
    canvas.config(cursor="")

def on_canvas_click(event,nota):
    global to
    to = list(acords.values()).index(nota)
    totext.set(nota)

def focus_out_combobox(event):
    global durada
    durada = int(desplegable.get())
    arrel.focus()

def crear_progressió():
    progressió = generar_progressió(durada,dades,to)
    acordstext.set(' '.join(progressió))

def reproduir_progressio():
    pygame.mixer.init()
    progressio = acordstext.get().split(' ')
    for acord in progressio:
        fitxer_audio = f"Sons/{acord}.mp3"
        pygame.mixer.music.load(fitxer_audio)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

# ---------------------------- generador -----------------------------
acords = {0: "C", 1: "Db", 2: "D", 3: "Eb", 4: "E", 5: "F", 6: "F#", 7: "G", 8: "Ab", 9: "A", 10: "Bb", 11: "B"}
with open('estadistica.txt', 'r') as arxiu:
    dades = arxiu.read().split(',')

def generar_progressió(durada, dades,to):
    progressió = []
    progressió_traduïda=[]
    caràcters = 0
    while caràcters < durada:
        acord_aleatori = random.choice(dades)
        acords_separats = acord_aleatori.split()
        if caràcters + len(acords_separats) <= durada:
            progressió.extend(list(acords_separats))
            caràcters += len(acords_separats)
    for i in progressió:
        if 'm' in i:
            nota = (int(i[:-1]) + to)%12
            nota_traduïda = acords[nota]
            progressió_traduïda.append(nota_traduïda + 'm')
        else:
            i=int(i)
            nota_traduïda = acords[(i+to)%12]
            progressió_traduïda.append(nota_traduïda)
    return progressió_traduïda

# --------------------------- arrel i fons ----------------------------
arrel = Tk()
arrel.title("Crea la teva cançó!")
arrel.attributes("-fullscreen", True)
arrel.resizable(False,False)
screen_width = arrel.winfo_screenwidth()
screen_height = arrel.winfo_screenheight()

fons = Image.open("Interface/Imatges/Fons.jpg")
fons = fons.resize((screen_width, screen_height), Image.LANCZOS)
fons = ImageTk.PhotoImage(fons)
frame = Label(arrel, image=fons)
frame.pack(fill="both", expand=True)

# -------------------------- desplegable ----------------------------
custom_font = font.Font(family="Arial Rounded MT Bold",size=30)
desplegable = ttk.Combobox(frame, state="readonly", width=4, values=["1", "2", "3", "4", "5", "6", "7", "8"], justify="center", foreground="white")
desplegable.place(x=330, y=340)
desplegable.option_add("*TCombobox*Listbox.font", custom_font)
desplegable.configure(font=custom_font)
desplegable.bind("<<ComboboxSelected>>", focus_out_combobox)
durada = ""

# ---------------------------- text to -----------------------------
totext = StringVar()
to_quadre = Entry(frame, state="readonly", textvariable=totext, font=custom_font, width=4, justify='center')
to_quadre.place(x=330, y=400)

# ---------------------------- text acords -----------------------------
custom_font3 = font.Font(family="Arial Rounded MT Bold",size=45)
acordstext = StringVar()
acords_quadre = Entry(frame, state="readonly", textvariable=acordstext, font=custom_font3, width=30, justify='center', fg="white")
acords_quadre.place(x=550, y=350)

# ---------------------------- teclat ------------------------------
teclat = Image.open("Interface/Imatges/Teclat.png")
teclat = ImageTk.PhotoImage(teclat)
teclat_foto = Label(frame, image=teclat)
teclat_foto.place(x=150, y=530)

canvas_configs = [
    {"x": 153, "y": 533, "width": 55, "height": 247, "bg": "white", "cursor": "arrow", "nota": "C"},
    {"x": 211, "y": 533, "width": 55, "height": 247, "bg": "white", "cursor": "arrow", "nota": "D"},
    {"x": 269, "y": 533, "width": 52, "height": 247, "bg": "white", "cursor": "arrow", "nota": "E"},
    {"x": 325, "y": 533, "width": 54, "height": 247, "bg": "white", "cursor": "arrow", "nota": "F"},
    {"x": 382, "y": 533, "width": 54, "height": 247, "bg": "white", "cursor": "arrow", "nota": "G"},
    {"x": 439, "y": 533, "width": 55, "height": 247, "bg": "white", "cursor": "arrow", "nota": "A"},
    {"x": 497, "y": 533, "width": 54, "height": 247, "bg": "white", "cursor": "arrow", "nota": "B"},
    {"x": 195, "y": 533, "width": 32, "height": 142, "bg": "black", "cursor": "arrow", "nota": "Db"},
    {"x": 252, "y": 533, "width": 31, "height": 142, "bg": "black", "cursor": "arrow", "nota": "Eb"},
    {"x": 366, "y": 533, "width": 31, "height": 142, "bg": "black", "cursor": "arrow", "nota": "F#"},
    {"x": 422, "y": 533, "width": 31, "height": 142, "bg": "black", "cursor": "arrow", "nota": "Ab"},
    {"x": 480, "y": 533, "width": 31, "height": 142, "bg": "black", "cursor": "arrow", "nota": "Bb"}
]

for config in canvas_configs:
    canvas = tk.Canvas(frame, width=config["width"], height=config["height"], bg=config["bg"], highlightthickness=0)
    canvas.place(x=config["x"], y=config["y"])
    rect = canvas.create_rectangle(0, 0, config["width"], config["height"], fill=config["bg"], outline=config["bg"])
    canvas.tag_bind(rect, "<Enter>", lambda e, c=canvas, t=config["cursor"]: on_enter(e, c, t))
    canvas.tag_bind(rect, "<Leave>", lambda e, c=canvas: on_leave(e, c))
    canvas.tag_bind(rect, "<Button-1>", lambda e, n=config["nota"]: on_canvas_click(e,n))

# ----------------------------- botons ---------------------------------
custom_font2 = font.Font(family="Arial Rounded MT Bold", size=50)
boto_crear = Button(frame, text="Crear!", font=custom_font2, command=crear_progressió, highlightbackground="gray" )
boto_crear.place(x=670, y=550)

imatge_boto = Image.open("Interface/Imatges/Botó.png")
imatge_boto = ImageTk.PhotoImage(imatge_boto)
boto_reproduir = Button(frame, image=imatge_boto, command=reproduir_progressio, highlightbackground="gray")
boto_reproduir.place(x=950, y=550)

# ----------------------------------------------------------------------
arrel.mainloop()