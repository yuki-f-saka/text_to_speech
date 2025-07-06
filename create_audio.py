

import asyncio
import edge_tts
import argparse
import os
import re
from datetime import datetime

# --- 設定 ---
# 読み上げるテキストファイル（デフォルト値）
DEFAULT_TEXT_FILE = "script.txt"
# 出力先ディレクトリ
OUTPUT_DIR = "output"
# デフォルトの声
DEFAULT_VOICE = "en-US-AriaNeural"
# --- 設定ここまで ---

def get_output_filename(text: str) -> str:
    """
    テキストの最初の行からファイル名を生成します。
    ファイル名に使えない文字は除去し、長すぎる場合は30文字に切り詰めます。
    """
    first_line = text.split('\n')[0]
    # ファイル名に使えない文字をアンダースコアに置換
    safe_title = re.sub(r'[\/:"*?<>|]+', '_', first_line)
    # 先頭と末尾の空白を削除
    safe_title = safe_title.strip()
    # 30文字に切り詰める
    truncated_title = safe_title[:30]
    # 日付を取得
    date_str = datetime.now().strftime("%Y%m%d")
    return f"{date_str}_{truncated_title}.mp3"

async def create_audio(voice: str, rate: str, text: str):
    """
    指定されたテキスト、声、速度で音声を生成し、ファイルに保存します。
    """
    # 出力ディレクトリがなければ作成
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"出力ディレクトリ '{OUTPUT_DIR}' を作成しました。")

    # 出力ファイル名を生成
    output_file = os.path.join(OUTPUT_DIR, get_output_filename(text))

    try:
        communicate = edge_tts.Communicate(text, voice, rate=rate)
        await communicate.save(output_file)
        print(f"\n🎉 音声ファイル '{output_file}' を作成しました！")
        print(f"   - 声: {voice}")
        print(f"   - 速度: {rate}")
    except Exception as e:
        print(f"\nエラーが発生しました: {e}")
        print("選択した声が有効か、以下のコマンドで確認してみてください。")
        print("edge-tts --list-voices | grep en-")

def get_available_voices():
    """
    利用可能な英語の声の一覧を取得して表示します。
    """
    print("\n利用可能な英語の声 (一部):")
    print("--------------------------")
    # 一般的なアメリカ英語とイギリス英語の声をいくつか例として表示
    voices_to_show = [
        "en-US-AriaNeural", "en-US-JennyNeural", "en-US-GuyNeural",
        "en-GB-SoniaNeural", "en-GB-RyanNeural", "en-GB-LibbyNeural",
        "en-AU-NatashaNeural", "en-CA-ClaraNeural", "en-IN-NeerjaNeural"
    ]
    for voice in voices_to_show:
        print(f"- {voice}")
    print("--------------------------")
    print("上記以外の声もたくさんあります。")
    print("すべての声を確認したい場合は、ターミナルで以下のコマンドを実行してください。")
    print("edge-tts --list-voices | grep en-")

def main():
    """
    コマンドライン引数を処理し、音声生成のメインプロセスを管理します。
    """
    parser = argparse.ArgumentParser(
        description="英文スクリプトからリスニング用の音声ファイルを生成します。",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--voice", "-v", type=str, default=DEFAULT_VOICE,
        help=f"読み上げる声を選択します。\n例: en-GB-SoniaNeural, en-US-JennyNeural\n(デフォルト: {DEFAULT_VOICE})"
    )
    parser.add_argument(
        "--rate", "-r", type=str, default="+0%",
        help="読み上げる速度を調整します。\n例: -10%%, +20%% (%%を忘れずに！)\n(デフォルト: +0%)"
    )
    parser.add_argument(
        "--file", "-f", type=str, default=DEFAULT_TEXT_FILE,
        help=f"読み上げるテキストファイル名。\n(デフォルト: {DEFAULT_TEXT_FILE})"
    )
    parser.add_argument(
        '--list-voices', action='store_true',
        help="利用可能な英語の声のリストを表示します。"
    )

    args = parser.parse_args()

    if args.list_voices:
        get_available_voices()
        return

    # 読み上げるテキストファイルが存在するかチェック
    if not os.path.exists(args.file):
        print(f"\nエラー: テキストファイル '{args.file}' が見つかりません。")
        # サンプルのテキストファイルを作成
        try:
            with open(args.file, "w", encoding="utf-8") as f:
                f.write("Hello, this is a sample script. You can replace this with your own English text. "
                        "This tool will help you create listening materials with various voices and speeds. "
                        "Enjoy your learning!")
            print(f"-> サンプルの '{args.file}' を作成しました。")
            print("   このファイルの内容を好きな英文に書き換えて、もう一度実行してください。")
        except Exception as e:
            print(f"サンプルのファイル作成中にエラーが発生しました: {e}")
        return

    # テキストファイルから内容を読み込む
    try:
        with open(args.file, "r", encoding="utf-8") as f:
            text_to_read = f.read()
        if not text_to_read.strip():
            print(f"\nエラー: '{args.file}' の中身が空です。英文を記入してください。")
            return
    except Exception as e:
        print(f"\nファイル読み込み中にエラーが発生しました: {e}")
        return

    # asyncioイベントループを実行して音声を生成
    asyncio.run(create_audio(args.voice, args.rate, text_to_read))

if __name__ == "__main__":
    main()

