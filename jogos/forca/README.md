# Jogo da Forca

Um jogo clássico da forca implementado em Python, disponível em duas versões: terminal e interface gráfica.

## Versões Disponíveis

### 1. Versão Terminal (jogo_da_forca.py)
- Interface via linha de comando
- Execução simples e rápida
- Ideal para qualquer ambiente Python

### 2. Versão Gráfica (jogo_da_forca_gui.py)
- Interface gráfica moderna
- Teclado virtual para jogar
- Visualização do boneco da forca em tempo real
- Requer Tkinter e PIL (Pillow)

## Como Jogar

### Versão Terminal
1. Certifique-se de ter o Python instalado
2. Abra o terminal/prompt de comando
3. Navegue até a pasta do jogo
4. Execute:
   ```
   python jogo_da_forca.py
   ```

### Versão Gráfica
1. Certifique-se de ter o Python instalado
2. Instale as dependências necessárias:
   ```
   pip install pillow
   ```
3. Execute o jogo:
   ```
   python jogo_da_forca_gui.py
   ```

## Regras do Jogo

- Uma palavra secreta é escolhida aleatoriamente
- Você deve adivinhar a palavra letra por letra
- Para cada letra errada, uma parte do boneco é desenhada
- O jogo termina quando você:
  - Acerta todas as letras da palavra (vitória)
  - O boneco é completamente desenhado (derrota)

## Características

- Duas versões para diferentes preferências
- Palavras relacionadas à computação
- Feedback visual do progresso
- Sistema de tentativas
- Interface intuitiva e amigável 