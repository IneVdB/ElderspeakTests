import math
import os

from pydub import AudioSegment
from pydub.utils import make_chunks, which

from speech_recognition import Recognizer, AudioFile
from speech_recognition import UnknownValueError
def speech_recognition(filename: str):
    """Convert audio file to text"""
    recognizer = Recognizer()
    try:
        print(filename, " to chunks")
        AudioSegment.converter = which("ffmpeg")
        myaudio: AudioSegment = AudioSegment.from_file(filename)  # type: ignore
        channel_count: int = myaudio.channels  # Get channels    # type: ignore
        # sample_width = myaudio.sample_width  # Get sample width
        duration_in_sec: float = len(myaudio) / 1000
        sample_rate: int = myaudio.frame_rate  # type: ignore

        print("duration_in_sec=", duration_in_sec)
        print("frame_rate=", sample_rate)  # type: ignore
        bit_rate = (
            16  # assumption , you can extract from mediainfo("test.wav") dynamically
        )

        wav_file_size: float = (
            sample_rate * bit_rate * channel_count * duration_in_sec
        ) / 20
        print("wav_file_size = ", wav_file_size)

        chunk_length_in_sec = math.ceil(
            (duration_in_sec * 20000000) / wav_file_size
        )  # in sec
        chunk_length_ms = chunk_length_in_sec * 2000
        chunks: list[AudioSegment] = make_chunks(myaudio, chunk_length_ms)  # type: ignore

        # Export all of the individual chunks as wav files

        if not os.path.exists("./uploads/chunks"):
            os.makedirs("./uploads/chunks")

        for i, chunk in enumerate(chunks):
            chunk_name = f"./uploads/chunks/chunck{i}.flac"
            print("exporting", chunk_name)
            chunk.export(chunk_name, format="flac")  # type: ignore
    except Exception as error:
        error_message = f"Fout bij het bewerken van de audiofile: {error}."
        print(error_message)
        return error_message

    chunk_dir = "./uploads/chunks/"

    nr_of_items = len(
        [
            name
            for name in os.listdir(chunk_dir)
            if os.path.isfile(os.path.join(chunk_dir, name))
        ]
    )

    total_text = ""

    try:
        for i in range(nr_of_items):
            # Speech Recognition
            audio_file = AudioFile(f"./uploads/chunks/chunck{i}.flac")
            with audio_file as source:
                recognizer.adjust_for_ambient_noise(source)  # type: ignore
                audio = recognizer.record(source)  # type: ignore
                text = recognize_google_safe(
                    recognizer, audio_data=audio, language="nl-BE"
                )

                total_text += text
                print("######## Google Recognize ####################")
                print(text)
                print("##############################################")
        return total_text.strip()
    except Exception as error:
        error_message = f"Fout bij de spraakherkenning: test123{error}."
        print(error_message)
        return ''

def recognize_google_safe(
    recognizer: Recognizer, audio_data, language: str = "nl-NL"
) -> str:  # type: ignore
    """Safe version of recognize_google"""
    try:
        text = recognizer.recognize_google(audio_data, language=language)  # type: ignore
        if isinstance(text, str):
            return " " + text
        else:
            return " " + " ".join(text)  # type: ignore
    except UnknownValueError:
        error_message = "!!Er is geen tekst herkend in het spraakbericht.!!"
        print(error_message)
        return ""

def transcribe_all_files():
    directory = './videos'

    #clear file first
    open('google_sr_transcription.txt', 'w').close()

    transcript = open('google_sr_transcription.txt', 'a')

    for filename in os.listdir(directory):

        f = os.path.join(directory, filename)
        print('transcribing file:', f)
        if os.path.isfile(f):
            text = speech_recognition(f) + '\n'
            transcript.write(text)

    transcript.close()

if __name__ == '__main__':

    transcribe_all_files()