import noisereduce as nr
from scipy.io import wavfile
import os


def convert_aac_file_to_wav_file(aac_file, wav_file):
    try:
        os.system(f"ffmpeg -y -i {aac_file} {wav_file}")
    except Exception as e:
        print(e)


def convert_m4a_file_to_wav_file(m4a_file, wav_file):
    try:
        os.system(f"ffmpeg -y -i {m4a_file} {wav_file}")
    except Exception as e:
        print(e)



def remove_noise_from_audio(input_file, output_file):
    """
        This function takes an input_file of the audio (either as a .aac or a .wav)
        and removes the background noise then saves it to the outputfile path (as a .wav)
    """


    file_name, file_extension = os.path.splitext(input_file)

    if file_extension == ".aac":
        convert_aac_file_to_wav_file(input_file, f"{file_name}.wav")
        remove_noise_from_audio(f"{file_name}.wav", output_file)

    elif file_extension == ".m4a":
        convert_m4a_file_to_wav_file(input_file, f"{file_name}.wav")
        remove_noise_from_audio(f"{file_name}.wav", output_file)



    else:

        # load data
        rate, data = wavfile.read(input_file)

        if len(list(data.shape)) == 2:
            try:
                data = data[:,0]
                reduced_noise = nr.reduce_noise(y=data, sr=rate)
                wavfile.write(output_file, rate, reduced_noise)
                print("downloaded")
            except Exception as e:
                print(e)

        else:
            try:
                reduced_noise = nr.reduce_noise(y=data, sr=rate)
                wavfile.write(output_file, rate, reduced_noise)
                print("downloaded")
            except Exception as e:
                print(e)



input_file = "test.m4a"
output_file = "new_sound.wav"
remove_noise_from_audio(input_file, output_file)

#####################################################################################################################################


import librosa
from pysndfx import AudioEffectsChain
import numpy as np
import math
import python_speech_features
import scipy as sp
from scipy import signal
from scipy.io.wavfile import write
import noisereduce as nr

file_name = "test.wav"




def read_file(file_name):
#     sample_file = file_name
#     sample_directory = '00_samples/'
#     sample_path = sample_directory + sample_file

    # generating audio time series and a sampling rate (int)
    y, sr = librosa.load(file_name)

    return y, sr


def reduce_noise_power(y, sr):

    cent = librosa.feature.spectral_centroid(y=y, sr=sr)


    threshold_h = round(np.median(cent))*1.5
    threshold_l = round(np.median(cent))*0.1
    
    print(threshold_h, threshold_l)

    less_noise = AudioEffectsChain().lowshelf(gain=-30.0, frequency=threshold_l, slope=0.8).highshelf(gain=-12.0, frequency=threshold_h, slope=0.5)#.limiter(gain=6.0)
    
    y_clean = less_noise(y)

    return y_clean
	


def reduce_noise_centroid_s(y, sr):

    cent = librosa.feature.spectral_centroid(y=y, sr=sr)

    threshold_h = np.max(cent)
    threshold_l = np.min(cent)

    less_noise = AudioEffectsChain().lowshelf(gain=-12.0, frequency=threshold_l, slope=0.5).highshelf(gain=-12.0, frequency=threshold_h, slope=0.5).limiter(gain=6.0)

    y_cleaned = less_noise(y)

    return y_cleaned
    
    
def reduce_noise_centroid_mb(y, sr):

    cent = librosa.feature.spectral_centroid(y=y, sr=sr)

    threshold_h = np.max(cent)
    threshold_l = np.min(cent)

    less_noise = AudioEffectsChain().lowshelf(gain=-30.0, frequency=threshold_l, slope=0.5).highshelf(gain=-30.0, frequency=threshold_h, slope=0.5).limiter(gain=10.0)
    # less_noise = AudioEffectsChain().lowpass(frequency=threshold_h).highpass(frequency=threshold_l)
    y_cleaned = less_noise(y)


    cent_cleaned = librosa.feature.spectral_centroid(y=y_cleaned, sr=sr)
    columns, rows = cent_cleaned.shape
    boost_h = math.floor(rows/3*2)
    boost_l = math.floor(rows/6)
    boost = math.floor(rows/3)

    # boost_bass = AudioEffectsChain().lowshelf(gain=20.0, frequency=boost, slope=0.8)
    boost_bass = AudioEffectsChain().lowshelf(gain=16.0, frequency=boost_h, slope=0.5)#.lowshelf(gain=-20.0, frequency=boost_l, slope=0.8)
    y_clean_boosted = boost_bass(y_cleaned)

    return y_clean_boosted


def reduce_noise_mfcc_down(y, sr):

    hop_length = 512

    ## librosa
    # mfcc = librosa.feature.mfcc(y=y, sr=sr, hop_length=hop_length, n_mfcc=13)
    # librosa.mel_to_hz(mfcc)

    ## mfcc
    mfcc = python_speech_features.base.mfcc(y)
    mfcc = python_speech_features.base.logfbank(y)
    mfcc = python_speech_features.base.lifter(mfcc)

    sum_of_squares = []
    index = -1
    for r in mfcc:
        sum_of_squares.append(0)
        index = index + 1
        for n in r:
            sum_of_squares[index] = sum_of_squares[index] + n**2

    strongest_frame = sum_of_squares.index(max(sum_of_squares))
    hz = python_speech_features.base.mel2hz(mfcc[strongest_frame])

    max_hz = max(hz)
    min_hz = min(hz)

    speech_booster = AudioEffectsChain().highshelf(frequency=min_hz*(-1)*1.2, gain=-12.0, slope=0.6).limiter(gain=8.0)
    y_speach_boosted = speech_booster(y)

    return (y_speach_boosted)
    

def reduce_noise_mfcc_up(y, sr):

    hop_length = 512

    ## librosa
    # mfcc = librosa.feature.mfcc(y=y, sr=sr, hop_length=hop_length, n_mfcc=13)
    # librosa.mel_to_hz(mfcc)

    ## mfcc
    mfcc = python_speech_features.base.mfcc(y)
    mfcc = python_speech_features.base.logfbank(y)
    mfcc = python_speech_features.base.lifter(mfcc)

    sum_of_squares = []
    index = -1
    for r in mfcc:
        sum_of_squares.append(0)
        index = index + 1
        for n in r:
            sum_of_squares[index] = sum_of_squares[index] + n**2

    strongest_frame = sum_of_squares.index(max(sum_of_squares))
    hz = python_speech_features.base.mel2hz(mfcc[strongest_frame])

    max_hz = max(hz)
    min_hz = min(hz)

    speech_booster = AudioEffectsChain().lowshelf(frequency=min_hz*(-1), gain=12.0, slope=0.5)#.highshelf(frequency=min_hz*(-1)*1.2, gain=-12.0, slope=0.5)#.limiter(gain=8.0)
    y_speach_boosted = speech_booster(y)

    return (y_speach_boosted)
	
	
y, sr = read_file(file_name)



#cleaned = reduce_noise_power(y, sr)
#cleaned = reduce_noise_centroid_s(y, sr)
#cleaned = reduce_noise_centroid_mb(y, sr)
#cleaned = reduce_noise_mfcc_down(y, sr)

cleaned = reduce_noise_mfcc_up(y, sr)

print(cleaned)
write("trying.wav", sr, cleaned)

file_name = "trying.wav"
y, sr = read_file(file_name)


reduced_noise = nr.reduce_noise(y=y, sr=sr)
write("trying4.wav", sr, reduced_noise)
print("downloaded")
