import tkinter as tk
from tkinter import ttk, font, messagebox
from tkinter import PhotoImage

#criando janela

#se ocorrer problema na iniciação do TK, ir na pasta: C:\Users\Jhon\AppData\Local\Programs\Python\Python313\tcl e copiar as pastas tcl8.#  tk8.# para a pasta Lib (CTRL+C e CTRL+V)
janela = tk.Tk()
janela.title("Meu App de Tarefas")
janela.configure(bg="#F0F0F0") #cor de fundo
janela.geometry("500x600") #tamanho de tela

janela.mainloop()