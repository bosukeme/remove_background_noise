import noisereduce as nr
from scipy.io import wavfile
import os

BASE_DIR = os.getcwd()

def convert_aac_file_to_wav_file(aac_file, wav_file):
    try:
        os.system(f"ffmpeg -y -i {aac_file} {wav_file}")
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



input_file = "wall_rec.wav"
output_file = "vscodes.wav"
remove_noise_from_audio(input_file, output_file)

