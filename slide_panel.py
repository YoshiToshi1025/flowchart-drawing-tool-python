import tkinter as tk

class SlidePanel(tk.Frame):
    """
    左右からスライドインする汎用 Frame

    parent : 配置先のFrame
    side   : "left" または "right"
    width  : 初期幅
    min_width : 最小幅
    max_width : 最大幅
    """

    def __init__(
        self,
        parent,
        side="left", # "left" or "right"
        width=500,
        min_width=200,
        max_width=900,
        bg="#f0f0f0",
        animation_step=60,
        animation_interval=10,
        **kwargs
    ):
        super().__init__(parent, bg=bg, **kwargs)

        if side not in ("left", "right"):
            raise ValueError('side must be "left" or "right"')

        self.parent = parent
        self.side = side

        self.panel_width = width
        self.min_width = min_width
        self.max_width = max_width

        self.animation_step = animation_step
        self.animation_interval = animation_interval

        self.is_open = False
        self._animation_id = None

        # ドラッグ開始時の情報
        self._drag_start_x = 0
        self._drag_start_width = width

        # リサイズ用ハンドル
        self.resize_handle = tk.Frame(
            self,
            width=3,
            bg="#888888",
            cursor="sb_h_double_arrow"
        )

        if self.side == "left":
            self.resize_handle.pack(side="right", fill="y")
        else:
            self.resize_handle.pack(side="left", fill="y")

        self.resize_handle.bind(
            "<ButtonPress-1>",
            self._start_resize
        )

        self.resize_handle.bind(
            "<B1-Motion>",
            self._resize
        )

        # 親Frameサイズ変更時
        self.parent.bind(
            "<Configure>",
            self._on_parent_resize,
            add="+"
        )

        # 初期配置
        self.after_idle(self._set_initial_position)

    # --------------------------------------------------
    # 初期位置
    # --------------------------------------------------
    def _set_initial_position(self):
        parent_width = self.parent.winfo_width()

        if self.side == "left":
            x = -self.panel_width
        else:
            x = parent_width

        self.place(
            x=x,
            y=0,
            width=self.panel_width,
            relheight=1
        )

        # Canvas等より前面へ
        self.lift()

    # --------------------------------------------------
    # 目標X座標
    # --------------------------------------------------
    def _get_target_x(self, open_state):
        parent_width = self.parent.winfo_width()

        if self.side == "left":

            if open_state:
                return 0
            else:
                return -self.panel_width

        else:

            if open_state:
                return parent_width - self.panel_width
            else:
                return parent_width

    # --------------------------------------------------
    # 開く
    # --------------------------------------------------
    def open(self):
        if self.is_open:
            return

        self.is_open = True
        self.lift()

        target_x = self._get_target_x(True)

        self._animate(target_x)

    # --------------------------------------------------
    # 閉じる
    # --------------------------------------------------
    def close(self):
        if not self.is_open:
            return

        self.is_open = False

        target_x = self._get_target_x(False)

        self._animate(target_x)

    # --------------------------------------------------
    # 開閉切り替え
    # --------------------------------------------------
    def toggle(self):
        if self.is_open:
            self.close()
        else:
            self.open()

    # --------------------------------------------------
    # アニメーション
    # --------------------------------------------------
    def _animate(self, target_x):

        if self._animation_id is not None:
            self.after_cancel(self._animation_id)
            self._animation_id = None

        current_x = self.winfo_x()

        distance = target_x - current_x

        # 到達
        if abs(distance) <= self.animation_step:
            self.place_configure(x=target_x)
            self._animation_id = None
            return

        if distance > 0:
            new_x = current_x + self.animation_step
        else:
            new_x = current_x - self.animation_step

        self.place_configure(x=new_x)

        self._animation_id = self.after(
            self.animation_interval,
            lambda: self._animate(target_x)
        )

    # --------------------------------------------------
    # リサイズ開始
    # --------------------------------------------------
    def _start_resize(self, event):
        self._drag_start_x = event.x_root
        self._drag_start_width = self.panel_width

    # --------------------------------------------------
    # ドラッグリサイズ
    # --------------------------------------------------
    def _resize(self, event):

        if not self.is_open:
            return

        delta_x = event.x_root - self._drag_start_x

        if self.side == "left":
            # 左パネル
            # 右端を右へ動かす → 幅を広げる
            new_width = self._drag_start_width + delta_x

        else:
            # 右パネル
            # 左端を左へ動かす → 幅を広げる
            new_width = self._drag_start_width - delta_x

        parent_width = self.parent.winfo_width()

        max_width = min(
            self.max_width,
            parent_width - 50
        )

        new_width = max(
            self.min_width,
            min(new_width, max_width)
        )

        self.panel_width = int(new_width)

        self._update_position()

    # --------------------------------------------------
    # 現在状態に応じて位置更新
    # --------------------------------------------------
    def _update_position(self):

        parent_width = self.parent.winfo_width()

        if self.side == "left":

            if self.is_open:
                x = 0
            else:
                x = -self.panel_width

        else:

            if self.is_open:
                x = parent_width - self.panel_width
            else:
                x = parent_width

        self.place_configure(
            x=x,
            width=self.panel_width
        )

        self.lift()

    # --------------------------------------------------
    # 親Frameのサイズ変更
    # --------------------------------------------------
    def _on_parent_resize(self, event):
        self._update_position()

    # --------------------------------------------------
    # 外部から幅を設定
    # --------------------------------------------------
    def set_width(self, width):

        width = max(
            self.min_width,
            min(width, self.max_width)
        )

        self.panel_width = width

        self._update_position()

    # --------------------------------------------------
    # 現在幅取得
    # --------------------------------------------------
    def get_width(self):
        return self.panel_width


# ======================================================
# メインアプリケーション
# ======================================================

class Application(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Tkinter Slide Panel Sample")
        self.geometry("1200x800")
        self.minsize(800, 500)

        # ==============================================
        # ツールバー
        # ==============================================
        toolbar = tk.Frame(
            self,
            height=50,
            bg="#333333"
        )

        toolbar.pack(
            side="top",
            fill="x"
        )

        toolbar.pack_propagate(False)

        # ==============================================
        # Canvasを入れるメイン領域
        # ==============================================
        self.main_frame = tk.Frame(
            self,
            bg="white"
        )

        self.main_frame.pack(
            side="top",
            fill="both",
            expand=True
        )

        # ==============================================
        # Canvas
        # ==============================================
        self.canvas = tk.Canvas(
            self.main_frame,
            bg="white",
            highlightthickness=0
        )

        self.canvas.pack(
            fill="both",
            expand=True
        )

        # Canvas上にサンプル描画
        self.canvas.create_rectangle(
            300,
            200,
            600,
            400,
            fill="#dcecff",
            outline="#4682b4",
            width=2
        )

        self.canvas.create_text(
            450,
            300,
            text="Main Canvas",
            font=("Arial", 24)
        )

        # ==============================================
        # 左スライドパネル
        # ==============================================
        self.left_panel = SlidePanel(
            self.main_frame,
            side="left",
            width=500,
            min_width=200,
            max_width=900,
            bg="#e8eef5"
        )

        self._create_left_panel_contents()

        # ==============================================
        # 右スライドパネル
        # ==============================================
        self.right_panel = SlidePanel(
            self.main_frame,
            side="right",
            width=500,
            min_width=200,
            max_width=900,
            bg="#f5eee8"
        )

        self._create_right_panel_contents()

        # ==============================================
        # ツールバーボタン
        # ==============================================
        btn_left = tk.Button(
            toolbar,
            text="左パネル",
            command=self.left_panel.toggle,
            width=12
        )

        btn_left.pack(
            side="left",
            padx=5,
            pady=8
        )

        btn_right = tk.Button(
            toolbar,
            text="右パネル",
            command=self.right_panel.toggle,
            width=12
        )

        btn_right.pack(
            side="left",
            padx=5,
            pady=8
        )

    # --------------------------------------------------
    # 左パネル内容
    # --------------------------------------------------
    def _create_left_panel_contents(self):

        # resize_handle以外の内容を配置するFrame
        content = tk.Frame(
            self.left_panel,
            bg="#e8eef5"
        )

        content.pack(
            side="left",
            fill="both",
            expand=True
        )

        title = tk.Label(
            content,
            text="左スライドパネル",
            bg="#e8eef5",
            font=("Arial", 18, "bold")
        )

        title.pack(
            pady=(30, 20)
        )

        tk.Label(
            content,
            text="通常のFrameなので\n自由にWidgetを配置できます。",
            bg="#e8eef5",
            font=("Arial", 12)
        ).pack(pady=20)

        tk.Button(
            content,
            text="閉じる",
            command=self.left_panel.close
        ).pack(pady=10)

        tk.Entry(
            content,
            width=30
        ).pack(pady=10)

        tk.Text(
            content,
            width=40,
            height=10
        ).pack(
            padx=20,
            pady=10,
            fill="both",
            expand=True
        )

    # --------------------------------------------------
    # 右パネル内容
    # --------------------------------------------------
    def _create_right_panel_contents(self):

        content = tk.Frame(
            self.right_panel,
            bg="#f5eee8"
        )

        content.pack(
            side="right",
            fill="both",
            expand=True
        )

        title = tk.Label(
            content,
            text="右スライドパネル",
            bg="#f5eee8",
            font=("Arial", 18, "bold")
        )

        title.pack(
            pady=(30, 20)
        )

        tk.Label(
            content,
            text="左端をドラッグすると\nパネル幅を変更できます。",
            bg="#f5eee8",
            font=("Arial", 12)
        ).pack(pady=20)

        tk.Button(
            content,
            text="閉じる",
            command=self.right_panel.close
        ).pack(pady=10)

        listbox = tk.Listbox(
            content
        )

        for i in range(1, 21):
            listbox.insert(
                tk.END,
                f"Item {i}"
            )

        listbox.pack(
            padx=20,
            pady=20,
            fill="both",
            expand=True
        )


# ======================================================
# 起動
# ======================================================

if __name__ == "__main__":

    app = Application()
    app.mainloop()