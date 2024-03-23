from tiktoktts import tts
from pydub import AudioSegment
import os

def clear_directory(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    else:
        for file in os.listdir(dir_path):
            os.remove(os.path.join(dir_path, file))

def concatenate_audios(input_files, output_file):
    combined = AudioSegment.empty()
    for file in input_files:
        audio = AudioSegment.from_file(file)
        combined += audio
    combined.export(output_file, format='mp3')

def create_shortened_audio(input_file, output_file, duration=60000):
    audio = AudioSegment.from_file(input_file)
    fade_duration = 5000
    shortened = audio[:duration].fade_out(fade_duration)
    shortened.export(output_file, format='mp3')

def generate_audio(post):
    audios_dir = 'audios'
    clear_directory(audios_dir)

    audio_files = []
    for index, sentence in enumerate(post['sentencesArray']):
        filename = f'{audios_dir}/sentence{index}.mp3'
        tts(session_id="", text_speaker="en_us_006", req_text=sentence, filename=filename)
        audio_files.append(filename)

    raw_output_path = 'results/audio-raw.mp3'
    concatenate_audios(audio_files, raw_output_path)

    shortened_output_path = 'results/audio-shortened.mp3'
    create_shortened_audio(raw_output_path, shortened_output_path)

    print('Audio generated successfully.')