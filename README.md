# English Listening Material Creation Script

This script generates audio files (.mp3) for listening practice from English text included in a text file. It uses the same high-quality speech synthesis engine as Microsoft Edge's read-aloud feature.

## Requirements

- Python 3
- `edge-tts` library

## Setup

1.  **Install the library:**
    ```shell
    pip install edge-tts
    ```

2.  **Prepare the English script:**
    Paste the English text you want to convert into speech into `script.txt` located in the project's root directory.

## Usage

The audio files will be generated in the `output` directory.

### Basic Usage

Run the following command to convert the content of `script.txt` into an audio file with the default settings (American English female voice, normal speed):

```bash
python create_audio.py
```

### Options

#### Change the voice type (`--voice` / `-v`)

First, check the list of available voices:

```bash
python create_audio.py --list-voices
```

Choose a voice from the list (e.g., `en-GB-SoniaNeural`) and specify it as follows:

```bash
python create_audio.py --voice en-GB-SoniaNeural
```

#### Adjust the speaking rate (`--rate` / `-r`)

Adjust the speed as a percentage relative to the default speed.

- **10% slower:**
  ```bash
  python create_audio.py --rate -10%
  ```
- **20% faster:**
  ```bash
  python create_audio.py --rate +20%
  ```

#### Change both voice and speed

```bash
python create_audio.py -v en-GB-RyanNeural -r -5%
```

#### Specify a different input file (`--file` / `-f`)

If you want to use a file other than `script.txt` (e.g., `article.txt`), specify it as follows:

```bash
python create_audio.py --file article.txt
```