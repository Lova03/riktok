import os
import random
from moviepy.editor import VideoFileClip, ColorClip, CompositeVideoClip

def get_random_video_file(directory):
    """Najde náhodné video v zadané složce."""
    video_files = [f for f in os.listdir(directory) if f.endswith('.mp4')]
    if not video_files:
        return None
    return os.path.join(directory, random.choice(video_files))

def cut_video(video_path, output_directory):
    """Vystřihne náhodnou minutu z videa a převede ji do formátu TikTok s mírně černým pozadím."""
    with VideoFileClip(video_path) as video:
        duration = video.duration
        start_time = random.uniform(0, max(0, duration - 60))
        end_time = min(start_time + 60, duration)

        # Oříznutí a změna velikosti videa
        cropped_video = video.subclip(start_time, end_time)
        cropped_video = cropped_video.crop(x_center=cropped_video.w / 2, y_center=cropped_video.h / 2, width=min(cropped_video.w, cropped_video.h * 9 / 16), height=min(cropped_video.h, cropped_video.w * 16 / 9))
        cropped_video = cropped_video.resize(newsize=(1080, 1920))

        # Vytvoření černého pozadí s průhledností
        black_background = ColorClip(size=cropped_video.size, color=(0, 0, 0), duration=cropped_video.duration, ismask=False).set_opacity(0.3)

        # Překrytí černého pozadí s videem
        video_with_background = CompositeVideoClip([cropped_video, black_background], size=cropped_video.size)

        output_path = os.path.join(output_directory, os.path.basename(video_path).replace('.mp4', '-cut.mp4'))
        video_with_background.write_videofile(output_path, codec='libx264', audio_codec='aac')

        return output_path
