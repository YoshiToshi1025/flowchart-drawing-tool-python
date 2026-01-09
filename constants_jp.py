from tkinter import font

# アプリケーション・タイトル
APP_TITLE = "簡易フローチャート作図ツール(TKinter Canvas)"

# キャンバス・パラメータ
CANVAS_PARAMS = {
    "size": "1200x800",
    "bg_color": "white",
    "grid_color": "#eeeeee",
    "grid_spacing": 15,
}

# モード辞書
MODE_DICT = {
    "Select" : "select",
    "Terminator" : "add:terminator",
    "Process" : "add:process",
    "Decision" : "add:decision",
    "I/O" : "add:io",
    "Link" : "link",
}

# デフォルトモード設定
DEFAULT_MODE = MODE_DICT["Select"]

# ノード・デフォルト・パラメータ
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

# ノード・処理・パラメータ
NODE_PROCESS_PARAMS = {
    "type": "process",
    "text": "処理",
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

# ノード・分岐・パラメータ
NODE_DECISION_PARAMS = {
    "type": "decision",
    "text": "分岐?",
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

# ノード・端点・パラメータ
NODE_TERMINATOR_PARAMS = {
    "type": "terminator",
    "text": "端点",
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

# ノード・入出力・パラメータ
NODE_IO_PARAMS = {
    "type": "io",
    "text": "入出力",
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

# エッジ・パラメータ
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

# 分岐ラベル定義
DECISION_YES = "Yes"
DECISION_NO = "No"
DECISION_UNKNOWN = "?"

# 端点ラベル定義
TERMINATOR_DEFAULT_START_TEXT = "開始"
TERMINATOR_DEFAULT_END_TEXT = "終了"
TERMINATOR_DEFAULT_UNKNOWN_TEXT = "（未定義）"

# エッジラベル位置補正定義
EDGE_LABEL_OFFSET = {
    "center": (0, -8),
    "ne": (-8, 4),
    "nw": (8, 6),
    "se": (-8, 0),
    "sw": (8, 0),
    "nw_from_decision": (8, 0),
}

# 選択範囲パラメータ
SELECTION_AREA_PARAMS = {
    "outline_color": "#808080",
    "outline_width": 1,
    "outline_dash": (4, 2),
}

# メッセージ定義一覧
WINDOW_CLOSE_DIALOG_TITLE = "終了確認"
WINDOW_CLOSE_DIALOG_MESSAGE = "本ツールを終了します。編集内容を保存しましたか？"

SAVE_FAILED_MESSAGE = "保存に失敗しました"
LOAD_FAILED_MESSAGE = "読み込みに失敗しました"

AI_GENERATED_MESSAGE1 = "AI生成された処理フローデータを保存しました。今すぐ読み込みますか？"
AI_GENERATED_MESSAGE2 = "今すぐ読み込みますか？"

OPENAI_API_KEY_NOT_SET_MESSAGE = "環境変数 OPENAI_API_KEY が未設定です。"


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
- ノード情報は、1行に、「ノード識別子」と「ノードの種類(開く)」と「タイトル」と「ノードの種類(閉じる)」を区切り文字や空白文字を含めずに接続した文字列の形式で出力する。 ノード情報の行に、フローチャート上での当該ノードの位置をカンマ(,)区切りで、上下位置と左右位置を付与する
  - ノード識別子：各ノードが重複しないようユニークな記号(A,B,C,...,Z,AA,BB,CC,...,ZZ)を付与する。
  - タイトル：処理名、なおノードが入出力の場合、タイトル文字にスラッシュ（/）を含めないこと。
  - ノードの種類：
    - 始点・終点・サブルーチンの場合、タイトルの前後に()を付ける。  出力例: A(開始)
    - 処理の場合、タイトルの前後に[]を付ける。  出力例: B[初期化処理]
    - 分岐の場合、タイトルの前後に{}を付ける。  出力例: C{リトライ?}
    - 入出力の場合、タイトルの前後に//を付ける。  出力例: D/データの保存/
  - フローチャート上でのノードの位置は、始点の位置を上下:0,左右:0として、処理が進むごとに上下位置を+1、分岐があると左右位置を-1,+1する。
- リンク情報は、接続する2つのノードを、接続元ノード識別子,リンク識別子,接続先ノード識別子の形式で出力する
  - 接続元ノード識別子：接続先ノード識別子はノード情報で定義したノード識別子を用いる。
  - リンク識別子：リンクにラベルが無い場合は"-->"とし、ラベルがある場合は"--ラベル値-->"で表現する。  例: A --> B,   A --Yes--> B
  - なお、リンクが連続して接続されている場合は、複数のリンクを1行に記載できる。  例: A --> B --> C

## 出力例
-----
mermaid

flowchart TD
  A(開始), 0, 0
  B[ツールの起動], 1, 0
  C{新規作成or編集?}, 2, 0
  D[作図], 3, -1
  E/データ読込/, 3, 1
  F[編集], 4,1
  G/画像出力/, 5, 0
  H[資料に画像を添付], 6, 0
  I(終了), 7, 0

  A --> B --> C --新規作成--> D --> G --> H --> I
  C --編集--> E --> F --> G
-----

# 出力フォーマット
テキスト形式

# 出力言語
日本語
'''

# 保存先（実行フォルダ直下の work/test.txt）
WORK_DIR_NAME = "work"
