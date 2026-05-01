from dataclasses import dataclass
import tkinter as tk
import constants as ct
import math
import re
from difflib import SequenceMatcher

@dataclass
class Swimlane:
    canvas: tk.Canvas
    kind: str # "horizontal"(横型レーン) or "vertical"(縦型レーン)
    title: str
    header_center_x: int
    header_center_y: int
    width: int = 0
    height: int = 0
    frame_id: int|None = None
    top_id: int|None = None
    bottom_id: int|None = None
    top_text_id: int|None = None
    bottom_text_id: int|None = None

    def __post_init__(self):
        self.kind = self.kind.replace("Swimlane_", "")  # "Swimlane_horizontal" -> "horizontal", "Swimlane_vertical" -> "vertical"
        if self.kind == ct.SWIMLANE_KIND_HORIZONTAL:
            self.width = ct.SWIMLANE_PARAMS["horizontal_width"] if self.width == 0 else self.width
            self.height = ct.SWIMLANE_PARAMS["horizontal_height"] if self.height == 0 else self.height
            self.top_left_x = self.header_center_x - ct.SWIMLANE_PARAMS["horizontal_header_width"] / 2
            self.top_left_y = self.header_center_y - self.height / 2
        elif self.kind == ct.SWIMLANE_KIND_VERTICAL:
            self.width = ct.SWIMLANE_PARAMS["vertical_width"] if self.width == 0 else self.width
            self.height = ct.SWIMLANE_PARAMS["vertical_height"] if self.height == 0 else self.height
            self.top_left_x = self.header_center_x - self.width / 2
            self.top_left_y = self.header_center_y - ct.SWIMLANE_PARAMS["vertical_header_height"] / 2
        else:
            raise ValueError(f"Invalid swimlane kind: {self.kind}")

        if self.canvas is not None: 
            self.draw()

    def draw(self):
        if self.kind == ct.SWIMLANE_KIND_VERTICAL:
            header_height = ct.SWIMLANE_PARAMS["vertical_header_height"]
            self.frame_id = self.canvas.create_rectangle(
                self.top_left_x, self.top_left_y,
                self.top_left_x + self.width, self.top_left_y + self.height,
                fill= "",
                outline=ct.SWIMLANE_PARAMS["outline_color"],
                width= ct.SWIMLANE_PARAMS["outline_width"],
                tags=("swimlane", ct.SWIMLANE_KIND_VERTICAL),
            )
            self.top_id = self.canvas.create_rectangle(
                self.top_left_x, self.top_left_y,
                self.top_left_x + self.width, self.top_left_y + header_height,
                fill= ct.SWIMLANE_PARAMS["fill_color"],
                outline= ct.SWIMLANE_PARAMS["outline_color"],
                width= ct.SWIMLANE_PARAMS["outline_width"],
                tags=("swimlane", ct.SWIMLANE_KIND_VERTICAL),
            )
            self.bottom_id = self.canvas.create_rectangle(
                self.top_left_x, self.top_left_y + self.height - header_height,
                self.top_left_x + self.width, self.top_left_y + self.height,
                fill= ct.SWIMLANE_PARAMS["fill_color"],
                outline= ct.SWIMLANE_PARAMS["outline_color"],
                width= ct.SWIMLANE_PARAMS["outline_width"],
                tags=("swimlane", ct.SWIMLANE_KIND_VERTICAL),
            )
            self.top_text_id = self.canvas.create_text(
                self.top_left_x + self.width / 2 , self.top_left_y + header_height / 2,
                text=self.title,
                anchor="center",
                fill= ct.SWIMLANE_PARAMS["text_color"],
                font=(ct.SWIMLANE_PARAMS["font_family"], ct.SWIMLANE_PARAMS["font_size"], ct.SWIMLANE_PARAMS["font_weight"]),
                tags=("swimlane", ct.SWIMLANE_KIND_VERTICAL),
            )
            self.bottom_text_id = self.canvas.create_text(
                self.top_left_x + self.width / 2 , self.top_left_y + self.height - header_height / 2,
                text=self.title,
                anchor="center",
                fill= ct.SWIMLANE_PARAMS["text_color"],
                font=(ct.SWIMLANE_PARAMS["font_family"], ct.SWIMLANE_PARAMS["font_size"], ct.SWIMLANE_PARAMS["font_weight"]),
                tags=("swimlane", ct.SWIMLANE_KIND_VERTICAL),
            )
        elif self.kind == ct.SWIMLANE_KIND_HORIZONTAL:
            header_width = ct.SWIMLANE_PARAMS["horizontal_header_width"]
            self.frame_id = self.canvas.create_rectangle(
                self.top_left_x, self.top_left_y,
                self.top_left_x + self.width, self.top_left_y + self.height,
                fill= "",
                outline=ct.SWIMLANE_PARAMS["outline_color"],
                width= ct.SWIMLANE_PARAMS["outline_width"],
                tags=("swimlane", ct.SWIMLANE_KIND_HORIZONTAL),
            )
            self.top_id = self.canvas.create_rectangle(
                self.top_left_x, self.top_left_y,
                self.top_left_x + header_width, self.top_left_y + self.height,
                fill= ct.SWIMLANE_PARAMS["fill_color"],
                outline= ct.SWIMLANE_PARAMS["outline_color"],
                width= ct.SWIMLANE_PARAMS["outline_width"],
                tags=("swimlane", ct.SWIMLANE_KIND_HORIZONTAL),
            )
            self.bottom_id = self.canvas.create_rectangle(
                self.top_left_x + self.width - header_width, self.top_left_y,
                self.top_left_x + self.width, self.top_left_y + self.height,
                fill= ct.SWIMLANE_PARAMS["fill_color"],
                outline= ct.SWIMLANE_PARAMS["outline_color"],
                width= ct.SWIMLANE_PARAMS["outline_width"],
                tags=("swimlane", ct.SWIMLANE_KIND_HORIZONTAL),
            )
            self.top_text_id = self.canvas.create_text(
                self.top_left_x + header_width / 2, self.top_left_y + self.height / 2,
                text=self.title, angle=90,
                anchor="center",
                fill= ct.SWIMLANE_PARAMS["text_color"],
                font=(ct.SWIMLANE_PARAMS["font_family"], ct.SWIMLANE_PARAMS["font_size"], ct.SWIMLANE_PARAMS["font_weight"]),
                tags=("swimlane", ct.SWIMLANE_KIND_HORIZONTAL),
            )
            self.bottom_text_id = self.canvas.create_text(
                self.top_left_x + self.width - header_width / 2, self.top_left_y + self.height / 2,
                text=self.title, angle=90,
                anchor="center",
                fill= ct.SWIMLANE_PARAMS["text_color"],
                font=(ct.SWIMLANE_PARAMS["font_family"], ct.SWIMLANE_PARAMS["font_size"], ct.SWIMLANE_PARAMS["font_weight"]),
                tags=("swimlane", ct.SWIMLANE_KIND_HORIZONTAL),
            )

    def resize(self):
        if self.frame_id is None or self.top_id is None or self.bottom_id is None or self.top_text_id is None or self.bottom_text_id is None:
            return

        if self.kind == ct.SWIMLANE_KIND_VERTICAL:
            self.top_left_x = self.header_center_x - self.width / 2
            self.top_left_y = self.header_center_y - ct.SWIMLANE_PARAMS["vertical_header_height"] / 2
            self.canvas.coords(self.frame_id, self.top_left_x, self.top_left_y, self.top_left_x + self.width, self.top_left_y + self.height)
            self.canvas.coords(self.top_id, self.top_left_x, self.top_left_y, self.top_left_x + self.width, self.top_left_y + ct.SWIMLANE_PARAMS["vertical_header_height"])
            self.canvas.coords(self.bottom_id, self.top_left_x, self.top_left_y + self.height - ct.SWIMLANE_PARAMS["vertical_header_height"], self.top_left_x + self.width, self.top_left_y + self.height)
            self.canvas.coords(self.top_text_id, self.top_left_x + self.width / 2, self.top_left_y + ct.SWIMLANE_PARAMS["vertical_header_height"] / 2)
            self.canvas.coords(self.bottom_text_id, self.top_left_x + self.width / 2, self.top_left_y + self.height - ct.SWIMLANE_PARAMS["vertical_header_height"] / 2)
        elif self.kind == ct.SWIMLANE_KIND_HORIZONTAL:
            self.top_left_x = self.header_center_x - ct.SWIMLANE_PARAMS["horizontal_header_width"] / 2
            self.top_left_y = self.header_center_y - self.height / 2
            self.canvas.coords(self.frame_id, self.top_left_x, self.top_left_y, self.top_left_x + self.width, self.top_left_y + self.height)
            self.canvas.coords(self.top_id, self.top_left_x, self.top_left_y, self.top_left_x + ct.SWIMLANE_PARAMS["horizontal_header_width"], self.top_left_y + self.height)
            self.canvas.coords(self.bottom_id, self.top_left_x + self.width - ct.SWIMLANE_PARAMS["horizontal_header_width"], self.top_left_y, self.top_left_x + self.width, self.top_left_y + self.height)
            self.canvas.coords(self.top_text_id, self.top_left_x + ct.SWIMLANE_PARAMS["horizontal_header_width"] / 2, self.top_left_y + self.height / 2)
            self.canvas.coords(self.bottom_text_id, self.top_left_x + self.width - ct.SWIMLANE_PARAMS["horizontal_header_width"] / 2, self.top_left_y + self.height / 2)
        else:
            raise ValueError(f"Invalid swimlane kind: {self.kind}")

    def redraw(self):
        if self.frame_id is not None:
            self.canvas.delete(self.frame_id)
        if self.top_id is not None:
            self.canvas.delete(self.top_id)
        if self.bottom_id is not None:
            self.canvas.delete(self.bottom_id)
        if self.top_text_id is not None:
            self.canvas.delete(self.top_text_id)
        if self.bottom_text_id is not None:
            self.canvas.delete(self.bottom_text_id)
        self.draw()

    def select(self):
        # print(f"Swimlane '{self.title}' selected")
        if self.frame_id is not None and self.top_id is not None and self.bottom_id is not None:
            self.canvas.itemconfig(self.frame_id, outline= ct.SWIMLANE_PARAMS["selected_outline_color"])
            self.canvas.itemconfig(self.top_id, outline= ct.SWIMLANE_PARAMS["selected_outline_color"])
            self.canvas.itemconfig(self.bottom_id, outline= ct.SWIMLANE_PARAMS["selected_outline_color"])

    def deselect(self):
        # print(f"Swimlane '{self.title}' deselected")
        if self.frame_id is not None and self.top_id is not None and self.bottom_id is not None:
            self.canvas.itemconfig(self.frame_id, outline= ct.SWIMLANE_PARAMS["outline_color"])
            self.canvas.itemconfig(self.top_id, outline= ct.SWIMLANE_PARAMS["outline_color"])
            self.canvas.itemconfig(self.bottom_id, outline= ct.SWIMLANE_PARAMS["outline_color"])

    def move(self, dx: int, dy: int):
        if self.frame_id is not None:
            self.canvas.move(self.frame_id, dx, dy)
            self.header_center_x += dx
            self.header_center_y += dy
            if self.top_id is not None:
                self.canvas.move(self.top_id, dx, dy)
            if self.bottom_id is not None:
                self.canvas.move(self.bottom_id, dx, dy)
            if self.top_text_id is not None:
                self.canvas.move(self.top_text_id, dx, dy)
            if self.bottom_text_id is not None:
                self.canvas.move(self.bottom_text_id, dx, dy)

    def move_to(self, x: int, y: int):
        if self.frame_id is not None:
            dx = x - self.header_center_x
            dy = y - self.header_center_y
            self.canvas.move(self.frame_id, dx, dy)
            self.header_center_x += dx
            self.header_center_y += dy
            if self.top_id is not None:
                self.canvas.move(self.top_id, dx, dy)
            if self.bottom_id is not None:
                self.canvas.move(self.bottom_id, dx, dy)
            if self.top_text_id is not None:
                self.canvas.move(self.top_text_id, dx, dy)
            if self.bottom_text_id is not None:
                self.canvas.move(self.bottom_text_id, dx, dy)

    def delete(self):
        if self.frame_id is not None:
            self.canvas.delete(self.frame_id)
        if self.top_id is not None:
            self.canvas.delete(self.top_id)
        if self.bottom_id is not None:
            self.canvas.delete(self.bottom_id)
        if self.top_text_id is not None:
            self.canvas.delete(self.top_text_id)
        if self.bottom_text_id is not None:
            self.canvas.delete(self.bottom_text_id)

    def change_width(self, increase: bool):
        if increase:
            if self.kind == ct.SWIMLANE_KIND_HORIZONTAL:
                self.width = min(ct.SWIMLANE_PARAMS["horizontal_max_width"], self.width + ct.CANVAS_PARAMS["grid_spacing"]*2)
            else:
                self.width = min(ct.SWIMLANE_PARAMS["vertical_max_width"], self.width + ct.CANVAS_PARAMS["grid_spacing"]*2)
        else:
            if self.kind == ct.SWIMLANE_KIND_HORIZONTAL:
                self.width = max(ct.SWIMLANE_PARAMS["horizontal_minimum_width"], self.width - ct.CANVAS_PARAMS["grid_spacing"]*2)
            else:
                self.width = max(ct.SWIMLANE_PARAMS["vertical_minimum_width"], self.width - ct.CANVAS_PARAMS["grid_spacing"]*2)
        self.resize()

    def change_height(self, increase: bool):
        if increase:
            if self.kind == ct.SWIMLANE_KIND_HORIZONTAL:
                self.height = min(ct.SWIMLANE_PARAMS["horizontal_max_height"], self.height + ct.CANVAS_PARAMS["grid_spacing"])
            else:
                self.height = min(ct.SWIMLANE_PARAMS["vertical_max_height"], self.height + ct.CANVAS_PARAMS["grid_spacing"])
        else:
            if self.kind == ct.SWIMLANE_KIND_HORIZONTAL:
                self.height = max(ct.SWIMLANE_PARAMS["horizontal_minimum_height"], self.height - ct.CANVAS_PARAMS["grid_spacing"])
            else:
                self.height = max(ct.SWIMLANE_PARAMS["vertical_minimum_height"], self.height - ct.CANVAS_PARAMS["grid_spacing"])
        self.resize()

    def get_fill_color(self):
        default_fill_color = ct.SWIMLANE_PARAMS["fill_color"]
        return default_fill_color

    def to_dict(self):
        swimlane_data = {
            "kind": self.kind,
            "title": self.title,
            "header_center_x": self.header_center_x,
            "header_center_y": self.header_center_y,
            "width": self.width,
            "height": self.height,
        }

        return swimlane_data