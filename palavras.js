// Lista de palavras para o jogo
const palavras = [
    'PYTHON',
    'JAVASCRIPT',
    'PROGRAMACAO',
    'COMPUTADOR',
    'ALGORITMO',
    'INTERNET',
    'DESENVOLVIMENTO',
    'TECNOLOGIA',
    'SOFTWARE',
    'HARDWARE',
    'DADOS',
    'REDE',
    'SISTEMA',
    'APLICACAO',
    'INTERFACE',
    'BANCO',
    'CODIGO',
    'PROGRAMA',
    'FUNCAO',
    'VARIAVEL'
];

// Função para escolher uma palavra aleatória
function escolherPalavraAleatoria() {
    const indice = Math.floor(Math.random() * palavras.length);
    return palavras[indice];
} 