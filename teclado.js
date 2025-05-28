// Classe que controla o teclado virtual
class Teclado {
    constructor() {
        this.teclas = []; // Array para armazenar as teclas
        this.iniciarTeclado();
    }

    // Método para inicializar o teclado
    iniciarTeclado() {
        const letras = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
        const teclasPorLinha = 10;
        const tamanhoTecla = 40;
        const espacoEntreTeclas = 5;
        
        for (let i = 0; i < letras.length; i++) {
            const linha = Math.floor(i / teclasPorLinha);
            const coluna = i % teclasPorLinha;
            
            this.teclas.push({
                letra: letras[i],
                x: 400 + coluna * (tamanhoTecla + espacoEntreTeclas),
                y: 200 + linha * (tamanhoTecla + espacoEntreTeclas),
                largura: tamanhoTecla,
                altura: tamanhoTecla,
                clicada: false
            });
        }
    }

    // Método para desenhar o teclado
    desenhar() {
        for (let tecla of this.teclas) {
            // Desenha o fundo da tecla
            fill(tecla.clicada ? 200 : 255);
            stroke(0);
            rect(tecla.x, tecla.y, tecla.largura, tecla.altura, 5);
            
            // Desenha a letra
            fill(0);
            noStroke();
            textAlign(CENTER, CENTER);
            textSize(20);
            text(tecla.letra, tecla.x + tecla.largura/2, tecla.y + tecla.altura/2);
        }
    }

    // Método para verificar se uma tecla foi clicada
    verificarClique(x, y) {
        for (let tecla of this.teclas) {
            if (!tecla.clicada && 
                x >= tecla.x && 
                x <= tecla.x + tecla.largura && 
                y >= tecla.y && 
                y <= tecla.y + tecla.altura) {
                
                tecla.clicada = true;
                processarLetra(tecla.letra.toLowerCase());
                break;
            }
        }
    }
} 