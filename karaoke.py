import numpy as np
import pyaudio
import tkinter as tk
import threading
from queue import Queue, Full
from array import array

class Karaoke:
    def __init__(self, mestre, escala, funcao1, arg1, botao):

        # Função construtora do objeto
        # Entrada:
        # - mestre = Instancia do TK que será utilizada como interface
        # - escala = Lista de frequências da escala musical da música reproduzida
        # - funcao1 = Função passada para realizar a troca de tela
        # - arg1 = Próxima tela a ser redirecionado
        # Saída: None --> O objeto é construído

        
        self.mestre = mestre
        self.escala = escala
        self.funcao1 = funcao1
        self.arg1 = arg1
        self.botao = botao


        self.TAMANHO_BLOCO = 4096
        self.TAXA = 44100
        self.p = None
        self.fluxo = None
        self.limite = 8 # Tolerância de erro em Hertz
        self.rodando = False
        self.lista_nota = [] # Lista com os erros e acertos das notas capturadas
        self.stopped = threading.Event()
        self.threshold = True
        self.q = Queue(maxsize=int(round((1024*10) / 1024)))

        listen_t = threading.Thread(target=self.iniciar_fluxo)
        listen_t.start()
        listen_t.join()

        self.create_widgets()

    # -----------------------------------------------------------------------------------------------------------------------

    def create_widgets(self):

        # Função para criar os widgets que serão exibidos na tela (título, nota, botões, etc)
        # Entrada esperada: None --> O próprio objeto instanciado
        # Saída: None --> (Criação dos widgets na tela)

        self.label_titulo = tk.Label(
            self.mestre, 
            text='SUA NOTA É:', 
            font=('Arial', 40, 'bold'), 
            background='#000080', 
            foreground='#F8F8FF'
            )
        
        self.label_titulo.grid(pady=(50, 10))

        self.frame_nota = tk.Frame(
            self.mestre, 
            background='#000080', 
            height=500, 
            width=500, 
            bd=10
            )
        
        self.frame_nota.grid(padx=30, pady=(0, 30))

        self.label_nota = tk.Label(
            self.frame_nota, text="", 
            font=('Arial', 300), 
            background='#000080', 
            foreground='#F8F8FF'
            )
        
        self.label_nota.grid()

        self.frame_home = tk.Frame(
            self.mestre, 
            background='#000080'
            )
        
        self.frame_home.grid()

        self.botao_home = tk.Button(
            self.frame_home, 
            text='MENU', 
            font=('Arial', 30), 
            command=self.return_to_home, 
            border=3, 
            width=20
            )
        
        self.botao_home.grid(pady=(100,0))

    # -----------------------------------------------------------------------------------------------------------------------

    def ligar_desligar(self):

        # Função para ligar e desligar o fluxo de captação do sinal do microfone
        # Entrada: None --> O próprio objeto instanciado
        # Saída: None --> Inicia e interrompe a captação de áudio

        if self.rodando:
            self.parar_fluxo()
            #self.botao_ligar_desligar.config(text="Iniciar")
            self.rodando = False
            self.gerar_pontuacao()
        else:
            self.iniciar_fluxo()
            #self.botao_ligar_desligar.config(text="Parar")
            self.rodando = True
            self.lista_nota = []
            self.mestre.after(5000, self.coletar_nota)

    # -----------------------------------------------------------------------------------------------------------------------

    def iniciar_fluxo(self):

        # Função para instanciar o objeto que capturará os dados de áudio
        # Entrada: None --> O próprio objeto instanciado
        # Saída: None --> Instancia o objeto e começa a capturar os dados de som

        self.p = pyaudio.PyAudio()

        self.fluxo = self.p.open(
            format=pyaudio.paInt16, 
            channels=1, 
            rate=self.TAXA, 
            input=True, 
            frames_per_buffer=self.TAMANHO_BLOCO
            )

    # -----------------------------------------------------------------------------------------------------------------------

    def parar_fluxo(self):

        # Função para interromper a captura dos dados de áudio
        # Entrada: None --> O próprio objeto instanciado
        # Saída: None --> Interrompe o fluxo de dados

        self.fluxo.stop_stream()
        self.fluxo.close()
        self.p.terminate()

    # -----------------------------------------------------------------------------------------------------------------------

    def analisar(self):

        # Função que utiliza os dados capturados pelo fluxo e os transforma em valores de frequência em Hertz
        # Entrada: None --> O própri objeto instanciado
        # Saída: Int --> Um inteiro representando o valor em Hertz que está sendo captado pelo microfone

        dados = np.frombuffer(self.fluxo.read(self.TAMANHO_BLOCO), dtype=np.int16)
        w = np.fft.fft(dados)
        freqs = np.fft.fftfreq(len(w))
        idx = np.argmax(np.abs(w))
        freq = freqs[idx]
        freq_em_hertz = int(abs(freq * self.TAXA))
        try:
            data_chunk = array('h', self.fluxo.read(self.TAMANHO_BLOCO))
            vol = max(data_chunk)
            if(vol >= 700):
                self.threshold = True
            else:
                self.threshold = False
                self.botao.configure(bg='yellow')

            if self.threshold:
                self.lista_nota.append(freq_em_hertz)
                return freq_em_hertz

        except Full:
                pass 
        
        return 3 # 3 = sem captura de áudio
        
    # -----------------------------------------------------------------------------------------------------------------------

    def coletar_nota(self):

        # Função para verificar se as frequências estão afinadas de acordo com o tom da música reproduzida
        # Entrada: None --> O próprio objeto instanciado
        # Saída: None --> A função adiciona todos os acertos e erro a uma lista chamada "lista_nota"

        if self.rodando:
            freq = self.analisar()

            for nota in self.escala:
                if abs(freq - nota) <= self.limite: #frequencia dentro do limite
                    pontuacao = 1
                    self.botao.configure(bg='green')
                    break
                elif freq < 80: #Threshold do microfone
                    pontuacao = 5
                else:
                    pontuacao = 0
                    self.botao.configure(bg='red')

            self.lista_nota.append(pontuacao)
            self.mestre.after(10, self.coletar_nota)

    # -----------------------------------------------------------------------------------------------------------------------

    def gerar_pontuacao(self):

        # Função para calcular a nota baseada nos acertos e erros
        # Entrada: None --> O próprio objeto instanciado
        # Saída: None --> Final da execução do programa

        numero_total = self.lista_nota.count(0) + self.lista_nota.count(1)
        acertos = self.lista_nota.count(1)
        vinte_por_cento = len(self.lista_nota) * 0.35

        if acertos < vinte_por_cento:
            pontuacao_final = ((100 * acertos) // len(self.lista_nota)) // 3
        else:
            pontuacao_final = (100 * acertos) // numero_total

        self.label_nota.config(text=str(pontuacao_final))

        return None
    
    # -----------------------------------------------------------------------------------------------------------------------
    
    def return_to_home(self):

        # Função para destruir todos os widgets antes de voltar à tela inicial
        # Entrada: None --> O próprio objeto instanciado
        # Saída: None --> Todos os widgets são destruídos
        
        self.funcao1(self.arg1)
        self.label_titulo.destroy()
        self.frame_nota.destroy()
        self.label_nota.destroy()
        self.frame_home.destroy()
        self.botao_home.destroy()