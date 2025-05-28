import tkinter as tk
from tkinter import messagebox
import random

class JogoAdivinhacaoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo de Adivinhação de Palavras")
        self.root.geometry("600x400")
        self.root.configure(bg='#f0f0f0')

        # Lista de palavras
        self.palavras = ["PYTHON", "JOGO", "COMPUTADOR", "PROGRAMACAO", "JANELA", "TECLADO", "MOUSE", "INTERFACE"]
        
        # Inicialização das variáveis do jogo
        self.palavra_atual = ""
        self.palavra_oculta = []
        self.letras_usadas = set()
        self.tentativas = 6
        
        # Configuração do estilo
        self.fonte_titulo = ('Arial', 16, 'bold')
        self.fonte_normal = ('Arial', 12)
        self.fonte_palavra = ('Arial', 24, 'bold')

        # Frame principal
        self.frame_principal = tk.Frame(root, bg='#f0f0f0')
        self.frame_principal.pack(expand=True, fill='both', padx=20, pady=20)

        # Título
        self.label_titulo = tk.Label(
            self.frame_principal,
            text="Jogo de Adivinhação de Palavras",
            font=self.fonte_titulo,
            bg='#f0f0f0'
        )
        self.label_titulo.pack(pady=10)

        # Palavra oculta
        self.label_palavra = tk.Label(
            self.frame_principal,
            text=' '.join(self.palavra_oculta),
            font=self.fonte_palavra,
            bg='#f0f0f0'
        )
        self.label_palavra.pack(pady=20)

        # Frame para entrada
        self.frame_entrada = tk.Frame(self.frame_principal, bg='#f0f0f0')
        self.frame_entrada.pack(pady=10)

        # Entrada de letra
        self.entrada_letra = tk.Entry(
            self.frame_entrada,
            width=5,
            font=self.fonte_normal,
            justify='center'
        )
        self.entrada_letra.pack(side='left', padx=5)
        self.entrada_letra.bind('<Return>', self.tentar_letra)

        # Botão de tentativa
        self.botao_tentar = tk.Button(
            self.frame_entrada,
            text="Tentar",
            command=self.tentar_letra,
            font=self.fonte_normal,
            bg='#4CAF50',
            fg='white',
            relief='flat',
            padx=10
        )
        self.botao_tentar.pack(side='left', padx=5)

        # Informações do jogo
        self.label_tentativas = tk.Label(
            self.frame_principal,
            text=f"Tentativas restantes: {self.tentativas}",
            font=self.fonte_normal,
            bg='#f0f0f0'
        )
        self.label_tentativas.pack(pady=5)

        self.label_letras = tk.Label(
            self.frame_principal,
            text="Letras usadas: ",
            font=self.fonte_normal,
            bg='#f0f0f0'
        )
        self.label_letras.pack(pady=5)

        # Botão de reiniciar
        self.botao_reiniciar = tk.Button(
            self.frame_principal,
            text="Novo Jogo",
            command=self.reiniciar_jogo,
            font=self.fonte_normal,
            bg='#2196F3',
            fg='white',
            relief='flat',
            padx=10
        )
        self.botao_reiniciar.pack(pady=20)

        # Inicialização do jogo (após widgets)
        self.reiniciar_jogo()

    def reiniciar_jogo(self):
        self.palavra_atual = random.choice(self.palavras)
        self.palavra_oculta = ['_' for _ in self.palavra_atual]
        self.letras_usadas = set()
        self.tentativas = 6
        self.atualizar_interface()

    def tentar_letra(self, event=None):
        letra = self.entrada_letra.get().upper()
        self.entrada_letra.delete(0, tk.END)

        if not letra or not letra.isalpha() or len(letra) != 1:
            messagebox.showwarning("Aviso", "Por favor, digite uma única letra!")
            return

        if letra in self.letras_usadas:
            messagebox.showinfo("Aviso", "Esta letra já foi usada!")
            return

        self.letras_usadas.add(letra)
        acertou = False

        for i, char in enumerate(self.palavra_atual):
            if char == letra:
                self.palavra_oculta[i] = letra
                acertou = True

        if not acertou:
            self.tentativas -= 1

        self.atualizar_interface()

        if '_' not in self.palavra_oculta:
            messagebox.showinfo("Parabéns!", "Você venceu!")
            self.reiniciar_jogo()
        elif self.tentativas == 0:
            messagebox.showinfo("Game Over", f"A palavra era: {self.palavra_atual}")
            self.reiniciar_jogo()

    def atualizar_interface(self):
        if hasattr(self, 'label_palavra'):
            self.label_palavra.config(text=' '.join(self.palavra_oculta))
        if hasattr(self, 'label_tentativas'):
            self.label_tentativas.config(text=f"Tentativas restantes: {self.tentativas}")
        if hasattr(self, 'label_letras'):
            self.label_letras.config(text=f"Letras usadas: {', '.join(sorted(self.letras_usadas))}")

def main():
    root = tk.Tk()
    app = JogoAdivinhacaoGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 