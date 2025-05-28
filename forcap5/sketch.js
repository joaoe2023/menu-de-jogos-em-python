// Game state
let gameState = {
    currentScreen: 'start',
    difficulty: 'medium',
    word: '',
    category: '',
    guessedLetters: new Set(),
    lives: 6,
    gameOver: false,
    won: false,
    animation: 0
};

// Word categories and their words
const wordCategories = {
    easy: {
        'Animais': ['CACHORRO', 'GATO', 'ELEFANTE', 'LEÃO', 'MACACO', 'TARTARUGA', 'COELHO', 'GIRAFA'],
        'Frutas': ['BANANA', 'MAÇÃ', 'LARANJA', 'UVA', 'MORANGO', 'ABACAXI', 'MELANCIA', 'PERA'],
        'Cores': ['AZUL', 'VERMELHO', 'AMARELO', 'VERDE', 'ROXO', 'ROSA', 'LARANJA', 'PRETO']
    },
    medium: {
        'Países': ['BRASIL', 'PORTUGAL', 'ESPANHA', 'FRANÇA', 'ALEMANHA', 'ITALIA', 'JAPÃO', 'CANADÁ'],
        'Profissões': ['MÉDICO', 'PROFESSOR', 'ENGENHEIRO', 'ADVOGADO', 'DENTISTA', 'ARQUITETO', 'PROGRAMADOR'],
        'Esportes': ['FUTEBOL', 'BASQUETE', 'TÊNIS', 'NATAÇÃO', 'VOLEIBOL', 'ATLETISMO', 'CICLISMO']
    },
    hard: {
        'Ciência': ['QUÍMICA', 'FÍSICA', 'BIOLOGIA', 'ASTRONOMIA', 'GEOLOGIA', 'METEOROLOGIA'],
        'Tecnologia': ['COMPUTADOR', 'INTERNET', 'ROBÓTICA', 'INTELIGÊNCIA', 'ALGORITMO', 'PROGRAMAÇÃO'],
        'História': ['REVOLUÇÃO', 'INDEPENDÊNCIA', 'MONARQUIA', 'REPÚBLICA', 'DEMOCRACIA', 'IMPERIALISMO']
    }
};

// p5.js setup
function setup() {
    createCanvas(600, 400);
    setupGame();
    setupEventListeners();
}

// p5.js draw
function draw() {
    background(26, 26, 46);
    
    if (gameState.currentScreen === 'game') {
        drawHangman();
        drawWord();
        drawKeyboard();
        
        // Update animation
        gameState.animation += 0.05;
    }
}

// Setup game elements
function setupGame() {
    // Create keyboard
    const keyboard = document.getElementById('keyboard');
    keyboard.innerHTML = '';
    
    const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
    letters.forEach(letter => {
        const key = document.createElement('button');
        key.className = 'key';
        key.textContent = letter;
        key.setAttribute('data-letter', letter);
        key.addEventListener('click', () => handleLetterGuess(letter));
        keyboard.appendChild(key);
    });
}

// Setup event listeners
function setupEventListeners() {
    // Start button
    document.getElementById('start-button').addEventListener('click', startGame);
    
    // Play again button
    document.getElementById('play-again-button').addEventListener('click', resetGame);
    
    // Difficulty buttons
    document.querySelectorAll('.difficulty-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.difficulty-btn').forEach(b => b.classList.remove('selected'));
            btn.classList.add('selected');
            gameState.difficulty = btn.dataset.difficulty;
        });
    });
}

// Start the game
function startGame() {
    // Select random category and word
    const categories = Object.keys(wordCategories[gameState.difficulty]);
    gameState.category = categories[Math.floor(Math.random() * categories.length)];
    const words = wordCategories[gameState.difficulty][gameState.category];
    gameState.word = words[Math.floor(Math.random() * words.length)];
    
    // Reset game state
    gameState.guessedLetters.clear();
    gameState.lives = 6;
    gameState.gameOver = false;
    gameState.won = false;
    
    // Reset keyboard and update UI
    resetKeyboard();
    updateUI();
    
    // Show game screen
    showScreen('game-screen');
    gameState.currentScreen = 'game';
}

// Reset the game
function resetGame() {
    resetKeyboard();
    showScreen('start-screen');
    gameState.currentScreen = 'start';
}

// Handle letter guess
function handleLetterGuess(letter) {
    if (gameState.gameOver || gameState.guessedLetters.has(letter)) return;
    
    gameState.guessedLetters.add(letter);
    const key = document.querySelector(`.key[data-letter="${letter}"]`);
    
    if (gameState.word.includes(letter)) {
        key.classList.add('correct');
        checkWin();
    } else {
        key.classList.add('wrong');
        gameState.lives--;
        updateUI();
        checkLose();
    }
}

// Check if player won
function checkWin() {
    const wordComplete = gameState.word.split('').every(letter => 
        gameState.guessedLetters.has(letter)
    );
    
    if (wordComplete) {
        gameState.won = true;
        endGame();
    }
}

// Check if player lost
function checkLose() {
    if (gameState.lives <= 0) {
        gameState.gameOver = true;
        endGame();
    }
}

// End the game
function endGame() {
    showEndScreen();
    gameState.currentScreen = 'end';
}

// Draw the hangman
function drawHangman() {
    stroke(255);
    strokeWeight(3);
    noFill();
    
    // Base
    line(100, 350, 300, 350);
    
    // Vertical pole
    line(200, 350, 200, 100);
    
    // Top beam
    line(200, 100, 300, 100);
    
    // Rope
    line(300, 100, 300, 150);
    
    // Draw body parts based on lives with animation
    if (gameState.lives < 6) {
        push();
        // Add swinging animation
        let swing = sin(gameState.animation) * 5;
        translate(swing, 0);
        
        // Head
        circle(300, 170, 40);
        
        if (gameState.lives < 5) {
            // Body
            line(300, 190, 300, 270);
        }
        
        if (gameState.lives < 4) {
            // Left arm
            line(300, 210, 260, 250);
        }
        
        if (gameState.lives < 3) {
            // Right arm
            line(300, 210, 340, 250);
        }
        
        if (gameState.lives < 2) {
            // Left leg
            line(300, 270, 260, 320);
        }
        
        if (gameState.lives < 1) {
            // Right leg
            line(300, 270, 340, 320);
        }
        
        // Add face when head is drawn
        if (gameState.lives < 6) {
            // Eyes
            fill(255);
            noStroke();
            circle(290, 165, 5);
            circle(310, 165, 5);
            
            // Sad mouth
            noFill();
            stroke(255);
            arc(300, 175, 20, 10, 0, PI);
        }
        
        pop();
    }
}

// Draw the word with guessed letters
function drawWord() {
    textAlign(CENTER);
    textSize(32);
    fill(255);
    noStroke();
    
    const wordDisplay = gameState.word.split('').map(letter => 
        gameState.guessedLetters.has(letter) ? letter : '_'
    ).join(' ');
    
    text(wordDisplay, width/2, 380);
}

// Draw the keyboard
function drawKeyboard() {
    // Keyboard is handled by HTML/CSS
} 