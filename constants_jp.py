from tkinter import font

OS_WINDOWS = "Windows"
OS_MAC = "Darwin"
OS_LINUX = "Linux"

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
    "Swimlane" : "add:swimlane",
    "Terminator" : "add:terminator",
    "Process" : "add:process",
    "Decision" : "add:decision",
    "I/O" : "add:io",
    "Storage" : "add:storage",
    "Document" : "add:document",
    "Link_elbow" : "link_elbow",
    "Link_straight" : "link_straight",
}

# デフォルトモード設定
DEFAULT_MODE = MODE_DICT["Select"]

# ノード・背景色リスト
NODE_FILL_COLORS = [
    "#FDECEF",  # Light Pink
    "#FFEFF2",  # Light Orange
    "#FFF1E3",  # Light Yellow
    "#FFFDE6",  # Light Yellow
    "#F1FAEE",  # Light Green
    "#EFFFF7",  # Light Teal
    "#EAFBFF",  # Light Blue
    "#EEF4FF",  # Light Indigo
    "#F3EEFF",  # Light Purple
    "#F7F5F2",  # Light Gray
]

NODE_STATUS_NORMAL = "normal"
NODE_STATUS_ACTIVE = "active"
NODE_STATUS_INACTIVE = "inactive"

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
    "active_fill_color": "#FFFACD", # Lemon Chiffon
    "active_outline_color": "#DAA520", # Goldenrod
    "active_outline_width": 3,
    "active_font_weight": font.NORMAL,
    "active_text_color": "#DAA520", # Goldenrod
    "inactive_fill_color": "#f0f0f0", # Light Gray
    "inactive_outline_color": "#a9a9a9", # Dark Gray
    "inactive_outline_width": 2,
    "inactive_text_color": "#a9a9a9", # Dark Gray
    "inactive_font_weight": font.NORMAL,
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
    "shape_type": "corner_rounded_rectangle",   # option: "rectangle", "corner_rounded_rectangle", "rounded_rectangle",
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

# ノード・ストレージ・パラメータ
NODE_STORAGE_PARAMS = {
    "type": "storage",
    "text": "ストレージ",
    "width": 120,
    "height": 75,
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

# ノード・文書・パラメータ
NODE_DOCUMENT_PARAMS = {
    "type": "document",
    "text": "文書",
    "width": 120,
    "height": 75,
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
EDGE_TYPE_ELBOW = "elbow"
EDGE_TYPE_LINE = "line"
EDGE_LINE_STYLE_SOLID = "solid"
EDGE_LINE_STYLE_DASHED = "dashed"
EDGE_LINE_STYLE_DOTTED = "dotted"

EDGE_PARAMS = {
    "line_style": EDGE_LINE_STYLE_SOLID,
    "color": "#0f172a",
    "width": 2,
    "selected_color": "#0ea5e9",
    "outline_width": 2,
    "arrow_kind": "last",       # option: "last"(default), "first", "both", "none", None
    "arrow_shape": (8, 10, 3),  # default: (8, 10, 3)
    "text_width": 200,
    "text_color": "#0f172a",  # Dark Blue
    "font_family": "Arial",
    "font_size": 9,
    "font_weight": font.NORMAL,
    "tree_mode": False,
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

SWIMLANE_KIND_HORIZONTAL = "horizontal"
SWIMLANE_KIND_VERTICAL = "vertical"

# スイムレーン・パラメータ
SWIMLANE_PARAMS = {
    "kind": SWIMLANE_KIND_VERTICAL,  # SWIMLANE_KIND_HORIZONTAL(横型レーン) or SWIMLANE_KIND_VERTICAL(縦型レーン)
    "title": "Swimlane",
    "horizontal_width": 900,
    "horizontal_height": 120,
    "horizontal_header_width": 30,
    "horizontal_minimum_width": 300,
    "horizontal_max_width": 3000,
    "horizontal_minimum_height": 60,
    "horizontal_max_height": 810,
    "vertical_width": 210,
    "vertical_height": 720,
    "vertical_header_height": 30,
    "vertical_minimum_width": 180,
    "vertical_max_width": 800,
    "vertical_minimum_height": 300,
    "vertical_max_height": 3000,
    "fill_color": "#e0e0e0", # Light Gray
    "outline_color": "#808080", # Gray
    "selected_outline_color": "#0ea5e9",  # Light Blue
    "outline_width": 1,
    "text_color": "#0f172a",  # Dark Blue
    "font_family": "Arial",
    "font_size": 11,
    "font_weight": font.NORMAL,
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

OPENAI_API_KEY_NOT_SET_MESSAGE = ".envファイルで OPENAI_API_KEY が未設定です。.envファイルにAPIキーを定義してください。"
GEMINI_API_KEY_NOT_SET_MESSAGE = ".envファイルで GEMINI_API_KEY が未設定です。.envファイルにAPIキーを定義してください。"
ANTHROPIC_API_KEY_NOT_SET_MESSAGE = ".envファイルで ANTHROPIC_API_KEY が未設定です。.envファイルにAPIキーを定義してください。"

UNSUPPORTED_AI_MODEL_MESSAGE = "未対応のAIモデルが指定されています。constants.pyのAI_MODEL欄を確認してください。"

# 使用する生成AIモデル
AI_MODEL = "gpt-5.5"  # 例: "gpt-5.4", "gemini-3-flash-preview", "claude-opus-4-7"
# 指定可能な生成AIモデル名例（2026.3.28時点、種類やバージョンの最新は各社のドキュメントを参照のこと）
#  OpenAI（gpt-*）："gpt-5.4", "gpt-5.4-mini", "gpt-5.4-nano"
#  GeminiAI（gemini-*）："gemini-3-flash-preview", "gemini-3.1-pro-preview", "gemini-3.1-flash-lite-preview", "gemini-pro-latest", "gemini-flash-lite-latest"
#    ※Geminiについては、無料枠での利用の場合はpro版のAIを利用できないようです。
#  AnthropicAI（claude-*）："claude-opus-4-7", "claude-sonnet-4-6", "claude-haiku-4-5"

# AI関連定数
AI_CHAT_WIDTH = 550
AI_CHAT_WINDOW_SLIDE_STEP = 20
AI_CHAT_WINDOW_SLIDE_INTERVAL = 15  # ms


AI_INPUT_TEMPLATE = "「 $order 」の処理フローをまとめて、指定された形式で定義してください。"
AI_SPEC_TEMPLATE = "# 詳細仕様\n$spec"
AI_SYSTEM_INSTRUCTIONS = '''# 役割
あなたは、業務フローや処理概要を整理するシステム構築の専門家です。
指定された条件にしたがって効率の良い明快なフローを組み立て、フローチャートで定義できるようフローを適度な要素（端点、処理、分岐、入出力）に分類して、
以下に規定された出力形式で出力してください。

# 出力形式
以下のルールにのっとったMermaid記法で出力する。
- ヘッダー情報、ノード情報、リンク情報、フッター情報の順に出力する。
- ヘッダー情報は、１行目に"```mermaid"、2行目に"flowchart TD"を出力する。
- ノード情報では、以下のフォーマットで、1行に1ノードを「ノードの種類」と「タイトル」と フローチャート上での当該ノードの「左右位置」と「上下位置」を出力し、すべてのノード情報を出力する。
  - フォーマット:   <ノード識別子]>@{ shape: ノードの種類, label: "タイトル", bx: 左右位置, by: 上下位置 }
  - ノード識別子：各ノードが重複しないようユニークな記号(A,B,C,...,Z,AA,BB,CC,...,ZZ)を付与する。
  - ノードの種類：
    - 始点・終点・サブルーチンの場合：shapeにstadiumを指定する。  出力例: A@{ shape: stadium, label: "開始", bx: 0, by: 0 }
    - 処理の場合：shapeにroundedを指定する。  出力例: B@{ shape: rounded, label: "初期化処理", bx: 0, by: 0 }
    - 分岐の場合：shapeにdiamondを指定する。  出力例: C@{ shape: diamond, label: "リトライ?", bx: 0, by: 0 }
    - 入出力の場合：shapeにlean-rを指定する。  出力例: D@{ shape: lean-r, label: "データの保存", bx: 0, by: 0 }
  - タイトル：labelに処理名を指定する。タイトルの前後にダブルクォートを付ける。    出力例: A@{ shape: stadium, label: "開始", bx: 0, by: 0 }
  - フローチャート上での当該ノードの左右位置と上下位置：始点の位置を上下:0,左右:0として、処理が進むごとに上下位置を+1、分岐があると左右位置を-1,+1として数値で表現する。    出力例: B@{ shape: rounded, label: "処理A", bx: -1, by: +1 }
- リンク情報は、接続する2つのノードを、以下のフォーマットで、「接続元ノード識別子」、「ラベル（ある場合）」、「接続先ノード識別子」を出力する。
  - フォーマット: 
        ラベルがある場合：  接続元ノード識別子-- "ラベル値" -->接続先ノード識別子
        ラベルがない場合：  接続元ノード識別子-->接続先ノード識別子
  - 接続元ノード識別子：ノード情報で定義した接続元ノード識別子を指定する。
  - 接続先ノード識別子：ノード情報で定義した接続先ノード識別子を指定する。
  - リンク識別子：リンクにラベルが無い場合は --> とし、ラベルがある場合は -- "ラベル値" --> で表現する。  例1: A --> B    例2: A -- "Yes" --> B
  - なお、リンクが連続して接続されている場合は、複数のリンクを1行に記載できる。  例: A --> B --> C
- フッター情報は、最後の行に"```"を出力する。

## 出力例
-----
```mermaid
flowchart TD
  A@{ shape: stadium, label: "開始", bx: 0, by: 0 }
  B@{ shape: rounded, label: "ツールの起動", bx: 0, by: 1 }
  C@{ shape: diamond, label: "新規作成or編集?", bx: 0, by: 2 }
  D@{ shape: rounded, label: "作図", bx: 1, by: 3 }
  E@{ shape: lean-r, label: "データ読込", bx: -1, by: 3 }
  F@{ shape: rounded, label: "編集", bx: -1, by: 4 }
  G@{ shape: rounded, label: "画像出力", bx: 0, by: 5 }
  H@{ shape: rounded, label: "資料に画像を添付", bx: 0, by: 6 }
  I@{ shape: stadium, label: "終了", bx: 0, by: 7 }

  A --> B --> C -- "新規作成" --> D --> G --> H --> I
  C -- "編集" --> E --> F --> G
```
-----

# 出力フォーマット
テキスト形式

# 出力言語
日本語
'''

# 保存先（実行フォルダ直下の work/test.txt）
WORK_DIR_NAME = "work"
