import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class JogoDaForca:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo da Forca")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Lista de palavras para o jogo
        self.PALAVRAS = [
            'python', 'programacao', 'computador', 'teclado', 'mouse',
            'internet', 'software', 'hardware', 'dados', 'algoritmo',
            'desenvolvimento', 'interface', 'sistema', 'rede', 'seguranca'
        ]
        
        # Variáveis do jogo
        self.palavra_secreta = ""
        self.letras_corretas = set()
        self.letras_erradas = set()
        self.tentativas = 0
        self.max_tentativas = 6
        
        # Criar interface
        self.criar_interface()
        self.novo_jogo()
    
    def criar_interface(self):
        # Frame principal
        self.frame_principal = tk.Frame(self.root, bg="#f0f0f0")
        self.frame_principal.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Título
        self.label_titulo = tk.Label(
            self.frame_principal,
            text="Jogo da Forca",
            font=("Arial", 24, "bold"),
            bg="#f0f0f0"
        )
        self.label_titulo.pack(pady=10)
        
        # Canvas para o boneco
        self.canvas = tk.Canvas(
            self.frame_principal,
            width=300,
            height=300,
            bg="white",
            highlightthickness=1,
            highlightbackground="black"
        )
        self.canvas.pack(pady=10)
        
        # Frame para a palavra
        self.frame_palavra = tk.Frame(self.frame_principal, bg="#f0f0f0")
        self.frame_palavra.pack(pady=10)
        
        # Label para mostrar letras erradas
        self.label_erradas = tk.Label(
            self.frame_principal,
            text="Letras erradas:",
            font=("Arial", 12),
            bg="#f0f0f0"
        )
        self.label_erradas.pack(pady=5)
        
        # Frame para o teclado
        self.frame_teclado = tk.Frame(self.frame_principal, bg="#f0f0f0")
        self.frame_teclado.pack(pady=10)
        
        # Criar botões do teclado
        self.criar_teclado()
        
        # Botão novo jogo
        self.btn_novo_jogo = tk.Button(
            self.frame_principal,
            text="Novo Jogo",
            font=("Arial", 12),
            command=self.novo_jogo,
            bg="#4CAF50",
            fg="white",
            padx=10,
            pady=5
        )
        self.btn_novo_jogo.pack(pady=10)
    
    def criar_teclado(self):
        # Layout do teclado
        teclado = [
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
        ]
        
        for i, linha in enumerate(teclado):
            for j, letra in enumerate(linha):
                btn = tk.Button(
                    self.frame_teclado,
                    text=letra,
                    font=("Arial", 12),
                    width=3,
                    command=lambda l=letra: self.tentar_letra(l),
                    bg="#e0e0e0",
                    activebackground="#d0d0d0"
                )
                btn.grid(row=i, column=j, padx=2, pady=2)
    
    def novo_jogo(self):
        self.palavra_secreta = random.choice(self.PALAVRAS)
        self.letras_corretas = set()
        self.letras_erradas = set()
        self.tentativas = 0
        self.atualizar_interface()
        self.desenhar_forca()
    
    def tentar_letra(self, letra):
        letra = letra.lower()
        
        if letra in self.letras_corretas or letra in self.letras_erradas:
            return
        
        if letra in self.palavra_secreta:
            self.letras_corretas.add(letra)
        else:
            self.letras_erradas.add(letra)
            self.tentativas += 1
            self.desenhar_forca()
        
        self.atualizar_interface()
        self.verificar_fim_jogo()
    
    def atualizar_interface(self):
        # Atualizar palavra
        for widget in self.frame_palavra.winfo_children():
            widget.destroy()
        
        for letra in self.palavra_secreta:
            label = tk.Label(
                self.frame_palavra,
                text=letra if letra in self.letras_corretas else "_",
                font=("Arial", 20),
                width=2,
                bg="#f0f0f0"
            )
            label.pack(side=tk.LEFT, padx=5)
        
        # Atualizar letras erradas
        self.label_erradas.config(
            text=f"Letras erradas: {' '.join(sorted(self.letras_erradas))}"
        )
    
    def desenhar_forca(self):
        self.canvas.delete("all")
        
        # Desenhar a forca base
        self.canvas.create_line(50, 250, 250, 250, width=2)  # Base
        self.canvas.create_line(100, 250, 100, 50, width=2)  # Poste vertical
        self.canvas.create_line(100, 50, 200, 50, width=2)   # Topo
        self.canvas.create_line(200, 50, 200, 80, width=2)   # Corda
        
        if self.tentativas >= 1:
            self.canvas.create_oval(180, 80, 220, 120, width=2)  # Cabeça
        if self.tentativas >= 2:
            self.canvas.create_line(200, 120, 200, 180, width=2)  # Corpo
        if self.tentativas >= 3:
            self.canvas.create_line(200, 140, 160, 160, width=2)  # Braço esquerdo
        if self.tentativas >= 4:
            self.canvas.create_line(200, 140, 240, 160, width=2)  # Braço direito
        if self.tentativas >= 5:
            self.canvas.create_line(200, 180, 160, 220, width=2)  # Perna esquerda
        if self.tentativas >= 6:
            self.canvas.create_line(200, 180, 240, 220, width=2)  # Perna direita
    
    def verificar_fim_jogo(self):
        if all(letra in self.letras_corretas for letra in self.palavra_secreta):
            messagebox.showinfo("Vitória!", f"Parabéns! Você venceu!\nA palavra era: {self.palavra_secreta}")
            self.novo_jogo()
        elif self.tentativas >= self.max_tentativas:
            messagebox.showinfo("Game Over", f"Você perdeu!\nA palavra era: {self.palavra_secreta}")
            self.novo_jogo()

def main():
    root = tk.Tk()
    app = JogoDaForca(root)
    root.mainloop()

if __name__ == "__main__":
    main() 