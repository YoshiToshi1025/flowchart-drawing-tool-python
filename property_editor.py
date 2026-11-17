import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk, messagebox, font, colorchooser
from dataclasses import dataclass, fields
from typing import Optional, Literal, get_type_hints, Callable
from type_info import get_type_info
from node import Node
from edge import Edge
import re
import constants as ct

class ResizableText(tk.Frame):
    """
    下端のハンドルをドラッグして、
    ユーザーが表示行数を変更できるTextウィジェット。
    """
    def __init__(self, parent, value="", height_lines=4, min_lines=1, max_lines=30, readonly=False, on_height_changed=None,):
        super().__init__(parent)

        self.min_lines = min_lines
        self.max_lines = max_lines
        self.on_height_changed = on_height_changed

        self.drag_start_y = 0
        self.drag_start_height = height_lines

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.text = tk.Text(
            self,
            wrap=tk.WORD,
            height=height_lines,
            undo=True,
            # relief=tk.SOLID,
            borderwidth=1,
            padx=5,
            pady=4,
        )
        self.text.grid(row=0, column=0, sticky="nsew",)

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.text.yview,)
        scrollbar.grid(row=0, column=1, sticky="ns",)

        self.text.configure(yscrollcommand=scrollbar.set,)

        # 高さ変更用ハンドル
        self.resize_handle = tk.Canvas(self, height=2, highlightthickness=0, cursor="sb_v_double_arrow",)
        self.resize_handle.grid(row=1, column=0, columnspan=2, sticky="ew",)

        self.resize_handle.bind("<Configure>", self.draw_resize_handle,)
        self.resize_handle.bind("<ButtonPress-1>", self.start_resize,)
        self.resize_handle.bind("<B1-Motion>", self.resize,)

        self.set_text(value)

        if readonly:
            self.text.configure(state=tk.DISABLED, background="#eeeeee",)

    def draw_resize_handle(self, event=None):
        self.resize_handle.delete("all")

        width = self.resize_handle.winfo_width()
        center_x = width // 2

        self.resize_handle.create_line(center_x - 20, 3, center_x + 20, 3, fill="#888888",)
        self.resize_handle.create_line(center_x - 20, 6, center_x + 20, 6, fill="#888888",)

    def start_resize(self, event):
        self.drag_start_y = event.y_root
        self.drag_start_height = int(self.text.cget("height"))

    def resize(self, event):
        delta_y = (event.y_root - self.drag_start_y)

        font = tkfont.Font(font=self.text.cget("font"))
        line_height = max(font.metrics("linespace"), 1,)

        changed_lines = round(delta_y / line_height)

        new_height = (self.drag_start_height + changed_lines)

        new_height = max(self.min_lines, min(self.max_lines, new_height),)

        current_height = int(self.text.cget("height"))

        if new_height == current_height:
            return

        self.text.configure(height=new_height)

        if self.on_height_changed:
            self.on_height_changed(new_height)

    def set_text(self, value):
        old_state = self.text.cget("state")

        if old_state == tk.DISABLED:
            self.text.configure(state=tk.NORMAL)

        self.text.delete("1.0", tk.END,)
        self.text.insert("1.0", str(value),)

        if old_state == tk.DISABLED:
            self.text.configure(state=tk.DISABLED)

    def get_text(self):
        return self.text.get("1.0", "end-1c",)

    def focus_editor(self):
        self.text.focus_set()

class PropertyEditor(ttk.Frame):
    def __init__(
            self,
            master,
            refresh_callback: Callable[[], None],
            isdataexists_callback: Callable[[str], bool],
            reload_callback: Callable[[], None]
    ):
        super().__init__(master)
        self.master = master
        self.refresh_callback = refresh_callback
        self.isdataexists_callback = isdataexists_callback
        self.reload_callback = reload_callback

        self.current_object = None
        self.editors = {}

        # 読み取り専用プロパティ名のセット
        self.readonly_properties = {
            "id",
            "from_node_obj",
            "to_node_obj",
            "points",
            "line_id",
            "shape_id",
            "label_x",
            "label_y",
            "label_anchor",
            "label_justify",
        }

        # 複数行テキストを表示するプロパティ名のセット
        self.multiline_properties = {
            "text",
            "details",
            "label_text",
        }

        # プロパティ編集対象外のプロパティ名のセット
        self.excluded_properties = {
            "text_id",
            "image_id",
            "base_image_data",
            "display_image_data",
            "canvas",
            "label_id",

        }

        self.rgbcolor_properties = {
            "fill_color",
            "outline_color",
            "text_color",
            "line_color",
            "color",
        }

        self.objects = []  # NodeやEdgeのオブジェクトを格納するリスト

        hints = get_type_hints(Node)

        # オブジェクト・属性ごとのテキスト欄の高さ
        self.editor_heights = {}

        # 属性列の幅
        self.attribute_column_width = 100
        self.attribute_column_min_width = 100
        self.attribute_column_max_width = 300

        # 列境界のドラッグ情報
        self.column_drag_start_x = 0
        self.column_drag_start_width = 0

        # 境界ハンドルの幅
        self.divider_width = 0

        self.create_widgets()

        # comboboxで選択肢が登録されていたら、最初の要素を選択状態にする
        if self.object_combo["values"]:
            self.object_combo.current(0)
            self.on_object_selected()
        else:
            self.current_object = None
            self.clear_properties()

    def set_target_objects(self, objects):
        # print(f"  Setting target objects: {[obj.id for obj in objects]}")    # for DEBUG
        self.objects = objects

        id_list = []
        for obj in self.objects:
            if isinstance(obj, Node):
                id_text = f"{obj.id}: {str(obj.text)}"
                id_list.append(id_text)
            elif isinstance(obj, Edge):
                from_to_id = str(obj.from_node_obj.id) + "-" + str(obj.to_node_obj.id)
                id_list.append(from_to_id)

        if id_list == []:
            self.object_combo["values"] = [""]
        else:
            self.object_combo["values"] = id_list

        if id_list:
            self.object_combo.current(0)
            self.on_object_selected()
        else:
            self.current_object = None
            self.clear_properties()

    def reset_target_objects(self):
        self.objects = []
        self.object_combo["values"] = [""]
        self.current_object = None
        self.clear_properties()
        self.object_combo.current(0)

    def create_widgets(self):
        self.create_object_selector()
        self.create_header()
        self.create_property_area()
        self.create_buttons()

    def create_object_selector(self):
        select_frame = ttk.Frame(self.master)
        select_frame.pack(fill=tk.X, padx=4, pady=10,)

        ttk.Label(select_frame, text="Selected Object :",).pack(side=tk.LEFT)

        id_list = []
        for obj in self.objects:
            if isinstance(obj, Node):
                id_text = f"{obj.id}: {str(obj.text)}"
                id_list.append(id_text)
            elif isinstance(obj, Edge):
                from_to_id = obj.from_node_obj.id + "-" + obj.to_node_obj.id
                id_list.append(from_to_id)

        self.object_combo = ttk.Combobox(
            select_frame,
            state="readonly",
            values=id_list,
            width=40,
        )
        self.object_combo.pack(side=tk.LEFT, padx=8,)

        self.object_combo.bind("<<ComboboxSelected>>", self.on_object_selected,)

    def create_header(self):
        """
        Header configuration / ヘッダー構成

        column 0: Attribute / 属性名
        column 1: handle for adjusting width  / 幅変更用ハンドル
        column 2: Value / 値
        """
        self.header_frame = ttk.Frame(self.master)
        self.header_frame.pack(fill=tk.X, padx=4,)

        self.header_frame.columnconfigure(0, minsize=self.attribute_column_width,)
        self.header_frame.columnconfigure(1, minsize=self.divider_width,)
        self.header_frame.columnconfigure(2, weight=1,)

        self.attribute_header = ttk.Label(self.header_frame, text="Attribute", anchor=tk.CENTER, relief=tk.SOLID, )
        self.attribute_header.grid(row=0, column=0, sticky="nsew", ipady=4,)

        # 属性列幅変更用のハンドル
        self.column_resize_handle = tk.Canvas(self.header_frame, width=self.divider_width, height=1, highlightthickness=0, borderwidth=0, cursor="sb_h_double_arrow",)
        self.column_resize_handle.grid(row=0, column=1, sticky="nsew",)

        self.column_resize_handle.bind("<Configure>", self.draw_column_resize_handle,)
        self.column_resize_handle.bind("<ButtonPress-1>", self.start_column_resize,)
        self.column_resize_handle.bind("<B1-Motion>", self.resize_attribute_column,)

        self.value_header = ttk.Label(self.header_frame, text="Value", anchor=tk.CENTER, relief=tk.SOLID, )
        self.value_header.grid(row=0, column=2, sticky="nsew", ipady=4,)

    def create_property_area(self):
        container = ttk.Frame(self.master)
        container.pack(fill=tk.BOTH, expand=True, padx=4, pady=(0, 10),)

        self.canvas = tk.Canvas(container, highlightthickness=0,)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True,)

        # scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=self.canvas.yview,)
        # scrollbar.pack(side=tk.RIGHT, fill=tk.Y,)

        # self.canvas.configure(yscrollcommand=scrollbar.set,)

        self.property_frame = ttk.Frame(self.canvas)

        # ヘッダーと同じ3列構成
        self.property_frame.columnconfigure(0, minsize=self.attribute_column_width,)
        self.property_frame.columnconfigure(1, minsize=self.divider_width,)
        self.property_frame.columnconfigure(2, weight=1,)

        self.canvas_window = (
            self.canvas.create_window((0, 0), window=self.property_frame, anchor=tk.NW,)
        )

        self.property_frame.bind("<Configure>", self.update_scroll_region,)

        self.canvas.bind("<Configure>", self.resize_property_frame,)

    def create_buttons(self):
        button_frame = ttk.Frame(self.master)
        button_frame.pack(fill=tk.X, padx=10, pady=(0, 10),)
        ttk.Button(button_frame, text="Apply Changes", command=self.apply_changes,).pack(side=tk.LEFT, padx=6,)
        ttk.Button(button_frame, text="Reload", command=self.reload_callback,).pack(side=tk.LEFT, padx=6,)
        # ttk.Button(button_frame, text="Print Content", command=self.print_current_object,).pack(side=tk.LEFT)

    # --------------------------------
    # 属性列幅の変更処理
    # --------------------------------

    def draw_column_resize_handle(self, event=None,):
        self.column_resize_handle.delete("all")

        width = (self.column_resize_handle.winfo_width())
        height = (self.column_resize_handle.winfo_height())

        center_x = width // 2

        self.column_resize_handle.create_line(center_x, 0,center_x, height, fill="#777777", width=1,)

    def start_column_resize(self, event):
        """
        属性列の幅変更を開始する。
        """
        self.column_drag_start_x = (event.x_root)
        self.column_drag_start_width = self.property_frame.grid_bbox(0, 0)[2]

    def resize_attribute_column(self, event,):
        """
        マウスの横移動量に応じて属性列の幅を変更する。
        """
        delta_x = (event.x_root - self.column_drag_start_x)

        new_width = (self.column_drag_start_width + delta_x)

        # 値列が完全になくならないよう、
        # 現在の表示領域から動的な最大幅を計算する
        canvas_width = self.canvas.winfo_width()

        dynamic_max_width = (self.attribute_column_max_width)

        if canvas_width > 250:
            dynamic_max_width = min(dynamic_max_width, canvas_width - 150,)

        dynamic_max_width = max(self.attribute_column_min_width, dynamic_max_width,)

        new_width = max(
            self.attribute_column_min_width,
            min(dynamic_max_width, new_width,),
        )

        self.set_attribute_column_width(new_width)

    def set_attribute_column_width(self, width,):
        """
        ヘッダーと各プロパティ行の属性列幅を同期する。
        """
        self.attribute_column_width = int(width)

        # プロパティ行側
        self.property_frame.columnconfigure(0, minsize=self.attribute_column_width,)

        self.property_frame.update_idletasks()

        self.update_scroll_region()

    # --------------------------------
    # プロパティ一覧
    # --------------------------------

    def update_scroll_region(self, event=None,):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"),)
        self.sync_header_columns()

    def sync_header_columns(self):
        """内容に応じて広がった本体の実際の列幅をヘッダーに反映する。"""
        for column in (0, 1):
            width = self.property_frame.grid_bbox(column, 0)[2]
            self.header_frame.columnconfigure(column, minsize=width,)

    def resize_property_frame(self, event,):
        self.canvas.itemconfigure(self.canvas_window, width=event.width,)

    def on_object_selected(self, event=None,):
        # print("Object selected:", self.object_combo.get())
        selected_id = self.object_combo.get()

        id_list = []
        for obj in self.objects:
            if isinstance(obj, Node):
                id_text = f"{obj.id}: {str(obj.text)}"
                id_list.append((id_text, obj))
            elif isinstance(obj, Edge):
                from_to_id = str(obj.from_node_obj.id) + "-" + str(obj.to_node_obj.id)
                id_list.append((from_to_id, obj))

        for obj_id, obj in id_list:
            if str(obj_id) == selected_id:
                self.current_object = obj
                break   

        self.load_properties()

    def clear_properties(self):
        for widget in (self.property_frame.winfo_children()):
            widget.destroy()

        self.editors.clear()

    def load_properties(self):
        self.clear_properties()

        if self.current_object is None:
            return

        Object_fields = fields(self.current_object)
        # self.excluded_propertiesで指定されている要素を除外する
        Object_fields = [field for field in Object_fields if field.name not in self.excluded_properties]

        for row_index, field_info in enumerate(Object_fields):
            property_name = field_info.name
            value = getattr(self.current_object, property_name,)

            property_label = ttk.Label(self.property_frame, text=property_name, anchor=tk.NW, relief=tk.SOLID, padding=(8, 3),)
            property_label.grid(row=row_index, column=0, sticky="nsew",)

            # ヘッダーのリサイズハンドルと
            # 同じ位置に境界線を配置する
            separator = ttk.Separator(self.property_frame, orient=tk.VERTICAL,)
            separator.grid(row=row_index, column=1, sticky="ns",)

            editor = self.create_editor(property_name, value, field_info.type)
            editor.grid(row=row_index, column=2, sticky="nsew",)

            if property_name in self.rgbcolor_properties:
                editor.bind("<Double-Button-1>", self.open_color_picker)

            self.editors[property_name] = editor

        # 再読み込み時にも現在の列幅を適用
        self.set_attribute_column_width(self.attribute_column_width)

        self.after_idle(self.update_scroll_region)

    def open_color_picker(self, event):
        editor = event.widget
        initial_color = editor.get()
        color_code = colorchooser.askcolor(initialcolor=initial_color)[1]
        if color_code:
            editor.delete(0, tk.END)
            editor.insert(0, color_code)

    def create_editor(self, property_name, value, value_type):
        type_info_name, type_info_choices = get_type_info(value_type)

        if value is None:
            value = ""

        # print(f"Creating editor for property: {property_name}, value: {value}, type: {value_type}, type_info: {type_info_name}, choices: {type_info_choices}")

        if value_type is bool:
            editor = ttk.Combobox(self.property_frame, state="readonly", values=("True", "False"),)
            editor.set(str(value))
            return editor

        if type_info_name == "Literal" and type_info_choices is not None:
            if property_name in self.readonly_properties:
                editor = ttk.Entry(self.property_frame, )
                editor.insert(0, str(value))
                editor.configure(state="readonly")
                return editor
            else:
                if property_name == "shape_type":
                    type_value = getattr(self.current_object, "type")
                    if type_value == "terminator":
                        type_info_choices = ["normal", "small"]
                    elif type_value == "process":
                        type_info_choices = ["rectangle", "corner_rounded_rectangle", "ellipse"]
                    elif type_value == "decision":
                        type_info_choices = ["decision"]
                    elif type_value == "io":
                        type_info_choices = ["io"]
                    elif type_value == "storage":
                        type_info_choices = ["storage"]
                    elif type_value == "document":
                        type_info_choices = ["document"]
                    elif type_value == "special_node":
                        type_info_choices = ["special_node"]
                elif property_name == "path_type":
                    edge_type = getattr(self.current_object, "edge_type")
                    if edge_type == "line":
                        type_info_choices = [""]
                    
                editor = ttk.Combobox(self.property_frame, state="readonly", values=type_info_choices,)
                editor.set(str(value))
                return editor

        if type_info_name == "Optional[Literal]" and type_info_choices is not None:
            if property_name in self.readonly_properties:
                editor = ttk.Entry(self.property_frame, )
                editor.insert(0, str(value))
                editor.configure(state="readonly")
                return editor
            else:
                type_info_choices_with_none = [None] + type_info_choices
                editor = ttk.Combobox(self.property_frame, state="readonly", values=type_info_choices_with_none,)
                editor.set(str(value))
                return editor

        if (type_info_name in ("str", "Optional[str]") and property_name in self.multiline_properties):
            # print(f"Creating ResizableText for property: {property_name}, value: {value}, type: {value_type}")
            if isinstance(self.current_object, Node):
                height_key = (self.current_object.id, property_name,)
            elif isinstance(self.current_object, Edge):
                height_key = (self.current_object.id, property_name,)
            else:
                raise ValueError("Unsupported object type for multiline property.")

            if property_name == "details":
                initial_height = (self.editor_heights.get(height_key, 10,))
            else:
                initial_height = (self.editor_heights.get(height_key, 3,))

            def save_height(new_height, key=height_key,):
                self.editor_heights[key] = (new_height)

                self.after_idle(self.update_scroll_region)

            return ResizableText(
                self.property_frame,
                value=value,
                height_lines=initial_height,
                min_lines=1,
                max_lines=30,
                readonly=(property_name in self.readonly_properties),
                on_height_changed=save_height,
            )

        # カラーコードプロパティリストに含まれている属性値は、カラーコードの入力欄として扱う
        if property_name in self.rgbcolor_properties:
            color_var = tk.StringVar(value=value)
            editor = tk.Entry(self.property_frame, textvariable=color_var,)

            def update_bgcolor(*args):
                color = color_var.get()

                # #RRGGBB形式かチェック
                if re.fullmatch(r"#[0-9A-Fa-f]{6}", color):
                    editor.config(bg=color)

                    # 背景の明るさに応じて文字色を変更
                    r = int(color[1:3], 16)
                    g = int(color[3:5], 16)
                    b = int(color[5:7], 16)

                    brightness = (r * 299 + g * 587 + b * 114) / 1000
                    editor.config(fg="black" if brightness > 128 else "white")
                else:
                    editor.config(bg="white", fg="black")

            color_var.trace_add("write", update_bgcolor)
            update_bgcolor()  # 初期値を反映
        elif type_info_name == "Node":
            # Nodeオブジェクトの参照を表示するためのエントリを作成
            editor = ttk.Entry(self.property_frame,)
            editor.insert(0, str("Node(" + str(value.id) + ":" + str(value.type) + ":" + str(value.text) + ")"))
        else:
            editor = ttk.Entry(self.property_frame, )
            editor.insert(0, str(value))

        if (property_name in self.readonly_properties):
            editor.configure(state="readonly")

        return editor

    # --------------------------------
    # オブジェクトへの反映
    # --------------------------------

    def apply_changes(self):
        if self.current_object is None:
            return

        # self.masterのnodes[]から当該オブジェクトが除外されていないかをチェック
        if isinstance(self.current_object, Node):
            if self.isdataexists_callback(self.current_object.id) != True:
                messagebox.showinfo("Error", "The data does not exist. It may have been deleted.",)
                return
        elif isinstance(self.current_object, Edge):
            if self.isdataexists_callback(self.current_object.id) != True:
                messagebox.showinfo("Error", "The data does not exist. It may have been deleted.",)
                return

        converted_values = {}

        for field_info in fields(self.current_object):
            property_name = field_info.name

            if (property_name in self.readonly_properties):
                continue

            if (property_name in self.excluded_properties):
                continue

            editor = self.editors[property_name]

            if isinstance(editor, ResizableText,):
                raw_value = editor.get_text()
            else:
                raw_value = editor.get()

            try:
                converted_values[property_name] = self.convert_value(property_name, raw_value, field_info.type,)

            except ValueError as error:
                messagebox.showerror("Input Error / 入力エラー", f"{property_name}: {error}",)
                if isinstance(editor, ResizableText,):
                    editor.focus_editor()
                else:
                    editor.focus_set()
                return

        # type変更時のshape_typeの自動補正
        if isinstance(self.current_object, Node):
            new_type_value = converted_values["type"]
            new_shape_type = converted_values["shape_type"]
            if new_type_value in ["decision", "io", "storage", "document", "special_node"]:
                converted_values["shape_type"] = new_type_value
            elif new_type_value == "terminator":
                if new_shape_type not in ["normal", "small"]:
                    converted_values["shape_type"] = "normal"
            elif new_type_value == "process":
                if new_shape_type not in ["rectangle", "corner_rounded_rectangle", "ellipse"]:
                    converted_values["shape_type"] = "corner_rounded_rectangle"
        elif isinstance(self.current_object, Edge):
            new_edge_type = converted_values["edge_type"]
            new_path_type = converted_values["path_type"]
            new_label_position = converted_values["label_position"] if "label_position" in converted_values else None
            if new_edge_type == "elbow":
                if new_path_type is None:
                    converted_values["path_type"] = "vertical"
            # elif new_edge_type == "line":
            #     converted_values["label_position"] = "auto"
            if new_label_position is None:
                converted_values["label_position"] = "auto"

        for property_name, value in (converted_values.items()):
            # print(f"self.current_object.id: {self.current_object.id},  Applying change: {property_name} => {value}")
            setattr(self.current_object, property_name, value,)

        self.refresh_callback()

        messagebox.showinfo("Finish.", "Settings have been applied. / 設定値を反映しました。",)

    def convert_value(self, property_name, raw_value, value_type,):
        type_info_name, type_info_choices = get_type_info(value_type)
        # print(f"Converting value: property_name:{property_name}, raw_value:{raw_value}, value_type:{value_type}, type_info:{type_info_name}, choices:{type_info_choices}")

        # xxxx_colorという属性の値が#RRGGBB形式かをチェック
        if property_name in self.rgbcolor_properties:
            # print("color code check.")
            if not isinstance(raw_value, str) or not re.fullmatch(r"#[0-9A-Fa-f]{6}", raw_value):
                raise ValueError(f"The value of {property_name} is not a valid hexadecimal RGB color code. Please use the #RRGGBB format. / {property_name}の値が、16進のRGBコードではありません。 #RRGGBB 形式で指定してください。")

        if raw_value is None:
            return None

        if raw_value == "":
            return None

        if type_info_name in ("str", "Optional[str]"):
            return str(raw_value)

        if type_info_name in ("int", "Optional[int]"):
            try:
                return int(raw_value)
            except ValueError as error:
                raise ValueError("Please enter an integer. / 整数を入力してください。") from error

        if type_info_name in ("float", "Optional[float]"):
            try:
                return float(raw_value)
            except ValueError as error:
                raise ValueError("Please enter a numeric value. / 数値を入力してください。") from error

        if type_info_name in ("bool", "Optional[bool]"):
            if raw_value == "True":
                return True
            else:
                return False

            raise ValueError("TrueまたはFalseを選択してください。")

        if type_info_name == "Literal" and type_info_choices is not None:
            if str(raw_value) in type_info_choices:
                return str(raw_value)
            elif int(raw_value) in type_info_choices:
                return int(raw_value) 
            raise ValueError(f"Invalid value. Please select one of the following: {type_info_choices}. / 有効な値ではありません。{type_info_choices}のいずれかを選択してください。")

        if type_info_name == "Optional[Literal]" and type_info_choices is not None:
            if str(raw_value) in type_info_choices:
                return str(raw_value)
            elif int(raw_value) in type_info_choices:
                return int(raw_value) 
            raise ValueError(f"Invalid value. Please select one of the following: {type_info_choices}. / 有効な値ではありません。{type_info_choices}のいずれかまたはNoneを選択してください。")

        return raw_value

    def print_current_object(self):
        if self.current_object is None:
            return

        print("---- 	Current Object / 現在のオブジェクト ----")

        for field_info in fields(self.current_object):
            property_name = field_info.name
            if (property_name in self.excluded_properties):
                continue

            value = getattr(self.current_object, property_name,)

            print(f"{property_name} = {value!r}")

if __name__ == "__main__":

    root = tk.Tk()
    root.title("列幅・行高変更可能なプロパティエディタ")
    root.geometry("400x700")
    root.minsize(350, 500)
    root.maxsize(600, 900)

    Node1 = Node(
            id = "1",
            type = "process",
            text = "処理",
            x = 100,
            y = 100,
            w = 100,
            h = 30,
            shape_type = "rectangle",
            fill_color = "#a0a0a0",
            outline_color = "#a0a0a0",
            details = "test\n複数行のテキスト\nを表示できます。",
            status = "normal",
            outline_width = 2,
            text_width = 110,
            text_color = "#a0a0a0",
            font_family = "Arial",
            font_size = 9,
            font_weight = font.NORMAL,
        )

    Node2 = Node(
            id = "2",
            type = "process",
            text = "処理",
            x = 100,
            y = 100,
            w = 100,
            h = 30,
            shape_type = "rectangle",
            fill_color = "#a0a0a0",
            outline_color = "#a0a0a0",
            details = "test",
            status = "normal",
            outline_width = 2,
            text_width = 110,
            text_color = "#a0a0a0",
            font_family = "Arial",
            font_size = 9,
            font_weight = font.NORMAL,
        )
    node_objects = [
        Node1,
        Node2,
    ]
    edge_objects = [
        Edge(
            id = 1,
            line_id = 100,
            from_node_obj = Node1,
            to_node_obj = Node2,
            edge_type = "elbow",
            path_type = "vertical",
            line_style = "solid",
            color = "#000000",
            points = [(100, 100), (150, 150), (200, 100)],
            label_x = 150,
            label_y = 125,
            label_text = "Edge Label",
            label_anchor = "center",
            label_justify = "left",
            label_position = "auto",
            connection_mode = "auto",
            from_node_connection_point = "bottom",
            to_node_connection_point = "top",
            edge_wrap_margin = 10,
            edge_wrap_ratio1 = 0.5,
            edge_wrap_ratio2 = 0.5,
        ),
    ]

    def refresh_callback():
        print("Refresh called")

    def isdataexists_callback(data_id: str) -> bool:
        print(f"Check if data exists: {data_id}")
        return True

    def reload_callback():
        print("Reload called")

    app = PropertyEditor(root, refresh_callback, isdataexists_callback, reload_callback)
    # app.set_target_objects(node_objects)
    app.set_target_objects(edge_objects)
    app.mainloop()