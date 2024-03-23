import whisper_timestamped

def transcribe(audio_path):
    model = whisper_timestamped.load_model("base")
    result = whisper_timestamped.transcribe(model, audio_path, verbose=False)

    words_with_timestamps = []
    for segment in result["segments"]:
        for word in segment["words"]:
            words_with_timestamps.append({
                "start_time": format(word["start"], '.2f'),
                "end_time": format(word["end"], '.2f'),
                "text": word["text"]
            })

    return words_with_timestamps

def transcribe_audio(audio_path):
    print('Starting audio transcribing...')
    try:
        # Spuštění transkripční funkce
        words_with_timestamps = transcribe(audio_path)
        print('Transcription completed.')
        return words_with_timestamps
    except Exception as e:
        print('Error during transcription:', str(e))
        return []