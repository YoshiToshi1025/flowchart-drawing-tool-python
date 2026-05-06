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
    status = "normal" # "normal", "active", "inactive"

    def __init__(self, node_id, node_type, x:int, y:int, w=None, h=None, shape_type=None, fill_color=None, text=None, status=None, canvas=None):
        # print(f"Creating Node: id={node_id}, type={node_type}, x={x}, y={y}, w={w}, h={h}, shape_type={shape_type}, fill_color={fill_color}, text={text}, status={status}")
        self.id = node_id
        self.type = node_type
        self.x = x
        self.y = y
        self.shape_type = shape_type if self.type == ct.NODE_PROCESS_PARAMS["type"] and shape_type is not None else ct.NODE_PROCESS_PARAMS["shape_type"]
        self.status = status if status is not None else ct.NODE_STATUS_NORMAL

        # print(f"create Node {self.id} initialized with type={self.type}, shape_type={self.shape_type}, status={self.status}")

        if w is None:
            self.w = {
                ct.NODE_PROCESS_PARAMS["type"] : ct.NODE_PROCESS_PARAMS["width"],
                ct.NODE_DECISION_PARAMS["type"] : ct.NODE_DECISION_PARAMS["width"],
                ct.NODE_TERMINATOR_PARAMS["type"] : ct.NODE_TERMINATOR_PARAMS["width"],
                ct.NODE_IO_PARAMS["type"] : ct.NODE_IO_PARAMS["width"],
                ct.NODE_IO_PARAMS["type"] : ct.NODE_IO_PARAMS["width"],
                ct.NODE_STORAGE_PARAMS["type"] : ct.NODE_STORAGE_PARAMS["width"],
                ct.NODE_DOCUMENT_PARAMS["type"] : ct.NODE_DOCUMENT_PARAMS["width"],
            }.get(self.type, ct.NODE_DEFAULT_PARAMS["width"])
        else:
            self.w = w

        if h is None:
            self.h = {
                ct.NODE_PROCESS_PARAMS["type"] : ct.NODE_PROCESS_PARAMS["height"],
                ct.NODE_DECISION_PARAMS["type"] : ct.NODE_DECISION_PARAMS["height"],
                ct.NODE_TERMINATOR_PARAMS["type"] : ct.NODE_TERMINATOR_PARAMS["height"],
                ct.NODE_IO_PARAMS["type"] : ct.NODE_IO_PARAMS["height"],
                ct.NODE_STORAGE_PARAMS["type"] : ct.NODE_STORAGE_PARAMS["height"],
                ct.NODE_DOCUMENT_PARAMS["type"] : ct.NODE_DOCUMENT_PARAMS["height"],
            }.get(self.type, ct.NODE_DEFAULT_PARAMS["height"])
        else:
            self.h = h

        if text is None:
            self.text = {
                ct.NODE_PROCESS_PARAMS["type"] : ct.NODE_PROCESS_PARAMS["text"],
                ct.NODE_DECISION_PARAMS["type"] : ct.NODE_DECISION_PARAMS["text"],
                ct.NODE_TERMINATOR_PARAMS["type"] : ct.NODE_TERMINATOR_PARAMS["text"],
                ct.NODE_IO_PARAMS["type"] : ct.NODE_IO_PARAMS["text"],
                ct.NODE_STORAGE_PARAMS["type"] : ct.NODE_STORAGE_PARAMS["text"],
                ct.NODE_DOCUMENT_PARAMS["type"] : ct.NODE_DOCUMENT_PARAMS["text"],

            }.get(self.type, ct.NODE_DEFAULT_PARAMS["text"])
        else:
            self.text = text

        if fill_color is None:
            self.fill_color = {
                ct.NODE_PROCESS_PARAMS["type"] : ct.NODE_PROCESS_PARAMS["fill_color"],
                ct.NODE_DECISION_PARAMS["type"] : ct.NODE_DECISION_PARAMS["fill_color"],
                ct.NODE_TERMINATOR_PARAMS["type"] : ct.NODE_TERMINATOR_PARAMS["fill_color"],
                ct.NODE_IO_PARAMS["type"] : ct.NODE_IO_PARAMS["fill_color"],
                ct.NODE_STORAGE_PARAMS["type"] : ct.NODE_STORAGE_PARAMS["fill_color"],
                ct.NODE_DOCUMENT_PARAMS["type"] : ct.NODE_DOCUMENT_PARAMS["fill_color"],
            }.get(self.type, ct.NODE_DEFAULT_PARAMS["fill_color"])
        else:
            self.fill_color = fill_color
        # print(f"Node fill_color set to {self.fill_color}")

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
        elif self.type == ct.NODE_STORAGE_PARAMS["type"]:      # ストレージ
            self.draw_storage(canvas)
        elif self.type == ct.NODE_DOCUMENT_PARAMS["type"]:     # ドキュメント
            self.draw_document(canvas)
        else:                                   # その他（未定義）
            self.draw_undefined(canvas)
        
        self.draw_text(canvas)

    def draw_process(self, canvas: tk.Canvas):
        if self.x is not None and self.y is not None and self.w is not None and self.h is not None:
            points = self.get_process_points()
            self.shape_id = canvas.create_polygon(
                points, fill=self.get_fill_color(),
                outline=self.get_outline_color(),
                width=self.get_outline_width(),
                tags=("node", f"node-{self.id}", "node-shape")
            )

    def draw_decision(self, canvas: tk.Canvas):
        if self.x is not None and self.y is not None and self.w is not None and self.h is not None:
            points = self.get_decision_points()
            self.shape_id = canvas.create_polygon(
                points, fill=self.get_fill_color(),
                outline=self.get_outline_color(),
                width=self.get_outline_width(),
                tags=("node", f"node-{self.id}", "node-shape")
            )

    def draw_terminator(self, canvas: tk.Canvas):
        if self.x is not None and self.y is not None and self.w is not None and self.h is not None:
            points = self.get_terminator_points()
            self.shape_id = canvas.create_polygon(
                points, fill=self.get_fill_color(),
                outline=self.get_outline_color(),
                width=self.get_outline_width(),
                tags=("node", f"node-{self.id}", "node-shape")
            )

    def draw_io(self, canvas: tk.Canvas):
        if self.x is not None and self.y is not None and self.w is not None and self.h is not None:
            points = self.get_io_points()
            self.shape_id = canvas.create_polygon(
                points, fill=self.get_fill_color(),
                outline=self.get_outline_color(),
                width=self.get_outline_width(),
                tags=("node", f"node-{self.id}", "node-shape")
            )

    def draw_storage(self, canvas: tk.Canvas):
        if self.x is not None and self.y is not None and self.w is not None and self.h is not None:
            points = self.get_storage_points()
            self.shape_id = canvas.create_polygon(
                points, fill=self.get_fill_color(),
                outline=self.get_outline_color(),
                width=self.get_outline_width(),
                tags=("node", f"node-{self.id}", "node-shape")
            )

    def draw_document(self, canvas: tk.Canvas):
        if self.x is not None and self.y is not None and self.w is not None and self.h is not None:
            points = self.get_document_points()
            self.shape_id = canvas.create_polygon(
                points, fill=self.get_fill_color(),
                outline=self.get_outline_color(),
                width=self.get_outline_width(),
                tags=("node", f"node-{self.id}", "node-shape")
            )

    def draw_undefined(self, canvas: tk.Canvas):
        if self.x is not None and self.y is not None and self.w is not None and self.h is not None:
            points = self.get_undefined_points()
            self.shape_id = canvas.create_polygon(
                points, fill=self.get_fill_color(),
                outline=self.get_outline_color(),
                width=self.get_outline_width(),
            tags=("node", f"node-{self.id}", "node-shape")
        )

    def reset_fill_color(self):
        self.fill_color = None
        return self.get_fill_color()

    def get_fill_color(self):
        print("Get fill color")
        default_fill_color = ct.NODE_DEFAULT_PARAMS["fill_color"]
        default_active_fill_color = ct.NODE_DEFAULT_PARAMS.get("active_fill_color", default_fill_color)
        default_inactive_fill_color = ct.NODE_DEFAULT_PARAMS.get("inactive_fill_color", default_fill_color)

        if self.type == ct.NODE_PROCESS_PARAMS["type"]:        # 処理
            if self.status == "active":
                fill_color = ct.NODE_PROCESS_PARAMS.get("active_fill_color", default_active_fill_color)
            elif self.status == "inactive":
                fill_color = ct.NODE_PROCESS_PARAMS.get("inactive_fill_color", default_inactive_fill_color)
            else:
                fill_color = ct.NODE_PROCESS_PARAMS.get("fill_color", default_fill_color) if self.fill_color is None else self.fill_color
                print(f"A Node {self.id} fill_color for process determined as {fill_color}")
        elif self.type == ct.NODE_DECISION_PARAMS["type"]:     # 分岐
            if self.status == "active":
                fill_color = ct.NODE_DECISION_PARAMS.get("active_fill_color", default_active_fill_color)
            elif self.status == "inactive":
                fill_color = ct.NODE_DECISION_PARAMS.get("inactive_fill_color", default_inactive_fill_color)
            else:
                fill_color = ct.NODE_DECISION_PARAMS.get("fill_color", default_fill_color) if self.fill_color is None else self.fill_color
        elif self.type == ct.NODE_TERMINATOR_PARAMS["type"]:   # 端点
            if self.status == "active":
                fill_color = ct.NODE_TERMINATOR_PARAMS.get("active_fill_color", default_active_fill_color)
            elif self.status == "inactive":
                fill_color = ct.NODE_TERMINATOR_PARAMS.get("inactive_fill_color", default_inactive_fill_color)
            else:
                fill_color = ct.NODE_TERMINATOR_PARAMS.get("fill_color", default_fill_color) if self.fill_color is None else self.fill_color
        elif self.type == ct.NODE_IO_PARAMS["type"]:           # 入出力
            if self.status == "active":
                fill_color = ct.NODE_IO_PARAMS.get("active_fill_color", default_active_fill_color)
            elif self.status == "inactive":
                fill_color = ct.NODE_IO_PARAMS.get("inactive_fill_color", default_inactive_fill_color)
            else:
                fill_color = ct.NODE_IO_PARAMS.get("fill_color", default_fill_color) if self.fill_color is None else self.fill_color
        elif self.type == ct.NODE_STORAGE_PARAMS["type"]:           # ストレージ
            if self.status == "active":
                fill_color = ct.NODE_STORAGE_PARAMS.get("active_fill_color", default_active_fill_color)
            elif self.status == "inactive":
                fill_color = ct.NODE_STORAGE_PARAMS.get("inactive_fill_color", default_inactive_fill_color)
            else:
                fill_color = ct.NODE_STORAGE_PARAMS.get("fill_color", default_fill_color) if self.fill_color is None else self.fill_color
        elif self.type == ct.NODE_DOCUMENT_PARAMS["type"]:           # ドキュメント
            if self.status == "active":
                fill_color = ct.NODE_DOCUMENT_PARAMS.get("active_fill_color", default_active_fill_color)
            elif self.status == "inactive":
                fill_color = ct.NODE_DOCUMENT_PARAMS.get("inactive_fill_color", default_inactive_fill_color)
            else:
                fill_color = ct.NODE_DOCUMENT_PARAMS.get("fill_color", default_fill_color) if self.fill_color is None else self.fill_color
        else:
            if self.status == "active":                        # その他（未定義）
                fill_color = default_active_fill_color
            elif self.status == "inactive":
                fill_color = default_inactive_fill_color
            else:
                fill_color = default_fill_color if self.fill_color is None else self.fill_color

        print(f"Node {self.id} fill_color determined as {fill_color}")
        return fill_color

    def get_outline_color(self):
        default_outline_color = ct.NODE_DEFAULT_PARAMS["outline_color"]
        default_active_outline_color = ct.NODE_DEFAULT_PARAMS.get("active_outline_color", default_outline_color)
        default_inactive_outline_color = ct.NODE_DEFAULT_PARAMS.get("inactive_outline_color", default_outline_color)

        if self.type == ct.NODE_PROCESS_PARAMS["type"]:        # 処理
            if self.status == "active":
                outline_color = ct.NODE_PROCESS_PARAMS.get("active_outline_color", default_active_outline_color)
            elif self.status == "inactive":
                outline_color = ct.NODE_PROCESS_PARAMS.get("inactive_outline_color", default_inactive_outline_color)
            else:
                outline_color = ct.NODE_PROCESS_PARAMS.get("outline_color", default_outline_color)
        elif self.type == ct.NODE_DECISION_PARAMS["type"]:     # 分岐
            if self.status == "active":
                outline_color = ct.NODE_DECISION_PARAMS.get("active_outline_color", default_active_outline_color)
            elif self.status == "inactive":
                outline_color = ct.NODE_DECISION_PARAMS.get("inactive_outline_color", default_inactive_outline_color)
            else:
                outline_color = ct.NODE_DECISION_PARAMS.get("outline_color", default_outline_color)
        elif self.type == ct.NODE_TERMINATOR_PARAMS["type"]:   # 端点
            if self.status == "active":
                outline_color = ct.NODE_TERMINATOR_PARAMS.get("active_outline_color", default_active_outline_color)
            elif self.status == "inactive":
                outline_color = ct.NODE_TERMINATOR_PARAMS.get("inactive_outline_color", default_inactive_outline_color)
            else:
                outline_color = ct.NODE_TERMINATOR_PARAMS.get("outline_color", default_outline_color)
        elif self.type == ct.NODE_IO_PARAMS["type"]:           # 入出力
            if self.status == "active":
                outline_color = ct.NODE_IO_PARAMS.get("active_outline_color", default_active_outline_color)
            elif self.status == "inactive":
                outline_color = ct.NODE_IO_PARAMS.get("inactive_outline_color", default_inactive_outline_color)
            else:
                outline_color = ct.NODE_IO_PARAMS.get("outline_color", default_outline_color)
        elif self.type == ct.NODE_STORAGE_PARAMS["type"]:           # ストレージ
            if self.status == "active":
                outline_color = ct.NODE_STORAGE_PARAMS.get("active_outline_color", default_active_outline_color)
            elif self.status == "inactive":
                outline_color = ct.NODE_STORAGE_PARAMS.get("inactive_outline_color", default_inactive_outline_color)
            else:
                outline_color = ct.NODE_STORAGE_PARAMS.get("outline_color", default_outline_color)
        elif self.type == ct.NODE_DOCUMENT_PARAMS["type"]:           # ドキュメント
            if self.status == "active":
                outline_color = ct.NODE_DOCUMENT_PARAMS.get("active_outline_color", default_active_outline_color)
            elif self.status == "inactive":
                outline_color = ct.NODE_DOCUMENT_PARAMS.get("inactive_outline_color", default_inactive_outline_color)
            else:
                outline_color = ct.NODE_DOCUMENT_PARAMS.get("outline_color", default_outline_color)
        else:
            if self.status == "active":                        # その他（未定義）
                outline_color = default_active_outline_color
            elif self.status == "inactive":
                outline_color = default_inactive_outline_color
            else:
                outline_color = default_outline_color

        return outline_color
    
    def get_outline_width(self):
        default_outline_width = ct.NODE_DEFAULT_PARAMS["outline_width"]
        default_active_outline_width = ct.NODE_DEFAULT_PARAMS.get("active_outline_width", default_outline_width)
        default_inactive_outline_width = ct.NODE_DEFAULT_PARAMS.get("inactive_outline_width", default_outline_width)

        if self.type == ct.NODE_PROCESS_PARAMS["type"]:        # 処理
            if self.status == "active":
                outline_width = ct.NODE_PROCESS_PARAMS.get("active_outline_width", default_active_outline_width)
            elif self.status == "inactive":
                outline_width = ct.NODE_PROCESS_PARAMS.get("inactive_outline_width", default_inactive_outline_width)
            else:
                outline_width = ct.NODE_PROCESS_PARAMS.get("outline_width", default_outline_width)
        elif self.type == ct.NODE_DECISION_PARAMS["type"]:     # 分岐
            if self.status == "active":
                outline_width = ct.NODE_DECISION_PARAMS.get("active_outline_width", default_active_outline_width)
            elif self.status == "inactive":
                outline_width = ct.NODE_DECISION_PARAMS.get("inactive_outline_width", default_inactive_outline_width)
            else:
                outline_width = ct.NODE_DECISION_PARAMS.get("outline_width", default_outline_width)
        elif self.type == ct.NODE_TERMINATOR_PARAMS["type"]:   # 端点
            if self.status == "active":
                outline_width = ct.NODE_TERMINATOR_PARAMS.get("active_outline_width", default_active_outline_width)
            elif self.status == "inactive":
                outline_width = ct.NODE_TERMINATOR_PARAMS.get("inactive_outline_width", default_inactive_outline_width)
            else:
                outline_width = ct.NODE_TERMINATOR_PARAMS.get("outline_width", default_outline_width)
        elif self.type == ct.NODE_IO_PARAMS["type"]:           # 入出力
            if self.status == "active":
                outline_width = ct.NODE_IO_PARAMS.get("active_outline_width", default_active_outline_width)
            elif self.status == "inactive":
                outline_width = ct.NODE_IO_PARAMS.get("inactive_outline_width", default_inactive_outline_width)
            else:
                outline_width = ct.NODE_IO_PARAMS.get("outline_width", default_outline_width)
        elif self.type == ct.NODE_STORAGE_PARAMS["type"]:           # ストレージ
            if self.status == "active":
                outline_width = ct.NODE_STORAGE_PARAMS.get("active_outline_width", default_active_outline_width)
            elif self.status == "inactive":
                outline_width = ct.NODE_STORAGE_PARAMS.get("inactive_outline_width", default_inactive_outline_width)
            else:
                outline_width = ct.NODE_STORAGE_PARAMS.get("outline_width", default_outline_width)
        elif self.type == ct.NODE_DOCUMENT_PARAMS["type"]:           # ドキュメント
            if self.status == "active":
                outline_width = ct.NODE_DOCUMENT_PARAMS.get("active_outline_width", default_active_outline_width)
            elif self.status == "inactive":
                outline_width = ct.NODE_DOCUMENT_PARAMS.get("inactive_outline_width", default_inactive_outline_width)
            else:
                outline_width = ct.NODE_DOCUMENT_PARAMS.get("outline_width", default_outline_width)
        else:
            if self.status == "active":                        # その他（未定義）
                outline_width = default_active_outline_width
            elif self.status == "inactive":
                outline_width = default_inactive_outline_width
            else:
                outline_width = default_outline_width

        return outline_width

    def get_text_color(self):
        default_text_color = ct.NODE_DEFAULT_PARAMS["text_color"]
        default_active_text_color = ct.NODE_DEFAULT_PARAMS.get("active_text_color", default_text_color)
        default_inactive_text_color = ct.NODE_DEFAULT_PARAMS.get("inactive_text_color", default_text_color)

        if self.type == ct.NODE_PROCESS_PARAMS["type"]:        # 処理
            if self.status == "active":
                text_color = ct.NODE_PROCESS_PARAMS.get("active_text_color", default_active_text_color)
            elif self.status == "inactive":
                text_color = ct.NODE_PROCESS_PARAMS.get("inactive_text_color", default_inactive_text_color)
            else:
                text_color = ct.NODE_PROCESS_PARAMS.get("text_color", default_text_color)
        elif self.type == ct.NODE_DECISION_PARAMS["type"]:     # 分岐
            if self.status == "active":
                text_color = ct.NODE_DECISION_PARAMS.get("active_text_color", default_active_text_color)
            elif self.status == "inactive":
                text_color = ct.NODE_DECISION_PARAMS.get("inactive_text_color", default_inactive_text_color)
            else:
                text_color = ct.NODE_DECISION_PARAMS.get("text_color", default_text_color)
        elif self.type == ct.NODE_TERMINATOR_PARAMS["type"]:   # 端点
            if self.status == "active":
                text_color = ct.NODE_TERMINATOR_PARAMS.get("active_text_color", default_active_text_color)
            elif self.status == "inactive":
                text_color = ct.NODE_TERMINATOR_PARAMS.get("inactive_text_color", default_inactive_text_color)
            else:
                text_color = ct.NODE_TERMINATOR_PARAMS.get("text_color", default_text_color)
        elif self.type == ct.NODE_IO_PARAMS["type"]:           # 入出力
            if self.status == "active":
                text_color = ct.NODE_IO_PARAMS.get("active_text_color", default_active_text_color)
            elif self.status == "inactive":
                text_color = ct.NODE_IO_PARAMS.get("inactive_text_color", default_inactive_text_color)
            else:
                text_color = ct.NODE_IO_PARAMS.get("text_color", default_text_color)
        elif self.type == ct.NODE_STORAGE_PARAMS["type"]:           # ストレージ
            if self.status == "active":
                text_color = ct.NODE_STORAGE_PARAMS.get("active_text_color", default_active_text_color)
            elif self.status == "inactive":
                text_color = ct.NODE_STORAGE_PARAMS.get("inactive_text_color", default_inactive_text_color)
            else:
                text_color = ct.NODE_STORAGE_PARAMS.get("text_color", default_text_color)
        elif self.type == ct.NODE_DOCUMENT_PARAMS["type"]:           # ドキュメント
            if self.status == "active":
                text_color = ct.NODE_DOCUMENT_PARAMS.get("active_text_color", default_active_text_color)
            elif self.status == "inactive":
                text_color = ct.NODE_DOCUMENT_PARAMS.get("inactive_text_color", default_inactive_text_color)
            else:
                text_color = ct.NODE_DOCUMENT_PARAMS.get("text_color", default_text_color)
        else:
            if self.status == "active":                        # その他（未定義）
                text_color = default_active_text_color
            elif self.status == "inactive":
                text_color = default_inactive_text_color
            else:
                text_color = default_text_color

        return text_color

    def get_text_font_weight(self):
        default_font_weight = ct.NODE_DEFAULT_PARAMS["font_weight"]
        default_active_font_weight = ct.NODE_DEFAULT_PARAMS.get("active_font_weight", default_font_weight)
        default_inactive_font_weight = ct.NODE_DEFAULT_PARAMS.get("inactive_font_weight", default_font_weight)

        if self.type == ct.NODE_PROCESS_PARAMS["type"]:        # 処理
            if self.status == "active":
                font_weight = ct.NODE_PROCESS_PARAMS.get("active_font_weight", default_active_font_weight)
            elif self.status == "inactive":
                font_weight = ct.NODE_PROCESS_PARAMS.get("inactive_font_weight", default_inactive_font_weight)
            else:
                font_weight = ct.NODE_PROCESS_PARAMS.get("font_weight", default_font_weight)
        elif self.type == ct.NODE_DECISION_PARAMS["type"]:     # 分岐
            if self.status == "active":
                font_weight = ct.NODE_DECISION_PARAMS.get("active_font_weight", default_active_font_weight)
            elif self.status == "inactive":
                font_weight = ct.NODE_DECISION_PARAMS.get("inactive_font_weight", default_inactive_font_weight)
            else:
                font_weight = ct.NODE_DECISION_PARAMS.get("font_weight", default_font_weight)
        elif self.type == ct.NODE_TERMINATOR_PARAMS["type"]:   # 端点
            if self.status == "active":
                font_weight = ct.NODE_TERMINATOR_PARAMS.get("active_font_weight", default_active_font_weight)
            elif self.status == "inactive":
                font_weight = ct.NODE_TERMINATOR_PARAMS.get("inactive_font_weight", default_inactive_font_weight)
            else:
                font_weight = ct.NODE_TERMINATOR_PARAMS.get("font_weight", default_font_weight)
        elif self.type == ct.NODE_IO_PARAMS["type"]:           # 入出力
            if self.status == "active":
                font_weight = ct.NODE_IO_PARAMS.get("active_font_weight", default_active_font_weight)
            elif self.status == "inactive":
                font_weight = ct.NODE_IO_PARAMS.get("inactive_font_weight", default_inactive_font_weight)
            else:
                font_weight = ct.NODE_IO_PARAMS.get("font_weight", default_font_weight)
        elif self.type == ct.NODE_STORAGE_PARAMS["type"]:           # 入出力
            if self.status == "active":
                font_weight = ct.NODE_STORAGE_PARAMS.get("active_font_weight", default_active_font_weight)
            elif self.status == "inactive":
                font_weight = ct.NODE_STORAGE_PARAMS.get("inactive_font_weight", default_inactive_font_weight)
            else:
                font_weight = ct.NODE_STORAGE_PARAMS.get("font_weight", default_font_weight)
        elif self.type == ct.NODE_DOCUMENT_PARAMS["type"]:           # 入出力
            if self.status == "active":
                font_weight = ct.NODE_DOCUMENT_PARAMS.get("active_font_weight", default_active_font_weight)
            elif self.status == "inactive":
                font_weight = ct.NODE_DOCUMENT_PARAMS.get("inactive_font_weight", default_inactive_font_weight)
            else:
                font_weight = ct.NODE_DOCUMENT_PARAMS.get("font_weight", default_font_weight)
        else:
            if self.status == "active":                        # その他（未定義）
                font_weight = default_active_font_weight
            elif self.status == "inactive":
                font_weight = default_inactive_font_weight
            else:
                font_weight = default_font_weight

        return font_weight

    def get_process_points(self):
        # print(f"Calculating process points for Node {self.id} with shape_type={self.shape_type}")

        left, top, right, bottom = self.x - self.w/2, self.y - self.h/2, self.x + self.w/2, self.y + self.h/2
        shape_type = self.shape_type if self.shape_type is not None else ct.NODE_PROCESS_PARAMS["shape_type"]
        if shape_type == "rounded_rectangle":
            points = self.get_rounded_rectangle_coords(left, top, right, bottom)
        elif shape_type == "corner_rounded_rectangle":
            points = self.get_corner_rounded_rectangle_coords(left, top, right, bottom)
        elif shape_type == "ellipse":
            points = self.get_ellipse_coords(left, top, right, bottom)
        else:
            points = self.get_rectangle_coords(left, top, right, bottom)
        return points

    def get_decision_points(self):
        left, top, right, bottom = self.x - self.w/2, self.y - self.h/2, self.x + self.w/2, self.y + self.h/2
        return [
            self.x, top,
            right, self.y,
            self.x, bottom,
            left, self.y,
        ]

    def get_terminator_points(self):
        left, top, right, bottom = self.x - self.w/2, self.y - self.h/2, self.x + self.w/2, self.y + self.h/2
        return self.get_rounded_rectangle_coords(left, top, right, bottom)

    def get_io_points(self):
        left, top, right, bottom = self.x - self.w/2, self.y - self.h/2, self.x + self.w/2, self.y + self.h/2
        skew = ct.NODE_IO_PARAMS["skew"]
        return [
            left + skew, top,
            right, top,
            right - skew, bottom,
            left, bottom,
        ]

    def get_storage_points(self):
        left, top, right, bottom = self.x - self.w/2, self.y - self.h/2, self.x + self.w/2, self.y + self.h/2
        points = self.get_storage_coords(left, top, right, bottom)
        return points

    def get_document_points(self):
        left, top, right, bottom = self.x - self.w/2, self.y - self.h/2, self.x + self.w/2, self.y + self.h/2
        points = self.get_document_coords(left, top, right, bottom)
        return points

    def get_undefined_points(self):
        left, top, right, bottom = self.x - self.w/2, self.y - self.h/2, self.x + self.w/2, self.y + self.h/2
        return [
            left, top,
            right, top,
            right, bottom,
            left, bottom,
        ]

    def draw_text(self, canvas: tk.Canvas):
        # テキストの描画（nodeタグを付与）
        if self.x is not None and self.y is not None and self.text is not None:
            font_family, font_size, font_weight, text_width, text_color = self._get_text_params()
            if self.type == ct.NODE_STORAGE_PARAMS["type"]:      # ストレージ
                self.text_id = canvas.create_text(
                    self.x, self.y + self.h / 10, text=self.text, font=(font_family, font_size, font_weight), width=text_width,
                    fill=text_color,
                    tags=("node", f"node-{self.id}", "node-text")
                )
            elif self.type == ct.NODE_DOCUMENT_PARAMS["type"]:      # ドキュメント
                self.text_id = canvas.create_text(
                    self.x, self.y - self.h / 10, text=self.text, font=(font_family, font_size, font_weight), width=text_width,
                    fill=text_color,
                    tags=("node", f"node-{self.id}", "node-text")
                )
            else:
                self.text_id = canvas.create_text(
                    self.x, self.y, text=self.text, font=(font_family, font_size, font_weight), width=text_width,
                    fill=text_color,
                    tags=("node", f"node-{self.id}", "node-text")
                )
    
    def _get_text_params(self):
        if self.type == ct.NODE_PROCESS_PARAMS["type"]:        # 処理
            font_family, font_size, text_width  = ct.NODE_PROCESS_PARAMS["font_family"], ct.NODE_PROCESS_PARAMS["font_size"], ct.NODE_PROCESS_PARAMS["text_width"]
        elif self.type == ct.NODE_DECISION_PARAMS["type"]:     # 分岐
            font_family, font_size, text_width = ct.NODE_DECISION_PARAMS["font_family"], ct.NODE_DECISION_PARAMS["font_size"], ct.NODE_DECISION_PARAMS["text_width"]
        elif self.type == ct.NODE_TERMINATOR_PARAMS["type"]:   # 端点
            font_family, font_size, text_width = ct.NODE_TERMINATOR_PARAMS["font_family"], ct.NODE_TERMINATOR_PARAMS["font_size"], ct.NODE_TERMINATOR_PARAMS["text_width"]
        elif self.type == ct.NODE_IO_PARAMS["type"]:           # 入出力
            font_family, font_size, text_width = ct.NODE_IO_PARAMS["font_family"], ct.NODE_IO_PARAMS["font_size"], ct.NODE_IO_PARAMS["text_width"]
        elif self.type == ct.NODE_STORAGE_PARAMS["type"]:      # ストレージ
            font_family, font_size, text_width = ct.NODE_STORAGE_PARAMS["font_family"], ct.NODE_STORAGE_PARAMS["font_size"], ct.NODE_STORAGE_PARAMS["text_width"]
        elif self.type == ct.NODE_DOCUMENT_PARAMS["type"]:     # ドキュメント
            font_family, font_size, text_width = ct.NODE_DOCUMENT_PARAMS["font_family"], ct.NODE_DOCUMENT_PARAMS["font_size"], ct.NODE_DOCUMENT_PARAMS["text_width"]
        else:                                   # その他（未定義）
            font_family, font_size, text_width = ct.NODE_DEFAULT_PARAMS["font_family"], ct.NODE_DEFAULT_PARAMS["font_size"], ct.NODE_DEFAULT_PARAMS["text_width"]

        font_weight = self.get_text_font_weight()
        text_color = self.get_text_color()

        return font_family, font_size, font_weight, text_width, text_color

    def get_rectangle_coords(self, left, top, right, bottom):
        return [left, top, right, top, right, bottom, left, bottom]

    def get_rounded_rectangle_coords(self, left, top, right, bottom):
        r = self.h / 2
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

    def get_corner_rounded_rectangle_coords(self, left, top, right, bottom):
        r = self.round_half_up(self.h / 5)
        if r < 0 or r > min((right - left)/2, (bottom - top)/2):
            return [left, top, right, top, right, bottom, left, bottom]

        coords = []
        angle_step = 15
        coords += [left + r, top]
        coords += [right - r, top]
        for angle in range(0 + angle_step, 91 - angle_step, angle_step):
            # print(f"Calculating top-right corner: angle={angle}")
            radius = math.radians(angle)
            coords += [right - r + r * math.sin(radius), top + r - r * math.cos(radius)]
        coords += [right, top + r]
        coords += [right, bottom - r]
        for angle in range(90 + angle_step, 181 - angle_step, angle_step):
            radius = math.radians(angle)
            coords += [right - r + r * math.sin(radius), bottom - r - r * math.cos(radius)]
        coords += [right - r, bottom]
        coords += [left + r, bottom]
        for angle in range(180 + angle_step, 271 - angle_step, angle_step):
            radius = math.radians(angle)
            coords += [left + r + r * math.sin(radius), bottom - r - r * math.cos(radius)]
        coords += [left, bottom - r]
        coords += [left, top + r]
        for angle in range(270 + angle_step, 361 - angle_step, angle_step):
            radius = math.radians(angle)
            coords += [left + r + r * math.sin(radius), top + r - r * math.cos(radius)]
        return coords
    
    def get_ellipse_coords(self, left, top, right, bottom):
        rw = self.w / 2
        rh = self.h / 2
        x = (left + right) / 2
        y = (top + bottom) / 2

        coords = []
        angle_step = 5
        for angle in range(0, 361, angle_step):
            radius = math.radians(angle)
            coords += [x - rw * math.cos(radius), y - rh * math.sin(radius)]

        return coords

    def get_storage_coords(self, left, top, right, bottom):
        r = self.w / 2
        x = (left + right) /2
        y1 = top + r / 5
        y2 = bottom - r / 5

        coords = [left, y1]
        angle_step = 5
        for angle in range(0 + angle_step, 361 - angle_step, angle_step):
            radius = math.radians(angle)
            coords += [x - r * math.cos(radius), y1 - r / 5 * math.sin(radius)]
        for angle in range(360 - angle_step, 179 + angle_step, -angle_step):
            radius = math.radians(angle)
            coords += [x - r * math.cos(radius), y1 - r / 5 * math.sin(radius)]
        coords += [right, y1]
        coords += [right, y2]
        for angle in range(180 + angle_step, 361 - angle_step, angle_step):
            radius = math.radians(angle)
            coords += [x - r * math.cos(radius), y2 - r / 5 * math.sin(radius)]
        coords += [left, y2]
        coords += [left, y1]

        return coords

    def get_document_coords(self, left, top, right, bottom):
        r = self.w / 3.9

        x = (left + right) / 2
        x1 = (3 * left + right) / 4
        x2 = (left + 3 * right) / 4
        y = bottom - r / 3

        coords = []
        angle_step = 5
        coords += [left, top]
        coords += [right, top]
        coords += [right, y]
        for angle in range(150 - angle_step, 30 + angle_step, -angle_step):
            radius = math.radians(angle)
            coords += [x2 - r * math.cos(radius), y - r / 3 * math.sin(radius) + 4]
        coords += [x, y]
        for angle in range(210 + angle_step, 351 - angle_step, angle_step):
            radius = math.radians(angle)
            coords += [x1 - r * math.cos(radius), y - r / 3 * math.sin(radius) - 4]
        coords += [left, y]
        coords += [left, top]

        return coords

    def to_dict(self):
        node_data = {
            "id": self.id,
            "type": self.type,
            "x": self.x,
            "y": self.y,
            "w": self.w,
            "h": self.h,
            "shape_type": self.shape_type,
            "text": self.text,
        }
        if self.fill_color is not None:
            node_data["fill_color"] = self.fill_color
        if self.status is not None and self.status != ct.NODE_STATUS_NORMAL:
            node_data["status"] = self.status

        return node_data

    @staticmethod
    def round_half_up(value):
        return math.floor(value + 0.5)

    @classmethod
    def get_width_of_type(cls, node_type):
        width = {
            ct.NODE_PROCESS_PARAMS["type"] : ct.NODE_PROCESS_PARAMS["width"],
            ct.NODE_DECISION_PARAMS["type"] : ct.NODE_DECISION_PARAMS["width"],
            ct.NODE_TERMINATOR_PARAMS["type"] : ct.NODE_TERMINATOR_PARAMS["width"],
            ct.NODE_IO_PARAMS["type"] : ct.NODE_IO_PARAMS["width"],
            ct.NODE_STORAGE_PARAMS["type"] : ct.NODE_STORAGE_PARAMS["width"],
            ct.NODE_DOCUMENT_PARAMS["type"] : ct.NODE_DOCUMENT_PARAMS["width"],
        }.get(node_type, ct.NODE_DEFAULT_PARAMS["width"])
        return width

    @classmethod
    def get_height_of_type(cls, node_type):
        height = {
            ct.NODE_PROCESS_PARAMS["type"] : ct.NODE_PROCESS_PARAMS["height"],
            ct.NODE_DECISION_PARAMS["type"] : ct.NODE_DECISION_PARAMS["height"],
            ct.NODE_TERMINATOR_PARAMS["type"] : ct.NODE_TERMINATOR_PARAMS["height"],
            ct.NODE_IO_PARAMS["type"] : ct.NODE_IO_PARAMS["height"],
            ct.NODE_STORAGE_PARAMS["type"] : ct.NODE_STORAGE_PARAMS["height"],
            ct.NODE_DOCUMENT_PARAMS["type"] : ct.NODE_DOCUMENT_PARAMS["height"],
        }.get(node_type, ct.NODE_DEFAULT_PARAMS["height"])
        return height
