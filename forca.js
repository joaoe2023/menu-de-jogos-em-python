// Classe que controla o desenho da forca
class Forca {
    constructor() {
        this.erros = 0; // Número de erros cometidos
        this.posicaoX = 200; // Posição X da forca
        this.posicaoY = 400; // Posição Y da forca
    }

    // Método para desenhar a forca
    desenhar() {
        stroke(0);
        strokeWeight(4);
        
        // Base da forca
        line(this.posicaoX - 50, this.posicaoY, this.posicaoX + 50, this.posicaoY);
        
        // Poste vertical
        line(this.posicaoX, this.posicaoY, this.posicaoX, this.posicaoY - 200);
        
        // Barra horizontal
        line(this.posicaoX, this.posicaoY - 200, this.posicaoX + 100, this.posicaoY - 200);
        
        // Corda
        line(this.posicaoX + 100, this.posicaoY - 200, this.posicaoX + 100, this.posicaoY - 160);
        
        // Desenha o boneco baseado no número de erros
        this.desenharBoneco();
    }

    // Método para desenhar o boneco
    desenharBoneco() {
        if (this.erros >= 1) {
            // Cabeça
            circle(this.posicaoX + 100, this.posicaoY - 140, 40);
        }
        
        if (this.erros >= 2) {
            // Corpo
            line(this.posicaoX + 100, this.posicaoY - 120, this.posicaoX + 100, this.posicaoY - 60);
        }
        
        if (this.erros >= 3) {
            // Braço esquerdo
            line(this.posicaoX + 100, this.posicaoY - 100, this.posicaoX + 70, this.posicaoY - 80);
        }
        
        if (this.erros >= 4) {
            // Braço direito
            line(this.posicaoX + 100, this.posicaoY - 100, this.posicaoX + 130, this.posicaoY - 80);
        }
        
        if (this.erros >= 5) {
            // Perna esquerda
            line(this.posicaoX + 100, this.posicaoY - 60, this.posicaoX + 70, this.posicaoY - 20);
        }
        
        if (this.erros >= 6) {
            // Perna direita
            line(this.posicaoX + 100, this.posicaoY - 60, this.posicaoX + 130, this.posicaoY - 20);
        }
    }

    // Método para registrar um erro
    erro() {
        this.erros++;
    }
} 