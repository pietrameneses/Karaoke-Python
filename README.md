# Karaoke-Python 🎤

Um aplicativo de **karaokê** desenvolvido inteiramente em **Python**, que utiliza vídeos do YouTube como base para a música e aplica um algoritmo de análise de frequências para pontuação.  
Projeto ideal para quem quer cantar, se divertir e aprender mais sobre processamento de áudio.

---

## 🚀 Funcionalidades

- Reprodução de vídeos do YouTube como base musical  
- Captura de áudio do microfone para comparar com a música  
- Algoritmo de verificação de frequências para avaliar a performance  
- Pontuação para indicar quão próxima a voz do usuário esteve da melodia  
- Ferramentas de apoio, como escalas e identificação de tom (key finding)  

---

## 📁 Estrutura do repositório

| Arquivo / Módulo | Descrição |
|------------------|-----------|
| `main.py` | Entrada / ponto inicial do programa |
| `karaoke.py` | Lógica principal do karaokê (mixagem, comparação, pontuação) |
| `youtube_api.py` | Integração com API do YouTube para busca / streaming de vídeos |
| `vlc_player.py` | Controle de reprodução de vídeo / áudio via VLC (bindings) |
| `finder.py` | Algoritmos auxiliares para análise de áudio / comparação |
| `keyfinder.py` | Funções para identificação do tom (key) da música |
| `escalas.py` | Recursos musicais (escalas, intervalos etc.) |
| `requirements.txt` | Dependências do projeto |
| `primeiros-passos.txt` | Guia rápido de como começar / executar o projeto |

---

## 🛠 Pré-requisitos / Instalação

1. Ter **Python 3.x** instalado  
2. Instalar dependências:

   ```bash
   pip install -r requirements.txt
