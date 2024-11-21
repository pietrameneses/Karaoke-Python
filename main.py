import tkinter as tk
from escalas import Tom
from karaoke import Karaoke
from finder import finder
from youtube_api import Video
from vlc_player import Video_Player


def raise_frame(frame):

    # Função para realizar o redirecionamento das telas
    # Entrada: frame --> A instancia da tela que será redirecionada
    # Saída: None --> A tela é redirecionada para o frama desejado

    frame.tkraise()



if __name__ == "__main__":

    # Instancia e personalzação da interface principal
    interface = tk.Tk()
    interface.title('Karaoke')
    interface.geometry("{0}x{1}".format(interface.winfo_screenwidth(), interface.winfo_screenheight()))
    interface.configure(background='#000080')
    interface.grid_columnconfigure(0, weight=1)
    status = tk.Button(
        interface,
        bg='yellow',
        width=3
    )

    # Instanciação das telas
    Home = tk.Frame(interface)
    Karaoke_display = tk.Frame(interface)
    Player = tk.Frame(interface)
    
    def instanciar_karaoke():

        # Função para iniciar instanciar e inicializar o Karaoke
        # Entrada: None
        # Saída: None --> Inicia a reprodução do vídeo e a captação das frequências

        key = finder('audio_karaoke.mp3')
        tom = Tom(key)
        #afinador = Karaoke(Karaoke_display, tom.get_frequencias(), raise_frame, Home)
        #afinador.ligar_desligar()
        media_player = Video_Player(Player, raise_frame, Karaoke_display, Home, tom.get_frequencias())


    Youtube_Search = Video(Home, raise_frame, Player, instanciar_karaoke)

    # Configurar as telas que serão exibidas na interface
    for frame in (Home, Karaoke_display, Player):
        frame.grid(row=0, column=0,sticky='news')
        frame.configure(background='#000080')
        frame.grid_columnconfigure(0, weight=1)

    # Inicialização da aplicação em si
    raise_frame(Home)
    interface.mainloop()
