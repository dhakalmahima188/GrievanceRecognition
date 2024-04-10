import torch
import torchaudio
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import soundfile as sf 
import pyloudnorm as pyln 
import numpy as np
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import os
from django.conf import settings
from pydub import AudioSegment
from pydub.silence import split_on_silence

# import tokenizer

model_path=os.path.join(settings.BASE_DIR,'backend/best_wav2vec_model')
processor_path=os.path.join(settings.BASE_DIR,'backend/best_wav2vec_processor')


def loadModelInitial():
    device = "cpu"
    model = Wav2Vec2ForCTC.from_pretrained(model_path).to(device)
    processor = Wav2Vec2Processor.from_pretrained(processor_path)
    return model, processor, device

model, processor, device = loadModelInitial()

torch.cuda.empty_cache()

def segmentLargeArray(inputTensor,chunksize=200000):
    # print(inputTensor)
    list_of_segments = []
    tensor_length = inputTensor.shape[1]
    for i in range(0,tensor_length+1,chunksize):
        list_of_segments.append(inputTensor[:,i:i+chunksize])
    return list_of_segments 



def clean_wav_file(file_path, cleaned_file_path):
    # Load the audio file
    sound = AudioSegment.from_wav(file_path)
    
    # Split on silence will create chunks of sound separated by silence
    chunks = split_on_silence(sound, 
        # Must be silent for at least half a second
        min_silence_len=500,
        # Consider it silent if quieter than -16 dBFS
        silence_thresh=-16
    )
    
    # Process each chunk with your parameters
    processed_chunks = [chunk for chunk in chunks]

    # Now recombine the processed chunks
    cleaned_sound = sum(processed_chunks, AudioSegment.silent(duration=0))

    # Export the cleaned sound
    cleaned_sound.export(cleaned_file_path, format="wav")
    
    return cleaned_sound

# Use the function



def adjust_volume(data,sr=16000,norm="peak"):
    # Peak normalization of all audio to -1dB
    meter = pyln.Meter(sr) #create BS.1770 Meter
    # print(data)
    # print(np.transpose(data).shape)
    loudness = meter.integrated_loudness(np.transpose(data)) 
    # print(f'Before: {loudness} dB')
    if norm == "peak":
        # This is peak normalization which depends on the original volume of audio file
        peak_normalized_audio = pyln.normalize.peak(data,-1.0)
    elif norm=="fixed":
        # Actually this is loudness normalization to a fixed level irrespective of volume in original file
        peak_normalized_audio = pyln.normalize.loudness(data, loudness, 0)
    else:
        peak_normalized_audio = data
    loudness = meter.integrated_loudness(np.transpose(peak_normalized_audio)) 
    # print(f'After peak normalization: {loudness} dB')
    return peak_normalized_audio

def predict_from_speech(file,do_segment=True):
    speech_array, sampling_rate = torchaudio.load(file)  
    speech_array = speech_array.numpy()
    speech_array = adjust_volume(speech_array,sampling_rate,norm="fixed") 
    speech_array = torch.from_numpy(speech_array) 
    resampler = torchaudio.transforms.Resample(sampling_rate, 16000)    
    resampled_array = resampler(speech_array).squeeze()
   
    if len(resampled_array.shape) == 1:
        resampled_array = resampled_array.reshape([1,resampled_array.shape[0]])
    # print(resampled_array.shape[1])
    if resampled_array.shape[1] >= 200000 and do_segment == True:
        # print('The input file is longer than 10 seconds')
        list_of_segments = segmentLargeArray(resampled_array)
        # print(list_of_segments)
        output = ''
        for segment in list_of_segments:
            if segment.size()[1] > 0:
                logits = model(segment.to(device)).logits
                # print(logits)
                pred_ids = torch.argmax(logits,dim=-1)[0]
                output += processor.decode(pred_ids)
            else:
                output += ''
    else:
        # print('The input file is less than 10 seconds')
        logits = model(resampled_array.to(device)).logits
        # print(logits)
        pred_ids = torch.argmax(logits, dim = -1)[0]
        # print("Prediction:")
        output = processor.decode(pred_ids)
        # print(output)
    
    return output
        
        
        
if __name__ == "__main__":
    predict_from_speech("test.flac")        