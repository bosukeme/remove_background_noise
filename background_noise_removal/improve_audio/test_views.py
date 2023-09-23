import os
import json
from background_noise_removal.tests.conftest import AppTestCase
from background_noise_removal import BASE_DIR



app = AppTestCase().create_app()

file_name = BASE_DIR + "/test.m4a"
BASE_URL = "http://localhost:8001/api/v1.0/remove-noise"


def test_noise_removal_ok():

    with app.test_client() as cli:
        with open(file_name, 'rb') as f:    
            resp = cli.post(
                f"{BASE_URL}/improve_audio",
                data={
                    'file': (f, 'test.m4a'),
                    "type": 'application/octet-stream'},
                )

            result = json.loads(resp.data.decode("utf-8"))
            print("results", result)
            assert resp.status_code == 200
            assert result.get("status") is True
            assert result.get("message") == "successful"
            
            assert result.get("data").get("stationary_noise_reduction_method") is not None
            assert result.get("data").get("reduce_noise_power_method") is not None
            assert result.get("data").get("reduce_noise_centroid_s_method") is not None
            assert result.get("data").get("reduce_noise_centroid_mb_method") is not None
            assert result.get("data").get("reduce_noise_mfcc_down_method") is not None
            assert result.get("data").get("reduce_noise_mfcc_up_method") is not None
            
            assert result.get("data").get("stationary_noise_reduction_method") ==  "https://res.cloudinary.com/bosukeme/video/upload/v1695489821/noise_reduction/stationary_noise_reduction.wav"
            assert result.get("data").get("reduce_noise_power_method") == "https://res.cloudinary.com/bosukeme/video/upload/v1695489040/noise_reduction/reduce_noise_power.wav"
            assert result.get("data").get("reduce_noise_centroid_s_method") == "https://res.cloudinary.com/bosukeme/video/upload/v1695489042/noise_reduction/reduce_noise_centroid_s.wav"
            assert result.get("data").get("reduce_noise_centroid_mb_method") == "https://res.cloudinary.com/bosukeme/video/upload/v1695489045/noise_reduction/reduce_noise_centroid_mb.wav"
            assert result.get("data").get("reduce_noise_mfcc_down_method") == "https://res.cloudinary.com/bosukeme/video/upload/v1695489048/noise_reduction/reduce_noise_mfcc_down.wav"
            assert result.get("data").get("reduce_noise_mfcc_up_method") == "https://res.cloudinary.com/bosukeme/video/upload/v1695489051/noise_reduction/reduce_noise_mfcc_up.wav"


def test_noise_removal_wrong_file():

    with app.test_client() as cli:
        with open(file_name, 'rb') as f:    
            resp = cli.post(
                f"{BASE_URL}/improve_audio",
                data={
                    'file': (f, 'wrong.m4a'),
                    "type": 'application/octet-stream'},
                )

            result = json.loads(resp.data.decode("utf-8"))

            assert resp.status_code == 400
            assert result.get("status") is False
            assert result.get("message") != "successful"
            
            assert result.get("data").get("stationary_noise_reduction_method") is  None
            assert result.get("data").get("reduce_noise_power_method") is None
            assert result.get("data").get("reduce_noise_centroid_s_method") is  None
            assert result.get("data").get("reduce_noise_centroid_mb_method") is  None
            assert result.get("data").get("reduce_noise_mfcc_down_method") is  None
            assert result.get("data").get("reduce_noise_mfcc_up_method") is  None
            
            assert result.get("data").get("stationary_noise_reduction_method") !=  "https://res.cloudinary.com/bosukeme/video/upload/v1695489821/noise_reduction/stationary_noise_reduction.wav"
            assert result.get("data").get("reduce_noise_power_method") != "https://res.cloudinary.com/bosukeme/video/upload/v1695489040/noise_reduction/reduce_noise_power.wav"
            assert result.get("data").get("reduce_noise_centroid_s_method") != "https://res.cloudinary.com/bosukeme/video/upload/v1695489042/noise_reduction/reduce_noise_centroid_s.wav"
            assert result.get("data").get("reduce_noise_centroid_mb_method") != "https://res.cloudinary.com/bosukeme/video/upload/v1695489045/noise_reduction/reduce_noise_centroid_mb.wav"
            assert result.get("data").get("reduce_noise_mfcc_down_method") != "https://res.cloudinary.com/bosukeme/video/upload/v1695489048/noise_reduction/reduce_noise_mfcc_down.wav"
            assert result.get("data").get("reduce_noise_mfcc_up_method") != "https://res.cloudinary.com/bosukeme/video/upload/v1695489051/noise_reduction/reduce_noise_mfcc_up.wav"
