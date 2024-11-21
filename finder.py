from keyfinder import KeyFinder

def finder(path):

    # Função para encontrar o tom de um arquivo de áudio
    # Entrada: path --> String com o caminho do arquivo de áudio
    # Saída: str --> Tom do arquivo de áudio analisado

    song = KeyFinder(path)
    key = song.key_primary

    return key