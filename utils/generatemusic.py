from pydub import AudioSegment
import random

def generate_music(input_music_path, output_music_path, duration=60000, fade_out_duration=5000):
    # Načtení audio souboru
    music = AudioSegment.from_file(input_music_path)

    # Výběr náhodné části hudby
    max_start = len(music) - duration
    start_time = random.randint(0, max(max_start, 1))
    end_time = start_time + duration
    selected_music = music[start_time:end_time]

    # Aplikace postupného snižování hlasitosti
    faded_music = selected_music.fade_out(fade_out_duration)

    # Uložení upraveného souboru
    faded_music.export(output_music_path, format="mp3")