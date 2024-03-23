from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

def add_final_touches(video_path, animation_path, output_path, font_path):
    # Načtení hlavního videa a animace
    video = VideoFileClip(video_path)
    animation = VideoFileClip(animation_path).resize(width=video.w)

    # Umístění animace na vrch videa
    animation_start = video.duration - 5
    animation = animation.set_start(animation_start).set_position(('center', 'top'))

    # Přidání textu "For Part 2" na spodní část videa
    text_clip = TextClip("For Part 2", fontsize=100, font=font_path, color='white')
    text_clip = text_clip.set_position(('center', 'bottom')).set_duration(5).set_start(animation_start)

    # Vytvoření finálního videa s přidanými prvky
    final_video = CompositeVideoClip([video, animation, text_clip], size=video.size)
    final_video.write_videofile(output_path, codec='libx264', audio_codec='aac')
