import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import itertools
import json
import constants as ct
import node
from node import Node
import edge
from PIL import ImageGrab


class FlowchartTool(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(ct.APP_TITLE)
        self.geometry(ct.CANVAS_PARAMS["size"])

        # 状態
        self.mode = tk.StringVar(value=ct.DEFAULT_MODE)  # 動作モード： select / add:process / add:decision / add:terminator / add:io / link
        self.grid_on = tk.BooleanVar(value=True)  # グリッド表示ON/OFF

        # 登録済みノード情報
        self.nodes: dict[int, node.Node] = {}   # node_id -> dict
        self._id_counter = itertools.count(1)   # 新規登録用ノードIDカウンタ
        self.selected_node_ids = []    # 選択中のノードIDリスト

        # 登録済みエッジ情報
        self.edges: dict[int, edge.Edge] = {}   # line_id -> list of edge dict
        self.selected_edge_id = None    # 選択中のエッジLine_ID
        self.link_start_node_id = None  # リンク始点ノードID

        self.drag_data = {"mode": None, "node_id": None, "start_x": 0, "start_y": 0, "end_x": 0, "end_y": 0}

        # 履歴（Undo/Redo）
        self.history = []
        self.history_index = -1

        # テキスト編集用
        self.text_edit = None  # {"entry":..., "node_id":..., "window_id":...}
        self.edge_label_edit = None  # {"entry":..., "edge_obj":..., "window_id":...}

        self._build_ui()    # UI構築

        self.push_history()  # 初期状態を履歴に追加

    # ------------ UI構築 ------------

    def _build_ui(self):
        # UI画面構築
        toolbar = ttk.Frame(self)
        toolbar.pack(side=tk.TOP, fill=tk.X, pady=4)

        for mode_key, mode_value in ct.MODE_DICT.items():
            self.add_mode_button(toolbar, mode_key, mode_value)

        ttk.Button(toolbar, text="Delete", command=self.delete_selected).pack(side=tk.LEFT, padx=1)

        # グリッドON/OFFボタン定義
        ttk.Checkbutton(toolbar, text="Grid", variable=self.grid_on, command=self.on_grid_toggle).pack(side=tk.LEFT, padx=1)

        # Undo/Redoボタン定義
        ttk.Button(toolbar, text="Undo", command=self.undo).pack(side=tk.LEFT, padx=1)
        ttk.Button(toolbar, text="Redo", command=self.redo).pack(side=tk.LEFT, padx=1)
        # JSON読み込み/保存ボタン定義
        ttk.Button(toolbar, text="Load JSON", command=self.load_json).pack(side=tk.LEFT, padx=1)
        ttk.Button(toolbar, text="Save JSON", command=self.save_json).pack(side=tk.LEFT, padx=1)
        # 画像保存ボタン定義
        ttk.Button(toolbar, text="Save Image", command=self.on_save).pack(side=tk.LEFT, padx=1)
        # 状態ラベル表示
        self.status_label = ttk.Label(toolbar, text="Mode: select")
        self.status_label.pack(side=tk.RIGHT, padx=4)

        # キャンバス
        self.canvas = tk.Canvas(self, bg=ct.CANVAS_PARAMS["bg_color"])
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # イベントバインド
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<ButtonPress-1>", self.on_drag_start, add="+")
        self.canvas.bind("<B1-Motion>", self.on_drag_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_drag_end)
        self.canvas.bind("<Configure>", self.on_canvas_resize)
        self.canvas.bind("<Double-1>", self.on_canvas_double_click)
        self.canvas.bind("<Button-3>", lambda event: self.popup_menu.tk_popup(event.x_root, event.y_root))  # 右クリックメニュー表示

        # Undo/Redo ショートカット
        self.bind_all("<Control-z>", lambda e: self.undo())
        self.bind_all("<Control-y>", lambda e: self.redo())

        # モード変更でラベル更新
        self.mode.trace_add("write", lambda *args: self.update_status())

        # ポップアップメニュー設定
        self.popup_menu = tk.Menu(self, tearoff=0)
        self.popup_menu.add_command(label="Select/Move", command=lambda: self.mode.set("select"))
        self.popup_menu.add_separator()
        self.popup_menu.add_command(label="Add Terminator", command=lambda: self.mode.set("add:terminator"))
        self.popup_menu.add_command(label="Add Process", command=lambda: self.mode.set("add:process"))
        self.popup_menu.add_command(label="Add Decision", command=lambda: self.mode.set("add:decision"))
        self.popup_menu.add_command(label="Add I/O", command=lambda: self.mode.set("add:io"))
        self.popup_menu.add_command(label="Link", command=lambda: self.mode.set("link"))
        self.popup_menu.add_separator()
        self.popup_menu.add_command(label="Delete Selected", command=self.delete_selected)
        self.popup_menu.add_separator()
        self.popup_menu.add_command(label="Undo", command=self.undo)
        self.popup_menu.add_command(label="Redo", command=self.redo)

        self._draw_grid()   # 初期グリッド描画

        # ウィンドウ終了時の確認
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def add_mode_button(self, toolbar, text, value):
        b = ttk.Radiobutton(toolbar, text=text, value=value, variable=self.mode)
        b.pack(side=tk.LEFT, padx=2)
        return b

    def update_status(self):
        mode = self.mode.get()
        self.status_label.config(text=f"Mode: {mode}")
        self.cancel_selection_node_and_edge()

    def _draw_grid(self):
        """グリッドを再描画"""
        self.canvas.delete("grid")
        if not self.grid_on.get():
            return
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w <= 0 or h <= 0:
            return
        step = ct.CANVAS_PARAMS["grid_spacing"] # グリッド間隔
        for x in range(0, w, step):
            self.canvas.create_line(x, 0, x, h, fill=ct.CANVAS_PARAMS["grid_color"], tags=("grid",))
        for y in range(0, h, step):
            self.canvas.create_line(0, y, w, y, fill=ct.CANVAS_PARAMS["grid_color"], tags=("grid",))
        # グリッドを最背面へ
        self.canvas.tag_lower("grid")

    # ------------ イベント・ハンドラ定義 ------------

    def on_canvas_click(self, event):
        mode = self.mode.get()

        if self.text_edit is not None and mode == "select":
            self.finish_text_edit(commit=True)
        if self.edge_label_edit is not None and mode == "select":
            self.finish_edge_label_edit(commit=True)

        if mode.startswith("add:"):
            node_type = mode.split(":", 1)[1]
            self.create_node(node_type, event.x, event.y)
            return

        nid = self.node_at(event.x, event.y)
        if nid is None:
            selected_edge = self.edge_at(event.x, event.y)
        else:
            selected_edge = None

        if mode == "select":
            self.select_node(nid)
            if nid is None and selected_edge is not None:
                self.select_edge(selected_edge)

        elif mode == "link":
            if nid is None:
                return
            if self.link_start_node_id is None:
                self.link_start_node_id = nid
                self.select_node(nid)
            else:
                self.create_edge(self.link_start_node_id, nid)
                self.cancel_selection_node_and_edge()

        elif mode == "delete":
            if nid is not None:
                self.select_node(nid)
                self.delete_selected()
                return
            edge = self.edge_at(event.x, event.y)
            if edge is not None:
                self.delete_edge(edge)

    def on_drag_start(self, event):
        if self.mode.get() == "link":
            return

        selected_node_id = self.node_at(event.x, event.y)
        selected_edge_id = self.edge_at(event.x, event.y)

        if selected_node_id is None and selected_edge_id is None:
            self.drag_data["mode"] = "select_nodes"
            self.drag_data["node_id"] = None
            self.drag_data["node_start_x"] = None
            self.drag_data["node_start_y"] = None
            self.drag_data["start_x"] = event.x
            self.drag_data["start_y"] = event.y
            self.drag_data["end_x"] = event.x
            self.drag_data["end_y"] = event.y
            # 選択範囲枠を描画
            selection_frame_shape_id = self.canvas.create_rectangle(
                self.drag_data["start_x"], self.drag_data["start_y"], self.drag_data["end_x"], self.drag_data["end_y"],
                outline=ct.SELECTION_AREA_PARAMS["outline_color"], width=ct.SELECTION_AREA_PARAMS["outline_width"], dash=ct.SELECTION_AREA_PARAMS["outline_dash"],
                tags=("selection")
            )
            self.drag_data["selection_frame_shape_id"] = selection_frame_shape_id

        elif selected_node_id is not None:
            self.select_node(selected_node_id)
            node_obj = self.nodes[selected_node_id]
            self.drag_data["mode"] = "move_node"
            self.drag_data["node_id"] = selected_node_id
            self.drag_data["node_start_x"] = node_obj.x
            self.drag_data["node_start_y"] = node_obj.y
            self.drag_data["start_x"] = event.x
            self.drag_data["start_y"] = event.y
            self.drag_data["end_x"] = event.x
            self.drag_data["end_y"] = event.y

    def on_drag_move(self, event):
        if self.mode.get() == "link":
            return

        mode = self.drag_data["mode"]
        if mode == "select_nodes":
            self.drag_data["end_x"] = event.x
            self.drag_data["end_y"] = event.y
            # 選択範囲枠を更新
            self.canvas.coords(
                self.drag_data["selection_frame_shape_id"], 
                self.drag_data["start_x"], self.drag_data["start_y"], self.drag_data["end_x"], self.drag_data["end_y"]
            )
        elif mode == "move_node":
            self.drag_data["end_x"] = event.x
            self.drag_data["end_y"] = event.y
            nid = self.drag_data["node_id"]
            if nid is None:
                return
            node_obj = self.nodes[nid]
            node_width = node_obj.w
            node_height = node_obj.h
            if node_width is None or node_height is None:
                return
            node_obj.x, node_obj.y = self.adjusted_xy(nid, event.x, event.y)
            self._move_node_graphics(node_obj)
            self._update_edges_for_node(nid)

    def on_drag_end(self, event):
        if self.mode.get() == "link":
            return

        mode = self.drag_data["mode"]
        if mode == "select_nodes":
            self.drag_data["end_x"] = event.x
            self.drag_data["end_y"] = event.y
            # 選択範囲内のノードを選択状態に
            left = min(self.drag_data["start_x"], self.drag_data["end_x"])
            right = max(self.drag_data["start_x"], self.drag_data["end_x"])
            top = min(self.drag_data["start_y"], self.drag_data["end_y"])
            bottom = max(self.drag_data["start_y"], self.drag_data["end_y"])
            selected_shape_ids = self.canvas.find_enclosed(left, top, right, bottom)
            nodes_in_selection_frame = []
            for item_shape_id in selected_shape_ids:
                for nid, node_obj in self.nodes.items():
                    if item_shape_id == node_obj.shape_id:
                        nodes_in_selection_frame.append(nid)
            self.select_nodes(nodes_in_selection_frame)
            # 選択範囲枠を削除
            self.canvas.delete(self.drag_data["selection_frame_shape_id"])
            self.drag_data["mode"] = None
            self.drag_data["selection_shape_id"] = None 
        elif mode == "move_node":
            self.drag_data["end_x"] = event.x
            self.drag_data["end_y"] = event.y
            move_x = event.x - self.drag_data["node_start_x"]
            move_y = event.y - self.drag_data["node_start_y"]
            mouse_move_x = abs(self.drag_data["end_x"] - self.drag_data["start_x"])
            mouse_move_y = abs(self.drag_data["end_y"] - self.drag_data["start_y"])

            nid = self.drag_data["node_id"]

            for selected_node_id in self.selected_node_ids:
                if selected_node_id != nid:
                    selected_node_obj = self.nodes[selected_node_id]
                    if selected_node_obj is not None and (mouse_move_x > 2 or mouse_move_y > 2):  # ダブルクリック時のノードのズレを防止
                        selected_node_obj.x, selected_node_obj.y = \
                                self.adjusted_xy(selected_node_id, selected_node_obj.x + move_x, selected_node_obj.y + move_y)
                        self._move_node_graphics(selected_node_obj)
                        self._update_edges_for_node(selected_node_id)

            if nid is not None:
                self.push_history()
            self.drag_data["node_id"] = None

    def on_canvas_double_click(self, event):
        if self.mode.get() != "select":
            self.mode.set("select")
            #return
        nid = self.node_at(event.x, event.y)
        if nid:
            self.start_text_edit(nid)
        else:
            selected_edge = self.edge_at(event.x, event.y)
            if selected_edge is not None:
                # エッジラベル編集
                self.start_edge_label_edit(selected_edge)

    def on_canvas_resize(self, event):
        self._draw_grid()

    def on_grid_toggle(self):
        self._draw_grid()

    def on_close(self):
        if self.nodes is None or len(self.nodes) == 0 or messagebox.askokcancel(ct.WINDOW_CLOSE_DIALOG_TITLE, ct.WINDOW_CLOSE_DIALOG_MESSAGE):
            self.destroy()

    # ------------ ノード・エッジ管理 ------------

    def create_node(self, node_type, x, y):
        """
        x, y は中心座標
        """
        node_id = next(self._id_counter)
        self._create_node_with_id(node_id, node_type, x, y)
        self.select_node(node_id)
        self.push_history()

    def _create_node_with_id(self, node_id, node_type, x, y, w=None, h=None, text=None):
        adjusted_x, adjusted_y = self.adjusted_xy(node_id, x, y, node_type)

        auto_text = self.auto_node_text(node_type, text)

        node_obj = node.Node(node_id, node_type, adjusted_x, adjusted_y, text=auto_text, canvas=self.canvas)

        self.nodes[node_id] = node_obj
        # ノードは常に最前面に
        self.canvas.tag_raise("node")

    def auto_node_text(self, node_type, text):
        # Terminator ノードには自動で "Start"/"End" テキストを設定
        if node_type == ct.NODE_TERMINATOR_PARAMS["type"] and text is None:
            existing_text = []
            for node_obj in self.nodes.values():
                if node_obj.type == ct.NODE_TERMINATOR_PARAMS["type"]:
                    if node_obj.text:
                        existing_text.append(node_obj.text)
            if ct.TERMINATOR_DEFAULT_START_TEXT not in existing_text:
                text = ct.TERMINATOR_DEFAULT_START_TEXT
            elif ct.TERMINATOR_DEFAULT_END_TEXT not in existing_text:
                text = ct.TERMINATOR_DEFAULT_END_TEXT
            else:
                text = ct.TERMINATOR_DEFAULT_UNKNOWN_TEXT
        return text

    def select_node(self, node_id):
        if node_id is not None:
            self.select_nodes([node_id])

    def select_nodes(self, node_ids):

        if node_ids is not None and len(node_ids) == 1:
            node_id = node_ids[0]
            if node_id in self.selected_node_ids:
                return  # 既に選択中の場合は選択状態を維持

        # 既存選択のハイライト解除（ノード）
        if self.selected_node_ids is not None and len(self.selected_node_ids) > 0:
            for selected_node_id in self.selected_node_ids:
                if selected_node_id in self.nodes:
                    self._reset_node_to_original_outline_color(self.nodes[selected_node_id])
        # 既存選択のハイライト解除（エッジ）
        if self.selected_edge_id:
            self._reset_edge_to_original_color(self.edges[self.selected_edge_id])

        self.selected_node_ids = node_ids if isinstance(node_ids, list) else [node_ids] 
        self.selected_edge_id = None

        if node_ids is not None and len(node_ids) > 0:
            for node_id in node_ids:
                if node_id in self.nodes:
                    self._set_node_to_selected_outline_color(self.nodes[node_id])

    # ノードの枠の色をオリジナルの定義に戻す
    def _reset_node_to_original_outline_color(self, node_obj):
        if node_obj is None or node_obj.shape_id is None:
            return
        outline_color = {
            ct.NODE_PROCESS_PARAMS["type"]: ct.NODE_PROCESS_PARAMS["outline_color"],
            ct.NODE_DECISION_PARAMS["type"]: ct.NODE_DECISION_PARAMS["outline_color"],
            ct.NODE_TERMINATOR_PARAMS["type"]: ct.NODE_TERMINATOR_PARAMS["outline_color"],
            ct.NODE_IO_PARAMS["type"]: ct.NODE_IO_PARAMS["outline_color"],
        }.get(node_obj.type, ct.NODE_DEFAULT_PARAMS["outline_color"])
        self.canvas.itemconfig(node_obj.shape_id, outline=outline_color)

    # 殿の枠の色をそれぞれのノード定義の選択職に変更する
    def _set_node_to_selected_outline_color(self, node_obj):
        if node_obj is None or node_obj.shape_id is None:
            return
        selected_outline_color = {
            ct.NODE_PROCESS_PARAMS["type"]: ct.NODE_PROCESS_PARAMS["selected_outline_color"],
            ct.NODE_DECISION_PARAMS["type"]: ct.NODE_DECISION_PARAMS["selected_outline_color"],
            ct.NODE_TERMINATOR_PARAMS["type"]: ct.NODE_TERMINATOR_PARAMS["selected_outline_color"],
            ct.NODE_IO_PARAMS["type"]: ct.NODE_IO_PARAMS["selected_outline_color"],
        }.get(node_obj.type, ct.NODE_DEFAULT_PARAMS["selected_outline_color"])
        self.canvas.itemconfig(node_obj.shape_id, outline=selected_outline_color)

    # エッジの色をオリジナルの定義に戻す
    def _reset_edge_to_original_color(self, edge_obj):
        if edge_obj is None or edge_obj.line_id is None:
            return
        self.canvas.itemconfig(edge_obj.line_id, fill=ct.EDGE_PARAMS["color"])

    def select_edge(self, edge_obj):
        if edge_obj is None:
            return
        edge_id = edge_obj.line_id

        # 既存選択のハイライト解除（ノード）
        if self.selected_node_ids is not None and len(self.selected_node_ids) > 0:
            for selected_node_id in self.selected_node_ids:
                if selected_node_id in self.nodes:
                    self._reset_node_to_original_outline_color(self.nodes[selected_node_id])
        # 既存選択のハイライト解除（エッジ）    
        if self.selected_edge_id:
            self._reset_edge_to_original_color(self.edges[self.selected_edge_id])

        self.selected_node_ids = []
        self.selected_edge_id = edge_id

        if edge_id:
            self.canvas.itemconfig(edge_id, fill=ct.EDGE_PARAMS["selected_color"])

    def cancel_selection_node_and_edge(self):
        # ノードとエッジの選択解除
        # 既存選択のハイライト解除（ノード）
        if self.selected_node_ids is not None and len(self.selected_node_ids) > 0:
            for selected_node_id in self.selected_node_ids:
                if selected_node_id in self.nodes:
                    self._reset_node_to_original_outline_color(self.nodes[selected_node_id])
        # 既存選択のハイライト解除（エッジ）
        if self.selected_edge_id:
            self._reset_edge_to_original_color(self.edges[self.selected_edge_id])

        # 既存選択の解除（ノード）
        self.selected_node_ids = []
        # 既存選択の解除（エッジ）
        self.selected_edge_id = None
        # リンク開始ノードの解除
        self.link_start_node_id = None

    def delete_selected(self):
        nids = self.selected_node_ids
        line_id = self.selected_edge_id
        if nids and len(nids) > 0:
            for nid in nids:
                if nid in self.nodes:
                    self.delete_selected_node(nid)
        elif line_id:
            self.delete_selected_edge(line_id)

    def delete_selected_node(self, nid):
        node_obj = self.nodes[nid]
        if node_obj:
            if node_obj.shape_id:
                self.canvas.delete(node_obj.shape_id)
            if node_obj.text_id:
                self.canvas.delete(node_obj.text_id)

        # 要素削除に伴う関連エッジの削除
        edges_to_keep = {}
        for edge_line_id, edge_obj in self.edges.items():
            from_node_id = edge_obj.from_node_obj.id if edge_obj.from_node_obj else None
            to_node_id = edge_obj.to_node_obj.id if edge_obj.to_node_obj else None
            if edge_line_id and from_node_id and to_node_id and (from_node_id == nid or to_node_id == nid):
                self.canvas.delete(edge_line_id)
                if edge_obj.label_id:
                    self.canvas.delete(edge_obj.label_id)
            else:
                edges_to_keep[edge_line_id] = edge_obj
        self.edges = edges_to_keep

        del self.nodes[nid]
        self.selected_node_ids = []
        self.push_history()

    def delete_selected_edge(self, line_id):
        edge_to_delete = None
        for edge_line_id, edge_obj in self.edges.items():
            if edge_line_id == line_id:
                edge_to_delete = edge_obj
                break
        if edge_to_delete is not None:
            self.delete_edge(edge_to_delete)
            self.selected_edge_id = None

    def node_at(self, x, y):
        """クリック位置からノードIDを逆引き"""
        items = self.canvas.find_overlapping(x, y, x, y)
        if not items:
            return None
        for item in reversed(items):
            for nid, node_obj in self.nodes.items():
                if item in (node_obj.shape_id, node_obj.text_id):
                    return nid
        return None
    
    def edge_at(self, x, y):
        """クリック位置からエッジを取得（線 or ラベル）"""
        items = self.canvas.find_overlapping(x-1, y-1, x+1, y+1)
        if not items:
            return None
        for item in reversed(items):
            for edge_line_id, edge_obj in self.edges.items():
                if item == edge_line_id or item == edge_obj.label_id:
                    return edge_obj
        return None

    @staticmethod
    def _clamp(v, vmin, vmax):
        return max(vmin, min(vmax, v))

    def create_edge(self, from_id, to_id):
        if from_id == to_id:
            return
        if from_id not in self.nodes or to_id not in self.nodes:
            return

        from_node_obj = self.nodes[from_id]
        to_node_obj = self.nodes[to_id]

        auto_text = self.auto_edge_label(None, from_node_obj)
        edge_obj = edge.Edge(from_node_obj, to_node_obj, text=auto_text, canvas=self.canvas)

        if edge_obj is not None and edge_obj.line_id is not None:
            self.edges[edge_obj.line_id] = edge_obj
        self.push_history()

    def delete_edge(self, edge_obj):
        """edge_obj を削除"""
        if edge_obj is None:
            return
        self.canvas.delete(edge_obj.line_id)
        if edge_obj.label_id:
            self.canvas.delete(edge_obj.label_id)
        del self.edges[edge_obj.line_id]
        self.push_history()

    def auto_edge_label(self, text, from_node_obj):
        # Decision ノードから出るエッジには Yes/No ラベルを自動設定
        if text is None:
            if from_node_obj.type == ct.NODE_DECISION_PARAMS["type"]:
                from_node_id = from_node_obj.id
                existing = []
                for one_edge_line_id, one_edge_obj in self.edges.items():
                    if one_edge_obj.from_node_obj and one_edge_obj.from_node_obj.id == from_node_id:
                        existing.append(one_edge_obj)
                used_labels = {edge_obj.label_text for edge_obj in existing}
                if "Yes" not in used_labels:
                    text = ct.DECISION_YES
                elif "No" not in used_labels:
                    text = ct.DECISION_NO
                else:
                    text = ct.DECISION_UNKNOWN
        return text

    # ------------ Undo/Redo用 モデル入出力 ------------

    def export_model(self):
        """現在のモデル（ノード・エッジ）をJSON化しやすい形で返す"""
        nodes_data = []
        for node_obj in self.nodes.values():
            nodes_data.append({
                "id": node_obj.id,
                "type": node_obj.type,
                "x": node_obj.x,
                "y": node_obj.y,
                "w": node_obj.w,
                "h": node_obj.h,
                "text": node_obj.text,
            })
        edges_data = [{
            "from_id": edge_obj.from_node_obj.id if edge_obj.from_node_obj else None,
            "to_id": edge_obj.to_node_obj.id if edge_obj.to_node_obj else None,
            "label": edge_obj.label_text
        } for edge_line_id, edge_obj in self.edges.items()]
        return {"nodes": nodes_data, "edges": edges_data}

    def import_model(self, data, push_to_history=False):
        """モデルを読み込み、Canvasを再構築"""
        self.canvas.delete("all")
        self.nodes.clear()
        self.edges.clear()
        self.selected_node_ids = []
        self.link_start_node_id = None

        # グリッド
        self._draw_grid()

        nodes_data = data.get("nodes", [])
        edges_data = data.get("edges", [])

        max_id = 0
        for nd in nodes_data:
            nid = nd.get("id")
            if nid is None:
                continue
            node_type = nd.get("type", ct.NODE_PROCESS_PARAMS["type"])
            x = nd.get("x", 0)
            y = nd.get("y", 0)
            w = nd.get("w", Node.get_width_of_type(node_type))
            h = nd.get("h", Node.get_height_of_type(node_type))
            text = nd.get("text", "")
            self._create_node_with_id(nid, node_type, x, y, w=w, h=h, text=text)
            if nid > max_id:
                max_id = nid

        self._id_counter = itertools.count(max_id + 1 if max_id > 0 else 1)

        # エッジ復元
        for ed in edges_data:
            fid = ed.get("from_id")
            tid = ed.get("to_id")
            label = ed.get("label")
            if fid in self.nodes and tid in self.nodes:
                from_node_obj = self.nodes[fid]
                to_node_obj = self.nodes[tid]
                edge_obj = edge.Edge(from_node_obj, to_node_obj, text=label, canvas=self.canvas)
                if edge_obj is not None and edge_obj.line_id is not None:
                    self.edges[edge_obj.line_id] = edge_obj

        # ノード最前面
        self.canvas.tag_raise("node")

        if push_to_history:
            self.push_history()

    def undo(self):
        if self.history_index <= 0:
            return
        self.history_index -= 1
        state = self.history[self.history_index]
        self.import_model(state, push_to_history=False)

    def redo(self):
        if self.history_index >= len(self.history) - 1:
            return
        self.history_index += 1
        state = self.history[self.history_index]
        self.import_model(state, push_to_history=False)

    # ------------ 編集履歴の記録（UNDO/REDO用） ------------

    def push_history(self):
        """現在状態を履歴に追加（Undo/Redo用）"""
        state = self.export_model()
        if self.history_index < len(self.history) - 1:
            self.history = self.history[:self.history_index + 1]
        pre_snapshot = self.history[self.history_index] if self.history_index >= 0 else None
        snapshot = json.loads(json.dumps(state))
        if pre_snapshot != snapshot:
            self.history.append(snapshot)
            self.history_index += 1

    # ------------ JSON保存/読み込み ------------

    def save_json(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        if not filename:
            return
        data = self.export_model()
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"{ct.SAVE_FAILED_MESSAGE}: {e}")

    def load_json(self):
        filename = filedialog.askopenfilename(
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        if not filename:
            return
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            messagebox.showerror("Error", f"{ct.LOAD_FAILED_MESSAGE}: {e}")
            return
        self.import_model(data, push_to_history=True)

    # ------------ テキスト編集（ダブルクリック） ------------

    def start_text_edit(self, node_id):
        if self.text_edit is not None:
            self.finish_text_edit(commit=False)
        if self.edge_label_edit is not None:
            self.finish_edge_label_edit(commit=False)

        if node_id not in self.nodes:
            return
        node_obj = self.nodes[node_id]
        x, y = node_obj.x, node_obj.y

        entry = ttk.Entry(self.canvas)
        if x and y and node_obj.text:
            entry.insert(0, node_obj.text)
            window_id = self.canvas.create_window(
                x, y,
                window=entry
            )
            self.text_edit = {"entry": entry, "node_id": node_id, "window_id": window_id}

        def commit(event=None):
            self.finish_text_edit(commit=True)

        def cancel(event=None):
            self.finish_text_edit(commit=False)

        entry.focus_set()
        entry.select_range(0, tk.END)
        entry.bind("<Return>", commit)
        entry.bind("<Escape>", cancel)
        entry.bind("<FocusOut>", commit)

    def finish_text_edit(self, commit=True):
        if self.text_edit is None:
            return
        entry = self.text_edit["entry"]
        nid = self.text_edit["node_id"]
        window_id = self.text_edit["window_id"]

        new_text = entry.get()
        self.canvas.delete(window_id)
        entry.destroy()

        if commit and nid in self.nodes:
            node_obj = self.nodes[nid]
            node_obj.text = new_text
            if node_obj.text_id:
                self.canvas.itemconfig(node_obj.text_id, text=new_text)
            self.push_history()

        self.text_edit = None

    def start_edge_label_edit(self, edge_obj):
        if self.text_edit is not None:
            self.finish_text_edit(commit=False)
        if self.edge_label_edit is not None:
            self.finish_edge_label_edit(commit=False)

        if edge_obj.label_x is None or edge_obj.label_y is None:
            return

        entry = ttk.Entry(self.canvas)
        if edge_obj.label_text:
            entry.insert(0, edge_obj.label_text)
        window_id = self.canvas.create_window(
            edge_obj.label_x, edge_obj.label_y,
            window=entry
        )
        self.edge_label_edit = {"entry": entry, "edge_obj": edge_obj, "window_id": window_id}

        def commit(event=None):
            self.finish_edge_label_edit(commit=True)

        def cancel(event=None):
            self.finish_edge_label_edit(commit=False)

        entry.focus_set()
        entry.select_range(0, tk.END)
        entry.bind("<Return>", commit)
        entry.bind("<Escape>", cancel)
        entry.bind("<FocusOut>", commit)

    def finish_edge_label_edit(self, commit=True):
        if self.edge_label_edit is None:
            return
        entry = self.edge_label_edit["entry"]
        edge_obj = self.edge_label_edit["edge_obj"]
        window_id = self.edge_label_edit["window_id"]

        new_text = entry.get()
        self.canvas.delete(window_id)
        entry.destroy()

        if commit and edge_obj:
            edge_obj.label_text = new_text
            if edge_obj.label_id:
                self.canvas.itemconfig(edge_obj.label_id, text=new_text)
            else:
                # ラベルがなければ新規作成
                edge_obj.draw_label(self.canvas, edge_obj.from_node_obj)
            self.push_history()

        self.edge_label_edit = None

    def adjusted_xy(self, node_id:int|None, x:int, y:int, node_type=ct.NODE_DEFAULT_PARAMS["type"]):
        if node_id is None:
            return x, y

        grid_size = ct.CANVAS_PARAMS["grid_spacing"]
        node_obj = self.nodes.get(node_id)

        if self.grid_on.get():
            if node_obj is None:     # 新規ノード作成時
                w = Node.get_width_of_type(node_type)
                h = Node.get_height_of_type(node_type)
            else:   # 既存ノード移動時
                w = node_obj.w if node_obj else 0
                h = node_obj.h if node_obj else 0
            adjusted_x = int(((x + grid_size/2 - w/2) // grid_size) * grid_size + w/2)
            adjusted_y = int(((y + grid_size/2 - h/2) // grid_size) * grid_size + h/2)
        else:
            adjusted_x = x
            adjusted_y = y

        return adjusted_x, adjusted_y

    def _move_node_graphics(self, node_obj):
        x, y = node_obj.x, node_obj.y
        w, h = node_obj.w, node_obj.h
        left, top, right, bottom = x - w/2, y - h/2, x + w/2, y + h/2

        shape_id = node_obj.shape_id
        node_type = node_obj.type

        if node_type == ct.NODE_PROCESS_PARAMS["type"]:    # 処理
            self.canvas.coords(shape_id, left, top, right, bottom)
        elif node_type == ct.NODE_DECISION_PARAMS["type"]:    # 分岐
            points = [
                x, top,
                right, y,
                x, bottom,
                left, y,
            ]
            self.canvas.coords(shape_id, *points)
        elif node_type == ct.NODE_TERMINATOR_PARAMS["type"]:   # 端点
            r = node_obj.h / 2
            points = node_obj.get_rounded_rectangle_coords(left, top, right, bottom, r)
            self.canvas.coords(shape_id, *points)
        elif node_type == ct.NODE_IO_PARAMS["type"]:     
            skew = ct.NODE_IO_PARAMS["skew"]
            points = [
                left + skew, top,
                right, top,
                right - skew, bottom,
                left, bottom,
            ]
            self.canvas.coords(shape_id, *points)
        else:
            self.canvas.coords(shape_id, left, top, right, bottom)

        self.canvas.coords(node_obj.text_id, x, y)
        self.canvas.tag_raise("node")

    def _update_edges_for_node(self, nid):
        """ノード移動時に関連エッジとラベルを再レイアウト"""
        for edge_line_id, edge_obj in self.edges.items():
            from_node_obj = edge_obj.from_node_obj
            to_node_obj = edge_obj.to_node_obj
            if edge_line_id and from_node_obj and to_node_obj:
                coords, label_x, label_y, anchor, justify = edge.Edge._compute_edge_geometry(edge_obj, from_node_obj, to_node_obj)
                edge_obj.update_points(self.canvas, coords, label_x, label_y)

                self.canvas.coords(edge_line_id, *coords)
                if edge_obj.label_text is not None and edge_obj.label_id is not None:
                    self.canvas.coords(edge_obj.label_id, label_x, label_y)
                    self.canvas.itemconfig(edge_obj.label_id, anchor=anchor, justify=justify)

        self.canvas.tag_lower("edge", "node")

    # ------------ Canvasの画像保存(JPEG,PNG) ------------

    def save_canvas_as_image(self, file_path: str):
        # Canvasの位置（画面座標）を取得して、その範囲だけキャプチャ
        self.canvas.update()  # 描画を確定
        x = self.canvas.winfo_rootx()
        y = self.canvas.winfo_rooty()
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        bbox = (x, y, x + w, y + h)  # (left, top, right, bottom)
        img = ImageGrab.grab(bbox=bbox)

        # 拡張子に合わせて保存（JPEGはRGB必須）
        ext = file_path.lower().split(".")[-1]
        if ext in ("jpg", "jpeg"):
            img = img.convert("RGB")
            img.save(file_path, "JPEG", quality=95)
        else:
            img.save(file_path, "PNG")

    def on_save(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg;*.jpeg")],
        )
        if not path:
            return
        try:
            self.save_canvas_as_image(path)
            messagebox.showinfo("Saved", f"Saved to:\n{path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app = FlowchartTool()
    app.mainloop()
