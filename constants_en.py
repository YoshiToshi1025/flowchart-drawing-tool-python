from tkinter import font

# App Application Title
APP_TITLE = "Flowchart Tool (Tkinter Canvas)"

# Canvas Parameters
CANVAS_PARAMS = {
    "size": "1200x800",
    "bg_color": "white",
    "grid_color": "#eeeeee",
    "grid_spacing": 15,
}

# Mode Dictionary
MODE_DICT = {
    "Select" : "select",
    "Terminator" : "add:terminator",
    "Process" : "add:process",
    "Decision" : "add:decision",
    "I/O" : "add:io",
    "Link" : "link",
}

# Default Mode Setting
DEFAULT_MODE = MODE_DICT["Select"]

# Node Default Parameters
NODE_DEFAULT_PARAMS = {
    "type": "default",
    "text": "Undefined",
    "width": 120,
    "height": 45,
    "fill_color": "#FFFFFF", # White
    "outline_color": "#334155",
    "selected_outline_color": "#0ea5e9",  # Light Blue
    "outline_width": 2,
    "text_width": 110,
    "text_color": "#0f172a",  # Dark Blue
    "font_family": "Arial",
    "font_size": 9,
    "font_weight": font.NORMAL,
}

# Node Process Parameters
NODE_PROCESS_PARAMS = {
    "type": "process",
    "text": "Process",
    "width": 120,
    "height": 45,
    "fill_color": "#FFFFFF", # 
    "outline_color": "#334155",
    "selected_outline_color": "#0ea5e9",  # Light Blue
    "outline_width": 2,
    "text_width": 110,
    "text_color": "#0f172a",  # Dark Blue
    "font_family": "Arial",
    "font_size": 9,
    "font_weight": font.NORMAL,
}

# Node Decision Parameters
NODE_DECISION_PARAMS = {
    "type": "decision",
    "text": "Decision?",
    "width": 120,
    "height": 45,
    "fill_color": "#FFFFFF", # White
    "outline_color": "#334155",
    "selected_outline_color": "#0ea5e9",  # Light Blue
    "outline_width": 2,
    "text_width": 110,
    "text_color": "#0f172a",  # Dark Blue
    "font_family": "Arial",
    "font_size": 9,
    "font_weight": font.NORMAL,
}

# Node Terminator Parameters
NODE_TERMINATOR_PARAMS = {
    "type": "terminator",
    "text": "Terminator",
    "width": 120,
    "height": 45,
    "fill_color": "#e0e0e0", # Light Gray 
    "outline_color": "#334155",
    "selected_outline_color": "#0ea5e9",  # Light Blue
    "outline_width": 2,
    "text_width": 110,
    "text_color": "#0f172a",  # Dark Blue
    "font_family": "Arial",
    "font_size": 9,
    "font_weight": font.NORMAL,
}

# Node I/O Parameters
NODE_IO_PARAMS = {
    "type": "io",
    "text": "I/O",
    "width": 120,
    "height": 45,
    "skew": 15,
    "fill_color": "#FFFFFF", # White
    "outline_color": "#334155",
    "selected_outline_color": "#0ea5e9",  # Light Blue
    "outline_width": 2,
    "text_width": 110,
    "text_color": "#0f172a",  # Dark Blue
    "font_family": "Arial",
    "font_size": 9,
    "font_weight": font.NORMAL,
}

# Edge Parameters
EDGE_PARAMS = {
    "color": "#0f172a",
    "width": 2,
    "selected_color": "#0ea5e9",
    "outline_width": 2,
    "text_width": 200,
    "text_color": "#0f172a",  # Dark Blue
    "font_family": "Arial",
    "font_size": 9,
    "font_weight": font.NORMAL,
}

# Decision Label Definitions
DECISION_YES = "Yes"
DECISION_NO = "No"
DECISION_UNKNOWN = "?"

# Terminator Label Definitions
TERMINATOR_DEFAULT_START_TEXT = "Start"
TERMINATOR_DEFAULT_END_TEXT = "End"
TERMINATOR_DEFAULT_UNKNOWN_TEXT = "???"

# Edge Label Position Offset Definitions
EDGE_LABEL_OFFSET = {
    "center": (0, -8),
    "ne": (-8, 4),
    "nw": (8, 6),
    "se": (-8, 0),
    "sw": (8, 0),
    "nw_from_decision": (8, 0),
}

# Selection Area Parameters
SELECTION_AREA_PARAMS = {
    "outline_color": "#808080",
    "outline_width": 1,
    "outline_dash": (4, 2),
}

# Message Definitions
WINDOW_CLOSE_DIALOG_TITLE = "Close Confirmation"
WINDOW_CLOSE_DIALOG_MESSAGE = "Are you sure you want to exit? Have you saved your changes?"

SAVE_FAILED_MESSAGE = "Failed to save"
LOAD_FAILED_MESSAGE = "Failed to load"

AI_GENERATED_MESSAGE1 = "AI-generated flow data has been saved."
AI_GENERATED_MESSAGE2 = "Do you want to load it now?"

# AI関連定数
CHAT_WIDTH = 500
CHAT_WINDOW_SLIDE_STEP = 20
CHAT_WINDOW_SLIDE_INTERVAL = 15  # ms

AI_MODEL = "gpt-5.2"  # 必要に応じて変更
AI_INPUT_TEMPLATE = "「 $order 」の処理フローをまとめて、以下の形式で定義してください。"
AI_SYSTEM_INSTRUCTIONS = '''# 役割
あなたは、業務フローや処理概要を整理するシステム構築の専門家です。
指定された条件にしたがって効率の良い明快なフローを組み立て、フローチャートで定義できるようフローを適度な要素（端点、処理、分岐、入出力）に分類して、
以下に規定された出力形式で出力してください。

# 出力形式
以下のルールにのっとったMermaid記法で出力する。
- 先にノード情報のリストを出力し、あとからリンク情報を出力する。
- ノード情報は、1行に、「ノード識別子」と「ノードの種類(開く)」と「タイトル」と「ノードの種類(閉じる)」を区切り文字や空白文字を含めずに接続した文字列の形式で出力する。 
  - ノード識別子：各ノードが重複しないようユニークな記号(A,B,C,...,Z,AA,BB,CC,...,ZZ)を付与する。
  - タイトル：処理名、なおノードが入出力の場合、タイトル文字にスラッシュ（/）を含めないこと。
  - ノードの種類：
    - 始点・終点・サブルーチンの場合、タイトルの前後に()を付ける。  出力例: A(開始)
    - 処理の場合、タイトルの前後に[]を付ける。  出力例: B[初期化処理]
    - 分岐の場合、タイトルの前後に{}を付ける。  出力例: C{リトライ?}
    - 入出力の場合、タイトルの前後に//を付ける。  出力例: D/データの保存/
- リンク情報は、接続する2つのノードを、接続元ノード識別子,リンク識別子,接続先ノード識別子の形式で出力する
  - 接続元ノード識別子：接続先ノード識別子はノード情報で定義したノード識別子を用いる。
  - リンク識別子：リンクにラベルが無い場合は"-->"とし、ラベルがある場合は"--ラベル値-->"で表現する。  例: A --> B,   A --Yes--> B
  - なお、リンクが連続して接続されている場合は、複数のリンクを1行に記載できる。  例: A --> B --> C

## 出力例
-----
mermaid

flowchart TD
  A(開始)
  B[ツールの起動]
  C{新規作成or編集?}
  D[作図]
  E/データ読込/
  F[編集]
  G/画像出力/
  H[資料に画像を添付]
  I(終了)

  A --> B --> C --新規作成--> D --> G --> H --> I
  C --編集--> E --> F --> G
-----

# 出力フォーマット
テキスト形式

# 出力言語
English
'''

# 保存先（実行フォルダ直下の work/test.txt）
WORK_DIR_NAME = "work"
