# Lista de palavras organizadas por categorias
PALAVRAS = {
    'tecnologia': [
        'python', 'computador', 'teclado', 'mouse', 'monitor',
        'internet', 'software', 'hardware', 'dados', 'programacao'
    ],
    'animais': [
        'cachorro', 'gato', 'elefante', 'girafa', 'leao',
        'tigre', 'macaco', 'panda', 'coelho', 'tartaruga'
    ],
    'frutas': [
        'banana', 'maca', 'laranja', 'uva', 'morango',
        'abacaxi', 'manga', 'pera', 'kiwi', 'melancia'
    ]
}

# Função para obter todas as palavras de todas as categorias
def obter_todas_palavras():
    todas_palavras = []
    for categoria in PALAVRAS.values():
        todas_palavras.extend(categoria)
    return todas_palavras

# Função para obter palavras de uma categoria específica
def obter_palavras_categoria(categoria):
    return PALAVRAS.get(categoria, []) 