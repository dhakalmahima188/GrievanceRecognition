import torch
import torchaudio
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import soundfile as sf 
import pyloudnorm as pyln 
import numpy as np
from pydub import AudioSegment
from pydub.silence import split_on_silence

# The Hugging Face model path
model_path = "Ashwini1412/wav2vec2-nepali-final"
processor_path = model_path  # The processor is typically stored in the same location as the model

def loadModelInitial():
    device = "cpu"  # Change to "cuda" if using a GPU
    model = Wav2Vec2ForCTC.from_pretrained(model_path).to(device)
    processor = Wav2Vec2Processor.from_pretrained(processor_path) 
    return model, processor, device

model, processor, device = loadModelInitial()

torch.cuda.empty_cache()

def segmentLargeArray(inputTensor, chunksize=200000):
    list_of_segments = []
    tensor_length = inputTensor.shape[1]
    for i in range(0, tensor_length + 1, chunksize):
        list_of_segments.append(inputTensor[:, i:i + chunksize])
    return list_of_segments

def clean_wav_file(file_path, cleaned_file_path):
    # Load the audio file
    sound = AudioSegment.from_wav(file_path)
    
    # Split on silence will create chunks of sound separated by silence
    chunks = split_on_silence(sound, 
        min_silence_len=500,  # Must be silent for at least half a second
        silence_thresh=-16     # Consider it silent if quieter than -16 dBFS
    )
    
    # Process each chunk with your parameters
    processed_chunks = [chunk for chunk in chunks]

    # Now recombine the processed chunks
    cleaned_sound = sum(processed_chunks, AudioSegment.silent(duration=0))

    # Export the cleaned sound
    cleaned_sound.export(cleaned_file_path, format="wav")
    
    return cleaned_sound

def adjust_volume(data, sr=16000, norm="peak"):
    # Peak normalization of all audio to -1dB
    meter = pyln.Meter(sr)  # create BS.1770 Meter
    loudness = meter.integrated_loudness(np.transpose(data)) 
    if norm == "peak":
        peak_normalized_audio = pyln.normalize.peak(data, -1.0)
    elif norm == "fixed":
        # Loudness normalization to a fixed level irrespective of original file's volume
        peak_normalized_audio = pyln.normalize.loudness(data, loudness, 0)
    else:
        peak_normalized_audio = data
    loudness = meter.integrated_loudness(np.transpose(peak_normalized_audio)) 
    return peak_normalized_audio

def predict_from_speech(file, do_segment=True):
    # Load audio file
    speech_array, sampling_rate = torchaudio.load(file)
    speech_array = speech_array.numpy()
    speech_array = adjust_volume(speech_array, sampling_rate, norm="fixed")
    speech_array = torch.from_numpy(speech_array)
    
    # Resample to 16kHz (required by the model)
    resampler = torchaudio.transforms.Resample(sampling_rate, 16000)    
    resampled_array = resampler(speech_array).squeeze()
   
    if len(resampled_array.shape) == 1:
        resampled_array = resampled_array.reshape([1, resampled_array.shape[0]]) 

    if resampled_array.shape[1] >= 200000 and do_segment:
        list_of_segments = segmentLargeArray(resampled_array)
        output = ''
        for segment in list_of_segments:
            if segment.size()[1] > 0:
                logits = model(segment.to(device)).logits
                pred_ids = torch.argmax(logits, dim=-1)[0]
                output += processor.decode(pred_ids)
            else:
                output += ''
    else:
        logits = model(resampled_array.to(device)).logits
        pred_ids = torch.argmax(logits, dim=-1)[0]
        output = processor.decode(pred_ids)
    
    return output
        
if __name__ == "__main__":
    # Test the function with a file
    result = predict_from_speech("test.flac") 
    print(result)
