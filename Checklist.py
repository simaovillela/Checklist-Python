import tkinter as tk
from tkinter import ttk
import schedule
import time
import json
from threading import Thread
from os.path import exists

ARQUIVO_DADOS = "checklist_dados.json"

def adicionar_item():
    texto = entrada_item.get()
    if texto:
        var = tk.BooleanVar()
        checkbox = ttk.Checkbutton(frame_itens, text=texto, variable=var, style="Custom.TCheckbutton")
        checkbox.pack(anchor="w", pady=5, padx=10)
        checkboxes.append((checkbox, var, texto))
        entrada_item.delete(0, tk.END)
        salvar_dados()

def mostrar_itens_marcados():
    marcados = [cb[2] for cb in checkboxes if cb[1].get()]
    resultado.config(text="Itens marcados:\n" + "\n".join(marcados), justify="left")

def desmarcar_todos():
    for checkbox, var, texto in checkboxes:
        var.set(False)
    resultado.config(text="Todos os itens foram desmarcados!")
    salvar_dados()

def salvar_dados():
    dados = [{"texto": cb[2], "marcado": cb[1].get()} for cb in checkboxes]
    with open(ARQUIVO_DADOS, "w") as f:
        json.dump(dados, f)

def carregar_dados():
    if exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, "r") as f:
            dados = json.load(f)
        for item in dados:
            var = tk.BooleanVar(value=item["marcado"])
            checkbox = ttk.Checkbutton(frame_itens, text=item["texto"], variable=var, style="Custom.TCheckbutton")
            checkbox.pack(anchor="w", pady=5, padx=10)
            checkboxes.append((checkbox, var, item["texto"]))

def agendar_tarefa():
    schedule.every().day.at("00:00").do(desmarcar_todos)

    def run_schedule():
        while True:
            schedule.run_pending()
            time.sleep(1)

    thread = Thread(target=run_schedule)
    thread.daemon = True
    thread.start()

janela = tk.Tk()
janela.title("Checklist Moderno")
janela.geometry("500x600")
janela.configure(bg="#f5f5f5")

style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=6)
style.configure("TLabel", font=("Arial", 12), background="#f5f5f5")
style.configure("Custom.TCheckbutton", font=("Arial", 11), background="#ffffff")

frame_titulo = tk.Frame(janela, bg="#007acc", height=50)
frame_titulo.pack(fill="x")
titulo = tk.Label(frame_titulo, text="Checklist Diário", font=("Arial", 16, "bold"), fg="white", bg="#007acc")
titulo.pack(pady=10)

frame_topo = tk.Frame(janela, bg="#f5f5f5")
frame_topo.pack(pady=10)
entrada_item = ttk.Entry(frame_topo, width=30, font=("Arial", 12))
entrada_item.pack(side="left", padx=5)
btn_adicionar = ttk.Button(frame_topo, text="Adicionar", command=adicionar_item)
btn_adicionar.pack(side="left")

frame_itens = tk.Frame(janela, bg="#ffffff", relief="solid", borderwidth=1)
frame_itens.pack(fill="both", expand=True, pady=10, padx=10)

frame_botoes = tk.Frame(janela, bg="#f5f5f5")
frame_botoes.pack(pady=10)
btn_mostrar = ttk.Button(frame_botoes, text="Mostrar itens marcados", command=mostrar_itens_marcados)
btn_mostrar.grid(row=0, column=0, padx=5)
btn_desmarcar = ttk.Button(frame_botoes, text="Desmarcar todos", command=desmarcar_todos)
btn_desmarcar.grid(row=0, column=1, padx=5)

resultado = ttk.Label(janela, text="", wraplength=450, font=("Arial", 11))
resultado.pack(pady=10)

checkboxes = []

carregar_dados()

agendar_tarefa()

janela.mainloop()
