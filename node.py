import tkinter as tk
import constants as ct
import math

class Node:
    id = None
    type = None
    x:int = 0
    y:int = 0
    w:int = 0
    h:int = 0
    text = None
    shape_id = None
    text_id = None

    def __init__(self, node_id, node_type, x:int, y:int, w=None, h=None, text=None, canvas=None):

        self.id = node_id
        self.type = node_type
        self.x = x
        self.y = y

        if w is None:
            self.w = {
                ct.NODE_PROCESS_PARAMS["type"] : ct.NODE_PROCESS_PARAMS["width"],
                ct.NODE_DECISION_PARAMS["type"] : ct.NODE_DECISION_PARAMS["width"],
                ct.NODE_TERMINATOR_PARAMS["type"] : ct.NODE_TERMINATOR_PARAMS["width"],
                ct.NODE_IO_PARAMS["type"] : ct.NODE_IO_PARAMS["width"],
            }.get(self.type, ct.NODE_DEFAULT_PARAMS["width"])
        else:
            self.w = w

        if h is None:
            self.h = {
                ct.NODE_PROCESS_PARAMS["type"] : ct.NODE_PROCESS_PARAMS["height"],
                ct.NODE_DECISION_PARAMS["type"] : ct.NODE_DECISION_PARAMS["height"],
                ct.NODE_TERMINATOR_PARAMS["type"] : ct.NODE_TERMINATOR_PARAMS["height"],
                ct.NODE_IO_PARAMS["type"] : ct.NODE_IO_PARAMS["height"],
            }.get(self.type, ct.NODE_DEFAULT_PARAMS["height"])
        else:
            self.h = h

        if text is None:
            self.text = {
                ct.NODE_PROCESS_PARAMS["type"] : ct.NODE_PROCESS_PARAMS["text"],
                ct.NODE_DECISION_PARAMS["type"] : ct.NODE_DECISION_PARAMS["text"],
                ct.NODE_TERMINATOR_PARAMS["type"] : ct.NODE_TERMINATOR_PARAMS["text"],
                ct.NODE_IO_PARAMS["type"] : ct.NODE_IO_PARAMS["text"],
            }.get(self.type, ct.NODE_DEFAULT_PARAMS["text"])
        else:
            self.text = text

        if canvas is not None:
            self.draw(canvas)

    def draw(self, canvas: tk.Canvas):
        # 図形描画（nodeタグを付与）
        if self.type == ct.NODE_PROCESS_PARAMS["type"]:        # 処理
            self.draw_process(canvas)
        elif self.type == ct.NODE_DECISION_PARAMS["type"]:     # 分岐
            self.draw_decision(canvas)  
        elif self.type == ct.NODE_TERMINATOR_PARAMS["type"]:   # 端点
            self.draw_terminator(canvas)
        elif self.type == ct.NODE_IO_PARAMS["type"]:           # 入出力
            self.draw_io(canvas)
        else:                                   # その他（未定義）
            self.draw_undefined(canvas)
        
        self.draw_text(canvas)

    def draw_process(self, canvas: tk.Canvas):
        if self.x and self.y and self.w and self.h:
            left, top, right, bottom = self.x - self.w/2, self.y - self.h/2, self.x + self.w/2, self.y + self.h/2
            self.shape_id = canvas.create_rectangle(
                left, top, right, bottom,
                fill=ct.NODE_PROCESS_PARAMS["fill_color"],
                outline=ct.NODE_PROCESS_PARAMS["outline_color"],
                width=ct.NODE_PROCESS_PARAMS["outline_width"],
                tags=("node", f"node-{self.id}", "node-shape")
            )

    def draw_decision(self, canvas: tk.Canvas):
        if self.x and self.y and self.w and self.h:
            left, top, right, bottom = self.x - self.w/2, self.y - self.h/2, self.x + self.w/2, self.y + self.h/2
            points = [
                self.x, top,
                right, self.y,
                self.x, bottom,
                left, self.y,
            ]
            self.shape_id = canvas.create_polygon(
                points, fill=ct.NODE_DECISION_PARAMS["fill_color"],
                outline=ct.NODE_DECISION_PARAMS["outline_color"],
                width=ct.NODE_DECISION_PARAMS["outline_width"],
                tags=("node", f"node-{self.id}", "node-shape")
            )

    def draw_terminator(self, canvas: tk.Canvas):
        if self.x and self.y and self.w and self.h:
            left, top, right, bottom = self.x - self.w/2, self.y - self.h/2, self.x + self.w/2, self.y + self.h/2
            r = self.h / 2
            points = self.get_rounded_rectangle_coords(left, top, right, bottom, r)
            self.shape_id = canvas.create_polygon(
                points,
                fill=ct.NODE_TERMINATOR_PARAMS["fill_color"],
                outline=ct.NODE_TERMINATOR_PARAMS["outline_color"],
                width=ct.NODE_TERMINATOR_PARAMS["outline_width"],
                tags=("node", f"node-{self.id}", "node-shape")
            )

    def draw_io(self, canvas: tk.Canvas):
        if self.x and self.y and self.w and self.h:
            left, top, right, bottom = self.x - self.w/2, self.y - self.h/2, self.x + self.w/2, self.y + self.h/2
            skew = ct.NODE_IO_PARAMS["skew"]
            points = [
                left + skew, top,
                right, top,
                right - skew, bottom,
                left, bottom,
            ]
            self.shape_id = canvas.create_polygon(
                points,
                fill=ct.NODE_IO_PARAMS["fill_color"],
                outline=ct.NODE_IO_PARAMS["outline_color"],
                width=ct.NODE_IO_PARAMS["outline_width"],
                tags=("node", f"node-{self.id}", "node-shape")
            )

    def draw_undefined(self, canvas: tk.Canvas):
        if self.x and self.y and self.w and self.h:
            left, top, right, bottom = self.x - self.w/2, self.y - self.h/2, self.x + self.w/2, self.y + self.h/2
            self.shape_id = canvas.create_rectangle(
                left, top, right, bottom,
                fill=ct.NODE_DEFAULT_PARAMS["fill_color"],
                outline=ct.NODE_DEFAULT_PARAMS["outline_color"],
                width=ct.NODE_DEFAULT_PARAMS["outline_width"],
            tags=("node", f"node-{self.id}", "node-shape")
        )

    def draw_text(self, canvas: tk.Canvas):
        # テキストの描画（nodeタグを付与）
        if self.x and self.y and self.text:
            font_family, font_size, font_weight, text_width = self._get_text_params()
            self.text_id = canvas.create_text(
                self.x, self.y, text=self.text, font=(font_family, font_size, font_weight), width=text_width,
                tags=("node", f"node-{self.id}", "node-text")
            )
    
    def _get_text_params(self):
        if self.type == ct.NODE_PROCESS_PARAMS["type"]:        # 処理
            font_family, font_size, font_weight, text_width = ct.NODE_PROCESS_PARAMS["font_family"], ct.NODE_PROCESS_PARAMS["font_size"], ct.NODE_PROCESS_PARAMS["font_weight"], ct.NODE_PROCESS_PARAMS["text_width"]
        elif self.type == ct.NODE_DECISION_PARAMS["type"]:     # 分岐
            font_family, font_size, font_weight, text_width = ct.NODE_DECISION_PARAMS["font_family"], ct.NODE_DECISION_PARAMS["font_size"], ct.NODE_DECISION_PARAMS["font_weight"], ct.NODE_DECISION_PARAMS["text_width"]
        elif self.type == ct.NODE_TERMINATOR_PARAMS["type"]:   # 端点
            font_family, font_size, font_weight, text_width = ct.NODE_TERMINATOR_PARAMS["font_family"], ct.NODE_TERMINATOR_PARAMS["font_size"], ct.NODE_TERMINATOR_PARAMS["font_weight"], ct.NODE_TERMINATOR_PARAMS["text_width"]
        elif self.type == ct.NODE_IO_PARAMS["type"]:           # 入出力
            font_family, font_size, font_weight, text_width = ct.NODE_IO_PARAMS["font_family"], ct.NODE_IO_PARAMS["font_size"], ct.NODE_IO_PARAMS["font_weight"], ct.NODE_IO_PARAMS["text_width"]
        else:                                   # その他（未定義）
            font_family, font_size, font_weight, text_width = ct.NODE_DEFAULT_PARAMS["font_family"], ct.NODE_DEFAULT_PARAMS["font_size"], ct.NODE_DEFAULT_PARAMS["font_weight"], ct.NODE_DEFAULT_PARAMS["text_width"]

        return font_family, font_size, font_weight, text_width

    def get_rounded_rectangle_coords(self, left, top, right, bottom, r):
        left_center_x = left + r
        left_center_y = (top + bottom) / 2
        right_center_x = right - r
        right_center_y = (top + bottom) / 2

        coords = []
        angle_step = 10
        coords += [left_center_x, top]
        coords += [right_center_x, top]
        for angle in range(0 + angle_step, 181 - angle_step, angle_step):
            radius = math.radians(angle)
            coords += [right_center_x + r * math.sin(radius), right_center_y - r * math.cos(radius)]
        coords += [right_center_x, bottom]
        coords += [left_center_x, bottom]
        for angle in range(0 + angle_step, 181 - angle_step, angle_step):
            radius = math.radians(angle)
            coords += [left_center_x - r * math.sin(radius), left_center_y + r * math.cos(radius)]

        return coords

    @classmethod
    def get_width_of_type(cls, node_type):
        width = {
            ct.NODE_PROCESS_PARAMS["type"] : ct.NODE_PROCESS_PARAMS["width"],
            ct.NODE_DECISION_PARAMS["type"] : ct.NODE_DECISION_PARAMS["width"],
            ct.NODE_TERMINATOR_PARAMS["type"] : ct.NODE_TERMINATOR_PARAMS["width"],
            ct.NODE_IO_PARAMS["type"] : ct.NODE_IO_PARAMS["width"],
        }.get(node_type, ct.NODE_DEFAULT_PARAMS["width"])
        return width

    @classmethod
    def get_height_of_type(cls, node_type):
        height = {
            ct.NODE_PROCESS_PARAMS["type"] : ct.NODE_PROCESS_PARAMS["height"],
            ct.NODE_DECISION_PARAMS["type"] : ct.NODE_DECISION_PARAMS["height"],
            ct.NODE_TERMINATOR_PARAMS["type"] : ct.NODE_TERMINATOR_PARAMS["height"],
            ct.NODE_IO_PARAMS["type"] : ct.NODE_IO_PARAMS["height"],
        }.get(node_type, ct.NODE_DEFAULT_PARAMS["height"])
        return height
