from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import tkinter as tk
import tkinter.font as tkfont
import constants as ct
import math
from math import inf

import node
import edge
import swimlane

@dataclass
class Note:
    canvas: Optional[tk.Canvas] = None
    base_node: Optional[node.Node] = None
    shape_id: Optional[int] = None
    line_id: Optional[int] = None
    text_id: Optional[int] = None
    text: Optional[str] = None
    dx: Optional[int] = None
    dy: Optional[int] = None
    display_state: Optional[str] = "normal"
    x: Optional[int] = None
    y: Optional[int] = None
    w: Optional[int] = None
    h: Optional[int] = None

    editor: Optional[tk.Text] = None
    editor_window_id: Optional[int] = None

    def __post_init__(self):
        if self.base_node is None:
            return
        if self.base_node.details is not None:
            self.text = self.base_node.details
        else:   # 新規編集の場合は初期値を設定
            self.text = ct.NOTE_PARAMS["text"]+"\n"
            self.base_node.details = self.text

        self.dx = ct.NOTE_PARAMS["dx"] if self.dx is None else self.dx
        self.dy = ct.NOTE_PARAMS["dy"] if self.dy is None else self.dy
        self.display_state = ct.NOTE_PARAMS.get("state", "normal") if self.display_state is None else self.display_state
        self.font = tkfont.Font(family=ct.NOTE_PARAMS["font_family"], size=ct.NOTE_PARAMS["font_size"], weight=ct.NOTE_PARAMS["font_weight"])
        self.display_state = "normal" if self.display_state is None else self.display_state

        if self.canvas is not None: 
            self.draw()

    def draw(self):

        if self.canvas is None or self.base_node is None or self.base_node.x is None or self.base_node.y is None or self.dx is None or self.dy is None:
            return

        self.x = self.base_node.x + self.dx
        self.y = self.base_node.y + self.dy
        self.w = ct.NOTE_PARAMS["width"]
        self.h = ct.NOTE_PARAMS["height"]

        self.shape_id = self.canvas.create_rectangle(
                            self.x - self.w / 2, self.y - self.h / 2, self.x + self.w / 2, self.y + self.h / 2,
                            fill=ct.NOTE_PARAMS["fill_color"], outline=ct.NOTE_PARAMS["outline_color"], width=ct.NOTE_PARAMS["outline_width"],
                            tags=("note", "note-shape"))

        coords = self.line_anchor(self.base_node, self)
        self.line_id = self.canvas.create_line(
                            coords[0], coords[1], coords[2], coords[3],
                            fill=ct.NOTE_PARAMS["line_color"], width=ct.NOTE_PARAMS["line_width"],
                            tags=("note", "note-line"))

        # ノートのテキストを描画（noteタグを付与）
        textarea_mergin_x = 2
        textarea_mergin_y = 2
        textarea_x = self.x - self.w/2 + textarea_mergin_x
        textarea_y = self.y - self.h/2 + textarea_mergin_y
        textarea_width = self.w - 2 * textarea_mergin_x
        textarea_height = self.h - 2 * textarea_mergin_y
        display_text = self.adjust_text(self.text, textarea_width, textarea_height, ct.NOTE_PARAMS["font_family"], ct.NOTE_PARAMS["font_size"])

        self.text_id = self.canvas.create_text(
            textarea_x, textarea_y, text=display_text,
            font=(ct.NOTE_PARAMS["font_family"], ct.NOTE_PARAMS["font_size"], ct.NOTE_PARAMS["font_weight"]),
            width=textarea_width,
            anchor="nw", justify="left",
            fill=ct.NOTE_PARAMS["text_color"],
            tags=("note", "note-text")
        )

    def start_text_edit(self, event=None):
        if self.canvas is None:
            return
        if self.editor is not None:
            return

        # 当該ノートが非表示の場合は表示する
        if self.display_state == "hidden":
            self.show(self.canvas)

        # 表示中の文字を一時的に隠す
        if self.text_id is not None:
            self.canvas.itemconfigure(self.text_id, state="hidden")

        self.editor = tk.Text(
            self.canvas,
            font=self.font,
            wrap="char",
            bd=0,
            padx=0,
            pady=0,
            bg="#FFF4A3",
            fg="#333333",
            highlightthickness=1,
            highlightbackground="#D6B94D"
        )

        self.editor.insert("1.0", self.text)

        textarea_mergin_x = 1
        textarea_mergin_y = 1
        textarea_x = self.x - self.w/2 + textarea_mergin_x
        textarea_y = self.y - self.h/2 + textarea_mergin_y
        textarea_width = self.w - 2 * textarea_mergin_x
        textarea_height = self.h - 2 * textarea_mergin_y

        self.editor_window_id = self.canvas.create_window(
            textarea_x,
            textarea_y,
            anchor="nw",
            width=textarea_width,
            height=textarea_height,
            window=self.editor
        )

        def commit(event=None):
            self.finish_text_edit(commit=True)

        def cancel(event=None):
            self.finish_text_edit(commit=False)

        self.editor.focus_set()
        self.editor.bind("<Escape>", cancel)
        self.editor.bind("<FocusOut>", commit)

    def finish_text_edit(self, commit=True):
        if self.canvas is None:
            return
        if self.editor is None:
            return

        if commit:
            self.text = self.editor.get("1.0", "end-1c")
            if self.base_node is not None:
                self.base_node.details = self.text

        if self.editor_window_id is not None:
            self.canvas.delete(self.editor_window_id)
        self.editor.destroy()
        self.editor = None
        self.editor_window_id = None

        if self.text_id is not None:
            self.canvas.itemconfigure(self.text_id, state="normal")

        if self.text == "":
            # テキストが空の場合はNoteを削除
            self.delete(self.canvas)
            self.text = None
            self.base_node.details = None
        else:
            # Noteの内容と位置を更新して再描画
            self.redraw(commit_text_edit=commit)

    def move_to(self, x, y):
        if self.base_node is None or self.base_node.x is None or self.base_node.y is None or self.dx is None or self.dy is None:
            return
        self.dx = x - self.base_node.x
        self.dy = y - self.base_node.y

        self.redraw()

    def redraw(self, commit_text_edit=True):
        # print(f"Redrawing note with base_node.id='{self.base_node.id}', text='{self.text}', dx={self.dx}, dy={self.dy}, display_state='{self.display_state}'")
        if self.canvas is None or self.base_node is None or self.base_node.x is None or self.base_node.y is None or self.dx is None or self.dy is None:
            return

        self.x = self.base_node.x + self.dx
        self.y = self.base_node.y + self.dy

        if self.shape_id is not None:
            self.canvas.coords(
                self.shape_id,
                self.x - self.w / 2, self.y - self.h / 2, self.x + self.w / 2, self.y + self.h / 2
            )

        coords = self.line_anchor(self.base_node, self)
        if self.line_id is not None:
            self.canvas.coords(
                self.line_id,
                coords[0], coords[1], coords[2], coords[3]
            )

        if self.text_id is not None:
            textarea_mergin_x = 2
            textarea_mergin_y = 2
            textarea_x = self.x - self.w/2 + textarea_mergin_x
            textarea_y = self.y - self.h/2 + textarea_mergin_y
            textarea_width = self.w - 2 * textarea_mergin_x
            textarea_height = self.h - 2 * textarea_mergin_y
            display_text = self.adjust_text(self.text, textarea_width, textarea_height, ct.NOTE_PARAMS["font_family"], ct.NOTE_PARAMS["font_size"])
            # print(f"Redrawing note with text='{self.text}', dx={self.dx}, dy={self.dy}, display_state='{self.display_state}'")

            # テキストの位置を更新
            self.canvas.coords(
                self.text_id,
                textarea_x, textarea_y
            )
            # テキストの内容を更新
            if commit_text_edit:
                self.canvas.itemconfigure(
                    self.text_id,
                    text=display_text
                )

    def line_anchor(self, base_node_obj, note_obj):
        # fromノードとtoノードの中心を結ぶ直線上のアンカー
        coords = []
        if base_node_obj.x is None or base_node_obj.y is None or base_node_obj.h is None or base_node_obj.w is None:
            return coords
        if note_obj.x is None or note_obj.y is None or note_obj.h is None or note_obj.w is None:
            return coords

        from_x, from_y = self.from_rect_intersection(base_node_obj, note_obj)
        to_x, to_y = self.to_rect_intersection(base_node_obj, note_obj)

        coords = [from_x, from_y, to_x, to_y]

        return coords

    def from_rect_intersection(self, base_node_obj, note_obj):
        lx1, ly1, lw1, lh1 = base_node_obj.x, base_node_obj.y, base_node_obj.w, base_node_obj.h
        lx2, ly2, lw2, lh2 = note_obj.x, note_obj.y, note_obj.w, note_obj.h
        w = abs(lw1)
        h = abs(lh1)

        dx = lx2 - lx1
        dy = ly2 - ly1

        if dx == 0 and dy == 0:
            return lx1, ly1

        t = min(
            inf if dx == 0 else (w / 2) / abs(dx),
            inf if dy == 0 else (h / 2) / abs(dy)
        )

        return lx1 + dx * t, ly1 + dy * t

    def to_rect_intersection(self, base_node_obj, note_obj):
        lx1, ly1, lw1, lh1 = base_node_obj.x, base_node_obj.y, base_node_obj.w, base_node_obj.h
        lx2, ly2, lw2, lh2 = note_obj.x, note_obj.y, note_obj.w, note_obj.h
        w = abs(lw2)
        h = abs(lh2)

        dx = lx1 - lx2
        dy = ly1 - ly2

        if dx == 0 and dy == 0:
            return lx2, ly2

        t = min(
            inf if dx == 0 else (w / 2) / abs(dx),
            inf if dy == 0 else (h / 2) / abs(dy)
        )

        return lx2 + dx * t, ly2 + dy * t

    def wrap_text(self, text, font, max_width):
        """文字列を指定幅に収まるように改行する"""
        lines = []
        current_line = ""

        for char in text:
            if char == "\n":
                if current_line:
                    lines.append(current_line)
                current_line = ""
            else:
                temp_line = current_line + char
                if font.measure(temp_line) <= max_width and char != "\n":
                    current_line = temp_line
                else:
                    if current_line:
                        lines.append(current_line.rstrip())
                    current_line = char

        if current_line:
            lines.append(current_line.rstrip())

        return lines


    # 表示するテキストを成形
    def adjust_text(self, text, textarea_width, textarea_height, font_family, font_size):

        font = tkfont.Font(family=font_family, size=font_size)

        # 自動改行
        lines = self.wrap_text(text, font, textarea_width)

        line_height = font.metrics("linespace")
        max_lines = (textarea_height + 1) // line_height

        # 高さに収まらない場合は省略
        if len(lines) > max_lines:
            lines = lines[:max_lines]
            if lines:
                while font.measure(lines[-1] + "...") > textarea_width and lines[-1]:
                    lines[-1] = lines[-1][:-1]
                lines[-1] += "..."

        return "\n".join(lines)

    def hidden(self, canvas: tk.Canvas):
        # print(f"Hiding note with base_node.id='{self.base_node.id}', text='{self.text}', dx={self.dx}, dy={self.dy}, display_state='{self.display_state}'")
        self.display_state = "hidden"
        if self.shape_id is not None:
            canvas.itemconfigure(self.shape_id, state="hidden")
        if self.text_id is not None:
            canvas.itemconfigure(self.text_id, state="hidden")
        if self.line_id is not None:
            canvas.itemconfigure(self.line_id, state="hidden")

    def show(self, canvas: tk.Canvas):
        # print(f"Showing note with base_node.id='{self.base_node.id}', text='{self.text}', dx={self.dx}, dy={self.dy}, display_state='{self.display_state}'")
        self.display_state = "normal"
        if self.shape_id is not None:
            canvas.itemconfigure(self.shape_id, state="normal")
        if self.text_id is not None:
            canvas.itemconfigure(self.text_id, state="normal")
        if self.line_id is not None:
            canvas.itemconfigure(self.line_id, state="normal")

    def delete(self, canvas: tk.Canvas):
        if self.shape_id is not None:
            canvas.delete(self.shape_id)
            self.shape_id = None
        if self.text_id is not None:
            canvas.delete(self.text_id)
            self.text_id = None
        if self.line_id is not None:
            canvas.delete(self.line_id)
            self.line_id = None

    def to_dict(self):
        note_data = {
            "base_node_id": self.base_node.id if self.base_node is not None else None,
            "text": self.text,
            "dx": self.dx,
            "dy": self.dy,
            "display_state": self.display_state,
        }
        return note_data

    def to_sub_dict(self):
        note_data = {
            "dx": self.dx,
            "dy": self.dy,
            "display_state": self.display_state,
        }
        return note_data
