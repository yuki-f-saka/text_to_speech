

import asyncio
import edge_tts
import argparse
import os
import re
from datetime import datetime

# --- Setting ---
DEFAULT_TEXT_FILE = "script.txt"
OUTPUT_DIR = "output"
DEFAULT_VOICE = "en-US-AriaNeural"

def get_output_filename(text: str) -> str:
    """
    Generate audio file name from the first line from the DEFAULT_TEXT_FILE
    Get rid of invalid characters
    Limit length is 30
    """
    first_line = text.split('\n')[0]
    # Replace invalid characters into under score
    safe_title = re.sub(r'[\/:"*?<>|]+', '_', first_line)
    # Remove leading and trailing whitespace
    safe_title = safe_title.strip()
    # Truncate string to 30 characters
    truncated_title = safe_title[:30]
    # Get timestamp
    date_str = datetime.now().strftime("%Y%m%d")
    return f"{date_str}_{truncated_title}.mp3"

async def create_audio(voice: str, rate: str, text: str):
    """
    Generate audio from given text, voice, and speed, then save to file
    """
    # Make output directory in case it
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"output directory '{OUTPUT_DIR}' was created")

    # Generate output file name
    output_file = os.path.join(OUTPUT_DIR, get_output_filename(text))

    try:
        communicate = edge_tts.Communicate(text, voice, rate=rate)
        await communicate.save(output_file)
        print(f"\n🎉 audio file '{output_file}' was created")
        print(f"   - voice: {voice}")
        print(f"   - voice speed: {rate}")
    except Exception as e:
        print(f"\nan error occured: {e}")
        print("please check if the selected voice is available with the following command")
        print("edge-tts --list-voices | grep en-")

def get_available_voices():
    """
    Get the list of available English voices and display
    """
    print("\navailable voices:")
    print("--------------------------")
    # Examples of common US and UK English voices
    voices_to_show = [
        "en-US-AriaNeural", "en-US-JennyNeural", "en-US-GuyNeural",
        "en-GB-SoniaNeural", "en-GB-RyanNeural", "en-GB-LibbyNeural",
        "en-AU-NatashaNeural", "en-CA-ClaraNeural", "en-IN-NeerjaNeural"
    ]
    for voice in voices_to_show:
        print(f"- {voice}")
    print("--------------------------")
    print("lots more voices are available.")
    print("check all voices with this command:")
    print("edge-tts --list-voices | grep en-")

def main():
    """
    Handle command-line arguments and manage the main audio generation process
    """
    parser = argparse.ArgumentParser(
        description="Generate audio file from English script",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--voice", "-v", type=str, default=DEFAULT_VOICE,
        help=f"select voice type: \n ex: en-GB-SoniaNeural, en-US-JennyNeural\n(default: {DEFAULT_VOICE})"
    )
    parser.add_argument(
        "--rate", "-r", type=str, default="+0%",
        help="adjust the speaking speed\n ex: -10%%, +20%% (don't forget the %%)\n(default: +0%)"
    )
    parser.add_argument(
        "--file", "-f", type=str, default=DEFAULT_TEXT_FILE,
        help=f"text file name\n(default: {DEFAULT_TEXT_FILE})"
    )
    parser.add_argument(
        '--list-voices', action='store_true',
        help="display the list of available voice types"
    )

    args = parser.parse_args()

    if args.list_voices:
        get_available_voices()
        return

    # Check if text file exist
    if not os.path.exists(args.file):
        print(f"\nerror: text file '{args.file}' isn't found")
        # Generate sample text file
        try:
            with open(args.file, "w", encoding="utf-8") as f:
                f.write("Hello, this is a sample script. You can replace this with your own English text. "
                        "This tool will help you create listening materials with various voices and speeds. "
                        "Enjoy your learning!")
            print(f"-> sample file '{args.file}' was generated")
            print("   rewrite the contents of this file with any text you like, then run it again")
        except Exception as e:
            print(f"an error occurred while creating the sample file: {e}")
        return

    # Read content from text file
    try:
        with open(args.file, "r", encoding="utf-8") as f:
            text_to_read = f.read()
        if not text_to_read.strip():
            print(f"\nerror: '{args.file}' is empty. please write down English script")
            return
    except Exception as e:
        print(f"\nan error occurred while reading the file: {e}")
        return

    # Run asyncio event loop and generate audio
    asyncio.run(create_audio(args.voice, args.rate, text_to_read))

if __name__ == "__main__":
    main()

