import tkinter as tk
import constants as ct
import math

class Node:
    id = None
    type = None
    x = None
    y = None
    w = None
    h = None
    text = None
    shape_id = None
    text_id = None

    def __init__(self, node_id, node_type, x:int, y:int, w:int, h:int, text, canvas=None):

        self.id = node_id
        self.type = node_type
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        if text is None:
            self.text = {
                "process": "Process",
                "decision": "Decision?",
                "terminator": "Start / End",
                "io": "Input / Output",
            }.get(self.type, "Undefined")
        else:
            self.text = text

        if canvas is not None:
            self.draw(canvas)

    def draw(self, canvas: tk.Canvas):
        # 図形描画（nodeタグを付与）
        if self.type == ct.TYPE_PROCESS:        # 処理
            self.draw_process(canvas)
        elif self.type == ct.TYPE_DECISION:     # 分岐
            self.draw_decision(canvas)  
        elif self.type == ct.TYPE_TERMINATOR:   # 端点
            self.draw_terminator(canvas)
        elif self.type == ct.TYPE_IO:           # 入出力
            self.draw_io(canvas)
        else:                                   # その他（未定義）
            self.draw_undefined(canvas)
        
        self.draw_text(canvas)

    def draw_process(self, canvas: tk.Canvas):
        if self.x and self.y and self.w and self.h:
            left, top, right, bottom = self.x - self.w/2, self.y - self.h/2, self.x + self.w/2, self.y + self.h/2
            self.shape_id = canvas.create_rectangle(
                left, top, right, bottom,
                fill=ct.PROCESS_DEFAULT_PARAMS["fill_color"], outline=ct.PROCESS_DEFAULT_PARAMS["outline_color"], width=ct.NODE_OUTLINE_WIDTH,
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
                points, fill=ct.DECISION_DEFAULT_PARAMS["fill_color"], outline=ct.DECISION_DEFAULT_PARAMS["outline_color"], width=ct.NODE_OUTLINE_WIDTH,
                tags=("node", f"node-{self.id}", "node-shape")
            )

    def draw_terminator(self, canvas: tk.Canvas):
        if self.x and self.y and self.w and self.h:
            left, top, right, bottom = self.x - self.w/2, self.y - self.h/2, self.x + self.w/2, self.y + self.h/2
            r = self.h / 2
            points = self.get_rounded_rectangle_coords(left, top, right, bottom, r)
            self.shape_id = canvas.create_polygon(
                points,
                fill=ct.TERMINATOR_DEFAULT_PARAMS["fill_color"], outline=ct.TERMINATOR_DEFAULT_PARAMS["outline_color"], width=ct.NODE_OUTLINE_WIDTH,
                tags=("node", f"node-{self.id}", "node-shape")
            )

    def draw_io(self, canvas: tk.Canvas):
        if self.x and self.y and self.w and self.h:
            left, top, right, bottom = self.x - self.w/2, self.y - self.h/2, self.x + self.w/2, self.y + self.h/2
            skew = ct.IO_DEFAULT_PARAMS["skew"]
            points = [
                left + skew, top,
                right, top,
                right - skew, bottom,
                left, bottom,
            ]
            self.shape_id = canvas.create_polygon(
                points,
                fill=ct.IO_DEFAULT_PARAMS["fill_color"], outline=ct.IO_DEFAULT_PARAMS["outline_color"], width=ct.NODE_OUTLINE_WIDTH,
                tags=("node", f"node-{self.id}", "node-shape")
            )

    def draw_undefined(self, canvas: tk.Canvas):
        if self.x and self.y and self.w and self.h:
            left, top, right, bottom = self.x - self.w/2, self.y - self.h/2, self.x + self.w/2, self.y + self.h/2
            self.shape_id = canvas.create_rectangle(
                left, top, right, bottom,
                fill=ct.NODE_FILL_COLOR, outline=ct.NODE_OUTLINE_COLOR, width=ct.NODE_OUTLINE_WIDTH,
            tags=("node", f"node-{self.id}", "node-shape")
        )

    def draw_text(self, canvas: tk.Canvas):
        # テキストの描画（nodeタグを付与）
        if self.x and self.y and self.text:
            self.text_id = canvas.create_text(
                self.x, self.y, text=self.text, font=(ct.TEXT_FONT_FAMILY, ct.TEXT_FONT_SIZE), width=ct.TEXT_WIDTH,
                tags=("node", f"node-{self.id}", "node-text")
            )

    def debug_info(self):
        print(f"Node ID: {self.id}, Type: {self.type}, Position: ({self.x}, {self.y}), Size: ({self.w}, {self.h}), Text: {self.text}")

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
