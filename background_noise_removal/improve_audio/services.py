import os
import glob
import noisereduce as nr
import librosa
from pysndfx import AudioEffectsChain
import numpy as np
import math
import python_speech_features
from scipy.io.wavfile import write, read
import traceback

from background_noise_removal import Base, FOLDER_PATH
from background_noise_removal import cloudinary_upload

logger = Base.logger_func()


class NoiseRemoverBase:

    @classmethod
    def convert_file_to_wav_file(cls, audio_file, wav_file_name):
        """
        This takes an audio file (either .aac or .m4a) and converts it to a .wav file

        Args:
            audio_file (audio): An audio file
            wav_file_name (.wav): The .wav file name
        """
        try:
            os.system(f"ffmpeg -y -i {audio_file} {wav_file_name}")
        except Exception as e:
            logger.exception(str(e))

    @classmethod
    def convert_audio_file(cls, input_file):
        """
        This takes an audio file and determines its extension, then
        converts the audio file to a .wav file

        Args:
            input_file (audio): The audio file we want to convert to a .wav file
        """
        file_name, file_extension = os.path.splitext(input_file)

        if file_extension == ".aac":
            cls.convert_file_to_wav_file(input_file, f"{file_name}.wav")

        elif file_extension == ".m4a":
            cls.convert_file_to_wav_file(input_file, f"{file_name}.wav")

        else:
            logger.info(f"new extension = {file_extension}")

    @classmethod
    def read_file(cls, file_name):
        """
        This reads an audio file to get the data and the sound rate

        Args:
            file_name (str): The name of the audio file

        Returns:
            y : the data of the audio file
            sr (int): the sound rate of the audio file
        """

        y, sr = librosa.load(file_name)

        return y, sr

    @classmethod
    def remove_files(cls, folder_path, wav_file):

        files = glob.glob(f'{folder_path}/*.wav')
        for f in files:
            os.remove(f)

        os.remove(f"{os.getcwd()}/{wav_file}")


def stationary_noise_reduction(input_file, output_file):

    rate, data = read(input_file)

    if len(list(data.shape)) == 2:
        try:
            data = data[:, 0]
            reduced_noise = nr.reduce_noise(y=data, sr=rate)
            write(f"{FOLDER_PATH}/{output_file}.wav", rate, reduced_noise)

            file_path = f"{FOLDER_PATH}/{output_file}.wav"
            link = cloudinary_upload.upload_file(file_path=file_path, file_name=f"{output_file}", folder="noise_reduction")
            logger.info("Stationary Noise Reduction completed")

            return link
        except Exception as e:
            logger.exception(str(e))
    else:
        try:
            reduced_noise = nr.reduce_noise(y=data, sr=rate)
            write(f"{FOLDER_PATH}/{output_file}.wav", rate, reduced_noise)

            file_path = f"{FOLDER_PATH}/{output_file}.wav"
            link = cloudinary_upload.upload_file(file_path=file_path, file_name=f"{output_file}", folder="noise_reduction")
            logger.info("Stationary Noise Reduction completed")

            return link
        except Exception as e:
            logger.exception(str(e))


def reduce_noise_power(y, sr):

    cent = librosa.feature.spectral_centroid(y=y, sr=sr)

    threshold_h = round(np.median(cent))*1.5
    threshold_l = round(np.median(cent))*0.1

    less_noise = AudioEffectsChain().lowshelf(gain=-30.0,
                                              frequency=threshold_l,
                                              slope=0.8).highshelf(gain=-12.0,
                                                                   frequency=threshold_h,
                                                                   slope=0.5)

    y_clean = less_noise(y)

    write(f"{FOLDER_PATH}/reduce_noise_power.wav", sr, y_clean)

    file_path = f"{FOLDER_PATH}/reduce_noise_power.wav"

    link = cloudinary_upload.upload_file(file_path=file_path,
                                         file_name="reduce_noise_power",
                                         folder="noise_reduction")
    logger.info("Noise Power Reduction completed")

    return link


def reduce_noise_centroid_s(y, sr):

    cent = librosa.feature.spectral_centroid(y=y, sr=sr)

    threshold_h = np.max(cent)
    threshold_l = np.min(cent)

    less_noise = AudioEffectsChain().lowshelf(gain=-12.0,
                                              frequency=threshold_l,
                                              slope=0.5).highshelf(gain=-12.0,
                                                                   frequency=threshold_h,
                                                                   slope=0.5).limiter(
                                                                       gain=6.0)

    y_clean = less_noise(y)

    write(f"{FOLDER_PATH}/reduce_noise_centroid_s.wav", sr, y_clean)

    file_path = f"{FOLDER_PATH}/reduce_noise_centroid_s.wav"
    link = cloudinary_upload.upload_file(file_path=file_path,
                                         file_name="reduce_noise_centroid_s",
                                         folder="noise_reduction")
    logger.info("Noise Centroid S Reduction completed")

    return link


def reduce_noise_centroid_mb(y, sr):

    cent = librosa.feature.spectral_centroid(y=y, sr=sr)

    threshold_h = np.max(cent)
    threshold_l = np.min(cent)

    less_noise = AudioEffectsChain().lowshelf(gain=-30.0,
                                              frequency=threshold_l,
                                              slope=0.5).highshelf(gain=-30.0,
                                                                   frequency=threshold_h,
                                                                   slope=0.5).limiter(
                                                                       gain=10.0)
    y_cleaned = less_noise(y)

    cent_cleaned = librosa.feature.spectral_centroid(y=y_cleaned, sr=sr)
    columns, rows = cent_cleaned.shape
    boost_h = math.floor(rows/3*2)
    # boost_l = math.floor(rows/6)

    boost_bass = AudioEffectsChain().lowshelf(gain=16.0, frequency=boost_h, slope=0.5)
    y_clean = boost_bass(y_cleaned)

    write(f"{FOLDER_PATH}/reduce_noise_centroid_mb.wav", sr, y_clean)

    file_path = f"{FOLDER_PATH}/reduce_noise_centroid_mb.wav"
    link = cloudinary_upload.upload_file(file_path=file_path,
                                         file_name="reduce_noise_centroid_mb",
                                         folder="noise_reduction")
    logger.info("Noise Centroid MB Reduction completed")

    return link


def reduce_noise_mfcc_down(y, sr):

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

    # max_hz = max(hz)
    min_hz = min(hz)

    speech_booster = AudioEffectsChain().highshelf(frequency=min_hz*(-1)*1.2, gain=-12.0, slope=0.6).limiter(gain=8.0)
    y_clean = speech_booster(y)

    write(f"{FOLDER_PATH}/reduce_noise_mfcc_down.wav", sr, y_clean)

    file_path = f"{FOLDER_PATH}/reduce_noise_mfcc_down.wav"
    link = cloudinary_upload.upload_file(file_path=file_path,
                                         file_name="reduce_noise_mfcc_down",
                                         folder="noise_reduction")
    logger.info("Noise mfcc down Reduction completed")

    return link


def reduce_noise_mfcc_up(y, sr):

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

    # max_hz = max(hz)
    min_hz = min(hz)

    speech_booster = AudioEffectsChain().lowshelf(frequency=min_hz*(-1), gain=12.0, slope=0.5)
    y_clean = speech_booster(y)

    write(f"{FOLDER_PATH}/reduce_noise_mfcc_up.wav", sr, y_clean)

    file_path = f"{FOLDER_PATH}/reduce_noise_mfcc_up.wav"
    link = cloudinary_upload.upload_file(file_path=file_path,
                                         file_name="reduce_noise_mfcc_up",
                                         folder="noise_reduction")
    logger.info("Noise mfcc up Reduction completed")

    return link


def start_noise_removing_script(input_file):

    try:
        file_name, file_extension = os.path.splitext(input_file)
        output_file = "remove_noise_from_audio"

        nrb = NoiseRemoverBase()
        nrb.convert_audio_file(input_file)

        wav_file = f"{file_name}.wav"
        y, sr = nrb.read_file(wav_file)

        stationary_noise_reduction_url = stationary_noise_reduction(wav_file, output_file)

        reduce_noise_power_url = reduce_noise_power(y, sr)

        reduce_noise_centroid_s_url = reduce_noise_centroid_s(y, sr)

        reduce_noise_centroid_mb_url = reduce_noise_centroid_mb(y, sr)

        reduce_noise_mfcc_down_url = reduce_noise_mfcc_down(y, sr)

        reduce_noise_mfcc_up_url = reduce_noise_mfcc_up(y, sr)

        result = {
            "stationary_noise_reduction_method": stationary_noise_reduction_url,
            "reduce_noise_power_method": reduce_noise_power_url,
            "reduce_noise_centroid_s_method": reduce_noise_centroid_s_url,
            "reduce_noise_centroid_mb_method": reduce_noise_centroid_mb_url,
            "reduce_noise_mfcc_down_method": reduce_noise_mfcc_down_url,
            "reduce_noise_mfcc_up_method": reduce_noise_mfcc_up_url,
            }

        nrb.remove_files(FOLDER_PATH, wav_file)

        return {
                "status": True,
                "message": "successful",
                "data": result
                }, 200

    except Exception as reason:
        logger.exception(f"Noice Reduction failed: {reason}")
        stacktrace = traceback.format_exc()
        return {
            "status": False,
            "message": stacktrace,
            "data": {}
            }, 400
