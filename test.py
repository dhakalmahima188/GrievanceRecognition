from pydub import AudioSegment
from pydub.silence import split_on_silence

# Load FLAC audio file
audio = AudioSegment.from_file("mayor.flac", format="flac")

# Normalize audio
normalized_audio = audio.normalize()

# Split on silence
chunks = split_on_silence(normalized_audio, silence_thresh=-40)  # Adjust silence threshold as needed

# Export individual chunks
for i, chunk in enumerate(chunks):
    chunk.export(f"output_chunk_{i}.flac", format="flac")
