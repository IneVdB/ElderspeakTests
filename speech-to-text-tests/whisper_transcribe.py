import whisper
import os

def speech_recognition(filename: str):
    try:
        model = whisper.load_model("small")
        result = model.transcribe(filename, language="nl")
        return result["text"]
    except Exception as error:
        print(f"Fout bij de spraakherkenning: {error}.")
        return ''

def transcribe_all_files():
    directory = './videos'

    #clear file first
    open('whisper_transcription.txt', 'w').close()

    transcript = open('whisper_transcription.txt', 'a')

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        print('transcribing file:', f)
        if os.path.isfile(f):
            text = speech_recognition(f) + '\n'
            transcript.write(text)

    transcript.close()


if __name__ == '__main__':

    transcribe_all_files()

    ## make sure ffmpeg is installed, in powershell: choco install ffmpeg