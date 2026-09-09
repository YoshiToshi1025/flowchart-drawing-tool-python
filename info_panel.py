import tkinter as tk
from tkinter import ttk
import constants as ct

class InfoPanel:
    """Canvas右側からスライド表示するタブ付きパネル"""

    def __init__(self, panel_frame):
        self.panel_frame = panel_frame

        # =====================================================
        # Notebook
        # =====================================================
        self.notebook = ttk.Notebook(self.panel_frame, padding=(0, 10, 0, 0))
        notebook_style = ttk.Style()
        notebook_style.configure("TNotebook", tabposition="nw")
        self.notebook.pack(fill="both", expand=True, padx=0, pady=0)

        # -----------------------------------------------------
        # タブ1 : リリースノート
        # -----------------------------------------------------
        self.changelog_frame = ttk.Frame(self.notebook)

        self.notebook.add(
            self.changelog_frame,
            text=ct.RELEASE_NOTE_TITLE,
            padding=(0, 0, 0, 0)
        )

        self._create_changelog_tab()

        # -----------------------------------------------------
        # タブ2 : キー&マウス定義
        # -----------------------------------------------------
        self.key_and_mouse_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.key_and_mouse_frame, text=ct.KEY_MOUSE_DEFINITIONS_TITLE, padding=(0, 0, 0, 0))
        # self._create_key_and_mouse_tab()

        # =====================================================
        # Sub_Notebook in キー&マウス定義
        # =====================================================
        self.sub_notebook_of_key_and_mouse = ttk.Notebook(self.key_and_mouse_frame, padding=(0, 5, 0, 0))
        self.sub_notebook_of_key_and_mouse.pack(fill="both", expand=True, padx=0, pady=0)

        # -----------------------------------------------------
        # タブ2-1 : キー操作
        # -----------------------------------------------------
        self.key_frame = ttk.Frame(self.sub_notebook_of_key_and_mouse)
        self.sub_notebook_of_key_and_mouse.add(self.key_frame, text=ct.SHORTCUT_KEY_TITLE, padding=(0, 0, 0, 0))
        self._create_key_tab()

        # -----------------------------------------------------
        # タブ2-2 : Canvasマウス操作
        # -----------------------------------------------------
        self.canvas_mouse_frame = ttk.Frame(self.sub_notebook_of_key_and_mouse)
        self.sub_notebook_of_key_and_mouse.add(self.canvas_mouse_frame, text=ct.MOUSE_ACTION_FOR_CANVAS_TITLE, padding=(0, 0, 0, 0))
        self._create_canvas_mouse_tab()

        # -----------------------------------------------------
        # タブ2-3 : Swimlaneマウス操作
        # -----------------------------------------------------
        self.swimlane_mouse_frame = ttk.Frame(self.sub_notebook_of_key_and_mouse)
        self.sub_notebook_of_key_and_mouse.add(self.swimlane_mouse_frame, text=ct.MOUSE_ACTION_FOR_SWIMLANE_TITLE, padding=(0, 0, 0, 0))
        self._create_swimlane_mouse_tab()

        # -----------------------------------------------------
        # タブ2-4 : Nodeマウス操作
        # -----------------------------------------------------
        self.node_mouse_frame = ttk.Frame(self.sub_notebook_of_key_and_mouse)
        self.sub_notebook_of_key_and_mouse.add(self.node_mouse_frame, text=ct.MOUSE_ACTION_FOR_NODE_TITLE, padding=(0, 0, 0, 0))
        self._create_node_mouse_tab()

        # -----------------------------------------------------
        # タブ2-5 : Linkマウス操作
        # -----------------------------------------------------
        self.link_mouse_frame = ttk.Frame(self.sub_notebook_of_key_and_mouse)
        self.sub_notebook_of_key_and_mouse.add(self.link_mouse_frame, text=ct.MOUSE_ACTION_FOR_LINK_TITLE, padding=(0, 0, 0, 0))
        self._create_link_mouse_tab()

        # -----------------------------------------------------
        # タブ2-6 : Noteマウス操作
        # -----------------------------------------------------
        self.note_mouse_frame = ttk.Frame(self.sub_notebook_of_key_and_mouse)
        self.sub_notebook_of_key_and_mouse.add(self.note_mouse_frame, text=ct.MOUSE_ACTION_FOR_NOTE_TITLE, padding=(0, 0, 0, 0))
        self._create_note_mouse_tab()

        # -----------------------------------------------------
        # タブ3 : 基本操作ガイド
        # -----------------------------------------------------
        self.help_frame = ttk.Frame(
            self.notebook
        )

        self.notebook.add(
            self.help_frame,
            text=ct.BASIC_HELP_TITLE,
            padding=(0, 0, 0, 0)
        )

        self._create_help_tab()


    # =========================================================
    # キー割り当てタブ
    # =========================================================
    def _create_key_tab(self):

        style = ttk.Style()
        # style.theme_use("default")
        style.configure("Treeview.Heading", background="#eeeeee", relief="flat")

        frame = ttk.Frame(self.key_frame)
        frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Treeview
        columns = ("key", "function")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        tree.heading("key", text=ct.SHORTCUT_KEY_COLUMN_1_TITLE)
        tree.heading("function", text=ct.SHORTCUT_KEY_COLUMN_2_TITLE)
        tree.column("key", width=80, anchor="w")
        tree.column("function", width=310, anchor="w")

        # scrollbar = ttk.Scrollbar(tree, orient="vertical", command=tree.yview)
        # tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        # scrollbar.pack(side="right", fill="y")

        shortcut_key_list = ct.SHORTCUT_KEY_LIST

        for key, function in shortcut_key_list:
            tree.insert("", "end", values=(key, function))

    # =========================================================
    # マウス割り当てタブ
    # =========================================================
    def _create_canvas_mouse_tab(self):

        frame = ttk.Frame(self.canvas_mouse_frame)
        frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Treeview
        columns = ("mouse", "function")

        tree_for_canvas = ttk.Treeview(frame, columns=columns, show="headings", height=4)
        tree_for_canvas.heading("mouse", text=ct.MOUSE_ACTION_FOR_CANVAS_COLUMN_1_TITLE)
        tree_for_canvas.heading("function", text=ct.MOUSE_ACTION_FOR_CANVAS_COLUMN_2_TITLE)
        tree_for_canvas.column("mouse", width=170, anchor="w")
        tree_for_canvas.column("function", width=220, anchor="w")
        # scrollbar_for_canvas = ttk.Scrollbar(frame, orient="vertical", command=tree_for_canvas.yview)
        # tree_for_canvas.configure(yscrollcommand=scrollbar_for_canvas.set)
        tree_for_canvas.pack(side="left", fill="both", expand=True)
        # scrollbar_for_canvas.pack(side="right", fill="y")

        mouse_operation_for_canvas_list = ct.MOUSE_ACTION_FOR_CANVAS_LIST

        for key, function in mouse_operation_for_canvas_list:
            tree_for_canvas.insert("", "end", values=(key, function))

    def _create_swimlane_mouse_tab(self):
        frame = ttk.Frame(self.swimlane_mouse_frame)
        frame.pack(fill="both", expand=True, padx=0, pady=0)

        columns = ("mouse", "function")

        tree_for_swimlane = ttk.Treeview(frame, columns=columns, show="headings", height=7)
        tree_for_swimlane.heading("mouse", text=ct.MOUSE_ACTION_FOR_SWIMLANE_COLUMN_1_TITLE)
        tree_for_swimlane.heading("function", text=ct.MOUSE_ACTION_FOR_SWIMLANE_COLUMN_2_TITLE)
        tree_for_swimlane.column("mouse", width=170, anchor="w")
        tree_for_swimlane.column("function", width=220, anchor="w")
        # scrollbar_for_swimlane = ttk.Scrollbar(frame, orient="vertical", command=tree_for_swimlane.yview)
        # tree_for_swimlane.configure(yscrollcommand=scrollbar_for_swimlane.set)
        tree_for_swimlane.pack(side="left", fill="both", expand=True)
        # scrollbar_for_swimlane.pack(side="right", fill="y")

        mouse_operation_for_swimlane_list = ct.MOUSE_ACTION_FOR_SWIMLANE_LIST

        for key, function in mouse_operation_for_swimlane_list:
            tree_for_swimlane.insert("", "end", values=(key, function))

    def _create_node_mouse_tab(self):
        frame = ttk.Frame(self.node_mouse_frame)
        frame.pack(fill="both", expand=True, padx=0, pady=0)

        columns = ("mouse", "function")

        tree_for_node = ttk.Treeview(frame, columns=columns, show="headings", height=9)
        tree_for_node.heading("mouse", text=ct.MOUSE_ACTION_FOR_NODE_COLUMN_1_TITLE)
        tree_for_node.heading("function", text=ct.MOUSE_ACTION_FOR_NODE_COLUMN_2_TITLE)
        tree_for_node.column("mouse", width=170, anchor="w")
        tree_for_node.column("function", width=220, anchor="w")
        # scrollbar_for_node = ttk.Scrollbar(frame, orient="vertical", command=tree_for_node.yview)
        # tree_for_node.configure(yscrollcommand=scrollbar_for_node.set)
        tree_for_node.pack(side="left", fill="both", expand=True)
        # scrollbar_for_node.pack(side="right", fill="y")

        mouse_operation_for_node_list = ct.MOUSE_ACTION_FOR_NODE_LIST

        for key, function in mouse_operation_for_node_list:
            tree_for_node.insert("", "end", values=(key, function))

    def _create_link_mouse_tab(self):
        frame = ttk.Frame(self.link_mouse_frame)
        frame.pack(fill="both", expand=True, padx=0, pady=0)

        columns = ("mouse", "function")

        tree_for_link = ttk.Treeview(frame, columns=columns, show="headings", height=5)
        tree_for_link.heading("mouse", text=ct.MOUSE_ACTION_FOR_LINK_COLUMN_1_TITLE)
        tree_for_link.heading("function", text=ct.MOUSE_ACTION_FOR_LINK_COLUMN_2_TITLE)
        tree_for_link.column("mouse", width=170, anchor="w")
        tree_for_link.column("function", width=220, anchor="w")
        # scrollbar_for_link = ttk.Scrollbar(frame, orient="vertical", command=tree_for_link.yview)
        # tree_for_link.configure(yscrollcommand=scrollbar_for_link.set)
        tree_for_link.pack(side="left", fill="both", expand=True)
        # scrollbar_for_link.pack(side="right", fill="y")

        mouse_operation_for_link_list = ct.MOUSE_ACTION_FOR_LINK_LIST

        for key, function in mouse_operation_for_link_list:
            tree_for_link.insert("", "end", values=(key, function))

    def _create_note_mouse_tab(self):
        frame = ttk.Frame(self.note_mouse_frame)
        frame.pack(fill="both", expand=True, padx=0, pady=0)

        columns = ("mouse", "function")

        tree_for_note = ttk.Treeview(frame, columns=columns, show="headings", height=3)
        tree_for_note.heading("mouse", text=ct.MOUSE_ACTION_FOR_NOTE_COLUMN_1_TITLE)
        tree_for_note.heading("function", text=ct.MOUSE_ACTION_FOR_NOTE_COLUMN_2_TITLE)
        tree_for_note.column("mouse", width=170, anchor="w")
        tree_for_note.column("function", width=220, anchor="w")
        # scrollbar_for_note = ttk.Scrollbar(frame, orient="vertical", command=tree_for_note.yview)
        # tree_for_note.configure(yscrollcommand=scrollbar_for_note.set)
        tree_for_note.pack(side="left", fill="both", expand=True)
        # scrollbar_for_note.pack(side="right", fill="y")

        mouse_operation_for_note_list = ct.MOUSE_ACTION_FOR_NOTE_LIST

        for key, function in mouse_operation_for_note_list:
            tree_for_note.insert("", "end", values=(key, function))

    # =========================================================
    # リリースノートタブ
    # =========================================================
    def _create_changelog_tab(self):

        frame = ttk.Frame(
            self.changelog_frame
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=0,
            pady=0
        )

        scrollbar = ttk.Scrollbar(
            frame
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        text = tk.Text(
            frame,
            wrap="word",
            relief="flat",
            font=("", 9),
            spacing3 = 3, # 段落間のスペース
            yscrollcommand=scrollbar.set
        )

        text.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.config(
            command=text.yview
        )

        changelog_text = ct.RELEASE_NOTE_TEXT

        text.insert(
            "1.0",
            changelog_text
        )

        text.config(
            state="disabled"
        )
    # =========================================================
    # 基本操作ガイドタブ
    # =========================================================
    def _create_help_tab(self):

        frame = ttk.Frame(
            self.help_frame
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=0,
            pady=0
        )

        scrollbar = ttk.Scrollbar(
            frame
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        text = tk.Text(
            frame,
            wrap="word",
            relief="flat",
            font=("", 9),
            spacing3 = 3, # 段落間のスペース
            yscrollcommand=scrollbar.set
        )

        text.pack(
            side="left",
            fill="both",
            expand=True,
        )

        scrollbar.config(
            command=text.yview
        )

        help_text = ct.BASIC_HELP_TEXT

        text.insert(
            "1.0",
            help_text
        )

        text.config(
            state="disabled"
        )

    # =========================================================
    # 指定タブを表示
    # =========================================================
    def show_tab(self, index):

        self.notebook.select(
            index
        )

        self.show()
