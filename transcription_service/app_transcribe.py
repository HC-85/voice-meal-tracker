from faster_whisper import WhisperModel
from os import listdir
from os.path import join as path_join, exists


def load_faster_whisper(model_size = "tiny.en"):
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    return model


def transcribe_audio(model, audio_file):
    segments, _ = model.transcribe(audio_file, beam_size=5)
    return [segment.text for segment in segments]


def transcribe_file(model, file_path, output_folder = "transcriptions"):
    segments, _ = model.transcribe(file_path, beam_size=5)
    transcription = [segment.text for segment in segments]
    filename = file_path.split('/')[-1].split('.')[0]

    if not exists(file_path := path_join(output_folder, f"{filename}.txt")):
        with open(file_path, 'w') as f:
            f.write(transcription[0])

        return f'File saved: {filename}'

    else:
        return f"File {filename} found in cache. Skipping download."


def transcribe_all(model, input_folder="vn_cache"):
    audio_files = listdir(input_folder)
    logs = []
    for audio_file in audio_files:
        log = transcribe_file(model, path_join(input_folder, audio_file))
        logs.append(log)
    return logs