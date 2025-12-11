import tkinter as tk
import constants as ct
import node
from typing import Literal

class Edge:
    line_id = None
    from_node_obj = None
    to_node_obj = None
    points = []  # List of (x, y) tuples
    label_id = None
    label_x = None
    label_y = None
    label_text = None
    anchor:Literal["center", "n", "ne", "e", "se", "s", "sw", "w", "nw"] = "center"
    justify:Literal["left", "center", "right"] = "left"

    def __init__(self, from_node_obj, to_node_obj, points=None, text=None, label_x=None, label_y=None, canvas=None,\
                    anchor:Literal["center", "n", "ne", "e", "se", "s", "sw", "w", "nw"]="center", \
                    justify:Literal["left", "center", "right"]="left"):
        self.from_node_obj = from_node_obj
        self.to_node_obj = to_node_obj
        self.label_text = text
        self.anchor = anchor
        self.justify = justify

        if points is None:
            # かぎ線の座標とラベル位置を計算
            self._compute_edge_geometry(from_node_obj, to_node_obj)
        else:
            self.points = points  # List of (x, y) tuples
            self.label_x = label_x
            self.label_y = label_y

        if canvas is not None:
            self.draw(canvas, from_node_obj, to_node_obj, text)

    def draw(self, canvas:tk.Canvas, from_node_obj, to_node_obj, text=None):
        """エッジとラベルの描画"""
        # エッジの描画
        self.draw_edge(canvas, from_node_obj, to_node_obj)
        # ラベルの描画
        if self.line_id is not None:
            self.draw_label(canvas, from_node_obj)

    def draw_edge(self, canvas:tk.Canvas, from_node_obj, to_node_obj):
        """エッジの描画"""
        self.line_id = canvas.create_line(
            *self.points,
            arrow=tk.LAST, width=ct.EDGE_WIDTH, fill=ct.EDGE_COLOR,
            tags=("edge", f"edge-{self.line_id}")
        )
        # エッジはノードの下に
        canvas.tag_lower(self.line_id, "node")

    def draw_label(self, canvas:tk.Canvas, from_node_obj):
        """エッジラベルの描画"""

        if self.label_x is not None and self.label_y is not None and self.label_text is not None:
            self.label_id = canvas.create_text(
                self.label_x, self.label_y,
                text=self.label_text,
                font=(ct.TEXT_FONT_FAMILY, ct.TEXT_FONT_SIZE), width=ct.TEXT_WIDTH,
                fill=ct.TEXT_COLOR, anchor = self.anchor, justify = self.justify,
                tags=("edge-label",)
            )
            # ラベルもノードの下でOK（少し上に描かれるので視認性は保てる）
            canvas.tag_lower(self.label_id, "node")

    def _compute_edge_geometry(self, from_node_obj: node.Node, to_node_obj: node.Node):
        """かぎ線の3点座標とラベル位置を計算"""
        # 各ノードのアンカーとラベル位置を設定
        self.points, self.label_x, self.label_y, self.anchor, self.justify = self.rect_anchor(from_node_obj, to_node_obj)

        return self.points, self.label_x, self.label_y, self.anchor, self.justify

    # --- rectAnchor: 矩形の境界上にアンカーを取る ---
    def rect_anchor(self, from_node_obj, to_node_obj):
        coords = []
        if from_node_obj.x is None or from_node_obj.y is None or from_node_obj.h is None or from_node_obj.w is None:
            return coords, None, None, None, None
        if to_node_obj.x is None or to_node_obj.y is None or to_node_obj.h is None or to_node_obj.w is None:
            return coords, None, None, None, None

        from_center_x, from_center_y, from_width, from_height = from_node_obj.x, from_node_obj.y, from_node_obj.w, from_node_obj.h
        from_top_x, from_top_y = from_center_x, from_center_y - from_height / 2
        from_bottom_x, from_bottom_y = from_center_x, from_center_y + from_height / 2
        from_left_x, from_left_y = from_center_x - from_width / 2, from_center_y
        from_right_x, from_right_y = from_center_x + from_width / 2, from_center_y

        to_center_x, to_center_y, to_width, to_height = to_node_obj.x, to_node_obj.y, to_node_obj.w, to_node_obj.h
        to_top_x, to_top_y = to_center_x, to_center_y - to_height / 2
        to_bottom_x, to_bottom_y = to_center_x, to_center_y + to_height / 2
        to_left_x, to_left_y = to_center_x - to_width / 2, to_center_y
        to_right_x, to_right_y = to_center_x + to_width / 2, to_center_y

        from_type = from_node_obj.type
        label_x = None
        label_y = None
        anchor = "center"
        justify = "left"

        if from_type == ct.TYPE_DECISION:
            if from_left_x <= to_top_x <= from_right_x and from_bottom_y < to_top_y:
                coords = self.rect_anchor_bottom_to_top(from_node_obj, to_node_obj)
                if coords is not None and coords != []:
                    label_x = coords[0] + 6
                    label_y = coords[1] + 8
                anchor = "nw"
            elif from_right_x < to_left_x and to_top_y <= from_bottom_y:
                coords = self.rect_anchor_right_to_left(from_node_obj, to_node_obj)
                if coords is not None and coords != []:
                    label_x = coords[0] + 8
                    label_y = coords[1]
                anchor = "sw"
            elif from_right_x < to_top_x and from_right_y < to_left_y:
                coords = self.rect_anchor_right_to_top(from_node_obj, to_node_obj)
                if coords is not None and coords != []:
                    label_x = coords[0] + 8
                    label_y = coords[1]
                anchor= "sw"
            elif to_right_x < from_left_x and to_top_y <= from_bottom_y:
                coords = self.rect_anchor_left_to_right(from_node_obj, to_node_obj)
                if coords is not None and coords != []:
                    label_x = coords[0] - 8
                    label_y = coords[1]
                anchor = "se"
            elif to_top_x < from_left_x and from_right_y < to_left_y:
                coords = self.rect_anchor_left_to_top(from_node_obj, to_node_obj)
                if coords is not None and coords != []:
                    label_x = coords[0] - 8
                    label_y = coords[1]
                anchor = "se"
            elif to_bottom_y <= from_top_y:
                if to_bottom_x < from_top_x:
                    coords = self.rect_anchor_right_to_right(from_node_obj, to_node_obj)
                    if coords is not None and coords != []:
                        label_x = coords[0] + 8
                        label_y = coords[1]
                    anchor = "sw"
                else:
                    coords = self.rect_anchor_left_to_left(from_node_obj, to_node_obj)
                    if coords is not None and coords != []:
                        label_x = coords[0] - 8
                        label_y = coords[1]
                    anchor = "se"
        else:
            if from_bottom_y < to_top_y <= from_bottom_y + ct.GRID_SPACING * 2:
                if to_right_x < from_left_x:
                    coords = self.rect_anchor_bottom_to_right(from_node_obj, to_node_obj)
                    if coords is not None and coords != []:
                        label_x = coords[0] + 6
                        label_y = coords[1] + 8
                    anchor = "nw"
                elif from_right_x < to_left_x:
                    coords = self.rect_anchor_bottom_to_left(from_node_obj, to_node_obj)
                    if coords is not None and coords != []:
                        label_x = coords[0] + 6
                        label_y = coords[1] + 8
                    anchor = "nw"
                else:
                    coords = self.rect_anchor_bottom_to_top(from_node_obj, to_node_obj)
                    if coords is not None and coords != []:
                        label_x = coords[0] + 6
                        label_y = coords[1] + 8
                    anchor = "nw"
            elif from_bottom_y < to_top_y:
                coords = self.rect_anchor_bottom_to_top(from_node_obj, to_node_obj)
                if coords is not None and coords != []:
                    label_x = coords[0] + 6
                    label_y = coords[1] + 8
                anchor = "nw"
            elif from_right_x < to_left_x and to_top_y <= from_bottom_y:
                coords = self.rect_anchor_right_to_left(from_node_obj, to_node_obj)
                if coords is not None and coords != []:
                    label_x = coords[0] + 8
                    label_y = coords[1]
                anchor = "sw"
            elif to_right_x < from_left_x and to_top_y <= from_bottom_y:
                coords = self.rect_anchor_left_to_right(from_node_obj, to_node_obj)
                if coords is not None and coords != []:
                    label_x = coords[0] - 8
                    label_y = coords[1]
                anchor = "se"
            elif to_bottom_y <= from_top_y:
                if to_bottom_x < from_top_x:
                    coords = self.rect_anchor_right_to_right(from_node_obj, to_node_obj)
                    if coords is not None and coords != []:
                        label_x = coords[0] + 8
                        label_y = coords[1]
                    anchor = "sw"
                else:
                    coords = self.rect_anchor_left_to_left(from_node_obj, to_node_obj)
                    if coords is not None and coords != []:
                        label_x = coords[0] - 8
                        label_y = coords[1]
                    anchor = "se"

        if coords == [] or coords is None:
            coords = self.line_anchor(from_node_obj, to_node_obj)

        if coords is not None and coords != [] and (label_x is None or label_y is None):
            label_x = (coords[0] + coords[2]) / 2
            label_y = (coords[1] + coords[3]) / 2 - 8
            anchor = "center"
            justify = "center"

        return coords, label_x, label_y, anchor, justify

    def rect_anchor_bottom_to_top(self, from_node_obj, to_node_obj):
        # bottom_to_top     1line or 3line
        # 条件: toオブジェクトがfromオブジェクトの下にある、fromオブジェクトとtoオブジェクトは接していない
        #          fromオブジェクトのbottom点がtoオブジェクトの幅の中にある場合、1line
        #          fromオブジェクトのbottom点がtoオブジェクトの幅の外にある場合、3line
        coords = []
        if from_node_obj.x is None or from_node_obj.y is None or from_node_obj.h is None or from_node_obj.w is None:
            return coords
        if to_node_obj.x is None or to_node_obj.y is None or to_node_obj.h is None or to_node_obj.w is None:
            return coords

        from_center_x, from_center_y, from_width, from_height = from_node_obj.x, from_node_obj.y, from_node_obj.w, from_node_obj.h
        from_top_x, from_top_y = from_center_x, from_center_y - from_height / 2
        from_bottom_x, from_bottom_y = from_center_x, from_center_y + from_height / 2
        from_left_x, from_left_y = from_center_x - from_width / 2, from_center_y
        from_right_x, from_right_y = from_center_x + from_width / 2, from_center_y

        to_center_x, to_center_y, to_width, to_height = to_node_obj.x, to_node_obj.y, to_node_obj.w, to_node_obj.h
        to_top_x, to_top_y = to_center_x, to_center_y - to_height / 2
        to_bottom_x, to_bottom_y = to_center_x, to_center_y + to_height / 2
        to_left_x, to_left_y = to_center_x - to_width / 2, to_center_y
        to_right_x, to_right_y = to_center_x + to_width / 2, to_center_y

        if to_top_y >= from_bottom_y:
            if from_bottom_x == to_top_x:
                # 1line
                coords = [from_bottom_x, from_bottom_y, to_top_x, to_top_y]
            else:
                # 3line
                mid_y = (from_bottom_y + to_top_y) / 2
                coords = [from_bottom_x, from_bottom_y, from_bottom_x, mid_y, to_top_x, mid_y, to_top_x, to_top_y]

        return coords

    def rect_anchor_bottom_to_right(self, from_node_obj, to_node_obj):
        # bottom_to_right   2line
        # 条件： toオブジェクトの右点がfromオブジェクトの下点より左下にある場合、2line
        coords = []
        if from_node_obj.x is None or from_node_obj.y is None or from_node_obj.h is None or from_node_obj.w is None:
            return coords
        if to_node_obj.x is None or to_node_obj.y is None or to_node_obj.h is None or to_node_obj.w is None:
            return coords

        from_center_x, from_center_y, from_width, from_height = from_node_obj.x, from_node_obj.y, from_node_obj.w, from_node_obj.h
        from_top_x, from_top_y = from_center_x, from_center_y - from_height / 2
        from_bottom_x, from_bottom_y = from_center_x, from_center_y + from_height / 2
        from_left_x, from_left_y = from_center_x - from_width / 2, from_center_y
        from_right_x, from_right_y = from_center_x + from_width / 2, from_center_y

        to_center_x, to_center_y, to_width, to_height = to_node_obj.x, to_node_obj.y, to_node_obj.w, to_node_obj.h
        to_top_x, to_top_y = to_center_x, to_center_y - to_height / 2
        to_bottom_x, to_bottom_y = to_center_x, to_center_y + to_height / 2
        to_left_x, to_left_y = to_center_x - to_width / 2, to_center_y
        to_right_x, to_right_y = to_center_x + to_width / 2, to_center_y

        if to_right_x < from_bottom_x and to_right_y > from_bottom_y:
            coords = [from_bottom_x, from_bottom_y, from_bottom_x, to_right_y, to_right_x, to_right_y]

        return coords

    def rect_anchor_bottom_to_left(self, from_node_obj, to_node_obj):
        # bottom_to_left    2line
        # 条件： toオブジェクトの左点がfromオブジェクトの下点より左下にある場合、2line
        coords = []
        if from_node_obj.x is None or from_node_obj.y is None or from_node_obj.h is None or from_node_obj.w is None:
            return coords
        if to_node_obj.x is None or to_node_obj.y is None or to_node_obj.h is None or to_node_obj.w is None:
            return coords

        from_center_x, from_center_y, from_width, from_height = from_node_obj.x, from_node_obj.y, from_node_obj.w, from_node_obj.h
        from_top_x, from_top_y = from_center_x, from_center_y - from_height / 2
        from_bottom_x, from_bottom_y = from_center_x, from_center_y + from_height / 2
        from_left_x, from_left_y = from_center_x - from_width / 2, from_center_y
        from_right_x, from_right_y = from_center_x + from_width / 2, from_center_y

        to_center_x, to_center_y, to_width, to_height = to_node_obj.x, to_node_obj.y, to_node_obj.w, to_node_obj.h
        to_top_x, to_top_y = to_center_x, to_center_y - to_height / 2
        to_bottom_x, to_bottom_y = to_center_x, to_center_y + to_height / 2
        to_left_x, to_left_y = to_center_x - to_width / 2, to_center_y
        to_right_x, to_right_y = to_center_x + to_width / 2, to_center_y

        if to_left_x > from_bottom_x and to_left_y > from_bottom_y:
            coords = [from_bottom_x, from_bottom_y, from_bottom_x, to_left_y, to_left_x, to_left_y]

        return coords

    def rect_anchor_bottom_to_bottom(self, from_node_obj, to_node_obj):
        # bottom_to_bottom  非対応
        coords = []
        if from_node_obj.x is None or from_node_obj.y is None or from_node_obj.h is None or from_node_obj.w is None:
            return coords
        if to_node_obj.x is None or to_node_obj.y is None or to_node_obj.h is None or to_node_obj.w is None:
            return coords

        from_center_x, from_center_y, from_width, from_height = from_node_obj.x, from_node_obj.y, from_node_obj.w, from_node_obj.h
        from_top_x, from_top_y = from_center_x, from_center_y - from_height / 2
        from_bottom_x, from_bottom_y = from_center_x, from_center_y + from_height / 2
        from_left_x, from_left_y = from_center_x - from_width / 2, from_center_y
        from_right_x, from_right_y = from_center_x + from_width / 2, from_center_y

        to_center_x, to_center_y, to_width, to_height = to_node_obj.x, to_node_obj.y, to_node_obj.w, to_node_obj.h
        to_top_x, to_top_y = to_center_x, to_center_y - to_height / 2
        to_bottom_x, to_bottom_y = to_center_x, to_center_y + to_height / 2
        to_left_x, to_left_y = to_center_x - to_width / 2, to_center_y
        to_right_x, to_right_y = to_center_x + to_width / 2, to_center_y

        margin_y = max(from_bottom_y, to_bottom_y) + from_node_obj.h * 0.5
        coords = [from_bottom_x, from_bottom_y, from_bottom_x, margin_y, to_bottom_x, margin_y, to_bottom_x, to_bottom_y]

        return coords

    def rect_anchor_right_to_top(self, from_node_obj, to_node_obj):
        # right_to_top    2line
        # 条件： fromオブジェクトが分岐で、bottom点からのリンクが既にあり右点からのリンクが無い、toオブジェクトの上点がfromオブジェクトの右点より右下にある場合、2line
        coords = []
        if from_node_obj.x is None or from_node_obj.y is None or from_node_obj.h is None or from_node_obj.w is None:
            return coords
        if to_node_obj.x is None or to_node_obj.y is None or to_node_obj.h is None or to_node_obj.w is None:
            return coords

        from_center_x, from_center_y, from_width, from_height = from_node_obj.x, from_node_obj.y, from_node_obj.w, from_node_obj.h
        from_top_x, from_top_y = from_center_x, from_center_y - from_height / 2
        from_bottom_x, from_bottom_y = from_center_x, from_center_y + from_height / 2
        from_left_x, from_left_y = from_center_x - from_width / 2, from_center_y
        from_right_x, from_right_y = from_center_x + from_width / 2, from_center_y

        to_center_x, to_center_y, to_width, to_height = to_node_obj.x, to_node_obj.y, to_node_obj.w, to_node_obj.h
        to_top_x, to_top_y = to_center_x, to_center_y - to_height / 2
        to_bottom_x, to_bottom_y = to_center_x, to_center_y + to_height / 2
        to_left_x, to_left_y = to_center_x - to_width / 2, to_center_y
        to_right_x, to_right_y = to_center_x + to_width / 2, to_center_y

        if to_top_x > from_right_x and to_top_y > from_right_y:
            coords = [from_right_x, from_right_y, to_top_x, from_right_y, to_top_x, to_top_y]

        return coords

    def rect_anchor_right_to_right(self, from_node_obj, to_node_obj):
        # right_to_right  3line
        # 条件: fromオブジェクトが分岐で、fromオブジェクトよりtoオブジェクトが上にある場合、3line
        coords = []
        if from_node_obj.x is None or from_node_obj.y is None or from_node_obj.h is None or from_node_obj.w is None:
            return coords
        if to_node_obj.x is None or to_node_obj.y is None or to_node_obj.h is None or to_node_obj.w is None:
            return coords
        
        from_center_x, from_center_y, from_width, from_height = from_node_obj.x, from_node_obj.y, from_node_obj.w, from_node_obj.h
        from_top_x, from_top_y = from_center_x, from_center_y - from_height / 2
        from_bottom_x, from_bottom_y = from_center_x, from_center_y + from_height / 2
        from_left_x, from_left_y = from_center_x - from_width / 2, from_center_y
        from_right_x, from_right_y = from_center_x + from_width / 2, from_center_y

        to_center_x, to_center_y, to_width, to_height = to_node_obj.x, to_node_obj.y, to_node_obj.w, to_node_obj.h
        to_top_x, to_top_y = to_center_x, to_center_y - to_height / 2
        to_bottom_x, to_bottom_y = to_center_x, to_center_y + to_height / 2
        to_left_x, to_left_y = to_center_x - to_width / 2, to_center_y
        to_right_x, to_right_y = to_center_x + to_width / 2, to_center_y

        if to_bottom_y <= from_top_y:
            mid_x = max(from_right_x, to_right_x) + from_node_obj.w * 0.3
            coords = [from_right_x, from_right_y, mid_x, from_right_y, mid_x, to_right_y, to_right_x, to_right_y]

        return coords

    def rect_anchor_right_to_left(self, from_node_obj, to_node_obj):
        # right_to_left   1line
        # 条件: fromオブジェクトが分岐で、fromオブジェクトとtoオブジェクトが重なっていない、
        #           toオブジェクトがfromオブジェクトと同じ高さで右側にある場合、1line
        #           toオブジェクトがfromオブジェクトより上にある場合、3line
        coords = []
        if from_node_obj.x is None or from_node_obj.y is None or from_node_obj.h is None or from_node_obj.w is None:
            return coords
        if to_node_obj.x is None or to_node_obj.y is None or to_node_obj.h is None or to_node_obj.w is None:
            return coords
        
        from_center_x, from_center_y, from_width, from_height = from_node_obj.x, from_node_obj.y, from_node_obj.w, from_node_obj.h
        from_top_x, from_top_y = from_center_x, from_center_y - from_height / 2
        from_bottom_x, from_bottom_y = from_center_x, from_center_y + from_height / 2
        from_left_x, from_left_y = from_center_x - from_width / 2, from_center_y
        from_right_x, from_right_y = from_center_x + from_width / 2, from_center_y

        to_center_x, to_center_y, to_width, to_height = to_node_obj.x, to_node_obj.y, to_node_obj.w, to_node_obj.h
        to_top_x, to_top_y = to_center_x, to_center_y - to_height / 2
        to_bottom_x, to_bottom_y = to_center_x, to_center_y + to_height / 2
        to_left_x, to_left_y = to_center_x - to_width / 2, to_center_y
        to_right_x, to_right_y = to_center_x + to_width / 2, to_center_y

        if from_right_x < to_left_x:
            if from_right_y == to_left_y:
                coords = [from_right_x, from_right_y, to_left_x, to_left_y]
            elif to_left_y < from_right_y:
                mid_x = (from_right_x + to_left_x) / 2
                coords = [from_right_x, from_right_y, mid_x, from_right_y, mid_x, to_left_y, to_left_x, to_left_y]
            elif from_right_y < to_left_y:
                mid_x = (from_right_x + to_left_x) / 2
                coords = [from_right_x, from_right_y, mid_x, from_right_y, mid_x, to_left_y, to_left_x, to_left_y]

        return coords

    def rect_anchor_right_to_bottom(self, from_node_obj, to_node_obj):
        # right_to_bottom 非対応 fromオブジェクトが分岐で、fromオブジェクトよりtoオブジェクトが上にある場合、2line
        coords = []
        if from_node_obj.x is None or from_node_obj.y is None or from_node_obj.h is None or from_node_obj.w is None:
            return coords
        if to_node_obj.x is None or to_node_obj.y is None or to_node_obj.h is None or to_node_obj.w is None:
            return coords

        from_center_x, from_center_y, from_width, from_height = from_node_obj.x, from_node_obj.y, from_node_obj.w, from_node_obj.h
        from_top_x, from_top_y = from_center_x, from_center_y - from_height / 2
        from_bottom_x, from_bottom_y = from_center_x, from_center_y + from_height / 2
        from_left_x, from_left_y = from_center_x - from_width / 2, from_center_y
        from_right_x, from_right_y = from_center_x + from_width / 2, from_center_y

        to_center_x, to_center_y, to_width, to_height = to_node_obj.x, to_node_obj.y, to_node_obj.w, to_node_obj.h
        to_top_x, to_top_y = to_center_x, to_center_y - to_height / 2
        to_bottom_x, to_bottom_y = to_center_x, to_center_y + to_height / 2
        to_left_x, to_left_y = to_center_x - to_width / 2, to_center_y
        to_right_x, to_right_y = to_center_x + to_width / 2, to_center_y

        if to_bottom_y < from_right_y and to_bottom_x > from_right_x:
            coords = [from_right_x, from_right_y, to_bottom_x, from_right_y, to_bottom_x, to_bottom_y]

        return coords

    def rect_anchor_left_to_top(self, from_node_obj, to_node_obj):
        # 条件： fromオブジェクトが分岐で、bottom点からのリンクが既にあり右点からのリンクが無い、toオブジェクトの上点がfromオブジェクトの右点より右下にある場合、2line
        coords = []
        if from_node_obj.x is None or from_node_obj.y is None or from_node_obj.h is None or from_node_obj.w is None:
            return coords
        if to_node_obj.x is None or to_node_obj.y is None or to_node_obj.h is None or to_node_obj.w is None:
            return coords

        from_center_x, from_center_y, from_width, from_height = from_node_obj.x, from_node_obj.y, from_node_obj.w, from_node_obj.h
        from_top_x, from_top_y = from_center_x, from_center_y - from_height / 2
        from_bottom_x, from_bottom_y = from_center_x, from_center_y + from_height / 2
        from_left_x, from_left_y = from_center_x - from_width / 2, from_center_y
        from_right_x, from_right_y = from_center_x + from_width / 2, from_center_y

        to_center_x, to_center_y, to_width, to_height = to_node_obj.x, to_node_obj.y, to_node_obj.w, to_node_obj.h
        to_top_x, to_top_y = to_center_x, to_center_y - to_height / 2
        to_bottom_x, to_bottom_y = to_center_x, to_center_y + to_height / 2
        to_left_x, to_left_y = to_center_x - to_width / 2, to_center_y
        to_right_x, to_right_y = to_center_x + to_width / 2, to_center_y

        if to_top_x < from_left_x and to_top_y > from_left_y:
            coords = [from_left_x, from_left_y, to_top_x, from_left_y, to_top_x, to_top_y]

        return coords

    def rect_anchor_left_to_right(self, from_node_obj, to_node_obj):
        # 条件: fromオブジェクトが分岐で、fromオブジェクトとtoオブジェクトが重なっていない
        #           toオブジェクトがfromオブジェクトと同じ高さで左側にある場合、1line
        #           toオブジェクトがfromオブジェクトより上にある場合、3line
        coords = []
        if from_node_obj.x is None or from_node_obj.y is None or from_node_obj.h is None or from_node_obj.w is None:
            return coords
        if to_node_obj.x is None or to_node_obj.y is None or to_node_obj.h is None or to_node_obj.w is None:
            return coords

        from_center_x, from_center_y, from_width, from_height = from_node_obj.x, from_node_obj.y, from_node_obj.w, from_node_obj.h
        from_top_x, from_top_y = from_center_x, from_center_y - from_height / 2
        from_bottom_x, from_bottom_y = from_center_x, from_center_y + from_height / 2
        from_left_x, from_left_y = from_center_x - from_width / 2, from_center_y
        from_right_x, from_right_y = from_center_x + from_width / 2, from_center_y

        to_center_x, to_center_y, to_width, to_height = to_node_obj.x, to_node_obj.y, to_node_obj.w, to_node_obj.h
        to_top_x, to_top_y = to_center_x, to_center_y - to_height / 2
        to_bottom_x, to_bottom_y = to_center_x, to_center_y + to_height / 2
        to_left_x, to_left_y = to_center_x - to_width / 2, to_center_y
        to_right_x, to_right_y = to_center_x + to_width / 2, to_center_y

        if to_right_x < from_left_x:
            if from_left_y == to_right_y:
                coords = [from_left_x, from_left_y, to_right_x, to_right_y]
            elif to_right_y < from_left_y:
                mid_x = (from_left_x + to_right_x) / 2
                coords = [from_left_x, from_left_y, mid_x, from_left_y, mid_x, to_right_y, to_right_x, to_right_y]
            elif from_left_y < to_right_y:
                mid_x = (from_left_x + to_right_x) / 2
                coords = [from_left_x, from_left_y, mid_x, from_left_y, mid_x, to_right_y, to_right_x, to_right_y]

        return coords

    def rect_anchor_left_to_left(self, from_node_obj, to_node_obj):
        # left_to_left    3line
        # 条件: fromオブジェクトが分岐で、fromオブジェクトよりtoオブジェクトが上にある場合、3line
        coords = []
        if from_node_obj.x is None or from_node_obj.y is None or from_node_obj.h is None or from_node_obj.w is None:
            return coords
        if to_node_obj.x is None or to_node_obj.y is None or to_node_obj.h is None or to_node_obj.w is None:
            return coords

        from_center_x, from_center_y, from_width, from_height = from_node_obj.x, from_node_obj.y, from_node_obj.w, from_node_obj.h
        from_top_x, from_top_y = from_center_x, from_center_y - from_height / 2
        from_bottom_x, from_bottom_y = from_center_x, from_center_y + from_height / 2
        from_left_x, from_left_y = from_center_x - from_width / 2, from_center_y
        from_right_x, from_right_y = from_center_x + from_width / 2, from_center_y

        to_center_x, to_center_y, to_width, to_height = to_node_obj.x, to_node_obj.y, to_node_obj.w, to_node_obj.h
        to_top_x, to_top_y = to_center_x, to_center_y - to_height / 2
        to_bottom_x, to_bottom_y = to_center_x, to_center_y + to_height / 2
        to_left_x, to_left_y = to_center_x - to_width / 2, to_center_y
        to_right_x, to_right_y = to_center_x + to_width / 2, to_center_y

        if to_bottom_y <= from_top_y:
            mid_x = min(from_left_x, to_left_x) - from_node_obj.w * 0.3
            coords = [from_left_x, from_left_y, mid_x, from_left_y, mid_x, to_left_y, to_left_x, to_left_y]

        return coords

    def rect_anchor_left_to_bottom(self, from_node_obj, to_node_obj):
        # left_to_bottom  非対応 fromオブジェクトが分岐で、fromオブジェクトよりtoオブジェクトが上にある場合、2line
        coords = []
        if from_node_obj.x is None or from_node_obj.y is None or from_node_obj.h is None or from_node_obj.w is None:
            return coords
        if to_node_obj.x is None or to_node_obj.y is None or to_node_obj.h is None or to_node_obj.w is None:
            return coords

        from_center_x, from_center_y, from_width, from_height = from_node_obj.x, from_node_obj.y, from_node_obj.w, from_node_obj.h
        from_top_x, from_top_y = from_center_x, from_center_y - from_height / 2
        from_bottom_x, from_bottom_y = from_center_x, from_center_y + from_height / 2
        from_left_x, from_left_y = from_center_x - from_width / 2, from_center_y
        from_right_x, from_right_y = from_center_x + from_width / 2, from_center_y

        to_center_x, to_center_y, to_width, to_height = to_node_obj.x, to_node_obj.y, to_node_obj.w, to_node_obj.h
        to_top_x, to_top_y = to_center_x, to_center_y - to_height / 2
        to_bottom_x, to_bottom_y = to_center_x, to_center_y + to_height / 2
        to_left_x, to_left_y = to_center_x - to_width / 2, to_center_y
        to_right_x, to_right_y = to_center_x + to_width / 2, to_center_y

        if to_bottom_y < from_right_y and to_bottom_x > from_right_x:
            coords = [from_right_x, from_right_y, to_bottom_x, from_right_y, to_bottom_x, to_bottom_y]

        return coords

    def rect_anchor_top_to_top(self, from_node_obj, to_node_obj):
        # top_to_top       非対応
        coords = []
        if from_node_obj.x is None or from_node_obj.y is None or from_node_obj.h is None or from_node_obj.w is None:
            return coords
        if to_node_obj.x is None or to_node_obj.y is None or to_node_obj.h is None or to_node_obj.w is None:
            return coords

        from_center_x, from_center_y, from_width, from_height = from_node_obj.x, from_node_obj.y, from_node_obj.w, from_node_obj.h
        from_top_x, from_top_y = from_center_x, from_center_y - from_height / 2
        from_bottom_x, from_bottom_y = from_center_x, from_center_y + from_height / 2
        from_left_x, from_left_y = from_center_x - from_width / 2, from_center_y
        from_right_x, from_right_y = from_center_x + from_width / 2, from_center_y

        to_center_x, to_center_y, to_width, to_height = to_node_obj.x, to_node_obj.y, to_node_obj.w, to_node_obj.h
        to_top_x, to_top_y = to_center_x, to_center_y - to_height / 2
        to_bottom_x, to_bottom_y = to_center_x, to_center_y + to_height / 2
        to_left_x, to_left_y = to_center_x - to_width / 2, to_center_y
        to_right_x, to_right_y = to_center_x + to_width / 2, to_center_y

        return coords

    def rect_anchor_top_to_right(self, from_node_obj, to_node_obj):
        # top_to_right     非対応
        coords = []
        if from_node_obj.x is None or from_node_obj.y is None or from_node_obj.h is None or from_node_obj.w is None:
            return coords
        if to_node_obj.x is None or to_node_obj.y is None or to_node_obj.h is None or to_node_obj.w is None:
            return coords

        from_center_x, from_center_y, from_width, from_height = from_node_obj.x, from_node_obj.y, from_node_obj.w, from_node_obj.h
        from_top_x, from_top_y = from_center_x, from_center_y - from_height / 2
        from_bottom_x, from_bottom_y = from_center_x, from_center_y + from_height / 2
        from_left_x, from_left_y = from_center_x - from_width / 2, from_center_y
        from_right_x, from_right_y = from_center_x + from_width / 2, from_center_y

        to_center_x, to_center_y, to_width, to_height = to_node_obj.x, to_node_obj.y, to_node_obj.w, to_node_obj.h
        to_top_x, to_top_y = to_center_x, to_center_y - to_height / 2
        to_bottom_x, to_bottom_y = to_center_x, to_center_y + to_height / 2
        to_left_x, to_left_y = to_center_x - to_width / 2, to_center_y
        to_right_x, to_right_y = to_center_x + to_width / 2, to_center_y

        return coords

    def rect_anchor_top_to_left(self, from_node_obj, to_node_obj):
        # top_to_left      非対応
        coords = []
        if from_node_obj.x is None or from_node_obj.y is None or from_node_obj.h is None or from_node_obj.w is None:
            return coords
        if to_node_obj.x is None or to_node_obj.y is None or to_node_obj.h is None or to_node_obj.w is None:
            return coords

        from_center_x, from_center_y, from_width, from_height = from_node_obj.x, from_node_obj.y, from_node_obj.w, from_node_obj.h
        from_top_x, from_top_y = from_center_x, from_center_y - from_height / 2
        from_bottom_x, from_bottom_y = from_center_x, from_center_y + from_height / 2
        from_left_x, from_left_y = from_center_x - from_width / 2, from_center_y
        from_right_x, from_right_y = from_center_x + from_width / 2, from_center_y

        to_center_x, to_center_y, to_width, to_height = to_node_obj.x, to_node_obj.y, to_node_obj.w, to_node_obj.h
        to_top_x, to_top_y = to_center_x, to_center_y - to_height / 2
        to_bottom_x, to_bottom_y = to_center_x, to_center_y + to_height / 2
        to_left_x, to_left_y = to_center_x - to_width / 2, to_center_y
        to_right_x, to_right_y = to_center_x + to_width / 2, to_center_y

        return coords

    def rect_anchor_top_to_bottom(self, from_node_obj, to_node_obj):
        # top_to_bottom    非対応
        coords = []
        if from_node_obj.x is None or from_node_obj.y is None or from_node_obj.h is None or from_node_obj.w is None:
            return coords
        if to_node_obj.x is None or to_node_obj.y is None or to_node_obj.h is None or to_node_obj.w is None:
            return coords

        from_center_x, from_center_y, from_width, from_height = from_node_obj.x, from_node_obj.y, from_node_obj.w, from_node_obj.h
        from_top_x, from_top_y = from_center_x, from_center_y - from_height / 2
        from_bottom_x, from_bottom_y = from_center_x, from_center_y + from_height / 2
        from_left_x, from_left_y = from_center_x - from_width / 2, from_center_y
        from_right_x, from_right_y = from_center_x + from_width / 2, from_center_y

        to_center_x, to_center_y, to_width, to_height = to_node_obj.x, to_node_obj.y, to_node_obj.w, to_node_obj.h
        to_top_x, to_top_y = to_center_x, to_center_y - to_height / 2
        to_bottom_x, to_bottom_y = to_center_x, to_center_y + to_height / 2
        to_left_x, to_left_y = to_center_x - to_width / 2, to_center_y
        to_right_x, to_right_y = to_center_x + to_width / 2, to_center_y

        return coords

    def line_anchor(self, from_node_obj, to_node_obj):
        """直線アンカー座標計算"""
        coords = [from_node_obj.x, from_node_obj.y, to_node_obj.x, to_node_obj.y]
        return coords

    def update_label_text(self, canvas, text):
        """エッジラベルのテキスト更新"""
        self.label_text = text
        if canvas:
            self.refresh_label(canvas)

    def refresh_label(self, canvas):
        """エッジラベルの再描画"""
        if self.label_id:
            canvas.itemconfig(self.label_id, text=self.label_text)
    
    def update_points(self, canvas, points, label_x=None, label_y=None):
        """エッジのポイント更新"""
        self.points = points
        if label_x:
            self.label_x = label_x
        if label_y:
            self.label_y = label_y
        if canvas:
            self.refresh_edge(canvas)
    
    def refresh_edge(self, canvas):
        """エッジの再描画"""
        if canvas and self.line_id:
            canvas.coords(self.line_id, *self.points)
            if self.label_id and self.label_x and self.label_y:
                canvas.coords(self.label_id, self.label_x, self.label_y)