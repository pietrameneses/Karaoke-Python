import yt_dlp
import os
import googleapiclient.discovery
import tkinter as tk
from dotenv import load_dotenv


class Search_Result:
    def __init__(self, search_result) -> None:
        self.video_id=     search_result['id']['videoId']
        self.title=        search_result['snippet']['title']
        self.description=  search_result['snippet']['description']
        self.thumbnails=   search_result['snippet']['thumbnails']['default']['url']

class Search_Response:
    def __init__(self, search_response) -> None:
        self.prev_page_token = search_response.get('prevPageToken')
        self.next_page_token = search_response.get('nextPageToken')

        # items element contain list of videos
        items = search_response.get('items')

        self.search_results = []
        
        for item in items:
            search_result = Search_Result(item)
            self.search_results.append(search_result)

class Video:
    def __init__(self, mestre, funcao1, arg1, funcao2):
        
        # Função construtora do objeto
        # Entrada:
        # - mestre = Instancia do TK que será utilizada como interface
        # - funcao1 = Função passada para realizar a troca de tela
        # - arg1 = Tela que será redirecionado
        # - funcao2 = Função para instanciar objeto Karaoke
        # Saída: None --> O objeto é construído

        load_dotenv()

        self.mestre = mestre
        self.funcao1 = funcao1
        self.arg1 = arg1
        self.funcao2 = funcao2
        self.YOUTUBE_DATA_API_KEY = os.getenv('YOUTUBE_DATA_API_KEY')
        
        self.first_search = True
        self.resultados = {}

        self.youtube = googleapiclient.discovery.build(
            serviceName='youtube', 
            version='v3', 
            developerKey=self.YOUTUBE_DATA_API_KEY
            )
        
        self.create_widgets()

    # -----------------------------------------------------------------------------------------------------------------------

    def create_widgets(self):
        
        # Função para criar os widgets que aparecerão na tela
        # Entrada: None --> O próprio objeto instanciado
        # Saída: None --> Os widgets são criados
        
        self.status_label = tk.Label(
            self.mestre, 
            background='#000080', 
            foreground='#F8F8FF', 
            pady=10
            )


        self.karaoke_label = tk.Label(
            self.mestre, text='KARAOKE',
              font=('Arial', 80, 'bold'), 
              background='#000080', 
              foreground='#F8F8FF'
              )
        
        self.karaoke_label.grid(pady=50)

        self.text_box = tk.Text(
            self.mestre, height=1, 
            width=70, 
            font=('Arial', 20), 
            padx=10, pady=10
            )
        
        self.text_box.grid(padx=20, pady=(0,20))

        self.search_button = tk.Button(
            self.mestre, text='PESQUISAR', 
            command=self.search_yt, 
            font=('Arial', 20), 
            border=3, 
            width=24
            )
        
        self.search_button.grid(pady=(0,30))


        # Implementação futura de pitch shifter
        '''self.pitch_frame = tk.Frame(self.mestre, background='#000080')
        self.pitch_frame.grid()
        self.download_button = tk.Button(
            self.pitch_frame,
            text="Download",
            font=("Arial", 20, "bold"),
            command='',
            width=10,
            border=3
        )
        self.download_button.grid(row=2, column=0)
        self.more_pitch = tk.Button(
            self.pitch_frame,
            text="+",
            font=("Arial", 20, "bold"),
            command='',
            width=2,
            border=3
        )
        self.more_pitch.grid(row=2, column=1)
        self.less_pitch = tk.Button(
            self.pitch_frame,
            text="-",
            font=("Arial", 20, "bold"),
            command='',
            width=2,
            border=3
        )
        self.less_pitch.grid(row=2,column=2)
        self.sample_button = tk.Button(
            self.pitch_frame,
            text="Sample",
            font=("Arial", 20, "bold"),
            command='',
            width=10,
            border=3
        )
        self.sample_button.grid(row=2, column=3)'''

    # -----------------------------------------------------------------------------------------------------------------------

    def display_yt_results(self):

        # Função para carregar na tela o resultado da requisição à API do Youtube
        # Entrada: None --> O próprio objeto instanciado
        # Saída: None --> É exibida uma lista com os resultados da requisição

        item_index = 1
        

        if self.first_search:
            
            self.list_item = tk.Listbox(
                self.mestre, 
                height=10, 
                width=80, 
                selectmode='single', 
                font=('Arial', 20), 
                background='#F8F8FF'
                )

            for search_result in self.search_response.search_results:
                self.list_item.insert(item_index, search_result.title)
                self.resultados[search_result.title] = search_result.video_id
                item_index = item_index + 1

            self.list_item.grid(pady=(30,0))
            
            self.select_button = tk.Button(
                self.mestre, 
                text="INICIAR", 
                font=('Arial', 20), 
                command=self.next_page, 
                width=20, 
                border=3
                )
            
            self.select_button.grid(pady=20)
            
            self.status_label.grid()
            
            self.first_search = False
        
        else:

            self.list_item.destroy()
            self.select_button.destroy()
            self.status_label.destroy()

            self.status_label = tk.Label(
                self.mestre, 
                background='#000080', 
                foreground='#F8F8FF', 
                pady=10
                )
            
            self.list_item = tk.Listbox(
                self.mestre, 
                height=10, 
                width=80, 
                selectmode='single', 
                font=('Arial', 20), 
                background='#F8F8FF'
                )

            for search_result in self.search_response.search_results:
                self.list_item.insert(item_index, search_result.title)
                self.resultados[search_result.title] = search_result.video_id
                item_index = item_index + 1

            self.list_item.grid(pady=(30,0))
            
            self.select_button = tk.Button(
                self.mestre, 
                text="INICIAR", 
                font=('Arial', 20), 
                command=self.next_page, 
                width=20, 
                border=3
                )
            
            self.select_button.grid(pady=20)
            
            self.status_label.grid()
            
    # -----------------------------------------------------------------------------------------------------------------------

    def search_yt(self):

        # Função que faz a requisição à API
        # Entrada: None --> O próprio objeto instanciado
        # Saída: None --> Chamada de função para exibir os resultados da requisição

        # Reference: https://developers.google.com/youtube/v3/docs/search/list
        # Reference: https://developers.google.com/youtube/v3/guides/implementation/pagination

        self.query = self.text_box.get(1.0, "end-1c") #tex tbox string argument

        request = self.youtube.search().list(
            part="snippet", # search by keyword
            maxResults=10,
            q=self.query,
            type='video',   # only include videos, not playlists/channels
        )
        response = request.execute()
        
        self.search_response = Search_Response(response)
        
        self.status_label.config(text="")
        
        self.display_yt_results()

    # -----------------------------------------------------------------------------------------------------------------------

    def video_downloader(self, video_link):

        # Função que realiza o download do vídeo selecionado
        # Entrada: videolink = Link do vídeo que será baixado
        # Saída: None --> O vídeo é baixado e armazenado na pasta raiz

        ydl_opts ={
            'outtmpl': 'video_karaoke',
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        }
        
        if os.path.isfile('video_karaoke.mp4'):
            os.remove('video_karaoke.mp4')
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_link])

        else:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_link])

    # -----------------------------------------------------------------------------------------------------------------------

    def audio_downloader(self, video_link):

        # Função que realiza o download do áudio do vídeo selecionado para análise
        # Entrada: videolink = Link do vídeo que será baixado
        # Saída: None --> O áudio é baixado e armazenado na pasta raiz

        ydl_opts = {
            'outtmpl': 'audio_karaoke',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192', }]
                }
        
        if os.path.isfile('audio_karaoke.mp3'):
            os.remove('audio_karaoke.mp3')
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_link])
        else:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_link])

    # -----------------------------------------------------------------------------------------------------------------------

    def select_video(self):

        # Função para selecionar o vídeo dentro da lista com a resposta da requisição
        # Entrada: None --> O próprio objeto instanciado
        # Saída: Bool --> Booleano que representa se ouve sucesso ou falha na requisição

        for i in self.list_item.curselection():
            self.video_id = self.resultados[self.list_item.get(i)]

        try:
            video_link = 'https://www.youtube.com/watch?v={0}'.format(self.video_id)
            self.audio_downloader(video_link)
            self.video_downloader(video_link)
            return True
        except:
            return False

    # -----------------------------------------------------------------------------------------------------------------------

    def video_fail(self):

        # Função que atualiza a etiqueta em caso de falha de requisição
        # Entrada: None --> O próprio objeto instanciado
        # Saída: None --> A mensagem exibida na etiqueta indica falha na requisição

        self.status = 'Falha na requisição, por favor tente novamente!'
        if self.status_label.cget('text') != self.status:
            self.status_label.config(text=self.status, font=('Arial', 25, 'bold'))
        else:
            pass

    # -----------------------------------------------------------------------------------------------------------------------

    def next_page(self):

        # Função para redirecionar à próxima tela do programa
        # Entrada: None --> O próprio objeto instanciado
        # Saída: None --> A tela é redirecionada
        
        self.status_label.grid()
        self.status = 'Seu video vai começar em breve!'
        self.status_label.config(text=self.status, font=('Arial', 25, 'bold'))

        if self.select_video():
            self.funcao1(self.arg1)
            self.funcao2()
            self.first_search = True
            self.destroy_widgets()
            self.create_widgets()

        else:
            self.video_fail()

    # -----------------------------------------------------------------------------------------------------------------------

    def destroy_widgets(self):

        # Função para destruir os widgets da tela atual
        # Entrada: None --> O próprio objeto instanciado
        # Saída: None --> Os widgets são destruídos

        self.status_label.destroy()
        self.karaoke_label.destroy()
        self.text_box.destroy()
        self.search_button.destroy()
        self.list_item.destroy()
        self.select_button.destroy()