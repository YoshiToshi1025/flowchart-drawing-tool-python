
APP_TITLE = "Flowchart Tool (Tkinter Canvas)"
CANVAS_SIZE = "1000x700"


TYPE_PROCESS = "process"
TYPE_DECISION = "decision"
TYPE_TERMINATOR = "terminator"
TYPE_IO = "io"

NODE_TYPES = [TYPE_PROCESS, TYPE_DECISION, TYPE_TERMINATOR, TYPE_IO]

PROCESS_DEFAULT_PARAMS = {
    "type": TYPE_PROCESS,
    "text": "Process",
    "width": 120,
    "height": 60,
    "fill_color": "#FFFFFF", # 
    "outline_color": "#334155"
}

DECISION_DEFAULT_PARAMS = {
    "type": TYPE_DECISION,
    "text": "Decision",
    "width": 120,
    "height": 60,
    "fill_color": "#FFFFFF", # White
    "outline_color": "#334155"
}

TERMINATOR_DEFAULT_PARAMS = {
    "type": TYPE_TERMINATOR,
    "text": "Terminator",
    "width": 120,
    "height": 60,
    "fill_color": "#e0e0e0", # Light Gray 
    "outline_color": "#334155"
}

IO_DEFAULT_PARAMS = {
    "type": TYPE_IO,
    "text": "I/O",
    "width": 120,
    "height": 60,
    "skew": 20,
    "fill_color": "#FFFFFF", # White
    "outline_color": "#334155"
}

NODE_FILL_COLOR = "#ffffff" # White
NODE_OUTLINE_COLOR = "#334155"
SELECTED_OUTLINE_COLOR = "#0ea5e9"
NODE_OUTLINE_WIDTH = 2

TEXT_COLOR = "#0f172a"  # White
TEXT_FONT_FAMILY = "Arial"
TEXT_FONT_SIZE = 11
TEXT_WIDTH = 150

EDGE_COLOR = "#0f172a"
EDGE_WIDTH = 2
SELECTED_EDGE_COLOR = "#0ea5e9"

CANVAS_BG_COLOR = "white"
GRID_COLOR = "#eeeeee"
GRID_SPACING = 20

DECISION_YES = "Yes"
DECISION_NO = "No"
DECISION_UNKNOWN = "?"

TERMINATOR_DEFAULT_START_TEXT = "Start"
TERMINATOR_DEFAULT_END_TEXT = "End"
TERMINATOR_DEFAULT_UNKNOWN_TEXT = "???"

SELECTION_OUTLINE_COLOR = "#808080"
SELECTION_OUTLINE_WIDTH = 1
SELECTION_OUTLINE_DASH = (4, 2)