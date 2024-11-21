FROM registry.access.redhat.com/ubi8/python-312@sha256:5bc39ac967491e7ca7d8c8a44338b2d4df1990b7ef769b29d459e3ca8744800e

USER 0

COPY . .

RUN dnf install diffutils -y python3-tkinter -y alsa-lib.x86_64 -y alsa-lib.i686 -y python3.12-tkinter.i686 -y python3.12-tkinter.x86_64 -y

RUN git clone https://git.ffmpeg.org/ffmpeg.git ffmpeg && \
    cd ffmpeg && \
    ./configure --disable-x86asm && \
    make -j && \
    make install

RUN git clone https://github.com/PortAudio/portaudio.git portaudio && \
    cd portaudio && \
    ./configure && \
    make -j && \
    make install

#RUN pip install -r requirements.txt


RUN python3 -m venv venv && source venv/bin/activate

RUN cp /usr/local/lib/libportaudio.a .

RUN pip install google_api_python_client
RUN pip install numpy
RUN pip install pygame
RUN pip install python-dotenv
RUN pip install python_vlc
RUN pip install yt_dlp
RUN pip install pyaudio
RUN cp /opt/app-root/src/portaudio/lib/.libs/libportaudio.so.2 /usr/lib
RUN export LD_LIBRARY_PATH=/usr/lib/ && ldconfig
RUN pip install matplotlib
RUN pip install librosa

#RUN pip install -r requirements.txt
#RUN pip install pyaudio

EXPOSE 5000

ENTRYPOINT python main.py