from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import numpy as np
from PIL import Image

def add_text_without_animation(text, fontsize, fontpath, start_time, end_time):
    start_time = float(start_time)
    end_time = float(end_time)
    txt_clip = (TextClip(text, fontsize=fontsize, font=fontpath, color='white')
                .set_position('center')
                .set_duration(end_time - start_time)
                .set_start(start_time))

    return txt_clip

def add_text_with_animation(text, fontsize, fontpath, start_time, end_time):
    start_time = float(start_time)
    end_time = float(end_time)

    def resize_text(get_frame, t):
        if start_time <= t <= end_time:
            progress = (t - start_time) / (end_time - start_time)
            factor = 1 + 0.2 * np.sin(3 * np.pi * progress)
            frame = get_frame(t)
            new_frame = np.array(Image.fromarray(frame).resize((int(frame.shape[1] * factor), int(frame.shape[0] * factor))))
            return new_frame
        else:
            return get_frame(t)

    txt_clip = (TextClip(text, fontsize=fontsize, font=fontpath, color='white')
                .set_position('center')
                .set_duration(end_time - start_time)
                .set_start(start_time))

    txt_clip = txt_clip.fl(resize_text)

    return txt_clip

def add_subtitles_to_video(input_video_path, subtitles, output_video_path, fontpath):
    video = VideoFileClip(input_video_path)
    texts = []

    for sub in subtitles:
        text_clip = add_text_with_animation(sub['text'], 88, fontpath, sub['start_time'], sub['end_time'])
        texts.append(text_clip)

    final = CompositeVideoClip([video] + texts, size=video.size)
    final.write_videofile(output_video_path, codec='libx264', audio_codec='aac')
