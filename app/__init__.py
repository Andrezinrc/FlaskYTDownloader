import os
from flask import Flask, render_template, request, redirect, url_for
from pytube import YouTube
from pySmartDL import SmartDL
from flask import send_from_directory

app = Flask(__name__)

BASE_DIR = os.path.expanduser("~")
DOWNLOAD_FOLDER = os.path.join(BASE_DIR, "videos") #adiciona a pasta videos

# Verifica se a pasta 'videos' existe, se não, cria
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    try:
        url = request.form['url']
        
        # Verifique se a URL é válida
        if not url:
            raise ValueError("URL inválida. Por favor, insira uma URL.")

        # Crie um objeto YouTube
        yt = YouTube(url)

        # Obtenha a melhor qualidade disponível
        video_stream = yt.streams.get_highest_resolution()

        # Caminho completo para o destino do download
        destination_path = os.path.join(DOWNLOAD_FOLDER, video_stream.title + ".mp4")

        # Configuração do download com caminho personalizado
        video_dl = SmartDL(video_stream.url, dest=destination_path)
        video_dl.start()

        return redirect(url_for('index'))

    except Exception as e:
        error_message = f"Erro: {str(e)}"
        return render_template('error.html', error_message=error_message)

@app.route('/videos_baixados')
def videos_baixados():
    videos = [f for f in os.listdir(DOWNLOAD_FOLDER) if f.endswith('.mp4')]
    return render_template('videos_baixados.html', videos=videos)

@app.route('/videos_baixados/<video_nome>')
def reproduzir_video(video_nome):
    #rota para produzir o  video
    return send_from_directory(DOWNLOAD_FOLDER, video_nome)

if __name__ == '__main__':
    app.run(debug=True)
