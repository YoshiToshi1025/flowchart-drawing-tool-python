from tkinter import font
import os
from dotenv import load_dotenv
from constants_i18n import get_i18n_ui_text, get_i18n_message, get_i18n_ai_prompt_template

# Application Language Setting / アプリケーションの言語設定
#   You can change the language by setting the "i18n_lang" variable to "en" for English or "ja" for Japanese.
#   "i18n_lang"変数を"en"に設定すると英語、"ja"に設定すると日本語になります。

load_dotenv()  # Load environment variables from .env file

if "i18n_lang" in os.environ and os.environ["i18n_lang"] in ["en", "ja"]:
    i18n_lang = os.environ["i18n_lang"]
else:
    print("Since i18n_lang is not defined in the .env file, the tool will be displayed in Japanese (ja).\nAdd the line i18n_lang=\"en\" to the .env file to display the tool in English.")  # .envファイルに i18n_lang="en" を定義しておけば、表示言語を英語にできます。
    i18n_lang = "ja"  # "en":English, "ja":Japanese / 日本語

# Operating System Detection / OS検出
OS_WINDOWS = "Windows"
OS_MAC = "Darwin"
OS_LINUX = "Linux" # Linux has not been tested.

# Application Title / アプリケーション・タイトル
APP_TITLE = get_i18n_ui_text("APP_TITLE", lang=i18n_lang)

# Canvas Parameters / キャンバス・パラメータ
CANVAS_PARAMS = {
    "size": "1200x800",
    "bg_color": "white",
    "grid_color": "#eeeeee",
    "grid_spacing": 15,
}

# Mode Dictionary / モード辞書
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

# Default Mode Setting / デフォルトモード設定
DEFAULT_MODE = MODE_DICT["Select"]

# Node Fill Colors / ノード・背景色リスト
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

# Node Default Parameters / ノード・デフォルト・パラメータ
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

# Node Process Parameters / ノード・処理・パラメータ
NODE_PROCESS_PARAMS = {
    "type": "process",
    "text": get_i18n_ui_text("NODE_PROCESS_PARAMS_TEXT", lang=i18n_lang),
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
    "shape_type": "corner_rounded_rectangle",   # option: "rectangle", "corner_rounded_rectangle", "ellipse"
}

# Node Decision Parameters / ノード・分岐・パラメータ
NODE_DECISION_PARAMS = {
    "type": "decision",
    "text": get_i18n_ui_text("NODE_DECISION_PARAMS_TEXT", lang=i18n_lang),
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

# Node Terminator Parameters / ノード・端点・パラメータ
NODE_TERMINATOR_PARAMS = {
    "type": "terminator",
    "text": get_i18n_ui_text("NODE_TERMINATOR_PARAMS_TEXT", lang=i18n_lang),
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

# Node I/O Parameters / ノード・入出力・パラメータ
NODE_IO_PARAMS = {
    "type": "io",
    "text": get_i18n_ui_text("NODE_IO_PARAMS_TEXT", lang=i18n_lang),
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

# Node Storage Parameters / ノード・ストレージ・パラメータ
NODE_STORAGE_PARAMS = {
    "type": "storage",
    "text": get_i18n_ui_text("NODE_STORAGE_PARAMS_TEXT", lang=i18n_lang),
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

# Node Document Parameters / ノード・文書・パラメータ
NODE_DOCUMENT_PARAMS = {
    "type": "document",
    "text": get_i18n_ui_text("NODE_DOCUMENT_PARAMS_TEXT", lang=i18n_lang),
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

# Note Parameters / ノート・パラメータ
NOTE_PARAMS = {
    "type": "note",
    "text": get_i18n_ui_text("NOTE_PARAMS_TEXT", lang=i18n_lang),
    "dx": 180,
    "dy": -60,
    "width": 150,
    "height": 135,
    "state" : "normal",    # option: normal, hidden
    "fill_color": "#FFF9CC", # Light Yellow
    "outline_color": "#D6B94D", # Light Brown
    "selected_outline_color": "#0ea5e9",  # Light Blue
    "outline_width": 1,
    "line_color": "#D6B94D", # Light Brown
    "line_width": 1,
    "text_width": 150,
    "text_color": "#0f172a",  # Dark Blue
    "font_family": ("Arial","Meiryo"),
    "font_size": 8,
    "font_weight": font.NORMAL,
}

# Edge Parameters / エッジ・パラメータ
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
    "path_type": "vertical"     # option(only elbow type): "vertical"(垂直型), "horizontal"(水平型), "tree"(ツリー型)
}

# Decision Label Definitions / 分岐ラベル定義
DECISION_YES = get_i18n_ui_text("DECISION_YES", lang=i18n_lang)
DECISION_NO = get_i18n_ui_text("DECISION_NO", lang=i18n_lang)
DECISION_UNKNOWN = get_i18n_ui_text("DECISION_UNKNOWN", lang=i18n_lang)

# Terminator Label Definitions / 端点ラベル定義
TERMINATOR_DEFAULT_START_TEXT = get_i18n_ui_text("TERMINATOR_DEFAULT_START_TEXT", lang=i18n_lang)
TERMINATOR_DEFAULT_END_TEXT = get_i18n_ui_text("TERMINATOR_DEFAULT_END_TEXT", lang=i18n_lang)
TERMINATOR_DEFAULT_UNKNOWN_TEXT = get_i18n_ui_text("TERMINATOR_DEFAULT_UNKNOWN_TEXT", lang=i18n_lang)

# Edge Label Offset Definitions / エッジラベル位置補正定義
EDGE_LABEL_OFFSET = {
    "center": (0, -8),
    "ne": (-8, 4),
    "nw": (8, 0),
    "se": (-8, 0),
    "sw": (8, 0),
    "nw_from_decision": (8, 0),
    "sw_from_decision": (8, 0),
}

SWIMLANE_KIND_HORIZONTAL = "horizontal"
SWIMLANE_KIND_VERTICAL = "vertical"

# Swimlane Parameters / スイムレーン・パラメータ
SWIMLANE_PARAMS = {
    "kind": SWIMLANE_KIND_VERTICAL,  # SWIMLANE_KIND_HORIZONTAL(横型レーン) or SWIMLANE_KIND_VERTICAL(縦型レーン)
    "title": "Swimlane",
    "horizontal_width": 900,
    "horizontal_height": 150,
    "horizontal_header_width": 30,
    "horizontal_minimum_width": 300,
    "horizontal_max_width": 3000,
    "horizontal_minimum_height": 60,
    "horizontal_max_height": 810,
    "vertical_width": 210,
    "vertical_height": 660,
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

# Selection Area Parameters / 選択範囲パラメータ
SELECTION_AREA_PARAMS = {
    "outline_color": "#808080",
    "outline_width": 1,
    "outline_dash": (4, 2),
}

# Swimlane Fill Colors / スイムレーン・背景色リスト
SWIMLANE_FILL_COLORS = [
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

# Message Definitions / メッセージ定義一覧
WINDOW_CLOSE_DIALOG_TITLE = get_i18n_message("WINDOW_CLOSE_DIALOG_TITLE", lang=i18n_lang)
WINDOW_CLOSE_DIALOG_MESSAGE = get_i18n_message("WINDOW_CLOSE_DIALOG_MESSAGE", lang=i18n_lang)

SAVE_FAILED_MESSAGE = get_i18n_message("SAVE_FAILED_MESSAGE", lang=i18n_lang)
LOAD_FAILED_MESSAGE = get_i18n_message("LOAD_FAILED_MESSAGE", lang=i18n_lang)

AI_GENERATED_MESSAGE1 = get_i18n_message("AI_GENERATED_MESSAGE1", lang=i18n_lang)
AI_GENERATED_MESSAGE2 = get_i18n_message("AI_GENERATED_MESSAGE2", lang=i18n_lang)

OPENAI_API_KEY_NOT_SET_MESSAGE = get_i18n_message("OPENAI_API_KEY_NOT_SET_MESSAGE", lang=i18n_lang)
GEMINI_API_KEY_NOT_SET_MESSAGE = get_i18n_message("GEMINI_API_KEY_NOT_SET_MESSAGE", lang=i18n_lang)
ANTHROPIC_API_KEY_NOT_SET_MESSAGE = get_i18n_message("ANTHROPIC_API_KEY_NOT_SET_MESSAGE", lang=i18n_lang)

UNSUPPORTED_AI_MODEL_MESSAGE = get_i18n_message("UNSUPPORTED_AI_MODEL_MESSAGE", lang=i18n_lang)

# AI Model Selection / 使用する生成AIモデル
AI_MODEL = "gpt-5.5"
# Example of available AI model names / 指定可能な生成AIモデル名例 (as of 2026.5.29)
#   OpenAI (gpt-*): "gpt-5.5", "gpt-5.4", "gpt-5.4-mini"
#   GeminiAI (gemini-*): "gemini-3.1-pro-preview", "gemini-3.5-flash", "gemini-3.1-flash-lite", "gemini-3-flash-preview", "gemini-pro-latest", "gemini-flash-lite-latest"
#   AnthropicAI (claude-*): "claude-opus-4-8", "claude-sonnet-4-6", "claude-haiku-4-5"

# AI Related Constants / AI関連定数
AI_CHAT_WIDTH = 550
AI_CHAT_WINDOW_SLIDE_STEP = 20
AI_CHAT_WINDOW_SLIDE_INTERVAL = 15  # ms

AI_INPUT_TEMPLATE = get_i18n_ai_prompt_template("AI_INPUT_TEMPLATE", lang=i18n_lang)
AI_SPEC_TEMPLATE = get_i18n_ai_prompt_template("AI_SPEC_TEMPLATE", lang=i18n_lang)
AI_SYSTEM_INSTRUCTIONS = get_i18n_ai_prompt_template("AI_SYSTEM_INSTRUCTIONS", lang=i18n_lang)

# Work Directory / 作業フォルダ
WORK_DIR_NAME = "work"
