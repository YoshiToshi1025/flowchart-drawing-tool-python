import tkinter as tk
import constants as ct
import node
from typing import Literal, Tuple
from math import inf

LABEL_POSITION_LIST = ["auto", "p0se", "p0sw", "p0nw", "p0ne", "p1se", "p1sw", "p1nw", "p1ne", "p2se", "p2sw", "p2nw", "p2ne", "p3se", "p3sw", "p3nw", "p3ne", "p4se", "p4sw", "p4nw", "p4ne", "p5se", "p5sw", "p5nw", "p5ne"]

class Edge:
    line_id = None
    edge_type:Literal["elbow", "line"] = "elbow"  # "elbow", "line"のいずれか
    line_style:Literal["solid", "dashed", "dotted"] = "solid"  # "solid", "dashed", "dotted"のいずれか
    from_node_obj = None
    to_node_obj = None
    points = None  # List of (x, y) tuples
    label_id = None
    label_x = None
    label_y = None
    label_text = None
    label_anchor:Literal["center", "n", "ne", "e", "se", "s", "sw", "w", "nw"] = "center"
    label_justify:Literal["left", "center", "right"] = "left"
    label_position = "auto"
    connection_mode:Literal["auto", "manual", None] = "auto"
    from_node_connection_point:Literal["top", "bottom", "left", "right", "auto", None] = None
    to_node_connection_point:Literal["top", "bottom", "left", "right", "auto", None] = None
    edge_wrap_margin = None

    def __init__(self, edge_type:Literal["elbow", "line"]="elbow", line_style:Literal["solid", "dashed", "dotted"]="solid", \
                    from_node_obj=None, to_node_obj=None, points=None, text=None, \
                    connection_mode=None, from_node_connection_point=None, to_node_connection_point=None, edge_wrap_margin=None, \
                    label_x=None, label_y=None, canvas=None,\
                    label_position:Literal["auto", "p0se", "p0sw", "p0nw", "p0ne", "p1se", "p1sw", "p1nw", "p1ne", "p2se", "p2sw", "p2nw", "p2ne", "p3se", "p3sw", "p3nw", "p3ne", "p4se", "p4sw", "p4nw", "p4ne", "p5se", "p5sw", "p5nw", "p5ne"]="auto"):
        self.edge_type = edge_type
        self.line_style = line_style
        self.from_node_obj = from_node_obj
        self.to_node_obj = to_node_obj
        self.label_text = text
        self.label_position = label_position
        if self.edge_type == ct.EDGE_TYPE_ELBOW:
            self.label_anchor = "center"
            self.label_justify = "left"
        else:
            self.label_anchor = "center"
            self.label_justify = "center"
        self.connection_mode = connection_mode if connection_mode in ["auto", "manual"] else None
        self.from_node_connection_point = from_node_connection_point if from_node_connection_point in ["top", "bottom", "left", "right", "auto"] else None
        self.to_node_connection_point = to_node_connection_point if to_node_connection_point in ["top", "bottom", "left", "right", "auto"] else None
        self.edge_wrap_margin = edge_wrap_margin

        if self.connection_mode is None:
            if self.from_node_connection_point is None or self.from_node_connection_point == "auto" or self.to_node_connection_point is None or self.to_node_connection_point == "auto":
                self.connection_mode = "auto"
                self.from_node_connection_point = None
                self.to_node_connection_point = None
            else:
                self.connection_mode = "manual"

        if points is None:
            # 直線またはかぎ線の頂点の座標とラベル位置を自動計算
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
        arrow_kind = ct.EDGE_PARAMS.get("arrow_kind", tk.LAST)
        arrow_shape = ct.EDGE_PARAMS.get("arrow_shape", (8, 10, 3))

        dash_pattern = self.get_dash_pattern()

        if arrow_kind is None:
            self.line_id = canvas.create_line(
                *self.points,
                width=ct.EDGE_PARAMS["width"], fill=ct.EDGE_PARAMS["color"], dash=dash_pattern,
                tags=("edge")
            )
        else:
            self.line_id = canvas.create_line(
                *self.points,
                arrow=arrow_kind, arrowshape=arrow_shape,
                width=ct.EDGE_PARAMS["width"], fill=ct.EDGE_PARAMS["color"], dash=dash_pattern,
                tags=("edge")
            )
        # エッジはノードの下に
        canvas.tag_lower(self.line_id, "node")
    
    def get_dash_pattern(self):
        if self.line_style == ct.EDGE_LINE_STYLE_DASHED:
            return "-"  # 破線（パターン指定が効かない）
        elif self.line_style == ct.EDGE_LINE_STYLE_DOTTED:
            return "."  # 点線（パターン指定が効かない）
        else:
            return ()

    def draw_label(self, canvas:tk.Canvas, from_node_obj):
        """エッジラベルの描画"""

        if self.label_x is not None and self.label_y is not None and self.label_text is not None:
            self.label_x, self.label_y, self.label_anchor, self.label_justify = self.get_label_position()
            self.label_id = canvas.create_text(
                self.label_x, self.label_y,
                text=self.label_text,
                font=(ct.EDGE_PARAMS["font_family"], ct.EDGE_PARAMS["font_size"], ct.EDGE_PARAMS["font_weight"]), width=ct.EDGE_PARAMS["text_width"],
                fill=ct.EDGE_PARAMS["text_color"], anchor = self.label_anchor, justify = self.label_justify,
                tags=("edge-label",)
            )
            # ラベルもノードの下でOK（少し上に描かれるので視認性は保てる）
            canvas.tag_raise(self.label_id, "node")

    def _compute_edge_geometry(self, from_node_obj: node.Node, to_node_obj: node.Node):
        """直線またはかぎ線の頂点の座標とラベル位置を計算"""
        # 各ノードのアンカーとラベル位置を設定
        if self.edge_type == "elbow":
            self.points, self.label_x, self.label_y, self.label_anchor, self.label_justify = self.rect_anchor(from_node_obj, to_node_obj)
        elif self.edge_type == "line":
            self.points, self.label_x, self.label_y, self.label_anchor, self.label_justify = self.line_anchor(from_node_obj, to_node_obj)
        else:
            self.points, self.label_x, self.label_y, self.label_anchor, self.label_justify = self.simple_line_anchor(from_node_obj, to_node_obj)

        return self.points, self.label_x, self.label_y, self.label_anchor, self.label_justify

    # --- rectAnchor: 矩形の境界上にアンカーを取る ---
    def rect_anchor(self, from_node_obj, to_node_obj):
        coords = []
        if from_node_obj.x is None or from_node_obj.y is None or from_node_obj.h is None or from_node_obj.w is None:
            return coords, None, None, "center", "center"
        if to_node_obj.x is None or to_node_obj.y is None or to_node_obj.h is None or to_node_obj.w is None:
            return coords, None, None, "center", "center"

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
        label_anchor = "center"
        label_justify = "center"

        if self.connection_mode == "auto":
            if from_type == ct.NODE_DECISION_PARAMS["type"]:
                # from側がDecisionノードの場合
                if from_left_x <= to_top_x <= from_right_x and from_bottom_y < to_top_y:
                    coords = self.rect_anchor_bottom_to_top(from_node_obj, to_node_obj)
                    if coords is not None and coords != []:
                        label_x = coords[0] + ct.EDGE_LABEL_OFFSET["nw_from_decision"][0]
                        label_y = coords[1] + ct.EDGE_LABEL_OFFSET["nw_from_decision"][1]
                        self.from_node_connection_point = "bottom"
                        self.to_node_connection_point = "top"
                    label_anchor = "nw"
                    label_justify = "left"
                elif from_right_x < to_left_x and to_top_y <= from_bottom_y:
                    coords = self.rect_anchor_right_to_left(from_node_obj, to_node_obj)
                    if coords is not None and coords != []:
                        label_x = coords[0] + ct.EDGE_LABEL_OFFSET["sw"][0]
                        label_y = coords[1] + ct.EDGE_LABEL_OFFSET["sw"][1]
                        self.from_node_connection_point = "right"
                        self.to_node_connection_point = "left"
                    label_anchor = "sw"
                    label_justify = "left"
                elif from_right_x < to_top_x and from_right_y < to_left_y:
                    coords = self.rect_anchor_right_to_top(from_node_obj, to_node_obj)
                    if coords is not None and coords != []:
                        label_x = coords[0] + ct.EDGE_LABEL_OFFSET["sw"][0]
                        label_y = coords[1] + ct.EDGE_LABEL_OFFSET["sw"][1] 
                        self.from_node_connection_point = "right"
                        self.to_node_connection_point = "top"
                    label_anchor= "sw"
                    label_justify = "left"
                elif to_right_x < from_left_x and to_top_y <= from_bottom_y:
                    coords = self.rect_anchor_left_to_right(from_node_obj, to_node_obj)
                    if coords is not None and coords != []:
                        label_x = coords[0] + ct.EDGE_LABEL_OFFSET["se"][0]
                        label_y = coords[1] + ct.EDGE_LABEL_OFFSET["se"][1]
                        self.from_node_connection_point = "left"
                        self.to_node_connection_point = "right"
                    label_anchor = "se"
                    label_justify = "right"
                elif to_top_x < from_left_x and from_right_y < to_left_y:
                    coords = self.rect_anchor_left_to_top(from_node_obj, to_node_obj)
                    if coords is not None and coords != []:
                        label_x = coords[0] + ct.EDGE_LABEL_OFFSET["se"][0]
                        label_y = coords[1] + ct.EDGE_LABEL_OFFSET["se"][1]
                        self.from_node_connection_point = "left"
                        self.to_node_connection_point = "top"
                    label_anchor = "se"
                    label_justify = "right"
                elif to_bottom_y <= from_top_y:
                    if to_bottom_x < from_top_x:
                        coords = self.rect_anchor_right_to_right(from_node_obj, to_node_obj)
                        if coords is not None and coords != []:
                            label_x = coords[0] + ct.EDGE_LABEL_OFFSET["sw"][0]
                            label_y = coords[1] + ct.EDGE_LABEL_OFFSET["sw"][1]
                            self.from_node_connection_point = "right"
                            self.to_node_connection_point = "right"
                        label_anchor = "sw"
                        label_justify = "left"
                    else:
                        coords = self.rect_anchor_left_to_left(from_node_obj, to_node_obj)
                        if coords is not None and coords != []:
                            label_x = coords[0] + ct.EDGE_LABEL_OFFSET["se"][0]
                            label_y = coords[1] + ct.EDGE_LABEL_OFFSET["se"][1]
                            self.from_node_connection_point = "left"
                            self.to_node_connection_point = "left"
                        label_anchor = "se"
                        label_justify = "right"
            else:
                # from側がDecision以外のノードの場合
                tree_mode = ct.EDGE_PARAMS.get("tree_mode", False)
                if tree_mode and from_bottom_y < to_top_y:
                    if to_bottom_x < from_bottom_x:
                        coords = self.rect_anchor_bottom_to_right(from_node_obj, to_node_obj)
                        if coords is not None and coords != []:
                            label_x = coords[0] + ct.EDGE_LABEL_OFFSET["nw"][0]
                            label_y = coords[1] + ct.EDGE_LABEL_OFFSET["nw"][1]
                            self.from_node_connection_point = "bottom"
                            self.to_node_connection_point = "right"
                        label_anchor = "nw"
                        label_justify = "left"
                    elif from_bottom_x < to_bottom_x:
                        coords = self.rect_anchor_bottom_to_left(from_node_obj, to_node_obj)
                        if coords is not None and coords != []:
                            label_x = coords[0] + ct.EDGE_LABEL_OFFSET["nw"][0]
                            label_y = coords[1] + ct.EDGE_LABEL_OFFSET["nw"][1]
                            self.from_node_connection_point = "bottom"
                            self.to_node_connection_point = "left"
                        label_anchor = "nw"
                        label_justify = "left"

                    else:
                        coords = self.rect_anchor_bottom_to_top(from_node_obj, to_node_obj)
                        if coords is not None and coords != []:
                            label_x = coords[0] + ct.EDGE_LABEL_OFFSET["nw"][0]
                            label_y = coords[1] + ct.EDGE_LABEL_OFFSET["nw"][1]
                            self.from_node_connection_point = "bottom"
                            self.to_node_connection_point = "top"
                        label_anchor = "nw"
                        label_justify = "left"
                elif from_bottom_y < to_top_y <= from_bottom_y + ct.CANVAS_PARAMS["grid_spacing"] * 2:
                    if to_right_x < from_left_x:
                        coords = self.rect_anchor_bottom_to_right(from_node_obj, to_node_obj)
                        if coords is not None and coords != []:
                            label_x = coords[0] + ct.EDGE_LABEL_OFFSET["nw"][0]
                            label_y = coords[1] + ct.EDGE_LABEL_OFFSET["nw"][1]
                            self.from_node_connection_point = "bottom"
                            self.to_node_connection_point = "right"
                        label_anchor = "nw"
                        label_justify = "left"
                    elif from_right_x < to_left_x:
                        coords = self.rect_anchor_bottom_to_left(from_node_obj, to_node_obj)
                        if coords is not None and coords != []:
                            label_x = coords[0] + ct.EDGE_LABEL_OFFSET["nw"][0]
                            label_y = coords[1] + ct.EDGE_LABEL_OFFSET["nw"][1]
                            self.from_node_connection_point = "bottom"
                            self.to_node_connection_point = "left"
                        label_anchor = "nw"
                        label_justify = "left"
                    else:
                        coords = self.rect_anchor_bottom_to_top(from_node_obj, to_node_obj)
                        if coords is not None and coords != []:
                            label_x = coords[0] + ct.EDGE_LABEL_OFFSET["nw"][0]
                            label_y = coords[1] + ct.EDGE_LABEL_OFFSET["nw"][1]
                            self.from_node_connection_point = "bottom"
                            self.to_node_connection_point = "top"
                        label_anchor = "nw"
                        label_justify = "left"
                elif from_bottom_y < to_top_y:
                    coords = self.rect_anchor_bottom_to_top(from_node_obj, to_node_obj)
                    if coords is not None and coords != []:
                        label_x = coords[0] + ct.EDGE_LABEL_OFFSET["nw"][0]
                        label_y = coords[1] + ct.EDGE_LABEL_OFFSET["nw"][1]
                        self.from_node_connection_point = "bottom"
                        self.to_node_connection_point = "top"
                    label_anchor = "nw"
                    label_justify = "left"
                elif from_right_x < to_left_x and from_top_y <= to_bottom_y and to_top_y <= from_bottom_y:
                    coords = self.rect_anchor_right_to_left(from_node_obj, to_node_obj)
                    if coords is not None and coords != []:
                        label_x = coords[0] + ct.EDGE_LABEL_OFFSET["sw"][0]
                        label_y = coords[1] + ct.EDGE_LABEL_OFFSET["sw"][1]
                        self.from_node_connection_point = "right"
                        self.to_node_connection_point = "left"
                    label_anchor = "sw"
                    label_justify = "left"
                elif from_right_x + from_width/2 < to_left_x and to_bottom_y < from_top_y:
                    coords = self.rect_anchor_right_to_left(from_node_obj, to_node_obj)
                    if coords is not None and coords != []:
                        label_x = coords[0] + ct.EDGE_LABEL_OFFSET["sw"][0]
                        label_y = coords[1] + ct.EDGE_LABEL_OFFSET["sw"][1]
                        self.from_node_connection_point = "right"
                        self.to_node_connection_point = "left"
                    label_anchor = "sw"
                    label_justify = "left"
                elif to_right_x < from_left_x and from_top_y <= to_bottom_y and to_top_y <= from_bottom_y:
                    coords = self.rect_anchor_left_to_right(from_node_obj, to_node_obj)
                    if coords is not None and coords != []:
                        label_x = coords[0] + ct.EDGE_LABEL_OFFSET["se"][0]
                        label_y = coords[1] + ct.EDGE_LABEL_OFFSET["se"][1]
                        self.from_node_connection_point = "left"
                        self.to_node_connection_point = "right"
                    label_anchor = "se"
                    label_justify = "right"
                elif to_bottom_y <= from_top_y:
                    if to_bottom_x < from_top_x:
                        coords = self.rect_anchor_right_to_right(from_node_obj, to_node_obj)
                        if coords is not None and coords != []:
                            label_x = coords[0] + ct.EDGE_LABEL_OFFSET["nw"][0]
                            label_y = coords[1] + ct.EDGE_LABEL_OFFSET["nw"][1]
                            self.from_node_connection_point = "right"
                            self.to_node_connection_point = "right"
                        label_anchor = "nw"
                        label_justify = "left"
                    else:
                        coords = self.rect_anchor_left_to_left(from_node_obj, to_node_obj)
                        if coords is not None and coords != []:
                            label_x = coords[0] + ct.EDGE_LABEL_OFFSET["ne"][0]
                            label_y = coords[1] + ct.EDGE_LABEL_OFFSET["ne"][1]
                            self.from_node_connection_point = "left"
                            self.to_node_connection_point = "left"
                        label_anchor = "ne"
                        label_justify = "right"
        else:
            # 明示的なアンカー指定あり
            if self.from_node_connection_point == "top" and self.to_node_connection_point == "top":
                coords = self.rect_anchor_top_to_top(from_node_obj, to_node_obj)
                if coords is not None and coords != []:
                    label_x = coords[0] + ct.EDGE_LABEL_OFFSET["sw"][0]
                    label_y = coords[1] + ct.EDGE_LABEL_OFFSET["sw"][1]
                    label_anchor = "sw"
                    label_justify = "left"
            elif self.from_node_connection_point == "top" and self.to_node_connection_point == "right":
                coords = self.rect_anchor_top_to_right(from_node_obj, to_node_obj)
                if coords is not None and coords != []:
                    label_x = coords[0] + ct.EDGE_LABEL_OFFSET["sw"][0]
                    label_y = coords[1] + ct.EDGE_LABEL_OFFSET["sw"][1]
                    label_anchor = "sw"
                    label_justify = "left"
            elif self.from_node_connection_point == "top" and self.to_node_connection_point == "bottom":
                coords = self.rect_anchor_top_to_bottom(from_node_obj, to_node_obj)
                if coords is not None and coords != []:
                    label_x = coords[0] + ct.EDGE_LABEL_OFFSET["sw"][0]
                    label_y = coords[1] + ct.EDGE_LABEL_OFFSET["sw"][1]
                    label_anchor = "sw"
                    label_justify = "left"
            elif self.from_node_connection_point == "top" and self.to_node_connection_point == "left":
                coords = self.rect_anchor_top_to_left(from_node_obj, to_node_obj)
                if coords is not None and coords != []:
                    label_x = coords[0] + ct.EDGE_LABEL_OFFSET["sw"][0]
                    label_y = coords[1] + ct.EDGE_LABEL_OFFSET["sw"][1]
                    label_anchor = "sw"
                    label_justify = "left"
            elif self.from_node_connection_point == "right" and self.to_node_connection_point == "top":
                coords = self.rect_anchor_right_to_top(from_node_obj, to_node_obj)
                if coords is not None and coords != []:
                    label_x = coords[0] + ct.EDGE_LABEL_OFFSET["sw"][0]
                    label_y = coords[1] + ct.EDGE_LABEL_OFFSET["sw"][1]
                    label_anchor = "sw"
                    label_justify = "left"
            elif self.from_node_connection_point == "right" and self.to_node_connection_point == "right":
                coords = self.rect_anchor_right_to_right(from_node_obj, to_node_obj)
                if coords is not None and coords != []:
                    if from_right_y < to_right_y:
                        label_x = coords[0] + ct.EDGE_LABEL_OFFSET["sw"][0]
                        label_y = coords[1] + ct.EDGE_LABEL_OFFSET["sw"][1]
                        label_anchor = "sw"
                        label_justify = "left"
                    else:
                        label_x = coords[0] + ct.EDGE_LABEL_OFFSET["nw"][0]
                        label_y = coords[1] + ct.EDGE_LABEL_OFFSET["nw"][1]
                        label_anchor = "nw"
                        label_justify = "left"
            elif self.from_node_connection_point == "right" and self.to_node_connection_point == "bottom":
                coords = self.rect_anchor_right_to_bottom(from_node_obj, to_node_obj)
                if coords is not None and coords != []:
                    label_x = coords[0] + ct.EDGE_LABEL_OFFSET["sw"][0]
                    label_y = coords[1] + ct.EDGE_LABEL_OFFSET["sw"][1]
                    label_anchor = "sw"
                    label_justify = "left"
            elif self.from_node_connection_point == "right" and self.to_node_connection_point == "left":
                coords = self.rect_anchor_right_to_left(from_node_obj, to_node_obj)
                if coords is not None and coords != []:
                    label_x = coords[0] + ct.EDGE_LABEL_OFFSET["sw"][0]
                    label_y = coords[1] + ct.EDGE_LABEL_OFFSET["sw"][1]
                    label_anchor = "sw"
                    label_justify = "left"
            elif self.from_node_connection_point == "bottom" and self.to_node_connection_point == "top":
                coords = self.rect_anchor_bottom_to_top(from_node_obj, to_node_obj)
                if coords is not None and coords != []:
                    label_x = coords[0] + ct.EDGE_LABEL_OFFSET["nw"][0]
                    label_y = coords[1] + ct.EDGE_LABEL_OFFSET["nw"][1]
                    label_anchor = "nw"
                    label_justify = "left"
            elif self.from_node_connection_point == "bottom" and self.to_node_connection_point == "right":
                coords = self.rect_anchor_bottom_to_right(from_node_obj, to_node_obj)
                if coords is not None and coords != []:
                    label_x = coords[0] + ct.EDGE_LABEL_OFFSET["nw"][0]
                    label_y = coords[1] + ct.EDGE_LABEL_OFFSET["nw"][1]
                    label_anchor = "nw"
                    label_justify = "left"
            elif self.from_node_connection_point == "bottom" and self.to_node_connection_point == "bottom":
                coords = self.rect_anchor_bottom_to_bottom(from_node_obj, to_node_obj)
                if coords is not None and coords != []:
                    label_x = coords[0] + ct.EDGE_LABEL_OFFSET["nw"][0]
                    label_y = coords[1] + ct.EDGE_LABEL_OFFSET["nw"][1]
                    label_anchor = "nw"
                    label_justify = "left"
            elif self.from_node_connection_point == "bottom" and self.to_node_connection_point == "left":
                coords = self.rect_anchor_bottom_to_left(from_node_obj, to_node_obj)
                if coords is not None and coords != []:
                    label_x = coords[0] + ct.EDGE_LABEL_OFFSET["nw"][0]
                    label_y = coords[1] + ct.EDGE_LABEL_OFFSET["nw"][1]
                    label_anchor = "nw"
                    label_justify = "left"
            elif self.from_node_connection_point == "left" and self.to_node_connection_point == "top":
                coords = self.rect_anchor_left_to_top(from_node_obj, to_node_obj)
                if coords is not None and coords != []:
                    label_x = coords[0] + ct.EDGE_LABEL_OFFSET["se"][0]
                    label_y = coords[1] + ct.EDGE_LABEL_OFFSET["se"][1]
                    label_anchor = "se"
                    label_justify = "right"
            elif self.from_node_connection_point == "left" and self.to_node_connection_point == "right":
                coords = self.rect_anchor_left_to_right(from_node_obj, to_node_obj)
                if coords is not None and coords != []:
                    label_x = coords[0] + ct.EDGE_LABEL_OFFSET["se"][0]
                    label_y = coords[1] + ct.EDGE_LABEL_OFFSET["se"][1]
                    label_anchor = "se"
                    label_justify = "right"
            elif self.from_node_connection_point == "left" and self.to_node_connection_point == "bottom":
                coords = self.rect_anchor_left_to_bottom(from_node_obj, to_node_obj)
                if coords is not None and coords != []:
                    label_x = coords[0] + ct.EDGE_LABEL_OFFSET["se"][0]
                    label_y = coords[1] + ct.EDGE_LABEL_OFFSET["se"][1]
                    label_anchor = "se"
                    label_justify = "right"
            elif self.from_node_connection_point == "left" and self.to_node_connection_point == "left":
                coords = self.rect_anchor_left_to_left(from_node_obj, to_node_obj)
                if coords is not None and coords != []:
                    if from_left_y < to_left_y:
                        label_x = coords[0] + ct.EDGE_LABEL_OFFSET["se"][0]
                        label_y = coords[1] + ct.EDGE_LABEL_OFFSET["se"][1]
                        label_anchor = "se"
                        label_justify = "right"
                    else:
                        label_x = coords[0] + ct.EDGE_LABEL_OFFSET["ne"][0]
                        label_y = coords[1] + ct.EDGE_LABEL_OFFSET["ne"][1]
                        label_anchor = "ne"
                        label_justify = "right"
            else:
                coords = []
                print("Error: Invalid connection_point values")

        if coords == [] or coords is None:
            coords = self.simple_line_anchor(from_node_obj, to_node_obj)
            # self.from_node_connection_point = None
            # self.to_node_connection_point = None

        if coords is not None and coords != [] and (label_x is None or label_y is None):
            label_x = (coords[0] + coords[2]) / 2 + ct.EDGE_LABEL_OFFSET["center"][0]
            label_y = (coords[1] + coords[3]) / 2 + ct.EDGE_LABEL_OFFSET["center"][1]
            label_anchor = "center"
            label_justify = "center"

        return coords, label_x, label_y, label_anchor, label_justify

    def line_anchor(self, from_node_obj, to_node_obj):
        # fromノードとtoノードの中心を結ぶ直線上のアンカー
        coords = []
        if from_node_obj.x is None or from_node_obj.y is None or from_node_obj.h is None or from_node_obj.w is None:
            return coords, None, None, "center", "center"
        if to_node_obj.x is None or to_node_obj.y is None or to_node_obj.h is None or to_node_obj.w is None:
            return coords, None, None, "center", "center"

        from_x, from_y = self.from_rect_intersection(from_node_obj, to_node_obj)
        to_x, to_y = self.to_rect_intersection(from_node_obj, to_node_obj)

        coords = [from_x, from_y, to_x, to_y]

        label_x = (coords[0] + coords[2]) / 2 + ct.EDGE_LABEL_OFFSET["center"][0]
        label_y = (coords[1] + coords[3]) / 2 + ct.EDGE_LABEL_OFFSET["center"][1]
        label_anchor = "center"
        label_justify = "center"

        return coords, label_x, label_y, label_anchor, label_justify

    def simple_line_anchor(self, from_node_obj, to_node_obj):
        """直線アンカー座標計算"""
        coords = [from_node_obj.x, from_node_obj.y, to_node_obj.x, to_node_obj.y]
        return coords

    def from_rect_intersection(self, from_node_obj, to_node_obj):
        lx1, ly1, lw1, lh1 = from_node_obj.x, from_node_obj.y, from_node_obj.w, from_node_obj.h
        lx2, ly2, lw2, lh2 = to_node_obj.x, to_node_obj.y, to_node_obj.w, to_node_obj.h
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

    def to_rect_intersection(self, from_node_obj, to_node_obj):
        lx1, ly1, lw1, lh1 = from_node_obj.x, from_node_obj.y, from_node_obj.w, from_node_obj.h
        lx2, ly2, lw2, lh2 = to_node_obj.x, to_node_obj.y, to_node_obj.w, to_node_obj.h
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
        # from_top_x, from_top_y = from_center_x, from_center_y - from_height / 2
        from_bottom_x, from_bottom_y = from_center_x, from_center_y + from_height / 2
        # from_left_x, from_left_y = from_center_x - from_width / 2, from_center_y
        # from_right_x, from_right_y = from_center_x + from_width / 2, from_center_y

        to_center_x, to_center_y, to_width, to_height = to_node_obj.x, to_node_obj.y, to_node_obj.w, to_node_obj.h
        to_top_x, to_top_y = to_center_x, to_center_y - to_height / 2
        # to_bottom_x, to_bottom_y = to_center_x, to_center_y + to_height / 2
        # to_left_x, to_left_y = to_center_x - to_width / 2, to_center_y
        #to_right_x, to_right_y = to_center_x + to_width / 2, to_center_y

        if from_bottom_y <= to_top_y:
            if from_bottom_x == to_top_x:
                # 1line
                coords = [from_bottom_x, from_bottom_y, to_top_x, to_top_y]
            else:
                # 3line
                if self.edge_wrap_margin is None:
                    mid_y = (from_bottom_y + to_top_y) / 2
                else:
                    mid_y = from_bottom_y + self.edge_wrap_margin
                coords = [from_bottom_x, from_bottom_y, from_bottom_x, mid_y, to_top_x, mid_y, to_top_x, to_top_y]
        else:
            # 5line
            margin_ya = from_bottom_y + from_node_obj.h * 0.5
            margin_yb = to_top_y - to_node_obj.h * 0.5
            if self.edge_wrap_margin is None:
                mid_x = (from_bottom_x + to_top_x) / 2
            else:
                mid_x = from_bottom_x + self.edge_wrap_margin
            coords = [from_bottom_x, from_bottom_y, from_bottom_x, margin_ya, mid_x, margin_ya, mid_x, margin_yb, to_top_x, margin_yb, to_top_x, to_top_y]

        return coords

    def rect_anchor_bottom_to_right(self, from_node_obj, to_node_obj):
        # bottom_to_right   2line or 4line
        # 条件： toオブジェクトの右点がfromオブジェクトの下点より左下にある場合、2line
        #     ： toオブジェクトの右点がfromオブジェクトの下点より左上にある場合、4line
        coords = []
        if from_node_obj.x is None or from_node_obj.y is None or from_node_obj.h is None or from_node_obj.w is None:
            return coords
        if to_node_obj.x is None or to_node_obj.y is None or to_node_obj.h is None or to_node_obj.w is None:
            return coords

        from_center_x, from_center_y, from_width, from_height = from_node_obj.x, from_node_obj.y, from_node_obj.w, from_node_obj.h
        # from_top_x, from_top_y = from_center_x, from_center_y - from_height / 2
        from_bottom_x, from_bottom_y = from_center_x, from_center_y + from_height / 2
        from_left_x, from_left_y = from_center_x - from_width / 2, from_center_y
        # from_right_x, from_right_y = from_center_x + from_width / 2, from_center_y

        to_center_x, to_center_y, to_width, to_height = to_node_obj.x, to_node_obj.y, to_node_obj.w, to_node_obj.h
        # to_top_x, to_top_y = to_center_x, to_center_y - to_height / 2
        # to_bottom_x, to_bottom_y = to_center_x, to_center_y + to_height / 2
        # to_left_x, to_left_y = to_center_x - to_width / 2, to_center_y
        to_right_x, to_right_y = to_center_x + to_width / 2, to_center_y

        if to_right_x < from_bottom_x and from_bottom_y < to_right_y:
            coords = [from_bottom_x, from_bottom_y, from_bottom_x, to_right_y, to_right_x, to_right_y]
        elif to_right_x < from_bottom_x and to_right_y <= from_bottom_y:
            if self.edge_wrap_margin is None:
                margin_y = from_bottom_y + from_node_obj.h * 0.5
                margin_x = (from_left_x + to_right_x) / 2
            else:
                margin_y = from_bottom_y + from_node_obj.h * 0.5
                margin_x = from_left_x - self.edge_wrap_margin
            coords = [from_bottom_x, from_bottom_y, from_bottom_x, margin_y, margin_x, margin_y, margin_x, to_right_y, to_right_x, to_right_y]

        return coords

    def rect_anchor_bottom_to_left(self, from_node_obj, to_node_obj):
        # bottom_to_left    2line or 4line
        # 条件： toオブジェクトの左点がfromオブジェクトの下点より右下にある場合、2line
        #     ： toオブジェクトの左点がfromオブジェクトの下点より右上にある場合、4line
        coords = []
        if from_node_obj.x is None or from_node_obj.y is None or from_node_obj.h is None or from_node_obj.w is None:
            return coords
        if to_node_obj.x is None or to_node_obj.y is None or to_node_obj.h is None or to_node_obj.w is None:
            return coords

        from_center_x, from_center_y, from_width, from_height = from_node_obj.x, from_node_obj.y, from_node_obj.w, from_node_obj.h
        # from_top_x, from_top_y = from_center_x, from_center_y - from_height / 2
        from_bottom_x, from_bottom_y = from_center_x, from_center_y + from_height / 2
        # from_left_x, from_left_y = from_center_x - from_width / 2, from_center_y
        from_right_x, from_right_y = from_center_x + from_width / 2, from_center_y

        to_center_x, to_center_y, to_width, to_height = to_node_obj.x, to_node_obj.y, to_node_obj.w, to_node_obj.h
        # to_top_x, to_top_y = to_center_x, to_center_y - to_height / 2
        # to_bottom_x, to_bottom_y = to_center_x, to_center_y + to_height / 2
        to_left_x, to_left_y = to_center_x - to_width / 2, to_center_y
        # to_right_x, to_right_y = to_center_x + to_width / 2, to_center_y

        if from_bottom_x < to_left_x and from_bottom_y < to_left_y:
            coords = [from_bottom_x, from_bottom_y, from_bottom_x, to_left_y, to_left_x, to_left_y]
        elif from_bottom_x < to_left_x and to_left_y <= from_bottom_y:
            if self.edge_wrap_margin is None:
                margin_y = from_bottom_y + from_node_obj.h * 0.5
                margin_x = (from_right_x + to_left_x) / 2
            else:
                margin_y = from_bottom_y + from_node_obj.h * 0.5
                margin_x = from_right_x + self.edge_wrap_margin
            coords = [from_bottom_x, from_bottom_y, from_bottom_x, margin_y, margin_x, margin_y, margin_x, to_left_y, to_left_x, to_left_y]

        return coords

    def rect_anchor_bottom_to_bottom(self, from_node_obj, to_node_obj):
        # bottom_to_bottom  3line
        coords = []
        if from_node_obj.x is None or from_node_obj.y is None or from_node_obj.h is None or from_node_obj.w is None:
            return coords
        if to_node_obj.x is None or to_node_obj.y is None or to_node_obj.h is None or to_node_obj.w is None:
            return coords

        from_center_x, from_center_y, from_width, from_height = from_node_obj.x, from_node_obj.y, from_node_obj.w, from_node_obj.h
        # from_top_x, from_top_y = from_center_x, from_center_y - from_height / 2
        from_bottom_x, from_bottom_y = from_center_x, from_center_y + from_height / 2
        # from_left_x, from_left_y = from_center_x - from_width / 2, from_center_y
        # from_right_x, from_right_y = from_center_x + from_width / 2, from_center_y

        to_center_x, to_center_y, to_width, to_height = to_node_obj.x, to_node_obj.y, to_node_obj.w, to_node_obj.h
        # to_top_x, to_top_y = to_center_x, to_center_y - to_height / 2
        to_bottom_x, to_bottom_y = to_center_x, to_center_y + to_height / 2
        # to_left_x, to_left_y = to_center_x - to_width / 2, to_center_y
        # to_right_x, to_right_y = to_center_x + to_width / 2, to_center_y

        if self.edge_wrap_margin is None:
            margin_y = max(from_bottom_y, to_bottom_y) + from_node_obj.h * 0.5
        else:
            margin_y = max(from_bottom_y, to_bottom_y) + self.edge_wrap_margin
        coords = [from_bottom_x, from_bottom_y, from_bottom_x, margin_y, to_bottom_x, margin_y, to_bottom_x, to_bottom_y]

        return coords

    def rect_anchor_right_to_top(self, from_node_obj, to_node_obj):
        # right_to_top    2line or 4line
        # 条件： toオブジェクトの上点がfromオブジェクトの右点より右下にある場合、2line
        #    ： toオブジェクトの上点がfromオブジェクトの右点より右上にある場合、4line
        coords = []
        if from_node_obj.x is None or from_node_obj.y is None or from_node_obj.h is None or from_node_obj.w is None:
            return coords
        if to_node_obj.x is None or to_node_obj.y is None or to_node_obj.h is None or to_node_obj.w is None:
            return coords

        from_center_x, from_center_y, from_width, from_height = from_node_obj.x, from_node_obj.y, from_node_obj.w, from_node_obj.h
        # from_top_x, from_top_y = from_center_x, from_center_y - from_height / 2
        # from_bottom_x, from_bottom_y = from_center_x, from_center_y + from_height / 2
        # from_left_x, from_left_y = from_center_x - from_width / 2, from_center_y
        from_right_x, from_right_y = from_center_x + from_width / 2, from_center_y

        to_center_x, to_center_y, to_width, to_height = to_node_obj.x, to_node_obj.y, to_node_obj.w, to_node_obj.h
        to_top_x, to_top_y = to_center_x, to_center_y - to_height / 2
        # to_bottom_x, to_bottom_y = to_center_x, to_center_y + to_height / 2
        to_left_x, to_left_y = to_center_x - to_width / 2, to_center_y
        # to_right_x, to_right_y = to_center_x + to_width / 2, to_center_y

        if from_right_x < to_top_x and from_right_y < to_top_y:
            coords = [from_right_x, from_right_y, to_top_x, from_right_y, to_top_x, to_top_y]
        elif from_right_x < to_top_x and to_top_y <= from_right_y:
            if self.edge_wrap_margin is None:
                margin_x = (from_right_x + to_left_x ) / 2
                margin_y = to_top_y - from_node_obj.h * 0.5
            else:
                margin_x = from_right_x + self.edge_wrap_margin
                margin_y = to_top_y - from_node_obj.h * 0.5
            coords = [from_right_x, from_right_y, margin_x, from_right_y, margin_x, margin_y, to_top_x, margin_y, to_top_x, to_top_y]

        return coords

    def rect_anchor_right_to_right(self, from_node_obj, to_node_obj):
        # right_to_right  3line
        # 条件: 3line
        coords = []
        if from_node_obj.x is None or from_node_obj.y is None or from_node_obj.h is None or from_node_obj.w is None:
            return coords
        if to_node_obj.x is None or to_node_obj.y is None or to_node_obj.h is None or to_node_obj.w is None:
            return coords
        
        from_center_x, from_center_y, from_width, from_height = from_node_obj.x, from_node_obj.y, from_node_obj.w, from_node_obj.h
        from_top_x, from_top_y = from_center_x, from_center_y - from_height / 2
        # from_bottom_x, from_bottom_y = from_center_x, from_center_y + from_height / 2
        # from_left_x, from_left_y = from_center_x - from_width / 2, from_center_y
        from_right_x, from_right_y = from_center_x + from_width / 2, from_center_y

        to_center_x, to_center_y, to_width, to_height = to_node_obj.x, to_node_obj.y, to_node_obj.w, to_node_obj.h
        # to_top_x, to_top_y = to_center_x, to_center_y - to_height / 2
        to_bottom_x, to_bottom_y = to_center_x, to_center_y + to_height / 2
        # to_left_x, to_left_y = to_center_x - to_width / 2, to_center_y
        to_right_x, to_right_y = to_center_x + to_width / 2, to_center_y

        # if to_bottom_y <= from_top_y:
        if self.edge_wrap_margin is None:
            mid_x = max(from_right_x, to_right_x) + from_node_obj.w * 0.3
        else:
            mid_x = max(from_right_x, to_right_x) + self.edge_wrap_margin
        coords = [from_right_x, from_right_y, mid_x, from_right_y, mid_x, to_right_y, to_right_x, to_right_y]

        return coords

    def rect_anchor_right_to_left(self, from_node_obj, to_node_obj):
        # right_to_left   1line or 3line
        # 条件: fromオブジェクトが分岐で、fromオブジェクトとtoオブジェクトが重なっていない、
        #           toオブジェクトがfromオブジェクトと同じ高さで右側にある場合、1line
        #           toオブジェクトがfromオブジェクトより上にある場合、3line
        coords = []
        if from_node_obj.x is None or from_node_obj.y is None or from_node_obj.h is None or from_node_obj.w is None:
            return coords
        if to_node_obj.x is None or to_node_obj.y is None or to_node_obj.h is None or to_node_obj.w is None:
            return coords
        
        from_center_x, from_center_y, from_width, from_height = from_node_obj.x, from_node_obj.y, from_node_obj.w, from_node_obj.h
        # from_top_x, from_top_y = from_center_x, from_center_y - from_height / 2
        # from_bottom_x, from_bottom_y = from_center_x, from_center_y + from_height / 2
        # from_left_x, from_left_y = from_center_x - from_width / 2, from_center_y
        from_right_x, from_right_y = from_center_x + from_width / 2, from_center_y

        to_center_x, to_center_y, to_width, to_height = to_node_obj.x, to_node_obj.y, to_node_obj.w, to_node_obj.h
        # to_top_x, to_top_y = to_center_x, to_center_y - to_height / 2
        # to_bottom_x, to_bottom_y = to_center_x, to_center_y + to_height / 2
        to_left_x, to_left_y = to_center_x - to_width / 2, to_center_y
        # to_right_x, to_right_y = to_center_x + to_width / 2, to_center_y

        if from_right_x < to_left_x:
            if from_right_y == to_left_y:
                coords = [from_right_x, from_right_y, to_left_x, to_left_y]
            elif to_left_y < from_right_y:
                if self.edge_wrap_margin is None:
                    mid_x = (from_right_x + to_left_x) / 2
                else:
                    mid_x = from_right_x + self.edge_wrap_margin
                coords = [from_right_x, from_right_y, mid_x, from_right_y, mid_x, to_left_y, to_left_x, to_left_y]
            elif from_right_y < to_left_y:
                if self.edge_wrap_margin is None:
                    mid_x = (from_right_x + to_left_x) / 2
                else:
                    mid_x = from_right_x + self.edge_wrap_margin
                coords = [from_right_x, from_right_y, mid_x, from_right_y, mid_x, to_left_y, to_left_x, to_left_y]

        return coords

    def rect_anchor_right_to_bottom(self, from_node_obj, to_node_obj):
        # right_to_top    2line or 4line
        # 条件： toオブジェクトの下点がfromオブジェクトの右点より右下にある場合、2line
        #    ： toオブジェクトの下点がfromオブジェクトの右点より右上にある場合、4line

        coords = []
        if from_node_obj.x is None or from_node_obj.y is None or from_node_obj.h is None or from_node_obj.w is None:
            return coords
        if to_node_obj.x is None or to_node_obj.y is None or to_node_obj.h is None or to_node_obj.w is None:
            return coords

        from_center_x, from_center_y, from_width, from_height = from_node_obj.x, from_node_obj.y, from_node_obj.w, from_node_obj.h
        # from_top_x, from_top_y = from_center_x, from_center_y - from_height / 2
        from_bottom_x, from_bottom_y = from_center_x, from_center_y + from_height / 2
        # from_left_x, from_left_y = from_center_x - from_width / 2, from_center_y
        from_right_x, from_right_y = from_center_x + from_width / 2, from_center_y

        to_center_x, to_center_y, to_width, to_height = to_node_obj.x, to_node_obj.y, to_node_obj.w, to_node_obj.h
        # to_top_x, to_top_y = to_center_x, to_center_y - to_height / 2
        to_bottom_x, to_bottom_y = to_center_x, to_center_y + to_height / 2
        to_left_x, to_left_y = to_center_x - to_width / 2, to_center_y
        to_right_x, to_right_y = to_center_x + to_width / 2, to_center_y

        if from_right_x < to_bottom_x and to_bottom_y < from_right_y:
            coords = [from_right_x, from_right_y, to_bottom_x, from_right_y, to_bottom_x, to_bottom_y]
        elif from_right_x < to_bottom_x and from_right_y <= to_bottom_y:
            if self.edge_wrap_margin is None:
                margin_x = (from_right_x + to_left_x) / 2
                margin_y = to_bottom_y + from_node_obj.h * 0.5
            else:
                margin_x = to_right_x + self.edge_wrap_margin
                margin_y = to_bottom_y + from_node_obj.h * 0.5
            coords = [from_right_x, from_right_y, margin_x, from_right_y, margin_x, margin_y, to_bottom_x, margin_y, to_bottom_x, to_bottom_y]

        return coords

    def rect_anchor_left_to_top(self, from_node_obj, to_node_obj):
        # left_to_top     2line
        # 条件： bottom点からのリンクが既にあり右点からのリンクが無い、toオブジェクトの上点がfromオブジェクトの右点より右下にある場合、2line
        coords = []
        if from_node_obj.x is None or from_node_obj.y is None or from_node_obj.h is None or from_node_obj.w is None:
            return coords
        if to_node_obj.x is None or to_node_obj.y is None or to_node_obj.h is None or to_node_obj.w is None:
            return coords

        from_center_x, from_center_y, from_width, from_height = from_node_obj.x, from_node_obj.y, from_node_obj.w, from_node_obj.h
        # from_top_x, from_top_y = from_center_x, from_center_y - from_height / 2
        # from_bottom_x, from_bottom_y = from_center_x, from_center_y + from_height / 2
        from_left_x, from_left_y = from_center_x - from_width / 2, from_center_y
        # from_right_x, from_right_y = from_center_x + from_width / 2, from_center_y

        to_center_x, to_center_y, to_width, to_height = to_node_obj.x, to_node_obj.y, to_node_obj.w, to_node_obj.h
        to_top_x, to_top_y = to_center_x, to_center_y - to_height / 2
        # to_bottom_x, to_bottom_y = to_center_x, to_center_y + to_height / 2
        # to_left_x, to_left_y = to_center_x - to_width / 2, to_center_y
        # to_right_x, to_right_y = to_center_x + to_width / 2, to_center_y

        if to_top_x < from_left_x and to_top_y > from_left_y:
            coords = [from_left_x, from_left_y, to_top_x, from_left_y, to_top_x, to_top_y]

        return coords

    def rect_anchor_left_to_right(self, from_node_obj, to_node_obj):
        # left_to_right   1line or 3line
        # 条件: fromオブジェクトが分岐で、fromオブジェクトとtoオブジェクトが重なっていない
        #           toオブジェクトがfromオブジェクトと同じ高さで左側にある場合、1line
        #           toオブジェクトがfromオブジェクトより上にある場合、3line
        coords = []
        if from_node_obj.x is None or from_node_obj.y is None or from_node_obj.h is None or from_node_obj.w is None:
            return coords
        if to_node_obj.x is None or to_node_obj.y is None or to_node_obj.h is None or to_node_obj.w is None:
            return coords

        from_center_x, from_center_y, from_width, from_height = from_node_obj.x, from_node_obj.y, from_node_obj.w, from_node_obj.h
        # from_top_x, from_top_y = from_center_x, from_center_y - from_height / 2
        # from_bottom_x, from_bottom_y = from_center_x, from_center_y + from_height / 2
        from_left_x, from_left_y = from_center_x - from_width / 2, from_center_y
        # from_right_x, from_right_y = from_center_x + from_width / 2, from_center_y

        to_center_x, to_center_y, to_width, to_height = to_node_obj.x, to_node_obj.y, to_node_obj.w, to_node_obj.h
        # to_top_x, to_top_y = to_center_x, to_center_y - to_height / 2
        # to_bottom_x, to_bottom_y = to_center_x, to_center_y + to_height / 2
        # to_left_x, to_left_y = to_center_x - to_width / 2, to_center_y
        to_right_x, to_right_y = to_center_x + to_width / 2, to_center_y

        if to_right_x < from_left_x:
            if from_left_y == to_right_y:
                coords = [from_left_x, from_left_y, to_right_x, to_right_y]
            elif to_right_y < from_left_y:
                if self.edge_wrap_margin is None:
                    mid_x = (from_left_x + to_right_x) / 2
                else:
                    mid_x = from_left_x + self.edge_wrap_margin
                coords = [from_left_x, from_left_y, mid_x, from_left_y, mid_x, to_right_y, to_right_x, to_right_y]
            elif from_left_y < to_right_y:
                if self.edge_wrap_margin is None:
                    mid_x = (from_left_x + to_right_x) / 2
                else:
                    mid_x = from_left_x + self.edge_wrap_margin
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
        # from_bottom_x, from_bottom_y = from_center_x, from_center_y + from_height / 2
        from_left_x, from_left_y = from_center_x - from_width / 2, from_center_y
        # from_right_x, from_right_y = from_center_x + from_width / 2, from_center_y

        to_center_x, to_center_y, to_width, to_height = to_node_obj.x, to_node_obj.y, to_node_obj.w, to_node_obj.h
        # to_top_x, to_top_y = to_center_x, to_center_y - to_height / 2
        to_bottom_x, to_bottom_y = to_center_x, to_center_y + to_height / 2
        to_left_x, to_left_y = to_center_x - to_width / 2, to_center_y
        # to_right_x, to_right_y = to_center_x + to_width / 2, to_center_y

        # if to_bottom_y <= from_top_y:
        if self.edge_wrap_margin is None:
            mid_x = min(from_left_x, to_left_x) - from_node_obj.w * 0.3
        else:
            mid_x = min(from_left_x, to_left_x) - self.edge_wrap_margin
        coords = [from_left_x, from_left_y, mid_x, from_left_y, mid_x, to_left_y, to_left_x, to_left_y]

        return coords

    def rect_anchor_left_to_bottom(self, from_node_obj, to_node_obj):
        # left_to_bottom　 2line
        # 条件： toオブジェクトの下点がfromオブジェクトの左点より左上にある場合、2line
        #     ： toオブジェクトの下点がfromオブジェクトの左点より左下にある場合、4line
        coords = []
        if from_node_obj.x is None or from_node_obj.y is None or from_node_obj.h is None or from_node_obj.w is None:
            return coords
        if to_node_obj.x is None or to_node_obj.y is None or to_node_obj.h is None or to_node_obj.w is None:
            return coords

        from_center_x, from_center_y, from_width, from_height = from_node_obj.x, from_node_obj.y, from_node_obj.w, from_node_obj.h
        # from_top_x, from_top_y = from_center_x, from_center_y - from_height / 2
        # from_bottom_x, from_bottom_y = from_center_x, from_center_y + from_height / 2
        from_left_x, from_left_y = from_center_x - from_width / 2, from_center_y
        from_right_x, from_right_y = from_center_x + from_width / 2, from_center_y

        to_center_x, to_center_y, to_width, to_height = to_node_obj.x, to_node_obj.y, to_node_obj.w, to_node_obj.h
        # to_top_x, to_top_y = to_center_x, to_center_y - to_height / 2
        to_bottom_x, to_bottom_y = to_center_x, to_center_y + to_height / 2
        # to_left_x, to_left_y = to_center_x - to_width / 2, to_center_y
        to_right_x, to_right_y = to_center_x + to_width / 2, to_center_y

        if to_bottom_x < from_left_x and to_bottom_y < from_left_y:
            coords = [from_left_x, from_left_y, to_bottom_x, from_left_y, to_bottom_x, to_bottom_y]
        elif to_bottom_x < from_left_x and from_left_y <= to_bottom_y:
            if self.edge_wrap_margin is None:
                margin_x = (from_left_x + to_right_x) / 2
                margin_y = to_bottom_y + from_node_obj.h * 0.5
            else:
                margin_x = from_left_x - self.edge_wrap_margin
                margin_y = to_bottom_y + from_node_obj.h * 0.5
            coords = [from_left_x, from_left_y, margin_x, from_left_y, margin_x, margin_y, to_bottom_x, margin_y, to_bottom_x, to_bottom_y]

        return coords

    def rect_anchor_top_to_top(self, from_node_obj, to_node_obj):
        # top_to_top    3line
        coords = []
        if from_node_obj.x is None or from_node_obj.y is None or from_node_obj.h is None or from_node_obj.w is None:
            return coords
        if to_node_obj.x is None or to_node_obj.y is None or to_node_obj.h is None or to_node_obj.w is None:
            return coords

        from_center_x, from_center_y, from_width, from_height = from_node_obj.x, from_node_obj.y, from_node_obj.w, from_node_obj.h
        from_top_x, from_top_y = from_center_x, from_center_y - from_height / 2
        # from_bottom_x, from_bottom_y = from_center_x, from_center_y + from_height / 2
        # from_left_x, from_left_y = from_center_x - from_width / 2, from_center_y
        # from_right_x, from_right_y = from_center_x + from_width / 2, from_center_y

        to_center_x, to_center_y, to_width, to_height = to_node_obj.x, to_node_obj.y, to_node_obj.w, to_node_obj.h
        to_top_x, to_top_y = to_center_x, to_center_y - to_height / 2
        # to_bottom_x, to_bottom_y = to_center_x, to_center_y + to_height / 2
        # to_left_x, to_left_y = to_center_x - to_width / 2, to_center_y
        # to_right_x, to_right_y = to_center_x + to_width / 2, to_center_y

        if self.edge_wrap_margin is None:
            margin_y = min(from_top_y, to_top_y) - from_node_obj.h * 0.5
        else:
            margin_y = min(from_top_y, to_top_y) - self.edge_wrap_margin
        coords = [from_top_x, from_top_y, from_top_x, margin_y, to_top_x, margin_y, to_top_x, to_top_y]

        return coords

    def rect_anchor_top_to_right(self, from_node_obj, to_node_obj):
        # top_to_right     2line or 4line
        # 条件： toオブジェクトの右点がfromオブジェクトの上点より左上にある場合、2line
        #    ： toオブジェクトの右点がfromオブジェクトの上点より左下にある場合、4line
        coords = []
        if from_node_obj.x is None or from_node_obj.y is None or from_node_obj.h is None or from_node_obj.w is None:
            return coords
        if to_node_obj.x is None or to_node_obj.y is None or to_node_obj.h is None or to_node_obj.w is None:
            return coords

        from_center_x, from_center_y, from_width, from_height = from_node_obj.x, from_node_obj.y, from_node_obj.w, from_node_obj.h
        from_top_x, from_top_y = from_center_x, from_center_y - from_height / 2
        # from_bottom_x, from_bottom_y = from_center_x, from_center_y + from_height / 2
        from_left_x, from_left_y = from_center_x - from_width / 2, from_center_y
        # from_right_x, from_right_y = from_center_x + from_width / 2, from_center_y

        to_center_x, to_center_y, to_width, to_height = to_node_obj.x, to_node_obj.y, to_node_obj.w, to_node_obj.h
        # to_top_x, to_top_y = to_center_x, to_center_y - to_height / 2
        # to_bottom_x, to_bottom_y = to_center_x, to_center_y + to_height / 2
        # to_left_x, to_left_y = to_center_x - to_width / 2, to_center_y
        to_right_x, to_right_y = to_center_x + to_width / 2, to_center_y

        if to_right_x < from_top_x and to_right_y < from_top_y:
            coords = [from_top_x, from_top_y, from_top_x, to_right_y, to_right_x, to_right_y]
        elif to_right_x < from_top_x and from_top_y <= to_right_y:
            if self.edge_wrap_margin is None:
                margin_y = from_top_y - from_node_obj.h * 0.5
                margin_x = (from_left_x + to_right_x) / 2
            else:
                margin_y = from_top_y - from_node_obj.h * 0.5
                margin_x = from_left_x - self.edge_wrap_margin
            coords = [from_top_x, from_top_y, from_top_x, margin_y, margin_x, margin_y, margin_x, to_right_y, to_right_x, to_right_y]

        return coords

    def rect_anchor_top_to_left(self, from_node_obj, to_node_obj):
        # top_to_left      2line or 4line
        # 条件： toオブジェクトの左点がfromオブジェクトの上点より右上にある場合、2line
        #    ： toオブジェクトの左点がfromオブジェクトの上点より右下にある場合、4line
        coords = []
        if from_node_obj.x is None or from_node_obj.y is None or from_node_obj.h is None or from_node_obj.w is None:
            return coords
        if to_node_obj.x is None or to_node_obj.y is None or to_node_obj.h is None or to_node_obj.w is None:
            return coords

        from_center_x, from_center_y, from_width, from_height = from_node_obj.x, from_node_obj.y, from_node_obj.w, from_node_obj.h
        from_top_x, from_top_y = from_center_x, from_center_y - from_height / 2
        # from_bottom_x, from_bottom_y = from_center_x, from_center_y + from_height / 2
        # from_left_x, from_left_y = from_center_x - from_width / 2, from_center_y
        from_right_x, from_right_y = from_center_x + from_width / 2, from_center_y

        to_center_x, to_center_y, to_width, to_height = to_node_obj.x, to_node_obj.y, to_node_obj.w, to_node_obj.h
        # to_top_x, to_top_y = to_center_x, to_center_y - to_height / 2
        # to_bottom_x, to_bottom_y = to_center_x, to_center_y + to_height / 2
        to_left_x, to_left_y = to_center_x - to_width / 2, to_center_y
        # to_right_x, to_right_y = to_center_x + to_width / 2, to_center_y

        if from_top_x < to_left_x and to_left_y < from_top_y:
            coords = [from_top_x, from_top_y, from_top_x, to_left_y, to_left_x, to_left_y]
        elif from_top_x < to_left_x and from_top_y <= to_left_y:
            if self.edge_wrap_margin is None:
                margin_y = from_top_y - from_node_obj.h * 0.5
                margin_x = (from_right_x + to_left_x) / 2
            else:
                margin_y = from_top_y - from_node_obj.h * 0.5
                margin_x = from_right_x + self.edge_wrap_margin
            coords = [from_top_x, from_top_y, from_top_x, margin_y, margin_x, margin_y, margin_x, to_left_y, to_left_x, to_left_y]

        return coords

    def rect_anchor_top_to_bottom(self, from_node_obj, to_node_obj):
        # top_to_bottom  1line or 3line
        coords = []
        if from_node_obj.x is None or from_node_obj.y is None or from_node_obj.h is None or from_node_obj.w is None:
            return coords
        if to_node_obj.x is None or to_node_obj.y is None or to_node_obj.h is None or to_node_obj.w is None:
            return coords

        from_center_x, from_center_y, from_width, from_height = from_node_obj.x, from_node_obj.y, from_node_obj.w, from_node_obj.h
        from_top_x, from_top_y = from_center_x, from_center_y - from_height / 2
        from_bottom_x, from_bottom_y = from_center_x, from_center_y + from_height / 2
        # from_left_x, from_left_y = from_center_x - from_width / 2, from_center_y
        # from_right_x, from_right_y = from_center_x + from_width / 2, from_center_y

        to_center_x, to_center_y, to_width, to_height = to_node_obj.x, to_node_obj.y, to_node_obj.w, to_node_obj.h
        to_top_x, to_top_y = to_center_x, to_center_y - to_height / 2
        to_bottom_x, to_bottom_y = to_center_x, to_center_y + to_height / 2
        # to_left_x, to_left_y = to_center_x - to_width / 2, to_center_y
        # to_right_x, to_right_y = to_center_x + to_width / 2, to_center_y

        if to_bottom_y < from_top_y:
            if from_top_x == to_top_x:
                coords = [from_top_x, from_top_y, to_bottom_x, to_bottom_y]
            else:
                if self.edge_wrap_margin is None:
                    middle_y = (from_top_y + to_bottom_y) / 2
                else:
                    middle_y = from_top_y - self.edge_wrap_margin
                coords = [from_top_x, from_top_y, from_top_x, middle_y, to_bottom_x, middle_y, to_bottom_x, to_bottom_y]

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
            dash_pattern = self.get_dash_pattern()

            canvas.coords(self.line_id, *self.points)
            canvas.itemconfig(self.line_id, dash=dash_pattern)
            if self.label_id and self.label_x and self.label_y:
                canvas.coords(self.label_id, self.label_x, self.label_y)

    def rotate_connection_points(self, increase=True, canvas=None):
        if self.edge_type == "elbow":
            self.rotate_elbow_connection_points(increase=increase, canvas=canvas)
        else:
            self.rotate_line_style(increase=increase, canvas=canvas)

    def rotate_line_style(self, increase=True, canvas=None):
        """エッジの線種をローテーションして再描画"""
        if increase:
            if self.line_style == ct.EDGE_LINE_STYLE_DASHED:
                self.line_style = ct.EDGE_LINE_STYLE_DOTTED
            elif self.line_style == ct.EDGE_LINE_STYLE_DOTTED:
                self.line_style = ct.EDGE_LINE_STYLE_SOLID
            else:
                self.line_style = ct.EDGE_LINE_STYLE_DASHED
        else:
            if self.line_style == ct.EDGE_LINE_STYLE_DASHED:
                self.line_style = ct.EDGE_LINE_STYLE_SOLID
            elif self.line_style == ct.EDGE_LINE_STYLE_DOTTED:
                self.line_style = ct.EDGE_LINE_STYLE_DASHED
            else:
                self.line_style = ct.EDGE_LINE_STYLE_DOTTED
        # print(f"** Rotate Line Style: {self.line_style} (increase: {increase})")
        if canvas and self.line_id:
            dash_pattern = self.get_dash_pattern()
            canvas.itemconfig(self.line_id, dash=dash_pattern)

    def rotate_elbow_connection_points(self, increase=True, canvas=None):
        """エッジの接続ポイントをローテーションして再描画(配線できないパターンを避けて最大18回スキャン)"""
        loop = 0
        while loop <= 17:
            self._rotate_elbow_connection_points(increase=increase, canvas=canvas)
            from_x, from_y = self.points[0], self.points[1]
            if self.from_node_obj and self.from_node_obj.x is not None and self.from_node_obj.y is not None:
                if self.from_node_connection_point == "auto" \
                or from_x != self.from_node_obj.x \
                or from_y != self.from_node_obj.y:
                    break
            loop += 1

    def _rotate_elbow_connection_points(self, increase=True, canvas=None):
        """エッジの接続ポイントをローテーション"""
        if self.from_node_obj is None or self.to_node_obj is None:
            return

        from_node_connection_point = self.from_node_connection_point
        to_node_connection_point = self.to_node_connection_point

        if increase:
            if from_node_connection_point == "auto" and to_node_connection_point == "auto":
                from_node_connection_point = "left"
                to_node_connection_point = "left"
            elif from_node_connection_point == "top" and to_node_connection_point == "top":
                from_node_connection_point = "left"
                to_node_connection_point = "left"
            elif from_node_connection_point == "top" and to_node_connection_point == "right":
                from_node_connection_point = "top"
                to_node_connection_point = "top"
            elif from_node_connection_point == "top" and to_node_connection_point == "bottom":
                from_node_connection_point = "top"
                to_node_connection_point = "right"
            elif from_node_connection_point == "top" and to_node_connection_point == "left":
                from_node_connection_point = "top"
                to_node_connection_point = "bottom"
            elif from_node_connection_point == "right" and to_node_connection_point == "top":
                from_node_connection_point = "top"
                to_node_connection_point = "left"
            elif from_node_connection_point == "right" and to_node_connection_point == "right":
                from_node_connection_point = "right"
                to_node_connection_point = "top"
            elif from_node_connection_point == "right" and to_node_connection_point == "bottom":
                from_node_connection_point = "right"
                to_node_connection_point = "right"
            elif from_node_connection_point == "right" and to_node_connection_point == "left":
                from_node_connection_point = "right"
                to_node_connection_point = "bottom"
            elif from_node_connection_point == "bottom" and to_node_connection_point == "top":
                from_node_connection_point = "right"
                to_node_connection_point = "left"
            elif from_node_connection_point == "bottom" and to_node_connection_point == "right":
                from_node_connection_point = "bottom"
                to_node_connection_point = "top"
            elif from_node_connection_point == "bottom" and to_node_connection_point == "bottom":
                from_node_connection_point = "bottom"
                to_node_connection_point = "right"
            elif from_node_connection_point == "bottom" and to_node_connection_point == "left":
                from_node_connection_point = "bottom"
                to_node_connection_point = "bottom"
            elif from_node_connection_point == "left" and to_node_connection_point == "top":
                from_node_connection_point = "bottom"
                to_node_connection_point = "left"
            elif from_node_connection_point == "left" and to_node_connection_point == "right":
                from_node_connection_point = "left"
                to_node_connection_point = "top" 
            elif from_node_connection_point == "left" and to_node_connection_point == "bottom":
                from_node_connection_point = "left"
                to_node_connection_point = "right"
            elif from_node_connection_point == "left" and to_node_connection_point == "left":
                from_node_connection_point = "left"
                to_node_connection_point = "bottom"
            else:
                from_node_connection_point = "auto"
                to_node_connection_point = "auto"
        else:
            if from_node_connection_point == "auto" and to_node_connection_point == "auto":
                from_node_connection_point = "top"
                to_node_connection_point = "top"
            elif from_node_connection_point == "top" and to_node_connection_point == "top":
                from_node_connection_point = "top"
                to_node_connection_point = "right"
            elif from_node_connection_point == "top" and to_node_connection_point == "right":
                from_node_connection_point = "top"
                to_node_connection_point = "bottom"
            elif from_node_connection_point == "top" and to_node_connection_point == "bottom":
                from_node_connection_point = "top"
                to_node_connection_point = "left"
            elif from_node_connection_point == "top" and to_node_connection_point == "left":
                from_node_connection_point = "right"
                to_node_connection_point = "top"
            elif from_node_connection_point == "right" and to_node_connection_point == "top":
                from_node_connection_point = "right"
                to_node_connection_point = "right"
            elif from_node_connection_point == "right" and to_node_connection_point == "right":
                from_node_connection_point = "right"
                to_node_connection_point = "bottom"
            elif from_node_connection_point == "right" and to_node_connection_point == "bottom":
                from_node_connection_point = "right"
                to_node_connection_point = "left"
            elif from_node_connection_point == "right" and to_node_connection_point == "left":
                from_node_connection_point = "bottom"
                to_node_connection_point = "top"
            elif from_node_connection_point == "bottom" and to_node_connection_point == "top":
                from_node_connection_point = "bottom"
                to_node_connection_point = "right"
            elif from_node_connection_point == "bottom" and to_node_connection_point == "right":
                from_node_connection_point = "bottom"
                to_node_connection_point = "bottom"
            elif from_node_connection_point == "bottom" and to_node_connection_point == "bottom":
                from_node_connection_point = "bottom"
                to_node_connection_point = "left"
            elif from_node_connection_point == "bottom" and to_node_connection_point == "left":
                from_node_connection_point = "left"
                to_node_connection_point = "top"
            elif from_node_connection_point == "left" and to_node_connection_point == "top":
                from_node_connection_point = "left"
                to_node_connection_point = "right"
            elif from_node_connection_point == "left" and to_node_connection_point == "right":
                from_node_connection_point = "left"
                to_node_connection_point = "bottom" 
            elif from_node_connection_point == "left" and to_node_connection_point == "bottom":
                from_node_connection_point = "left"
                to_node_connection_point = "left"
            elif from_node_connection_point == "left" and to_node_connection_point == "left":
                from_node_connection_point = "top"
                to_node_connection_point = "top"
            else:
                from_node_connection_point = "auto"
                to_node_connection_point = "auto"

        self.connection_mode = "manual"
        self.from_node_connection_point = from_node_connection_point
        self.to_node_connection_point = to_node_connection_point
        self.edge_wrap_margin = None

        if canvas is not None:
            self._update_edge(canvas)

    def rotate_label_position(self, increase, canvas):
        # print("rotate_label_position", self.label_position, increase)
        """エッジラベルの位置をローテーションして再描画"""
        if self.label_position is None:
            label_position_index = 0
        else:
            if self.label_position in LABEL_POSITION_LIST:
                label_position_index = LABEL_POSITION_LIST.index(self.label_position)
            else:
                label_position_index = 0

        points_len = len(self.points)
        if points_len == 4:
            label_position_rotation_len = 9
        elif points_len == 6:
            label_position_rotation_len = 13
        elif points_len == 8:
            label_position_rotation_len = 17
        elif points_len == 10:
            label_position_rotation_len = 21
        elif points_len == 12:
            label_position_rotation_len = 25
        else:
            label_position_rotation_len = 1

        if increase:
            next_label_position_index = (label_position_index - 1) % label_position_rotation_len
        else:
            next_label_position_index = (label_position_index + 1) % label_position_rotation_len
        # print(f"label_position pre:{label_position_index}, next:{next_label_position_index}")
        self.label_position = LABEL_POSITION_LIST[next_label_position_index] 
        
        if canvas is not None:
            self._update_edge(canvas)

    def _update_edge(self, canvas):
        """エッジとラベルを再レイアウト"""
        from_node_obj = self.from_node_obj
        to_node_obj = self.to_node_obj
        if self.line_id and from_node_obj and to_node_obj:
            coords, label_x, label_y, label_anchor, labe_justify = self._compute_edge_geometry(from_node_obj, to_node_obj)

            self.update_points(canvas, coords, label_x, label_y)
            dash_pattern = self.get_dash_pattern()

            canvas.coords(self.line_id, *coords)
            canvas.itemconfig(self.line_id, dash=dash_pattern)

            if self.label_text is not None and self.label_id is not None:
                self.label_x, self.label_y, self.label_anchor, self.label_justify = self.get_label_position()
                canvas.coords(self.label_id, self.label_x, self.label_y)
                canvas.itemconfig(self.label_id, anchor=self.label_anchor, justify=self.label_justify)

    def change_edge_wrap_margin_3line(self, increase=True, canvas=None):
        """エッジの折り返しオフセットを変更して再描画"""
        if len(self.points) != 8:
            return

        step_size = ct.CANVAS_PARAMS["grid_spacing"] / 2

        from_x, from_y, vertex1_x, vertex1_y, vertex2_x, vertex2_y, to_x, to_y = self.points
        if from_x == vertex1_x:
            # vertical line
            if from_y < vertex1_y < to_y:
                # vertical middle edge
                distance_to_from_node = vertex1_y - from_y
                if increase:
                    distance_to_from_node += step_size
                    if from_y + distance_to_from_node > to_y - step_size:
                        distance_to_from_node = to_y - from_y - step_size
                    self.edge_wrap_margin = distance_to_from_node
                    vertex_y = from_y + self.edge_wrap_margin
                    self.points = [from_x, from_y, from_x, vertex_y, to_x, vertex_y, to_x, to_y]
                else:
                    distance_to_from_node -= step_size
                    if distance_to_from_node < step_size:
                        distance_to_from_node = step_size
                    self.edge_wrap_margin = distance_to_from_node
                    vertex_y = from_y + self.edge_wrap_margin
                    self.points = [from_x, from_y, from_x, vertex_y, to_x, vertex_y, to_x, to_y]
            elif to_y < vertex1_y < from_y:
                # vertical middle edge
                distance_to_from_node = from_y - vertex1_y
                if increase:
                    distance_to_from_node += step_size
                    if from_y - distance_to_from_node < to_y + step_size:
                        distance_to_from_node = from_y - to_y - step_size
                    self.edge_wrap_margin = distance_to_from_node
                    vertex_y = from_y - self.edge_wrap_margin
                    self.points = [from_x, from_y, from_x, vertex_y, to_x, vertex_y, to_x, to_y]
                else:
                    distance_to_from_node -= step_size
                    if distance_to_from_node < step_size:
                        distance_to_from_node = step_size
                    self.edge_wrap_margin = distance_to_from_node
                    vertex_y = from_y - self.edge_wrap_margin
                    self.points = [from_x, from_y, from_x, vertex_y, to_x, vertex_y, to_x, to_y]
            elif vertex1_y < from_y and vertex2_y < to_y:
                # vertical upper edge
                distance_to_node = min(from_y - vertex1_y, to_y - vertex2_y)
                if increase:
                    distance_to_node += step_size
                    if distance_to_node > step_size * 50:
                        distance_to_node = step_size * 50
                    self.edge_wrap_margin = distance_to_node
                    vertex_y = min(from_y, to_y) - self.edge_wrap_margin
                    self.points = [from_x, from_y, from_x, vertex_y, to_x, vertex_y, to_x, to_y]
                else:
                    distance_to_node -= step_size
                    if distance_to_node < step_size:
                        distance_to_node = step_size
                    self.edge_wrap_margin = distance_to_node
                    vertex_y = min(from_y, to_y) - self.edge_wrap_margin
                    self.points = [from_x, from_y, from_x, vertex_y, to_x, vertex_y, to_x, to_y]
            elif from_y < vertex1_y and to_y < vertex2_y:
                # vertical lower edge
                distance_to_node = min(vertex1_y - from_y, vertex2_y - to_y)
                if increase:
                    distance_to_node += step_size
                    if distance_to_node > step_size * 50:
                        distance_to_node = step_size * 50
                    self.edge_wrap_margin = distance_to_node
                    vertex_y = max(from_y, to_y) + self.edge_wrap_margin
                    self.points = [from_x, from_y, from_x, vertex_y, to_x, vertex_y, to_x, to_y]
                else:
                    distance_to_node -= step_size
                    if distance_to_node < step_size:
                        distance_to_node = step_size
                    self.edge_wrap_margin = distance_to_node
                    vertex_y = max(from_y, to_y) + self.edge_wrap_margin
                    self.points = [from_x, from_y, from_x, vertex_y, to_x, vertex_y, to_x, to_y]
        else:
            # horizontal line
            if from_x < vertex1_x < to_x:
                # horizontal middle edge
                distance_to_from_node = vertex1_x - from_x
                if increase:
                    distance_to_from_node += step_size
                    if from_x + distance_to_from_node > to_x - step_size:
                        distance_to_from_node = to_x - from_x - step_size
                    self.edge_wrap_margin = distance_to_from_node
                    vertex_x = from_x + self.edge_wrap_margin
                    self.points = [from_x, from_y, vertex_x, from_y, vertex_x, to_y, to_x, to_y]
                else:
                    distance_to_from_node -= step_size
                    if distance_to_from_node < step_size:
                        distance_to_from_node = step_size
                    self.edge_wrap_margin = distance_to_from_node
                    vertex_x = from_x + self.edge_wrap_margin
                    self.points = [from_x, from_y, vertex_x, from_y, vertex_x, to_y, to_x, to_y]
            elif to_x < vertex1_x < from_x:
                # horizontal middle edge
                distance_to_from_node = from_x - vertex1_x
                if increase:
                    distance_to_from_node += step_size
                    if from_x - distance_to_from_node < to_x + step_size:
                        distance_to_from_node = from_x - to_x - step_size
                    self.edge_wrap_margin = distance_to_from_node
                    vertex_x = from_x - self.edge_wrap_margin
                    self.points = [from_x, from_y, vertex_x, from_y, vertex_x, to_y, to_x, to_y]
                else:
                    distance_to_from_node -= step_size
                    if distance_to_from_node < step_size:
                        distance_to_from_node = step_size
                    self.edge_wrap_margin = distance_to_from_node
                    vertex_x = from_x - self.edge_wrap_margin
                    self.points = [from_x, from_y, vertex_x, from_y, vertex_x, to_y, to_x, to_y]
            elif vertex1_x < from_x and vertex2_x < to_x:
                # horizontal left edge
                distance_to_node = min(from_x - vertex1_x, to_x - vertex2_x)
                if increase:
                    distance_to_node += step_size
                    if distance_to_node > step_size * 50:
                        distance_to_node = step_size * 50
                    self.edge_wrap_margin = distance_to_node
                    vertex_x = min(from_x, to_x) - self.edge_wrap_margin
                    self.points = [from_x, from_y, vertex_x, from_y, vertex_x, to_y, to_x, to_y]
                else:
                    distance_to_node -= step_size
                    if distance_to_node < step_size:
                        distance_to_node = step_size
                    self.edge_wrap_margin = distance_to_node
                    vertex_x = min(from_x, to_x) - self.edge_wrap_margin
                    self.points = [from_x, from_y, vertex_x, from_y, vertex_x, to_y, to_x, to_y]
            elif from_x < vertex1_x and to_x < vertex2_x:
                # horizontal right edge
                distance_to_node = min(vertex1_x - from_x, vertex2_x - to_x)
                if increase:
                    distance_to_node += step_size
                    if distance_to_node > step_size * 50:
                        distance_to_node = step_size * 50
                    self.edge_wrap_margin = distance_to_node
                    vertex_x = max(from_x, to_x) + self.edge_wrap_margin
                    self.points = [from_x, from_y, vertex_x, from_y, vertex_x, to_y, to_x, to_y]
                else:
                    distance_to_node -= step_size
                    if distance_to_node < step_size:
                        distance_to_node = step_size
                    self.edge_wrap_margin = distance_to_node
                    vertex_x = max(from_x, to_x) + self.edge_wrap_margin
                    self.points = [from_x, from_y, vertex_x, from_y, vertex_x, to_y, to_x, to_y]
        

        if canvas is not None:
            self.refresh_edge(canvas)

    def change_edge_wrap_margin_4line(self, increase=True, canvas=None):
        """エッジの折り返しオフセットを変更して再描画"""
        if len(self.points) != 10:
            return

        step_size = ct.CANVAS_PARAMS["grid_spacing"] / 2
        from_node_half_w = self.from_node_obj.w / 2 if self.from_node_obj and self.from_node_obj.w else 0
        to_node_half_w = self.to_node_obj.w / 2 if self.to_node_obj and self.to_node_obj.w else 0

        from_x, from_y, vertex1_x, vertex1_y, vertex2_x, vertex2_y, vertex3_x, vertex3_y, to_x, to_y = self.points
        if from_x == vertex1_x:
            # vertical - horizontal - vertical - horizontal line
            if from_x < to_x:
                # vertical middle edge
                distance_to_from_node = vertex2_x - (from_x + from_node_half_w)
                if increase:
                    distance_to_from_node += step_size
                    if from_x + from_node_half_w + distance_to_from_node > to_x - step_size:
                        distance_to_from_node = to_x - from_x - from_node_half_w - step_size
                    self.edge_wrap_margin = distance_to_from_node
                    vertex2_x = from_x + from_node_half_w + self.edge_wrap_margin
                    self.points = [from_x, from_y, from_x, vertex1_y, vertex2_x, vertex1_y, vertex2_x, to_y, to_x, to_y]
                else:
                    distance_to_from_node -= step_size
                    if distance_to_from_node < -from_node_half_w * 5:
                        distance_to_from_node = -from_node_half_w * 5
                    self.edge_wrap_margin = distance_to_from_node
                    vertex2_x = from_x + from_node_half_w + self.edge_wrap_margin
                    self.points = [from_x, from_y, from_x, vertex1_y, vertex2_x, vertex1_y, vertex2_x, to_y, to_x, to_y]
            elif to_x < from_x:
                # vertical middle edge
                distance_to_from_node = (from_x - from_node_half_w) - vertex2_x
                if increase:
                    distance_to_from_node += step_size
                    if from_x - from_node_half_w - distance_to_from_node < to_x + step_size:
                        distance_to_from_node = from_x - from_node_half_w - to_x - step_size
                    self.edge_wrap_margin = distance_to_from_node
                    vertex2_x = from_x - from_node_half_w - self.edge_wrap_margin
                    self.points = [from_x, from_y, from_x, vertex1_y, vertex2_x, vertex1_y, vertex2_x, to_y, to_x, to_y]
                else:
                    distance_to_from_node -= step_size
                    if distance_to_from_node < -from_node_half_w * 5:
                        distance_to_from_node = -from_node_half_w * 5
                    self.edge_wrap_margin = distance_to_from_node
                    vertex2_x = from_x - from_node_half_w - self.edge_wrap_margin
                    self.points = [from_x, from_y, from_x, vertex1_y, vertex2_x, vertex1_y, vertex2_x, to_y, to_x, to_y]
        elif from_y == vertex1_y:
            # horizontal - vertical - horizontal - vertical line
            if from_x < vertex1_x < to_x:
                # horizontal middle edge
                distance_to_from_node = vertex1_x - from_x
                if increase:
                    distance_to_from_node += step_size
                    if from_x + distance_to_from_node > to_x - to_node_half_w - step_size:
                        distance_to_from_node = to_x - to_node_half_w - from_x - step_size
                    self.edge_wrap_margin = distance_to_from_node
                    vertex_x = from_x + self.edge_wrap_margin
                    self.points = [from_x, from_y, vertex_x, from_y, vertex_x, vertex3_y, to_x, vertex3_y, to_x, to_y]
                else:
                    distance_to_from_node -= step_size
                    if distance_to_from_node < step_size:
                        distance_to_from_node = step_size
                    self.edge_wrap_margin = distance_to_from_node
                    vertex_x = from_x + self.edge_wrap_margin
                    self.points = [from_x, from_y, vertex_x, from_y, vertex_x, vertex3_y, to_x, vertex3_y, to_x, to_y]
            elif to_x < vertex1_x < from_x:
                # horizontal middle edge
                distance_to_from_node = from_x - vertex1_x
                if increase:
                    distance_to_from_node += step_size
                    if from_x - distance_to_from_node < to_x + to_node_half_w + step_size:
                        distance_to_from_node = from_x - to_x - to_node_half_w - step_size
                    self.edge_wrap_margin = distance_to_from_node
                    vertex_x = from_x - self.edge_wrap_margin
                    self.points = [from_x, from_y, vertex_x, from_y, vertex_x, vertex3_y, to_x, vertex3_y, to_x, to_y]
                else:
                    distance_to_from_node -= step_size
                    if distance_to_from_node < step_size:
                        distance_to_from_node = step_size
                    self.edge_wrap_margin = distance_to_from_node
                    vertex_x = from_x - self.edge_wrap_margin
                    self.points = [from_x, from_y, vertex_x, from_y, vertex_x, vertex3_y, to_x, vertex3_y, to_x, to_y]

        if canvas is not None:
            self.refresh_edge(canvas)

    def change_edge_wrap_margin_5line(self, increase=True, canvas=None):
        """エッジの折り返しオフセットを変更して再描画"""
        if len(self.points) != 12:
            return

        step_size = ct.CANVAS_PARAMS["grid_spacing"] / 2
        from_node_half_w = self.from_node_obj.w / 2 if self.from_node_obj and self.from_node_obj.w else 0
        to_node_half_w = self.to_node_obj.w / 2 if self.to_node_obj and self.to_node_obj.w else 0

        from_x, from_y, vertex1_x, vertex1_y, vertex2_x, vertex2_y, vertex3_x, vertex3_y, vertex4_x, vertex4_y, to_x, to_y = self.points
        if from_x == vertex1_x:
            # vertical - horizontal - vertical - horizontal - vertical line
            distance_to_from_node = vertex2_x - from_x
            if increase:
                distance_to_from_node += step_size
                max_x = max(from_x, to_x) + to_node_half_w * 5
                if from_x + distance_to_from_node > max_x:
                    distance_to_from_node = max_x - from_x
                self.edge_wrap_margin = distance_to_from_node
                vertex2_x = from_x + self.edge_wrap_margin
                self.points = [from_x, from_y, from_x, vertex1_y, vertex2_x, vertex1_y, vertex2_x, vertex3_y, to_x, vertex3_y, to_x, to_y]
            else:
                distance_to_from_node -= step_size
                min_x = min(from_x, to_x) - to_node_half_w * 5
                if from_x + distance_to_from_node < min_x:
                    distance_to_from_node = min_x - from_x
                self.edge_wrap_margin = distance_to_from_node
                vertex2_x = from_x + self.edge_wrap_margin
                self.points = [from_x, from_y, from_x, vertex1_y, vertex2_x, vertex1_y, vertex2_x, vertex3_y, to_x, vertex3_y, to_x, to_y]

        if canvas is not None:
            self.refresh_edge(canvas)

    def get_label_position(self) -> Tuple[int, int, Literal["center", "n", "ne", "e", "se", "s", "sw", "w", "nw"], Literal["left", "center", "right"]]:
        """エッジラベル位置計算"""
        points = self.points
        label_x:int = self.label_x if self.label_x is not None else 0
        label_y:int = self.label_y if self.label_y is not None else 0
        label_anchor:Literal["center", "n", "ne", "e", "se", "s", "sw", "w", "nw"] = self.label_anchor
        labe_justify:Literal["left", "center", "right"] = self.label_justify

        if self.label_position == "p0se":
            if len(points) >= 4:
                label_x = points[0] + ct.EDGE_LABEL_OFFSET["se"][0]
                label_y = points[1] + ct.EDGE_LABEL_OFFSET["se"][1]
                label_anchor = "se"
                labe_justify = "right"
        elif self.label_position == "p0sw":
            if len(points) >= 4:
                label_x = points[0] + ct.EDGE_LABEL_OFFSET["sw"][0]
                label_y = points[1] + ct.EDGE_LABEL_OFFSET["sw"][1]
                label_anchor = "sw"
                labe_justify = "left"
        elif self.label_position == "p0nw":
            if len(points) >= 4:
                label_x = points[0] + ct.EDGE_LABEL_OFFSET["nw"][0]
                label_y = points[1] + ct.EDGE_LABEL_OFFSET["nw"][1]
                label_anchor = "nw"
                labe_justify = "left"
        elif self.label_position == "p0ne":
            if len(points) >= 4:
                label_x = points[0] + ct.EDGE_LABEL_OFFSET["ne"][0]
                label_y = points[1] + ct.EDGE_LABEL_OFFSET["ne"][1]
                label_anchor = "ne"
                labe_justify = "right"
        elif self.label_position == "p1se":
            if len(points) >= 4:
                label_x = points[2] + ct.EDGE_LABEL_OFFSET["se"][0]
                label_y = points[3] + ct.EDGE_LABEL_OFFSET["se"][1]
                label_anchor = "se"
                labe_justify = "right"
        elif self.label_position == "p1sw":
            if len(points) >= 4:
                label_x = points[2] + ct.EDGE_LABEL_OFFSET["sw"][0]
                label_y = points[3] + ct.EDGE_LABEL_OFFSET["sw"][1]
                label_anchor = "sw"
                labe_justify = "left"
        elif self.label_position == "p1nw":
            if len(points) >= 4:
                label_x = points[2] + ct.EDGE_LABEL_OFFSET["nw"][0]
                label_y = points[3] + ct.EDGE_LABEL_OFFSET["nw"][1]
                label_anchor = "nw"
                labe_justify = "left"
        elif self.label_position == "p1ne":
            if len(points) >= 4:
                label_x = points[2] + ct.EDGE_LABEL_OFFSET["ne"][0]
                label_y = points[3] + ct.EDGE_LABEL_OFFSET["ne"][1]
                label_anchor = "ne"
                labe_justify = "right"
        elif self.label_position == "p2se":
            if len(points) >= 6:
                label_x = points[4] + ct.EDGE_LABEL_OFFSET["se"][0]
                label_y = points[5] + ct.EDGE_LABEL_OFFSET["se"][1]
                label_anchor = "se"
                labe_justify = "right"
        elif self.label_position == "p2sw":
            if len(points) >= 6:
                label_x = points[4] + ct.EDGE_LABEL_OFFSET["sw"][0]
                label_y = points[5] + ct.EDGE_LABEL_OFFSET["sw"][1]
                label_anchor = "sw"
                labe_justify = "left"
        elif self.label_position == "p2nw":
            if len(points) >= 6:
                label_x = points[4] + ct.EDGE_LABEL_OFFSET["nw"][0]
                label_y = points[5] + ct.EDGE_LABEL_OFFSET["nw"][1]
                label_anchor = "nw"
                labe_justify = "left"
        elif self.label_position == "p2ne":
            if len(points) >= 6:
                label_x = points[4] + ct.EDGE_LABEL_OFFSET["ne"][0]
                label_y = points[5] + ct.EDGE_LABEL_OFFSET["ne"][1]
                label_anchor = "ne"
                labe_justify = "right"
        elif self.label_position == "p3se":
            if len(points) >= 8:
                label_x = points[6] + ct.EDGE_LABEL_OFFSET["se"][0]
                label_y = points[7] + ct.EDGE_LABEL_OFFSET["se"][1]
                label_anchor = "se"
                labe_justify = "right"
        elif self.label_position == "p3sw":
            if len(points) >= 8:
                label_x = points[6] + ct.EDGE_LABEL_OFFSET["sw"][0]
                label_y = points[7] + ct.EDGE_LABEL_OFFSET["sw"][1]
                label_anchor = "sw"
                labe_justify = "left"
        elif self.label_position == "p3nw":
            if len(points) >= 8:
                label_x = points[6] + ct.EDGE_LABEL_OFFSET["nw"][0]
                label_y = points[7] + ct.EDGE_LABEL_OFFSET["nw"][1]
                label_anchor = "nw"
                labe_justify = "left"
        elif self.label_position == "p3ne":
            if len(points) >= 8:
                label_x = points[6] + ct.EDGE_LABEL_OFFSET["ne"][0]
                label_y = points[7] + ct.EDGE_LABEL_OFFSET["ne"][1]
                label_anchor = "ne"
                labe_justify = "right"
        elif self.label_position == "p4se":
            if len(points) >= 10:
                label_x = points[8] + ct.EDGE_LABEL_OFFSET["se"][0]
                label_y = points[9] + ct.EDGE_LABEL_OFFSET["se"][1]
                label_anchor = "se"
                labe_justify = "right"
        elif self.label_position == "p4sw":
            if len(points) >= 10:
                label_x = points[8] + ct.EDGE_LABEL_OFFSET["sw"][0]
                label_y = points[9] + ct.EDGE_LABEL_OFFSET["sw"][1]
                label_anchor = "sw"
                labe_justify = "left"
        elif self.label_position == "p4nw":
            if len(points) >= 10:
                label_x = points[8] + ct.EDGE_LABEL_OFFSET["nw"][0]
                label_y = points[9] + ct.EDGE_LABEL_OFFSET["nw"][1]
                label_anchor = "nw"
                labe_justify = "left"
        elif self.label_position == "p4ne":
            if len(points) >= 10:
                label_x = points[8] + ct.EDGE_LABEL_OFFSET["ne"][0]
                label_y = points[9] + ct.EDGE_LABEL_OFFSET["ne"][1]
                label_anchor = "ne"
                labe_justify = "right"
        elif self.label_position == "p5se":
            if len(points) >= 12:
                label_x = points[10] + ct.EDGE_LABEL_OFFSET["se"][0]
                label_y = points[11] + ct.EDGE_LABEL_OFFSET["se"][1]
                label_anchor = "se"
                labe_justify = "right"
        elif self.label_position == "p5sw":
            if len(points) >= 12:
                label_x = points[10] + ct.EDGE_LABEL_OFFSET["sw"][0]
                label_y = points[11] + ct.EDGE_LABEL_OFFSET["sw"][1]
                label_anchor = "sw"
                labe_justify = "left"
        elif self.label_position == "p5nw":
            if len(points) >= 12:
                label_x = points[10] + ct.EDGE_LABEL_OFFSET["nw"][0]
                label_y = points[11] + ct.EDGE_LABEL_OFFSET["nw"][1]
                label_anchor = "nw"
                labe_justify = "left"
        elif self.label_position == "p5ne":
            if len(points) >= 12:
                label_x = points[10] + ct.EDGE_LABEL_OFFSET["ne"][0]
                label_y = points[11] + ct.EDGE_LABEL_OFFSET["ne"][1]
                label_anchor = "ne"
                labe_justify = "right"
        return label_x, label_y, label_anchor, labe_justify

    def to_dict(self):
        """エッジオブジェクトを辞書化"""
        edge_data = {
            "from_id": self.from_node_obj.id if self.from_node_obj else None,
            "to_id": self.to_node_obj.id if self.to_node_obj else None,
        }
        if self.edge_type is not None:
            edge_data["edge_type"] = self.edge_type
        if self.line_style is not None:
            edge_data["line_style"] = self.line_style
        if self.connection_mode is not None:
            edge_data["connection_mode"] = self.connection_mode
        if self.from_node_connection_point is not None:
            edge_data["from_connection_point"] = self.from_node_connection_point
        if self.to_node_connection_point is not None:
            edge_data["to_connection_point"] = self.to_node_connection_point
        if self.edge_wrap_margin is not None:
            edge_data["edge_wrap_margin"] = self.edge_wrap_margin
        if self.label_text is not None:
            edge_data["label"] = self.label_text
        if self.label_text is not None:
            if self.label_position is not None:
                edge_data["label_position"] = self.label_position
            if self.label_x is not None:
                edge_data["label_x"] = self.label_x
            if self.label_y is not None:
                edge_data["label_y"] = self.label_y
            if self.label_anchor is not None:
                edge_data["label_anchor"] = self.label_anchor
            if self.label_justify is not None:
                edge_data["label_justify"] = self.label_justify

        return edge_data
