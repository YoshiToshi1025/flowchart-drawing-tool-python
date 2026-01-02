from tkinter import font

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

# AI-related constants
CHAT_WIDTH = 500
CHAT_WINDOW_SLIDE_STEP = 20
CHAT_WINDOW_SLIDE_INTERVAL = 15  # ms

AI_MODEL = "gpt-5.2"  # Change as needed
AI_INPUT_TEMPLATE = "Please summarize the processing flow for '$order' and define it in the following format."
AI_SYSTEM_INSTRUCTIONS = '''# Role
You are an expert in system construction who organizes business flows and process overviews.
According to the specified conditions, build an efficient and clear flow, classify the flow into appropriate elements (endpoints, processes, decisions, I/O) so that it can be defined in a flowchart,
and output it in the output format specified below.

# Output Format
Output in Mermaid notation according to the following rules.
- First output the list of node information, then output the link information.
- Node information is output in the format of a string that connects "node identifier", "node type (opening)", "title", and "node type (closing)" without delimiters or spaces on one line.
  - Node identifier: Assign a unique symbol (A, B, C, ..., Z, AA, BB, CC, ..., ZZ) to each node so that they do not overlap.
  - Title: Process name. Note that if the node is I/O, the title text should not include slashes (/).
  - Node type:
    - For start/end/subroutine, put () before and after the title. Example: A(Start)
    - For process, put [] before and after the title. Example: B[Initialize]
    - For decision, put {} before and after the title. Example: C{Retry?}
    - For I/O, put // before and after the title. Example: D/Save Data/
- Link information is output in the format of source node identifier, link identifier, destination node identifier for the two nodes to be connected.
  - Source node identifier: Destination node identifier uses the node identifier defined in the node information.
  - Link identifier: If the link has no label, use "-->", if it has a label, use "--label value-->". Example: A --> B, A --Yes--> B
  - Note that if links are connected consecutively, multiple links can be written on one line. Example: A --> B --> C

## Output Example
-----
mermaid

flowchart TD
  A(Start)
  B[Launch Tool]
  C{Create New or Edit?}
  D[Draw]
  E/Load Data/
  F[Edit]
  G/Output Image/
  H[Attach Image to Document]
  I(End)

  A --> B --> C --Create New--> D --> G --> H --> I
  C --Edit--> E --> F --> G
-----

# Output Format
Text format

# Output Language
English
'''

# Save destination (work/test.txt directly under the execution folder)
WORK_DIR_NAME = "work"
