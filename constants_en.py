from tkinter import font

OS_WINDOWS = "Windows"
OS_MAC = "Darwin"
OS_LINUX = "Linux"

# App Application Title
APP_TITLE = "Simple Flowchart Drawing Tool (TKinter Canvas)"

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

# Default Mode Setting
DEFAULT_MODE = MODE_DICT["Select"]

# Node Fill Colors
NODE_FILL_COLORS = [
    "#FADADD",  # Light Pink
    "#FFE5B4",  # Light Orange
    "#FFF9C4",  # Light Yellow
    "#E6F4D7",  # Light Green
    "#D7FBE8",  # Light Teal
    "#D6F0FF",  # Light Blue
    "#DCE7FF",  # Light Indigo
    "#E9D7FF",  # Light Purple
    "#F2F2F2",  # Light Gray
    "#F5EBDD",  # Light Brown
]

NODE_STATUS_NORMAL = "normal"
NODE_STATUS_ACTIVE = "active"
NODE_STATUS_INACTIVE = "inactive"

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
    "shape_type": "corner_rounded_rectangle",   # option: "rectangle", "corner_rounded_rectangle", "rounded_rectangle",
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

# Node Storage Parameters
NODE_STORAGE_PARAMS = {
    "type": "storage",
    "text": "Storage",
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

# Node Document Parameters
NODE_DOCUMENT_PARAMS = {
    "type": "document",
    "text": "Document",
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

# Edge Parameters
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

SWIMLANE_KIND_HORIZONTAL = "horizontal"
SWIMLANE_KIND_VERTICAL = "vertical"

# Swimlane Parameters
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

# Selection Area Parameters
SELECTION_AREA_PARAMS = {
    "outline_color": "#808080",
    "outline_width": 1,
    "outline_dash": (4, 2),
}

# スイムレーン・背景色リスト
SWIMLANE_FILL_COLORS = [
    "#FADADD",  # Light Pink
    "#FFE5B4",  # Light Orange
    "#FFF9C4",  # Light Yellow
    "#E6F4D7",  # Light Green
    "#D7FBE8",  # Light Teal
    "#D6F0FF",  # Light Blue
    "#DCE7FF",  # Light Indigo
    "#E9D7FF",  # Light Purple
    "#F2F2F2",  # Light Gray
    "#F5EBDD",  # Light Brown
]

# Message Definitions
WINDOW_CLOSE_DIALOG_TITLE = "Close Confirmation"
WINDOW_CLOSE_DIALOG_MESSAGE = "Are you sure you want to exit? Have you saved your changes?"

SAVE_FAILED_MESSAGE = "Failed to save"
LOAD_FAILED_MESSAGE = "Failed to load"

AI_GENERATED_MESSAGE1 = "AI-generated flow data has been saved."
AI_GENERATED_MESSAGE2 = "Do you want to load it now?"

OPENAI_API_KEY_NOT_SET_MESSAGE = "The OPENAI_API_KEY is not set in the .env file. Please define the API key in the .env file."
GEMINI_API_KEY_NOT_SET_MESSAGE = "The GEMINI_API_KEY is not set in the .env file. Please define the API key in the .env file."
ANTHROPIC_API_KEY_NOT_SET_MESSAGE = "The ANTHROPIC_API_KEY is not set in the .env file. Please define the API key in the .env file."

UNSUPPORTED_AI_MODEL_MESSAGE = "The specified AI model is not supported. Please check the AI_MODEL field in constants.py."

# AI Model to Use
AI_MODEL = "gpt-5.5"
# Example of available AI model names (as of 2026.3.28, for the latest types and versions, refer to each company's documentation)
#  OpenAI (gpt-*): "gpt-5.5", "gpt-5.4-mini", "gpt-5.4-nano"
#  GeminiAI (gemini-*): "gemini-3-flash-preview", "gemini-3.1-pro-preview", "gemini-3.1-flash-lite-preview", "gemini-pro-latest", "gemini-flash-lite-latest"
#    ※For Gemini, if using the free tier, the pro version AI may not be available.
#  AnthropicAI (claude-*): "claude-opus-4-7", "claude-sonnet-4-6", "claude-haiku-4-5"
    
# AI-related constants
AI_CHAT_WIDTH = 550
AI_CHAT_WINDOW_SLIDE_STEP = 20
AI_CHAT_WINDOW_SLIDE_INTERVAL = 15  # ms

AI_INPUT_TEMPLATE = "Summarize the process flow for \"$order\" and define it in the specified format."
AI_SPEC_TEMPLATE = "# Detailed Specifications\n$spec"
AI_SYSTEM_INSTRUCTIONS = '''# Role
You are an expert in system design specializing in organizing business workflows and process overviews.
Based on the given conditions, construct an efficient and clear flow, classify it into appropriate elements (start/end, process, decision, input/output),
and output it in the format defined below so that it can be represented as a flowchart.

# Output Format
Output using Mermaid notation according to the following rules:
- Output in the order: header information, node information, link information, and footer information.
- Header information:
  - First line: "```mermaid"
  - Second line: "flowchart TD"

- Node information:
  - Output all nodes, one per line, using the following format, including the node type, title, and its horizontal and vertical position in the flowchart.
  - Format:
    <NodeID>@{ shape: NodeType, label: "Title", bx: HorizontalPosition, by: VerticalPosition }

  - Node ID:
    Assign unique identifiers to each node so that no duplicates exist (A, B, C, ..., Z, AA, BB, CC, ..., ZZ).

  - Node types:
    - Start / End / Subroutine:
      Use shape: stadium
      Example: A@{ shape: stadium, label: "Start", bx: 0, by: 0 }

    - Process:
      Use shape: rounded
      Example: B@{ shape: rounded, label: "Initialization", bx: 0, by: 0 }

    - Decision:
      Use shape: diamond
      Example: C@{ shape: diamond, label: "Retry?", bx: 0, by: 0 }

    - Input/Output:
      Use shape: lean-r
      Example: D@{ shape: lean-r, label: "Save Data", bx: 0, by: 0 }

  - Title:
    Specify the process name in the label field and enclose it in double quotes.
    Example: A@{ shape: stadium, label: "Start", bx: 0, by: 0 }

  - Node position (horizontal and vertical):
    Treat the start node as (bx: 0, by: 0).
    As the process progresses, increment the vertical position by +1.
    When branching occurs, represent horizontal position as -1 or +1.
    Example: B@{ shape: rounded, label: "Process A", bx: -1, by: +1 }

- Link information:
  - For each connection between nodes, output the source node ID, label (if any), and destination node ID using the format below:

    With label:
      SourceNodeID -- "Label" --> DestinationNodeID

    Without label:
      SourceNodeID --> DestinationNodeID

  - Source node ID:
    Use the node ID defined in the node information.

  - Destination node ID:
    Use the node ID defined in the node information.

  - Link representation:
    - Without label: -->
    - With label: -- "Label" -->
    Examples:
      A --> B
      A -- "Yes" --> B

  - If links are connected sequentially, multiple links can be written on a single line.
    Example: A --> B --> C

- Footer information:
  - Output "```" on the last line.

## Output Example
mermaid

flowchart TD
  A@{ shape: stadium, label: "Start", bx: 0, by: 0 }
  B@{ shape: rounded, label: "Launch Tool", bx: 0, by: 1 }
  C@{ shape: diamond, label: "Create New or Edit?", bx: 0, by: 2 }
  D@{ shape: rounded, label: "Draw", bx: 1, by: 3 }
  E@{ shape: lean-r, label: "Data Load", bx: -1, by: 3 }
  F@{ shape: rounded, label: "Edit", bx: -1, by: 4 }
  G@{ shape: rounded, label: "Image Output", bx: 0, by: 5 }
  H@{ shape: rounded, label: "Attach Image to Document", bx: 0, by: 6 }
  I@{ shape: stadium, label: "End", bx: 0, by: 7 }

  A --> B --> C -- "Create New" --> D --> G --> H --> I
  C -- "Edit" --> E --> F --> G

# Output Format
Text format

# Output Language
English
'''

# Save destination (work/test.txt directly under the execution folder)
WORK_DIR_NAME = "work"
