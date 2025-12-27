from tkinter import font

# アプリケーション・タイトル
APP_TITLE = "簡易フローチャート作図ツール(TKinter Canvas)"

# キャンバス・パラメータ
CANVAS_PARAMS = {
    "size": "1200x800",
    "bg_color": "white",
    "grid_color": "#eeeeee",
    "grid_spacing": 20,
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
    "width": 160,
    "height": 60,
    "fill_color": "#FFFFFF", # White
    "outline_color": "#334155",
    "selected_outline_color": "#0ea5e9",  # Light Blue
    "outline_width": 2,
    "text_width": 150,
    "text_color": "#0f172a",  # Dark Blue
    "font_family": "Arial",
    "font_size": 11,
    "font_weight": font.NORMAL,
}

# ノード・処理・パラメータ
NODE_PROCESS_PARAMS = {
    "type": "process",
    "text": "処理",
    "width": 160,
    "height": 60,
    "fill_color": "#FFFFFF", # 
    "outline_color": "#334155",
    "selected_outline_color": "#0ea5e9",  # Light Blue
    "outline_width": 2,
    "text_width": 150,
    "text_color": "#0f172a",  # Dark Blue
    "font_family": "Arial",
    "font_size": 11,
    "font_weight": font.NORMAL,
}

# ノード・分岐・パラメータ
NODE_DECISION_PARAMS = {
    "type": "decision",
    "text": "分岐?",
    "width": 160,
    "height": 60,
    "fill_color": "#FFFFFF", # White
    "outline_color": "#334155",
    "selected_outline_color": "#0ea5e9",  # Light Blue
    "outline_width": 2,
    "text_width": 150,
    "text_color": "#0f172a",  # Dark Blue
    "font_family": "Arial",
    "font_size": 11,
    "font_weight": font.NORMAL,
}

# ノード・端点・パラメータ
NODE_TERMINATOR_PARAMS = {
    "type": "terminator",
    "text": "端点",
    "width": 160,
    "height": 60,
    "fill_color": "#e0e0e0", # Light Gray 
    "outline_color": "#334155",
    "selected_outline_color": "#0ea5e9",  # Light Blue
    "outline_width": 2,
    "text_width": 150,
    "text_color": "#0f172a",  # Dark Blue
    "font_family": "Arial",
    "font_size": 11,
    "font_weight": font.NORMAL,
}

# ノード・入出力・パラメータ
NODE_IO_PARAMS = {
    "type": "io",
    "text": "入出力",
    "width": 160,
    "height": 60,
    "skew": 20,
    "fill_color": "#FFFFFF", # White
    "outline_color": "#334155",
    "selected_outline_color": "#0ea5e9",  # Light Blue
    "outline_width": 2,
    "text_width": 150,
    "text_color": "#0f172a",  # Dark Blue
    "font_family": "Arial",
    "font_size": 11,
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
    "font_size": 11,
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
