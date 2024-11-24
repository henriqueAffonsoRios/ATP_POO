import tkinter as tk
from tkinter import messagebox
from common import *
from eleicao import Urna
import pickle


class UrnaEletronicaApp:
    def __init__(self, root, urna):
        self.root = root
        self.urna = urna
        self.root.title("Urna Eletrônica")
        
        self.criar_interface_inicial()

    def criar_interface_inicial(self):
        self.limpar_tela()

        self.titulo_label = tk.Label(self.root, text="Digite o título do eleitor:")
        self.titulo_label.pack()

        self.titulo_entry = tk.Entry(self.root)
        self.titulo_entry.pack()

        self.confirmar_button = tk.Button(self.root, text="Confirmar", command=self.verificar_eleitor)
        self.confirmar_button.pack()

    def criar_interface_votacao(self, eleitor):
        self.limpar_tela()

        self.info_label = tk.Label(self.root, text=str(eleitor))
        self.info_label.pack()

        self.voto_entry = tk.Entry(self.root)
        self.voto_entry.pack()
        self.voto_entry.insert(0, "Digite o número do candidato")

        self.votar_button = tk.Button(self.root, text="Votar", command=self.registrar_voto)
        self.votar_button.pack()

    def verificar_eleitor(self):
        try:
            titulo = int(self.titulo_entry.get())
            eleitor = self.urna.get_eleitor(titulo)
            if eleitor:
                self.criar_interface_votacao(eleitor)
            else:
                self.exibir_erro("Eleitor não encontrado nesta urna")
        except ValueError:
            self.exibir_erro("Título inválido")

    def registrar_voto(self):
        try:
            n_candidato = int(self.voto_entry.get())
            titulo = int(self.titulo_entry.get())
            eleitor = self.urna.get_eleitor(titulo)

            if eleitor:
                self.urna.registrar_voto(eleitor, n_candidato)
                messagebox.showinfo("Sucesso", "Voto registrado com sucesso!")
                self.criar_interface_inicial()
            else:
                self.exibir_erro("Eleitor não encontrado.")
        except ValueError:
            self.exibir_erro("Número de candidato inválido.")

    def limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.pack_forget()

    def exibir_erro(self, mensagem):
        messagebox.showerror("Erro", mensagem)


def carregar_dados():
    with open("eleitores.pkl", "rb") as f:
        eleitores = pickle.load(f)
    with open("candidatos.pkl", "rb") as f:
        candidatos = pickle.load(f)
    return eleitores, candidatos


if __name__ == "__main__":
    eleitores, candidatos = carregar_dados()
    mesario = Pessoa("Mesario Exemplo", "123456789", "123.456.789-00")
    urna = Urna(mesario, secao=1, zona=101, candidatos=candidatos, eleitores=eleitores)

    root = tk.Tk()
    app = UrnaEletronicaApp(root, urna)
    root.mainloop()
