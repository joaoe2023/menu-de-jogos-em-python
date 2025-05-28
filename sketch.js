// Variáveis globais do jogo
let forca; // Objeto que controla o estado da forca
let teclado; // Objeto que controla o teclado virtual
let palavraAtual; // Palavra atual do jogo
let letrasAcertadas; // Array com as letras acertadas
let letrasErradas; // Array com as letras erradas
let tentativasRestantes; // Número de tentativas restantes
let estadoJogo; // Estado atual do jogo (jogando, venceu, perdeu)

// Função que é executada uma vez quando o programa inicia
function setup() {
    createCanvas(800, 600);
    iniciarJogo();
}

// Função que é executada continuamente
function draw() {
    background(255);
    
    // Desenha a forca
    forca.desenhar();
    
    // Desenha o teclado virtual
    teclado.desenhar();
    
    // Desenha a palavra atual
    desenharPalavra();
    
    // Desenha as letras erradas
    desenharLetrasErradas();
    
    // Desenha o estado do jogo
    desenharEstadoJogo();
}

// Função que é chamada quando o mouse é clicado
function mousePressed() {
    if (estadoJogo === 'jogando') {
        teclado.verificarClique(mouseX, mouseY);
    } else if (estadoJogo === 'venceu' || estadoJogo === 'perdeu') {
        iniciarJogo();
    }
}

// Função para iniciar um novo jogo
function iniciarJogo() {
    palavraAtual = escolherPalavraAleatoria();
    letrasAcertadas = Array(palavraAtual.length).fill('_');
    letrasErradas = [];
    tentativasRestantes = 6;
    estadoJogo = 'jogando';
    forca = new Forca();
    teclado = new Teclado();
}

// Função para desenhar a palavra atual
function desenharPalavra() {
    textAlign(CENTER);
    textSize(32);
    fill(0);
    text(letrasAcertadas.join(' '), width/2, 100);
}

// Função para desenhar as letras erradas
function desenharLetrasErradas() {
    textAlign(LEFT);
    textSize(24);
    fill(255, 0, 0);
    text('Letras erradas: ' + letrasErradas.join(', '), 20, height - 20);
}

// Função para desenhar o estado do jogo
function desenharEstadoJogo() {
    if (estadoJogo === 'venceu') {
        textAlign(CENTER);
        textSize(40);
        fill(0, 255, 0);
        text('Você venceu! Clique para jogar novamente', width/2, height/2);
    } else if (estadoJogo === 'perdeu') {
        textAlign(CENTER);
        textSize(40);
        fill(255, 0, 0);
        text('Você perdeu! A palavra era: ' + palavraAtual, width/2, height/2);
        text('Clique para jogar novamente', width/2, height/2 + 50);
    }
}

// Função para verificar se o jogador ganhou
function verificarVitoria() {
    return !letrasAcertadas.includes('_');
}

// Função para verificar se o jogador perdeu
function verificarDerrota() {
    return tentativasRestantes <= 0;
}

// Função para processar uma letra jogada
function processarLetra(letra) {
    if (letrasAcertadas.includes(letra) || letrasErradas.includes(letra)) {
        return;
    }

    if (palavraAtual.includes(letra)) {
        for (let i = 0; i < palavraAtual.length; i++) {
            if (palavraAtual[i] === letra) {
                letrasAcertadas[i] = letra;
            }
        }
    } else {
        letrasErradas.push(letra);
        tentativasRestantes--;
        forca.erro();
    }

    if (verificarVitoria()) {
        estadoJogo = 'venceu';
    } else if (verificarDerrota()) {
        estadoJogo = 'perdeu';
    }
} 