import sys
sys.path.append('tiktok-voice')
sys.path.append('utils')
from tiktoktts import tts
from utils.cutvideo import get_random_video_file, cut_video
from utils.getrandompost import get_random_post
from utils.generateaudio import generate_audio
from utils.transcribeaudio import transcribe_audio
from utils.addsubtitles import add_subtitles_to_video
from utils.generatemusic import generate_music
from utils.addaudio import add_audio
from utils.finaltouches import add_final_touches

video_directory = 'videos'
output_directory = 'results'
video_path = get_random_video_file(video_directory)
if video_path:
    output_path = cut_video(video_path, output_directory)
    print(f'Video bylo zpracováno a uloženo do {output_path}')
else:
    print('Nebylo nalezeno žádné video.')


post = get_random_post('nosleep')
# # print(post)

generate_audio(post)

subtitles = transcribe_audio("results/audio-shortened.mp3")
# print(subtitles)

add_subtitles_to_video("results/video-cut.mp4", subtitles, "results/video-with-subtitles.mp4", "KGRedHands.ttf")

generate_music('music/ambient.mp3', 'results/ambient-shortened.mp3')

add_audio('results/video-with-subtitles.mp4', 'results/audio-shortened.mp3', 'results/ambient-shortened.mp3', 'results/video-with-audio.mp4')

add_final_touches("results/video-with-audio.mp4", "assets/subscribe_animation.mp4", "results/final_video.mp4", "KGRedHands.ttf")

