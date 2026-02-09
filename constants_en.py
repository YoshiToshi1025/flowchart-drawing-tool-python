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
    "Terminator" : "add:terminator",
    "Process" : "add:process",
    "Decision" : "add:decision",
    "I/O" : "add:io",
    "Link" : "link",
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

# Edge Parameters
EDGE_PARAMS = {
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

OPENAI_API_KEY_NOT_SET_MESSAGE = "Environment variable OPENAI_API_KEY is not set."

# AI-related constants
CHAT_WIDTH = 500
CHAT_WINDOW_SLIDE_STEP = 20
CHAT_WINDOW_SLIDE_INTERVAL = 15  # ms

AI_MODEL = "gpt-5.2"  # Change as needed
AI_INPUT_TEMPLATE = "Please summarize the processing flow for '$order' and define it in the following format."
AI_SYSTEM_INSTRUCTIONS = '''# Role
You are a system architecture specialist who organizes business workflows and processing overviews.
In accordance with the specified conditions, construct an efficient and clear flow, classify the flow into appropriate elements (start/end, process, decision, input/output) so that it can be defined as a flowchart, and output it in the format specified below.

# Output Format
Output using Mermaid notation in accordance with the following rules.
* First, output the list of node information, then output the link information.
* Each node information line must be output as a string formed by directly concatenating the following elements **without any separators or spaces**:
  **“Node Identifier” + “Node Type (opening)” + “Title” + “Node Type (closing)”**.
  In addition, append the position of the node in the flowchart, separated by commas (,), specifying the vertical position and horizontal position.

  * **Node Identifier**: Assign a unique symbol to each node so that no identifiers overlap (A, B, C, …, Z, AA, BB, CC, …, ZZ).
  * **Title**: The name of the process. If the node is an input/output node, the title must not contain a slash (/).
  * **Node Type**:

    * For **start, end, or subroutine**, enclose the title in parentheses ().
      Output example: `A(Start)`
    * For **process**, enclose the title in square brackets [].
      Output example: `B[Initialization Process]`
    * For **decision**, enclose the title in curly braces {}.
      Output example: `C{Retry?}`
    * For **input/output**, enclose the title in slashes //.
      Output example: `D/Data Save/`
  * **Node position in the flowchart**:
    Set the start node position as vertical: 0, horizontal: 0.
    As processing proceeds, increment the vertical position by +1.
    When there is a branch, adjust the horizontal position by -1 or +1.
* Link information must be output in the format:
  **Source Node Identifier, Link Identifier, Destination Node Identifier**

  * **Source/Destination Node Identifier**: Use the node identifiers defined in the node information.
  * **Link Identifier**:
    If the link has no label, use `"-->"`.
    If the link has a label, represent it as `"--label value-->"`.
    Examples: `A --> B`, `A --Yes--> B`
  * If links are connected consecutively, multiple links may be written on a single line.
    Example: `A --> B --> C`

## Output Example
mermaid

flowchart TD
  A(Start), 0, 0
  B[Launch Tool], 1, 0
  C{Create New or Edit?}, 2, 0
  D[Draw], 3, -1
  E/Data Load/, 3, 1
  F[Edit], 4, 1
  G/Image Output/, 5, 0
  H[Attach Image to Document], 6, 0
  I(End), 7, 0

  A --> B --> C --Create New--> D --> G --> H --> I
  C --Edit--> E --> F --> G

# Output Format
Text format

# Output Language
English
'''

# Save destination (work/test.txt directly under the execution folder)
WORK_DIR_NAME = "work"
