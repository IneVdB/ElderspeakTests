import assemblyai as aai
import os
aai.settings.api_key = "" # invullen
config = aai.TranscriptionConfig(language_code="nl", speaker_labels=True)

def speech_recognition(filename: str):
    transcriber = aai.Transcriber(config=config)
    transcript = transcriber.transcribe(filename)

    if transcript.status == aai.TranscriptStatus.error:
        print(transcript.error)
    else:
        return transcript.text

def transcribe_all_files():
    directory = './videos'

    #clear file first
    open('assembly_transcription.txt', 'w').close()

    transcript = open('assembly_transcription.txt', 'a')

    for filename in os.listdir(directory):

        f = os.path.join(directory, filename)
        print('transcribing file:', f)
        if os.path.isfile(f):
            text = speech_recognition(f) + '\n'
            transcript.write(text)

    transcript.close()

if __name__ == '__main__':

    transcribe_all_files()