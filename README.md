# 英文リスニング教材作成スクリプト

このスクリプトは、テキストファイルに含まれる英文からリスニング練習用の音声ファイル（.mp3）を生成します。
Microsoft Edge の読み上げ機能と同じ、高品質な音声合成エンジンを使用しています。

## 必要なもの

- Python 3
- `edge-tts` ライブラリ

## 準備

1.  **ライブラリのインストール:**
    ```shell
    pip install edge-tts
    ```

2.  **英文スクリプトの用意:**
    プロジェクトのルートにある `script.txt` に、音声にしたい英文を貼り付けます。

## 使い方

音声ファイルは `output` ディレクトリ内に生成されます。

### 基本的な使い方

以下のコマンドを実行すると、`script.txt` の内容がデフォルト設定（アメリカ英語の女性の声、通常の速度）で音声ファイルに変換されます。

```bash
python create_audio.py
```

### オプション

#### 声の種類を変更する (`--voice` / `-v`)

まず、利用可能な声のリストを確認します。

```bash
python create_audio.py --list-voices
```

リストから使いたい声（例: `en-GB-SoniaNeural`）を選び、以下のように指定します。

```bash
python create_audio.py --voice en-GB-SoniaNeural
```

#### 話す速度を変更する (`--rate` / `-r`)

元の速度を基準に、パーセンテージで速度を調整します。

- **10%遅くする:**
  ```bash
  python create_audio.py --rate -10%
  ```
- **20%速くする:**
  ```bash
  python create_audio.py --rate +20%
  ```

#### 声と速度を同時に変更する

```bash
python create_audio.py -v en-GB-RyanNeural -r -5%
```

#### 読み上げるファイルを変更する (`--file` / `-f`)

`script.txt` 以外のファイル（例: `article.txt`）を読み込みたい場合、以下のように指定します。

```bash
python create_audio.py --file article.txt
```
