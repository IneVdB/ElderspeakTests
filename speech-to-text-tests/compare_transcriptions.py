import jiwer

def get_accuracy(true, predicted):
    output = jiwer.process_words(true, predicted)
    wer = output.wer
    mer = output.mer
    wil = output.wil
    print('Word Error Rate:', wer)
    print('Match Error Rate:', mer)
    print('Word Information Lost:', wil)

if __name__ == '__main__':

    with open('assembly_transcription.txt', 'r') as f:
        predicted = f.read().splitlines()

    with open('compiled_transcriptions.txt', 'r', encoding='utf-8') as f:
        true = f.read().splitlines()

    print('Accuracy AssemblyAI:')
    get_accuracy(true, predicted)

    with open('whisper_transcription.txt', 'r') as f:
        predicted = f.read().splitlines()

    print('Accuracy Whisper:')
    get_accuracy(true, predicted)

    with open('google_sr_transcription.txt', 'r') as f:
        predicted = f.read().splitlines()

    print('Accuracy Google Speech Recognition:')
    get_accuracy(true, predicted)