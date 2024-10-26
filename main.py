import tkinter as tk
from locale import windows_locale
from struct import pack_into
from tkinter import ttk, font, messagebox
from tkinter import PhotoImage

#criando janela:

#se ocorrer problema na iniciação do TK, ir na pasta: C:\Users\Jhon\AppData\Local\Programs\Python\Python313\tcl e copiar as pastas tcl8.#  tk8.# para a pasta Lib (CTRL+C e CTRL+V)
janela = tk.Tk()
janela.title("Meu App de Tarefas")
janela.configure(bg="#F0F0F0") #cor de fundo
janela.geometry("500x600") #tamanho de tela

icone_editar = PhotoImage(file="img/editar.png").subsample(10,10)
icone_deletar = PhotoImage(file="img/deletar.png").subsample(10,10)

frame_em_edicao = None # variavel para controle de se é edição ou novo

# funcao para processar itens a inserir/atualizar:
def salvarTarefa():
    global frame_em_edicao # para acessar em demais partes da aplicação
    texto = input_tarefa.get().strip() #removendo espaços em branco no começo e fim da string
    if texto and texto != "Escreva a tarefa aqui":
        if frame_em_edicao is not None:
            atualizarTarefa(texto) # faz atualização de tarefa já existente
            frame_em_edicao = None # resetando
        else:
            adicionarItemTarefa(texto) # cria novo
            input_tarefa.delete(0, tk.END) # limpando o input do começo ao fim
    else:
        messagebox.showwarning("Atenção!", "Tarefa não pode ser vazia!")

# funcao para salvar novo item na lista:
def adicionarItemTarefa(novo_texto):
    # criando os recursos visuais dos novos itens inseridos:
    frame_nova_tarefa = tk.Frame(canvas_interior, bg="white", bd=1, relief=tk.SOLID)

    label_nova_tarefa = tk.Label(frame_nova_tarefa, text=novo_texto, font=("Garamond", 16), bg="white", width=25, height=2, anchor="w")
    label_nova_tarefa.pack(side=tk.LEFT, fill=tk.X, padx=10, pady=5)

    btn_editar = tk.Button(frame_nova_tarefa, image=icone_editar, command=lambda f=frame_nova_tarefa, l=label_nova_tarefa: prepararEdicao(f, l), bg="white", relief=tk.FLAT)
    btn_editar.pack(side=tk.RIGHT, padx=5)

    btn_deletar = tk.Button(frame_nova_tarefa, image=icone_deletar, command=lambda f=frame_nova_tarefa: deletarTarefa(f), bg="white", relief=tk.FLAT)
    btn_deletar.pack(side=tk.RIGHT, padx=5)

    frame_nova_tarefa.pack(fill=tk.X, padx=5, pady=5)

    btn_check = ttk.Checkbutton(frame_nova_tarefa, command=lambda label=label_nova_tarefa: aplicarTracejado(label))
    btn_check.pack(side=tk.RIGHT, padx=5)
    canvas_interior.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

# funcao que copia o conteudo do item selecionado e atribui ao input:
def prepararEdicao(frame_tarefa, label_tarefa):
    global frame_em_edicao
    frame_em_edicao = frame_tarefa
    input_tarefa.delete(0, tk.END) # limpando o input do começo ao fim
    input_tarefa.insert(0, label_tarefa.cget("text"))

# funcao para atualização:
def atualizarTarefa(novo_texto):
    global frame_em_edicao
    for item in frame_em_edicao.winfo_children():
        if isinstance(item, tk.Label):
            item.config(text=novo_texto)
            input_tarefa.delete(0, tk.END) # limpando o input após salvar edicao

# funcao para remover item da lista
def deletarTarefa(frame):
    frame.destroy()
    canvas_interior.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

# funcao para aplicar traço no item selecionado
def aplicarTracejado(label):
    fonte_atual = label.cget("font")
    if "overstrike" in fonte_atual:
        nova_fonte = fonte_atual.replace(" overstrike", "")
    else:
        nova_fonte = fonte_atual + " overstrike"
    label.config(font=nova_fonte)

# demais configurações de layout:
fonte_cabecalho = font.Font(family="Garamond", size=24, weight="bold")
label_cabecalho = tk.Label(janela, text="Meu App de Tarefas", font=fonte_cabecalho, bg="#F0F0F0", fg="#333").pack(pady=20)

frame_tarefa = (tk.Frame(janela, bg="#F0F0F0"))
frame_tarefa.pack(pady=10)

input_tarefa = tk.Entry(frame_tarefa, font=("Garamond", 14), relief=tk.FLAT, bg="white", fg="gray", width=30)
input_tarefa.pack(side=tk.LEFT, padx=10)

btn_salvar_tarefa = tk.Button(frame_tarefa, text="Salvar Tarefa", bg="#4CAF50", fg="white", height=1, width=15, font=("Robot", 11), relief=tk.FLAT, command=salvarTarefa)
btn_salvar_tarefa.pack(side=tk.LEFT, padx=10)

# frame para a lista de tarefas com recurso de barra de rolagem
frame_lista_tarefas = (tk.Frame(janela, bg="white"))
frame_lista_tarefas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

canvas = (tk.Canvas(frame_lista_tarefas, bg="white"))
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scroolbar = ttk.Scrollbar(frame_lista_tarefas, orient="vertical", command=canvas.yview)
scroolbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scroolbar.set)
canvas_interior = tk.Frame(canvas, bg="white")
canvas.create_window((0,0), window=canvas_interior, anchor="nw")
canvas_interior.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

janela.mainloop()