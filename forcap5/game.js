// Função para remover acentos
function removeAccents(str) {
    return str.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
}

// Palavras por categoria e dificuldade (sem acentos)
const wordCategories = {
    easy: {
        'Animais': ['CACHORRO', 'GATO', 'ELEFANTE', 'LEAO', 'MACACO', 'TARTARUGA', 'COELHO', 'GIRAFA'],
        'Frutas': ['BANANA', 'MACA', 'LARANJA', 'UVA', 'MORANGO', 'ABACAXI', 'MELANCIA', 'PERA'],
        'Cores': ['AZUL', 'VERMELHO', 'AMARELO', 'VERDE', 'ROXO', 'ROSA', 'LARANJA', 'PRETO']
    },
    medium: {
        'Paises': ['BRASIL', 'PORTUGAL', 'ESPANHA', 'FRANCA', 'ALEMANHA', 'ITALIA', 'JAPAO', 'CANADA'],
        'Profissoes': ['MEDICO', 'PROFESSOR', 'ENGENHEIRO', 'ADVOGADO', 'DENTISTA', 'ARQUITETO', 'PROGRAMADOR'],
        'Esportes': ['FUTEBOL', 'BASQUETE', 'TENIS', 'NATACAO', 'VOLEIBOL', 'ATLETISMO', 'CICLISMO']
    },
    hard: {
        'Ciencia': ['QUIMICA', 'FISICA', 'BIOLOGIA', 'ASTRONOMIA', 'GEOLOGIA', 'METEOROLOGIA'],
        'Tecnologia': ['COMPUTADOR', 'INTERNET', 'ROBOTICA', 'INTELIGENCIA', 'ALGORITMO', 'PROGRAMACAO'],
        'Historia': ['REVOLUCAO', 'INDEPENDENCIA', 'MONARQUIA', 'REPUBLICA', 'DEMOCRACIA', 'IMPERIALISMO']
    }
};

// Estado do jogo
const gameState = {
    word: '',
    category: '',
    difficulty: '',
    guessedLetters: new Set(),
    lives: 6,
    gameOver: false
};

// Configuração do canvas
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

// Inicia o jogo com a dificuldade selecionada
function startGame(difficulty) {
    gameState.difficulty = difficulty;
    
    // Escolhe uma categoria aleatória
    const categories = Object.keys(wordCategories[difficulty]);
    gameState.category = categories[Math.floor(Math.random() * categories.length)];
    
    // Escolhe uma palavra aleatória da categoria
    const words = wordCategories[difficulty][gameState.category];
    gameState.word = words[Math.floor(Math.random() * words.length)];
    
    // Reseta o estado do jogo
    gameState.guessedLetters.clear();
    gameState.lives = 6;
    gameState.gameOver = false;

    // Atualiza a interface
    document.getElementById('start-screen').style.display = 'none';
    document.getElementById('game-screen').style.display = 'flex';
    document.getElementById('difficulty-display').textContent = 
        difficulty.charAt(0).toUpperCase() + difficulty.slice(1);
    document.getElementById('lives-display').textContent = gameState.lives;
    
    // Cria o teclado
    createKeyboard();
    
    // Atualiza a palavra
    updateWord();
    
    // Desenha a forca
    drawHangman();
}

// Cria o teclado virtual
function createKeyboard() {
    const keyboard = document.getElementById('keyboard');
    keyboard.innerHTML = '';
    
    // Cria botões para cada letra (A-Z)
    for (let i = 65; i <= 90; i++) {
        const letter = String.fromCharCode(i);
        const button = document.createElement('button');
        button.className = 'key';
        button.textContent = letter;
        button.setAttribute('data-letter', letter);
        button.onclick = () => handleLetterGuess(letter);
        keyboard.appendChild(button);
    }

    // Adiciona o botão para a letra Ç
    const cedilhaButton = document.createElement('button');
    cedilhaButton.className = 'key';
    cedilhaButton.textContent = 'Ç';
    cedilhaButton.setAttribute('data-letter', 'Ç');
    cedilhaButton.onclick = () => handleLetterGuess('Ç');
    keyboard.appendChild(cedilhaButton);
}

// Atualiza a exibição da palavra
function updateWord() {
    const wordDisplay = gameState.word
        .split('')
        .map(letter => gameState.guessedLetters.has(letter) ? letter : '_')
        .join(' ');
    
    document.getElementById('word').textContent = wordDisplay;
}

// Desenha o boneco da forca
function drawHangman() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Configuração do estilo
    ctx.strokeStyle = '#fff';
    ctx.lineWidth = 4;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.shadowColor = 'rgba(0, 0, 0, 0.3)';
    ctx.shadowBlur = 5;
    ctx.shadowOffsetX = 2;
    ctx.shadowOffsetY = 2;

    // Base
    ctx.beginPath();
    ctx.moveTo(50, 350);
    ctx.lineTo(350, 350);
    ctx.stroke();

    // Poste vertical
    ctx.beginPath();
    ctx.moveTo(100, 350);
    ctx.lineTo(100, 50);
    ctx.stroke();

    // Viga horizontal
    ctx.beginPath();
    ctx.moveTo(100, 50);
    ctx.lineTo(250, 50);
    ctx.stroke();

    // Corda
    ctx.beginPath();
    ctx.moveTo(250, 50);
    ctx.lineTo(250, 100);
    ctx.stroke();

    // Desenha as partes do corpo baseado nas vidas restantes
    if (gameState.lives < 6) {
        // Cabeça
        ctx.beginPath();
        ctx.arc(250, 130, 30, 0, Math.PI * 2);
        ctx.stroke();

        // Olhos
        ctx.beginPath();
        ctx.arc(240, 125, 3, 0, Math.PI * 2);
        ctx.arc(260, 125, 3, 0, Math.PI * 2);
        ctx.fillStyle = '#fff';
        ctx.fill();

        // Boca triste
        ctx.beginPath();
        ctx.arc(250, 135, 15, 0, Math.PI);
        ctx.stroke();
    }
    
    if (gameState.lives < 5) {
        // Corpo
        ctx.beginPath();
        ctx.moveTo(250, 160);
        ctx.lineTo(250, 260);
        ctx.stroke();
    }
    
    if (gameState.lives < 4) {
        // Braço esquerdo
        ctx.beginPath();
        ctx.moveTo(250, 180);
        ctx.lineTo(200, 220);
        ctx.stroke();
    }
    
    if (gameState.lives < 3) {
        // Braço direito
        ctx.beginPath();
        ctx.moveTo(250, 180);
        ctx.lineTo(300, 220);
        ctx.stroke();
    }
    
    if (gameState.lives < 2) {
        // Perna esquerda
        ctx.beginPath();
        ctx.moveTo(250, 260);
        ctx.lineTo(200, 320);
        ctx.stroke();
    }
    
    if (gameState.lives < 1) {
        // Perna direita
        ctx.beginPath();
        ctx.moveTo(250, 260);
        ctx.lineTo(300, 320);
        ctx.stroke();
    }

    // Reseta as sombras
    ctx.shadowColor = 'transparent';
}

// Processa uma tentativa de letra
function handleLetterGuess(letter) {
    if (gameState.gameOver || gameState.guessedLetters.has(letter)) return;

    const button = document.querySelector(`.key[data-letter="${letter}"]`);
    gameState.guessedLetters.add(letter);

    if (gameState.word.includes(letter)) {
        button.classList.add('correct');
    } else {
        button.classList.add('wrong');
        gameState.lives--;
        document.getElementById('lives-display').textContent = gameState.lives;
        drawHangman();
    }

    button.classList.add('used');
    updateWord();
    checkGameOver();
}

// Função para mostrar animação de vitória
function showWinAnimation() {
    const anim = document.getElementById('end-animation');
    anim.innerHTML = '';
    anim.style.display = 'block';
    const colors = ['#FFD700', '#4CAF50', '#FF4081', '#2196F3', '#FF9800', '#9C27B0'];
    for (let i = 0; i < 40; i++) {
        const confetti = document.createElement('div');
        confetti.className = 'confetti';
        confetti.style.left = Math.random() * 100 + 'vw';
        confetti.style.background = colors[Math.floor(Math.random() * colors.length)];
        confetti.style.transform = `rotate(${Math.random() * 360}deg)`;
        anim.appendChild(confetti);
    }
    setTimeout(() => { anim.style.display = 'none'; anim.innerHTML = ''; }, 1500);
}

// Função para mostrar animação de derrota
function showLoseAnimation() {
    const anim = document.getElementById('end-animation');
    anim.innerHTML = '';
    anim.style.display = 'block';
    for (let i = 0; i < 30; i++) {
        const drop = document.createElement('div');
        drop.className = 'drop';
        drop.style.left = Math.random() * 100 + 'vw';
        drop.style.background = '#4fc3f7';
        anim.appendChild(drop);
    }
    // Mostrar mensagem Game Over
    const gameOverMsg = document.getElementById('game-over-message');
    gameOverMsg.style.display = 'block';
    setTimeout(() => {
        anim.style.display = 'none';
        anim.innerHTML = '';
        gameOverMsg.style.display = 'none';
    }, 1500);
}

// Verifica se o jogo terminou
function checkGameOver() {
    const wordComplete = gameState.word
        .split('')
        .every(letter => gameState.guessedLetters.has(letter));

    if (wordComplete) {
        gameState.gameOver = true;
        showWinAnimation();
        setTimeout(() => {
            alert('Parabéns! Você venceu!');
            document.getElementById('start-screen').style.display = 'flex';
            document.getElementById('game-screen').style.display = 'none';
        }, 1500);
    } else if (gameState.lives === 0) {
        gameState.gameOver = true;
        showLoseAnimation();
        setTimeout(() => {
            alert(`Game Over! A palavra era ${gameState.word}`);
            document.getElementById('start-screen').style.display = 'flex';
            document.getElementById('game-screen').style.display = 'none';
        }, 1500);
    }
}

// Inicia o jogo quando a página carregar
window.onload = () => {
    document.getElementById('start-screen').style.display = 'flex';
    document.getElementById('game-screen').style.display = 'none';
}; 