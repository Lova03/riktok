from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip

def add_audio(video_path, main_audio_path, background_music_path, output_video_path, background_music_volume=0.5):
    with VideoFileClip(video_path) as video:
        main_audio = AudioFileClip(main_audio_path).set_duration(video.duration)
        background_music = AudioFileClip(background_music_path).volumex(background_music_volume).set_duration(video.duration)

        final_audio = CompositeAudioClip([main_audio, background_music])
        
        final_video = video.set_audio(final_audio)
        final_video.write_videofile(output_video_path, codec='libx264', audio_codec='aac')