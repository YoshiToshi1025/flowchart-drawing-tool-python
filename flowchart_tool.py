import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import itertools
import json
from PIL import ImageGrab
import os
import threading
from tkinter import messagebox
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
import re

import mermaid_flowdata_loader as mfloader
import constants as ct
import node
from node import Node
import edge
from edge import Edge
import platform
if platform.system() == "Windows":
    import windows_monitor_info as wmi

class FlowchartTool(tk.Tk):
    def __init__(self):
        super().__init__()

        # 環境変数読み込み
        load_dotenv()   # .envファイルの読み込み

        self.title(ct.APP_TITLE)
        self.geometry(ct.CANVAS_PARAMS["size"])

        # 状態
        self.mode = tk.StringVar(value=ct.DEFAULT_MODE)  # 動作モード： select / add:process / add:decision / add:terminator / add:io / link
        self.grid_on = tk.BooleanVar(value=True)  # グリッド表示ON/OFF
        self.chat_window_on = tk.BooleanVar(value=False)  # チャットウィンドウ表示ON/OFF

        # 登録済みノード情報
        self.nodes: dict[int, Node] = {}   # node_id -> dict
        self._id_counter = itertools.count(1)   # 新規登録用ノードIDカウンタ
        self.selected_node_ids = []    # 選択中のノードIDリスト

        # 登録済みエッジ情報
        self.edges: dict[int, Edge] = {}   # line_id -> list of edge dict
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

        # -------------------------
        # 重要：コンテナを作って、全部 place で重ねる（安定）
        # -------------------------
        self.container = tk.Frame(self)
        self.container.pack(fill=tk.BOTH, expand=True)

        toolbar = ttk.Frame(self.container)
        toolbar.pack(side=tk.TOP, fill=tk.X, pady=4)

        self.main_panel = tk.Frame(self.container)
        self.main_panel.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

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
        # Mermaid形式ファイル読み込みボタン定義
        ttk.Button(toolbar, text="Load Mermaid", command=self.load_mermaid_flowdata).pack(side=tk.LEFT, padx=1)

        # 状態ラベル表示
        self.status_label = ttk.Label(toolbar, text="Mode: select")
        self.status_label.pack(side=tk.RIGHT, padx=4)

        # キャンバス
        self.canvas = tk.Canvas(self.main_panel, bg=ct.CANVAS_PARAMS["bg_color"])
        # self.canvas.pack(side=tk.TOP, fill=tk.X)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # マウス操作定義
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<ButtonPress-1>", self.on_drag_start, add="+")
        self.canvas.bind("<B1-Motion>", self.on_drag_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_drag_end)
        self.canvas.bind("<Configure>", self.on_canvas_resize)
        self.canvas.bind("<Double-1>", self.on_canvas_double_click)
        self.canvas.bind("<Button-3>", lambda event: self.popup_menu.tk_popup(event.x_root, event.y_root))  # 右クリックメニュー表示
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)  # マウスホイールイベント
        self.canvas.bind("<Shift-MouseWheel>", self.on_mouse_wheel_shift)  # Shift+マウスホイールイベント
        self.canvas.bind("<Control-MouseWheel>", self.on_mouse_wheel_ctrl)  # Ctrl+マウスホイールイベント
        self.canvas.bind("<Control-Shift-MouseWheel>", self.on_mouse_wheel_ctrl_shift)  # Ctrl+Shift+マウスホイールイベント

        # キー操作定義
        self.bind_all("<Delete>", lambda e: self.delete_selected())
        self.bind_all("<Escape>", lambda e: self.cancel_selection_node_and_edge())
        self.bind_all("<Control-a>", lambda e: self.select_all())
        self.bind_all("<Control-z>", lambda e: self.undo())
        self.bind_all("<Control-y>", lambda e: self.redo())

        # モード変更でラベル更新
        self.mode.trace_add("write", lambda *args: self.update_status())

        # ポップアップメニュー設定
        self.popup_menu = tk.Menu(self, tearoff=0)
        self.popup_menu.add_command(label="Select/Move", command=lambda: self.mode.set("select"))
        self.popup_menu.add_command(label="Select all nodes", command=self.select_all)
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
        self.popup_menu.add_separator()
        self.popup_menu.add_command(label="Save JSON", command=self.save_json)
        self.popup_menu.add_command(label="Save Image", command=self.on_save)

        self._draw_grid()   # 初期グリッド描画

        self.display_operation_info()  # 操作情報表示制御

        # ウィンドウ終了時の確認
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # ---- OpenAI client ----
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key is not None and api_key != "":
            self.openai_client = OpenAI()
            self.previous_response_id = None
        else:
            self.openai_client = None
            self.previous_response_id = None
            messagebox.showerror("Missing API Key", ct.OPENAI_API_KEY_NOT_SET_MESSAGE)

        # -------------------------
        # チャットパネル（Frame）
        # -------------------------
        # ---- state ----
        self.chat_visible = False
        self.chat_animating = False
        self.chat_x = 0

        self.chat_frame = tk.Frame(self.main_panel, bg="#eeeeee")
        self.chat_frame.pack_propagate(False)  # サイズ固定

        top = tk.Frame(self.chat_frame, bg="#eeeeee")
        top.pack(fill="x", padx=6, pady=(0, 6))

        tk.Label(top, text="Process flow:", bg="#eeeeee").pack(side="left")

        self.entry = tk.Entry(top)
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.bind("<Return>", lambda e: self.on_send_to_ai())

        self.send_btn = tk.Button(top, text="Generate", command=self.on_send_to_ai)
        self.send_btn.pack(side="left", padx=(6, 0))

        self.chat_text = tk.Text(self.chat_frame, wrap="word")
        self.chat_text.pack(fill="both", expand=True, padx=6, pady=6)
        self.chat_text.configure(state="disabled")

        # ChatWindow表示On/OFFボタン
        if self.openai_client is not None:
            ttk.Checkbutton(toolbar, text="AI-generation", variable=self.chat_window_on, command=self.on_chat_window_toggle).pack(side=tk.LEFT, padx=1)

        # リサイズ追従
        self.bind("<Configure>", self.on_resize)

        # 起動直後に配置確定
        self.after(0, self.on_resize_simple)

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

        nid = self.node_at(event.x, event.y)
        if nid is None:
            selected_edge = self.edge_at(event.x, event.y)
            if selected_edge is None:
                if mode.startswith("add:"):
                    node_type = mode.split(":", 1)[1]
                    self.create_node(node_type, event.x, event.y)
                    return
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
        # if self.mode.get() != "select":
        #    self.mode.set("select")
        #    #return
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

    def on_mouse_wheel(self, event):
        print("Mouse Wheel detected : No action assigned")

    def on_mouse_wheel_shift(self, event):
        # print("Shift + Mouse Wheel detected")

        delta = event.delta
        if delta > 0:
            self.change_edge_wrap_margin(increase=True)
        else:
            self.change_edge_wrap_margin(increase=False)

    def change_edge_wrap_margin(self, increase=True):
        # エッジ選択中の場合、エッジの回り込み距離を調整
        if self.selected_edge_id is not None:
            edge_obj = self.edges.get(self.selected_edge_id)
            if edge_obj is None:
                return
            elif edge_obj.points is not None:
                if len(edge_obj.points) == 8:
                    edge_obj.change_edge_wrap_margin_3line(increase=increase, canvas=self.canvas)
                elif len(edge_obj.points) == 10:
                    edge_obj.change_edge_wrap_margin_4line(increase=increase, canvas=self.canvas)

    def on_mouse_wheel_ctrl(self, event):
        # print("Ctrl + Mouse Wheel detected")
    
        delta = event.delta
        if delta > 0:
            self.change_edge_connection_points_in_sequence(increase=True)
        else:
            self.change_edge_connection_points_in_sequence(increase=False)

    def on_mouse_wheel_ctrl_shift(self, event):
        print("Ctrl + Shift + Mouse Wheel detected")

        delta = event.delta
        if delta > 0:
            self.rotate_edge_label_position(increase=True)
        else:
            self.rotate_edge_label_position(increase=False) 

    def change_edge_connection_points_in_sequence(self, increase=True):
        # エッジ選択中の場合、FromノードとToノードの接続位置を調整
        if self.selected_edge_id is not None:
            edge_obj = self.edges.get(self.selected_edge_id)
            if edge_obj is None:
                return
            edge_obj.rotate_connection_points(increase=increase, canvas=self.canvas)

    def rotate_edge_label_position(self, increase=True):
        print("Rotate edge label position")
        # エッジ選択中の場合、エッジラベルの位置を調整
        if self.selected_edge_id is not None:
            edge_obj = self.edges.get(self.selected_edge_id)
            if edge_obj is None:
                return
            edge_obj.rotate_label_position(increase=increase, canvas=self.canvas)

    # -----------------------------
    # リサイズ時：チャット位置を必ず補正（非表示なら必ず右外）
    # -----------------------------
    def on_resize(self, event):
        # ここは event.width/height を使わず、winfo_* を使う方が安定する環境があります
        self.on_resize_simple()

    def on_resize_simple(self):
        w = max(1, self.main_panel.winfo_width())
        h = max(1, self.main_panel.winfo_height())

        # canvasも念のため全面維持（containerは rel で追従してるので通常不要だが安全）
        self.canvas.place_configure(x=0, y=0, width=w, height=h)

        # アニメ中は高さだけ追従（位置はアニメ側に任せる）
        if self.chat_animating:
            self.chat_frame.place_configure(y=0, height=h, width=ct.CHAT_WIDTH)
            return

        if self.chat_visible:
            self.chat_x = max(0, w - ct.CHAT_WIDTH)
        else:
            self.chat_x = w  # ★常に右外へ退避

        self.chat_frame.place_configure(x=self.chat_x, y=0, height=h, width=ct.CHAT_WIDTH)

    # ------------ ノード・エッジ管理 ------------

    def create_node(self, node_type, x, y):
        """
        x, y は中心座標
        """
        node_id = next(self._id_counter)
        self._create_node_with_id(node_id, node_type, x, y)
        self.select_node(node_id)
        self.push_history()
        
        self.display_operation_info()  # 操作情報表示制御

    def _create_node_with_id(self, node_id, node_type, x, y, w=None, h=None, text=None):
        adjusted_x, adjusted_y = self.adjusted_xy(node_id, x, y, node_type)

        auto_text = self.auto_node_text(node_type, text)

        node_obj = Node(node_id, node_type, adjusted_x, adjusted_y, w=w, h=h, text=auto_text, canvas=self.canvas)

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

    def select_all(self):
        all_node_ids = list(self.nodes.keys())
        self.select_nodes(all_node_ids)

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
                
        self.display_operation_info()  # 操作情報表示制御


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
        edge_obj = Edge(from_node_obj, to_node_obj, text=auto_text, canvas=self.canvas)

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
        edges_data = []
        for edge_line_id, edge_obj in self.edges.items():
            edge_data = {
                "from_id": edge_obj.from_node_obj.id if edge_obj.from_node_obj else None,
                "to_id": edge_obj.to_node_obj.id if edge_obj.to_node_obj else None,
            }
            if edge_obj.from_node_connection_point is not None:
                edge_data["from_connection_point"] = edge_obj.from_node_connection_point
            if edge_obj.to_node_connection_point is not None:
                edge_data["to_connection_point"] = edge_obj.to_node_connection_point
            if edge_obj.edge_wrap_margin is not None:
                edge_data["edge_wrap_margin"] = edge_obj.edge_wrap_margin
            if edge_obj.label_text is not None:
                edge_data["label"] = edge_obj.label_text
            if edge_obj.label_position is not None:
                edge_data["label_position"] = edge_obj.label_position
            edges_data.append(edge_data)

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
            from_connection_point = ed.get("from_connection_point", None)
            to_connection_point = ed.get("to_connection_point", None)
            edge_wrap_margin = ed.get("edge_wrap_margin", None)
            label = ed.get("label")
            label_position = ed.get("label_position", None)
            if fid in self.nodes and tid in self.nodes:
                from_node_obj = self.nodes[fid]
                to_node_obj = self.nodes[tid]
                edge_obj = Edge(from_node_obj, to_node_obj, text=label, \
                                        from_node_connection_point=from_connection_point, \
                                        to_node_connection_point=to_connection_point, \
                                        edge_wrap_margin=edge_wrap_margin, \
                                        canvas=self.canvas, \
                                        label_position=label_position)
                if edge_obj is not None and edge_obj.line_id is not None:
                    self.edges[edge_obj.line_id] = edge_obj

        # ノード最前面
        self.canvas.tag_raise("node")

        if push_to_history:
            self.push_history()
        
        self.display_operation_info()  # 操作情報表示制御


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
        self.cancel_selection_node_and_edge()

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
            if (edge_obj.from_node_obj and edge_obj.from_node_obj.id == nid) or (edge_obj.to_node_obj and edge_obj.to_node_obj.id == nid):
                self._update_edge(edge_obj)

        self.canvas.tag_lower("edge", "node")
    
    def _update_edge(self, edge_obj):
        """エッジとラベルを再レイアウト"""
        from_node_obj = edge_obj.from_node_obj
        to_node_obj = edge_obj.to_node_obj
        if edge_obj.line_id and from_node_obj and to_node_obj:
            coords, label_x, label_y, anchor, justify = Edge._compute_edge_geometry(edge_obj, from_node_obj, to_node_obj)
            edge_obj.update_points(self.canvas, coords, label_x, label_y)

            self.canvas.coords(edge_obj.line_id, *coords)
            if edge_obj.label_text is not None and edge_obj.label_id is not None:
                ad_label_x, ad_label_y, ad_label_anchor, ad_label_justify = edge_obj.get_label_position()
                self.canvas.coords(edge_obj.label_id, ad_label_x, ad_label_y)
                self.canvas.itemconfig(edge_obj.label_id, anchor=ad_label_anchor, justify=ad_label_justify)

    # ------------ Canvasの画像保存(JPEG,PNG) ------------

    def save_canvas_as_image(self, file_path: str):
        # Canvasの位置（画面座標）を取得して、その範囲だけキャプチャ
        self.canvas.update()  # 描画を確定
        if platform.system() != "Windows":
            scaling = wmi.get_system_scale_percent(self.canvas) / 100.0  # Windowsのディスプレイ拡大率を取得
        else:
            scaling = 1.0
        x = int(self.canvas.winfo_rootx() * scaling)
        y = int(self.canvas.winfo_rooty() * scaling)
        w = int(self.canvas.winfo_width() * scaling)
        h = int(self.canvas.winfo_height() * scaling)
        bbox = (x, y, x + w, y + h)  # (left, top, right, bottom)
        print(f"scaling:{scaling}, Canvas bbox for image capture: {bbox}")
        img = ImageGrab.grab(bbox=bbox, all_screens=True)

        # 拡張子に合わせて保存（JPEGはRGB必須）
        ext = file_path.lower().split(".")[-1]
        if ext in ("jpg", "jpeg"):
            img = img.convert("RGB")
            img.save(file_path, "JPEG", quality=95)
        else:
            img.save(file_path, "PNG")

    def on_save(self):
        self.cancel_selection_node_and_edge()

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

    def load_mermaid_flowdata(self, mmd_filepath=None):
        if mmd_filepath is None:
            path = filedialog.askopenfilename(
                filetypes=[("Mermaid Flowchart", "*.mmd"), ("All files", "*.*")]
            )
        else:
            path = mmd_filepath

        if not path:
            return

        # try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        mmd_nodes, mmd_links = mfloader.parse_mermaid_flowdata(text)
        self.create_mermaid_flowdata(mmd_nodes, mmd_links)
        messagebox.showinfo("Loaded", f"Loaded Mermaid flowchart from:\n{path}")
        # except Exception as e:
        #     messagebox.showerror("Error", str(e))
        
        self.display_operation_info()  # 操作情報表示制御

    def create_mermaid_flowdata(self, mmd_nodes, mmd_links):
        """モデルを読み込み、Canvasを再構築"""
        self.canvas.delete("all")
        self.nodes.clear()
        self.edges.clear()
        self.selected_node_ids = []
        self.link_start_node_id = None
        self._id_counter = itertools.count(1)

        # グリッド
        self._draw_grid()

        if mmd_nodes is None or len(mmd_nodes) == 0:
            return

        nd = next(iter(mmd_nodes.values()))
        if nd.pos_tb is None or nd.pos_lr is None:
            # 自動配置
            auto_position_flag = True
            start_x = int(ct.CANVAS_PARAMS["grid_spacing"] * 10 + ct.NODE_DEFAULT_PARAMS["width"] / 2)
            start_y = int(ct.CANVAS_PARAMS["grid_spacing"] * 2 + ct.NODE_DEFAULT_PARAMS["height"] / 2)
        else:
            # mmdの位置情報を使う
            auto_position_flag = False
            start_x = int(self.canvas.winfo_width() / 2)
            start_y = int(ct.CANVAS_PARAMS["grid_spacing"] * 2 + ct.NODE_DEFAULT_PARAMS["height"] / 2)

        interval_x = ct.NODE_DEFAULT_PARAMS["width"] + ct.CANVAS_PARAMS["grid_spacing"] * 4
        interval_y = ct.NODE_DEFAULT_PARAMS["height"] + ct.CANVAS_PARAMS["grid_spacing"]
        vertical_count = 10

        id_map = {}
        for node_strid in mmd_nodes:
            nd = mmd_nodes[node_strid]
            node_id = next(self._id_counter)
            node_strid = nd.node_id if hasattr(nd, "node_id") else None
            if node_strid is None:
                continue
            node_type = nd.kind if hasattr(nd, "kind") else ct.NODE_PROCESS_PARAMS["type"]
            if auto_position_flag:
                x = start_x + (node_id-1) // vertical_count * interval_x  # 自動配置
                y = start_y + (node_id-1) % vertical_count * interval_y   # 自動配置
            else:
                x, y = mfloader.convert_pos_to_xy(pos_tb=nd.pos_tb, pos_lr=nd.pos_lr, start_x=start_x, start_y=start_y)
            w = Node.get_width_of_type(node_type)
            h = Node.get_height_of_type(node_type)
            text = nd.title if hasattr(nd, "title") else ""
            self._create_node_with_id(node_id, node_type, x, y, w=w, h=h, text=text)
            id_map[node_strid] = node_id

        for ed in mmd_links:
            src_id = ed.src if hasattr(ed, "src") else None
            dst_id = ed.dst if hasattr(ed, "dst") else None
            label = ed.label if hasattr(ed, "label") else None
            fid = id_map[src_id]
            tid = id_map[dst_id]
            if fid in self.nodes and tid in self.nodes:
                from_node_obj = self.nodes[fid]
                to_node_obj = self.nodes[tid]
                edge_obj = Edge(from_node_obj, to_node_obj, text=label, \
                                        canvas=self.canvas)
                if edge_obj is not None and edge_obj.line_id is not None:
                    self.edges[edge_obj.line_id] = edge_obj

        # ノード最前面
        self.canvas.tag_raise("node")

        self.push_history()

    # -----------------------------
    # UI: チャット表示切替
    # -----------------------------
    def on_chat_window_toggle(self):
        if self.chat_animating:
            return
        if self.chat_window_on.get():
            self.slide_in_chat_window()
        else:
            self.slide_out_chat_window()

    def slide_in_chat_window(self):
        self.chat_animating = True

        # ★必ず前面へ（ちらついて消える対策の本命）
        self.chat_frame.lift()

        def animate():
            w = max(1, self.main_panel.winfo_width())
            h = max(1, self.main_panel.winfo_height())
            target_x = max(0, w - ct.CHAT_WIDTH)  # 常に現在幅基準

            if self.chat_x > target_x:
                self.chat_x = max(target_x, self.chat_x - ct.CHAT_WINDOW_SLIDE_STEP)
                self.chat_frame.place_configure(x=self.chat_x, y=0, height=h, width=ct.CHAT_WIDTH)
                self.after(ct.CHAT_WINDOW_SLIDE_INTERVAL, animate)
            else:
                self.chat_x = target_x
                self.chat_frame.place_configure(x=self.chat_x, y=0, height=h, width=ct.CHAT_WIDTH)
                self.chat_visible = True
                self.chat_animating = False

        # スタート地点を「現在の右外」に強制（リサイズ後でも確実）
        w0 = max(1, self.main_panel.winfo_width())
        h0 = max(1, self.main_panel.winfo_height())
        self.chat_x = w0
        self.chat_frame.place_configure(x=self.chat_x, y=0, height=h0, width=ct.CHAT_WIDTH)

        animate()

    def slide_out_chat_window(self):
        self.chat_animating = True

        # 前面は維持（アニメ中に裏回りしない）
        self.chat_frame.lift()

        def animate():
            w = max(1, self.main_panel.winfo_width())
            h = max(1, self.main_panel.winfo_height())
            target_x = w  # 現在幅の右外

            if self.chat_x < target_x:
                self.chat_x = min(target_x, self.chat_x + ct.CHAT_WINDOW_SLIDE_STEP)
                self.chat_frame.place_configure(x=self.chat_x, y=0, height=h-40, width=ct.CHAT_WIDTH)
                self.after(ct.CHAT_WINDOW_SLIDE_INTERVAL, animate)
            else:
                self.chat_x = target_x
                self.chat_frame.place_configure(x=self.chat_x, y=0, height=h-40, width=ct.CHAT_WIDTH)
                self.chat_visible = False
                self.chat_animating = False

        animate()

    # -----------------------------
    # UI: チャット表示補助
    # -----------------------------
    def append_chat(self, speaker: str, text: str):
        self.chat_text.configure(state="normal")
        self.chat_text.insert("end", f"{speaker}: {text}\n")
        self.chat_text.see("end")
        self.chat_text.configure(state="disabled")

    def set_sending(self, sending: bool):
        state = "disabled" if sending else "normal"
        self.send_btn.configure(state=state)
        self.entry.configure(state=state)

    # -----------------------------
    # 生成AIに送信 → API呼び出し（別スレッド）
    # -----------------------------
    def on_send_to_ai(self):
        user_msg = self.entry.get().strip()
        if not user_msg:
            return

        self.entry.delete(0, "end")
        self.append_chat("You", user_msg)

        self.set_sending(True)
        input_msg = ct.AI_INPUT_TEMPLATE.replace("$order", user_msg)
        threading.Thread(target=self.call_gpt, args=(user_msg,), daemon=True).start()

    def call_gpt(self, user_msg: str):
        try:
            resp = self.openai_client.responses.create(
                model=ct.AI_MODEL,
                instructions=ct.AI_SYSTEM_INSTRUCTIONS,
                input=user_msg,
                previous_response_id=self.previous_response_id,
            )
            assistant_text = resp.output_text or ""
            self.previous_response_id = resp.id
            self.after(0, lambda: self.append_chat("GPT", assistant_text))
            success_flag, mmd_filepath = self.save_mmd_to_file(user_msg, assistant_text)
            if success_flag:
                self.after(0, lambda: messagebox.askokcancel("Saved", f"{ct.AI_GENERATED_MESSAGE1}\n{mmd_filepath}\n\n{ct.AI_GENERATED_MESSAGE2}") and self.load_mermaid_flowdata(mmd_filepath))
        except Exception as e:
            print(e)
            # self.after(0, lambda: messagebox.showerror("OpenAI API Error", str(e)))
        finally:
            self.after(0, lambda: self.set_sending(False))

    # -----------------------------
    # ファイル保存（work/[roder].mmd に追記）
    # -----------------------------
    def save_mmd_to_file(self, order: str, answer: str):
        # 保存先（実行フォルダ直下の work/test.txt）
        success_flag = False
        SAVE_DIR = Path(ct.WORK_DIR_NAME)
        filename = self.sanitize_filename(order)
        OUT_FILE = SAVE_DIR / f"{filename}.mmd"
 
        answer = self.strip_triple_quotes(answer)

        try:
            SAVE_DIR.mkdir(parents=True, exist_ok=True)  # work が無ければ作る
            with OUT_FILE.open("w", encoding="utf-8") as f:
                f.write(f"{answer}\n")
            success_flag = True
        except Exception as e:
            # 保存失敗は致命的ではないので、UIにだけ通知
            self.after(0, lambda: messagebox.showwarning("Save Warning", f"{ct.SAVE_FAILED_MESSAGE}: {e}"))

        return success_flag, OUT_FILE

    def sanitize_filename(self, filename: str) -> str:
        # Windowsで使用禁止の文字
        forbidden = r'[\\/:*?"<>|]'
        return re.sub(forbidden, '_', filename)

    def strip_triple_quotes(self, text: str) -> str:
        if text.startswith("```"):
            return text[3:]
        if text.endswith("```"):
            return text[:-3]
        return text

    def display_operation_info(self):
        if self.nodes is not None and len(self.nodes) > 0:
            self._hide_operation_info()
        else:
            self._show_operation_info()

    def _show_operation_info(self):
        if hasattr(self, "ope_info") and self.ope_info:
            return
        self.ope_info = tk.Label(self.canvas, justify="left", font=("Consolas", 9), fg="#0f172a", text=
            "[Key Operations]\n"
            " DEL: Delete selected node/edge\n"
            " ESC: Cancel selection\n"
            " Ctrl-a: Select all nodes\n"
            " Ctrl-z: Undo\n"
            " Ctrl-y: Redo\n"
            "\n"
            "[Mouse Operations]\n"
            " Right Button: Show context menu\n"
            " Click Node/Edge: Select node/edge\n"
            " Double-Click Node/Edge: Edit text\n"
            " Drag Area: Select nodes in area\n"
            " Drag Node: Move selected node(s)\n"
            " Ctrl+MouseWheel: Change connection point\n"
            " Shift+MouseWheel: Change edge wrap margin\n"
            " Ctrl+Shift+MouseWheel: Change edge label position"
            )
        self.ope_info.pack(padx=8, pady=8, anchor="ne")
    
    def _hide_operation_info(self):
        if hasattr(self, "ope_info") and self.ope_info:
            self.ope_info.destroy()
            self.ope_info = None

if __name__ == "__main__":
    app = FlowchartTool()
    app.mainloop()
