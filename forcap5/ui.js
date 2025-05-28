/**
 * Configura os elementos do jogo, incluindo a criação do teclado virtual
 * Esta função cria os botões para cada letra do alfabeto e configura seus eventos
 */
function setupGame() {
    // Cria o teclado virtual
    const keyboard = document.getElementById('keyboard');
    keyboard.innerHTML = '';
    
    // Cria botões para cada letra do alfabeto
    const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
    letters.forEach(letter => {
        const key = document.createElement('button');
        key.className = 'key';
        key.textContent = letter;
        key.setAttribute('data-letter', letter);
        key.addEventListener('click', () => game.handleLetterGuess(letter));
        keyboard.appendChild(key);
    });
}

/**
 * Configura todos os event listeners do jogo
 * Inclui os botões de início, jogar novamente e seleção de dificuldade
 */
function setupEventListeners() {
    // Configura o botão de início do jogo
    document.getElementById('start-button').addEventListener('click', () => {
        if (game.state.difficulty) {
            game.start();
        } else {
            alert('Por favor, selecione uma dificuldade primeiro!');
        }
    });
    
    // Configura o botão de jogar novamente
    document.getElementById('play-again-button').addEventListener('click', () => game.reset());
    
    // Configura os botões de dificuldade
    document.querySelectorAll('.difficulty-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.difficulty-btn').forEach(b => b.classList.remove('selected'));
            btn.classList.add('selected');
            game.state.difficulty = btn.dataset.difficulty;
        });
    });
}

/**
 * Inicializa o jogo quando a página é carregada
 * Configura o teclado, eventos e mostra a tela inicial
 */
function initializeGame() {
    setupGame();
    setupEventListeners();
    showScreen('start-screen');
}

/**
 * Reseta o teclado virtual
 * Remove as classes 'correct' e 'wrong' de todas as teclas
 */
function resetKeyboard() {
    document.querySelectorAll('.key').forEach(key => {
        key.classList.remove('correct', 'wrong');
    });
}

/**
 * Atualiza os elementos da interface do usuário
 * Atualiza a categoria e o número de vidas exibidos
 */
function updateUI() {
    document.getElementById('category').textContent = game.state.category;
    document.getElementById('lives').textContent = game.state.lives;
}

/**
 * Mostra uma tela específica e esconde as outras
 * @param {string} screenId - ID da tela que deve ser mostrada
 */
function showScreen(screenId) {
    const screens = ['start-screen', 'game-screen', 'end-screen'];
    screens.forEach(screen => {
        document.getElementById(screen).style.display = screen === screenId ? 'flex' : 'none';
    });
}

/**
 * Mostra a tela de fim de jogo
 * Exibe a mensagem de vitória ou derrota e a palavra correta
 */
function showEndScreen() {
    const endMessage = document.getElementById('end-message');
    const wordReveal = document.getElementById('word-reveal');
    
    endMessage.textContent = game.state.won ? 'Você Venceu!' : 'Game Over!';
    wordReveal.textContent = `A palavra era: ${game.state.word}`;
    
    showScreen('end-screen');
}

// Inicializa o jogo quando o DOM estiver completamente carregado
document.addEventListener('DOMContentLoaded', initializeGame); 