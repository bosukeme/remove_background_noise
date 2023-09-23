# remove_background_noise

## Table of Contents
h
- [Introduction](#introduction)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the web application](#running-the-web-application)
  - [Running tests](#running-test)
  - [Running Docker](#run-docker)
- [Rest API Documentation](#api-documentation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)


## Introduction

Noise reduction in audio processing involves the removal or reduction of unwanted background noise or interference from an audio signal. You can achieve noise reduction in Python using various libraries and techniques.

The remove_background_noise is a <a href="https://flask.palletsprojects.com/en/2.3.x/">Flask</a> application that reduces noise from an input recording file and returns several reduced noise audio files (wav) from several noise reducing methods

- Noisereduce is a noise reduction algorithm in python that reduces noise in a method called "spectral gating" which is a form of Noise Gate. It works by computing a spectrogram of a signal (and optionally a noise signal) and estimating a noise threshold (or gate) for each frequency band of that signal/noise. That threshold is used to compute a mask, which gates noise below the frequency-varying threshold.

- In audio processing with the Librosa library in Python, you can reduce noise using spectral centroid-based thresholding. This calculates high and low spectral centroid thresholds, and then applies a noise reduction filter using the pysndfx library based on those thresholds. The result is a denoised version of the input audio, which is saved as a new WAV file. 

- To perform noise reduction using MFCC (Mel-frequency cepstral coefficients) in Python, you can use the python_speech_features library to extract MFCC features from the audio signal and then apply thresholding to reduce noise.

Sources:
- <p>  https://pypi.org/project/noisereduce/ </p>
- <p> https://pypi.org/project/librosa/ </p>
- <p>  https://python-speech-features.readthedocs.io/en/latest/ </p>


<br>
Technologies used

- Backend: Python & Flask
- REST API documentation: Swagger UI
- Testing: Pytest
- CI: Github Actions
- Containerization: Docker
- File Storage: Cloudinary


## Getting Started

To run this web application on your local machine, follow the steps below:

### Prerequisites

Before getting started, ensure that you have the following software installed on your machine:

- Python: Download and install Python from the official website: https://www.python.org/downloads/
- GIT: Download and install GIT from the official website: https://git-scm.com/downloads

### Installation

Step-by-step guide on how to install the project and its dependencies.


1. Clone the repository to your local machine using Git: <br>
HTTPS

```bash
git clone https://github.com/bosukeme/remove_background_noise.git
```

SSH
```bash
git clone git@github.com:bosukeme/remove_background_noise.git
```

<br>

2. Navigate to the project directory

```bash
cd remove_background_noice
```

Before you start the application, you need to set up an environment variables. Here's how you can do it:

```bash
cloud_name=
api_key=
api_secret=
```

Create a file called `.env` file at the root folder of the project with the environmental variables above.

You can create your cloudinary key and secret by signing up on  https://cloudinary.com/ <br>


3. Install the project dependencies contained inside the requirements.txt file using PIP(Package Manager):

```bash
pip install -r requirements.txt
```

### Running the web application

Once you have installed the dependencies, you can start the web application using

<b>Linux</b>, <b> Windows "WSL" </b>, <b> MAC </b> 
```bash
gunicorn -c "gunicorn_config.py" "wsgi:app"
```

<b> Windows "CMD", "POWERSHELL" </b> 
```bash
python run.py
```

### Running Tests

Once you have installed the dependencies, and your flask app is running, you can run test within the directory

- run pytest

```bash
pytest
```

### Run docker

navigate to the root directory

```bash
docker-compose up --build
```

To stop the containers

```bash
docker-compose stop
```

## API documentation

Access API documentation via Swagger UI using the link below after starting up the application

```bash
http://localhost:8001/api/v1.0/remove-noise/doc/
```

## Usage
- Using the API: Refer to the Swagger API documentation at http://localhost:8001/api/v1.0/remove-noise/doc/ for a detailed list of available endpoints and how to interact with them.

- Troubleshooting
  If you encounter any issues or have questions, please feel free to reach out to us by creating an issue on our GitHub repository: https://github.com/bosukeme/remove_background_noise.git.


## License

This project is licensed under the MIT License.

## Authors

Contributors names and contact info

Ukeme Wilson