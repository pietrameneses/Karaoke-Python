import vlc
import tkinter as tk
import os
import threading
from karaoke import Karaoke
from escalas import Tom
from pygame import mixer

class Video_Player:
    def __init__(self, mestre, funcao, arg1, arg2, tom):
        
        # Função construtora do objeto
        # Entrada:
        # - mestre = Instancia do TK que será utilizada como interface
        # - funcao = Função passada para realizar a troca de tela
        # - arg1 = Tela 1 que será redirecionado
        # - arg2 = Tela 2 que será redirecionado
        # Saída: None --> O objeto é construído

        self.mestre = mestre
        self.funcao = funcao
        self.arg1 = arg1
        self.arg2 = arg2
        self.tom = tom
        self.isPlayed = True
        self.isNotPlayed = False
        #os.system("pactl load-module module-loopback latency_msec=1") # o retorno de áudio é ativado
        self.video_audio_instance()

    # -----------------------------------------------------------------------------------------------------------------------

    def video_audio_instance(self):

        # Função para criar a instância de vídeo
        # Entrada: None --> O próprio objeto instanciado
        # Saída: None --> O objeto de vídeo é instanciado

        mixer.init()
        #mixer.music.load('audio_video.mp3')

        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        
        self.create_widgets()

        os.system("pactl load-module module-loopback latency_msec=1 source=1 sink=1") # o retorno de áudio é ativado

        self.afinador = Karaoke(self.arg1, self.tom, self.funcao, self.arg2, self.botao)
        self.afinador.ligar_desligar()


        self.play()

        self.media_canvas.after(1000, self.get_end)

    # -----------------------------------------------------------------------------------------------------------------------

    def create_widgets(self):

        # Função para criar os widgets que aparecerão na tela
        # Entrada: None --> O próprio objeto instanciado
        # Saída: None --> Os widgets são criados

        width = (int(self.mestre.winfo_screenwidth()) - 354)
        height = (int(self.mestre.winfo_screenheight()) - 200)
        
        self.media_canvas = tk.Canvas(
            self.mestre, 
            bg="#000080", 
            width=width, 
            height=height
            )
        
        self.media_canvas.grid(row=0, pady=(40 ,10))

        self.control_buttons_frame = tk.Frame(
            self.mestre, 
            background='#000080'
            )
        
        self.control_buttons_frame.grid(pady=15)
        
        self.pause_button = tk.Button(
            self.control_buttons_frame,
            text='PAUSE',
            font=("Arial", 20, "bold"),
            bg="#FF9800",
            fg="white",
            command=self.pause,
            width=30
        )

        self.pause_button.grid(row=1, column=0, padx=100)
        
        self.menu_button = tk.Button(
            self.control_buttons_frame,
            text="MENU",
            font=("Arial", 20, "bold"),
            bg="#F44336",
            fg="white",
            command=self.return_to_home,
            width=30
        )

        self.menu_button.grid(row=1, column=1, padx=100)

        self.botao = tk.Button(
            self.control_buttons_frame,
            bg='yellow',
            width=3
    )
        self.botao.grid(row=1, column=2)

    # -----------------------------------------------------------------------------------------------------------------------

    def play(self):

        # Função para carregar e iniciar a reprodução do vídeo
        # Entrada: None --> O próprio objeto instanciado
        # Saída: None --> O vídeo inicia a reprodução

        media = self.instance.media_new('video_karaoke.mp4')
        self.player.set_media(media)
        self.player.set_xwindow(self.media_canvas.winfo_id())
        self.player.audio_set_volume(100)
        self.player.play()

        #mixer.music.play()

    # -----------------------------------------------------------------------------------------------------------------------

    def pause(self):
        
        # Função para pausar o vídeo em reprodução
        # Entrada: None --> O próprio objeto instanciado
        # Saída: None --> O vídeo em reprodução é pausado

        self.player.pause()

        if self.isPlayed:
            #mixer.music.pause()
            self.isPlayed = False
            self.pause_button.config(
                text="PLAY", 
                background='#4CAF50'
                )
        else:
            #mixer.music.unpause()
            self.isPlayed = True
            self.pause_button.config(
                text="PAUSE", 
                background='#FF9800'
                )

    # -----------------------------------------------------------------------------------------------------------------------

    def video_and_karaoke_end(self):

        # Função para encerrar o vídeo, redirecionar a tela e encerrar a captação das frequências
        # Entrada: None --> O próprio objeto instanciado
        # Saída: None --> A tela é redirecionada e os widgets são destruídos

        os.system("pactl unload-module module-loopback") #o retorno de áudio é encerrado
        self.media_canvas.destroy()
        self.control_buttons_frame.destroy()
        self.funcao(self.arg1)
        self.afinador.ligar_desligar()

    # -----------------------------------------------------------------------------------------------------------------------        

    def get_end(self):

        # Função para monitorar o final do vídeo
        # Entrada: None --> O próprio objeto instanciado
        # Saída: Função --> Quando o vídeo acaba, é chamada a função "video_and_karaoke_end"

        total_duration = self.player.get_length()
        current_time = self.player.get_time()

        if total_duration - current_time < 1000:
            return self.video_and_karaoke_end()
        
        self.media_canvas.after(1000, self.get_end)

    # -----------------------------------------------------------------------------------------------------------------------

    def return_to_home(self):

        # Função que para a reprodução dos vídeos, destrói os widgets e redireciona a tela
        # Entrada: None --> O próprio objeto instanciado
        # Saída: None --> Os widgets são destruídos e a tela é redirecionada

        self.player.release()
        self.media_canvas.destroy()
        self.control_buttons_frame.destroy()
        self.funcao(self.arg2)
        self.metodo()