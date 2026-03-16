import tkinter as tk
from tkinter import ttk, messagebox

class ModalWindow(tk.Toplevel):
    def __init__(self, parent, title="Modal Window", width=400, height=300):
        super().__init__(parent)
        parent_width = parent.winfo_width()  # 親ウィンドウの幅を取得
        parent_height = parent.winfo_height()  # 親ウィンドウの高さを取得
        window_x = parent.winfo_x() + (parent_width - width) // 2  # 親ウィンドウの中央に配置するためのX座標
        window_y = parent.winfo_y() + (parent_height - height) // 2  # 親ウィンドウの中央に配置するためのY座標
        self.title(title)
        self.geometry(f"{width}x{height}+{window_x}+{window_y}")
        self.transient(parent)  # 親ウィンドウの上に表示
        self.grab_set()  # モーダル状態にする

        # ウィンドウの内容をここに追加
        # label = ttk.Label(self, text="This is a modal window.")
        # label.pack(pady=20)

        # close_button = ttk.Button(self, text="Close", command=self.destroy)
        # close_button.pack(pady=10)
        # self.protocol("WM_DELETE_WINDOW", self.destroy)  # ウィンドウの閉じるボタンでdestroyを呼び出す

        # self.wait_window(self)  # モーダルウィンドウが閉じられるまで待機する

class ResizeCanvasModal(ModalWindow):
    def __init__(self, parent, title="Resizing Canvas"):
        dialog_width = 300
        dialog_height = 200
        super().__init__(parent, title, dialog_width, dialog_height)

        # Resize width x height
        input_frame = ttk.Frame(self)
        input_frame.pack(anchor="center", expand=True)

        # input width
        input_width_frame = ttk.Frame(input_frame)
        input_width_frame.pack(side=tk.TOP)
        ttk.Label(input_width_frame, text="Width").pack(side=tk.LEFT, padx=5, pady=(5,5))
        self.width_var = tk.StringVar(self, value=str(parent.canvas_width))
        self.width_entry = ttk.Entry(input_width_frame, textvariable=self.width_var, width=10, justify="right")
        self.width_entry.pack(side=tk.LEFT, padx=10, pady=(5, 5))
        ttk.Label(input_width_frame, text="px").pack(side=tk.LEFT, pady=(5,5))

        # input height
        input_height_frame = ttk.Frame(input_frame)
        input_height_frame.pack(side=tk.TOP)
        ttk.Label(input_height_frame, text="Height").pack(side=tk.LEFT, padx=5, pady=(5,5))
        self.height_var = tk.StringVar(self, value=str(parent.canvas_height))
        self.height_entry = ttk.Entry(input_height_frame, textvariable=self.height_var, width=10, justify="right")
        self.height_entry.pack(side=tk.LEFT, padx=10, pady=(5, 5))
        ttk.Label(input_height_frame, text="px").pack(side=tk.LEFT, pady=(5,5))

        # Minimum width x height
        minimum_canvas_width = int(parent.scrollbar_x.winfo_width())-4
        minimum_canvas_height = int(parent.scrollbar_y.winfo_height())-4
        mimimum_size_checkbox_var = tk.BooleanVar(value=False)
        minimum_size_checkbox = ttk.Checkbutton(input_frame,
                                                text=f"Minimum Size : {minimum_canvas_width} px x {minimum_canvas_height} px",
                                                variable=mimimum_size_checkbox_var,
                                                command=lambda: self._set_minimum_size(mimimum_size_checkbox_var, minimum_canvas_width, minimum_canvas_height))
        minimum_size_checkbox.pack(side=tk.TOP, pady=(10,10))

        bottom_frame = ttk.Frame(self)
        bottom_frame.pack(side=tk.BOTTOM)
        resize_button = ttk.Button(bottom_frame, text="Resize", command=lambda: self._resize_canvas(parent))
        resize_button.pack(side=tk.LEFT, fill=tk.X, padx=5, pady=(10,10))
        cancel_button = ttk.Button(bottom_frame, text="Cancel", command=self.destroy)
        cancel_button.pack(side=tk.LEFT, fill=tk.X, padx=5,pady=(10,10))

        self.protocol("WM_DELETE_WINDOW", self.destroy)  # ウィンドウの閉じるボタンでdestroyを呼び出す
        
        self.wait_window(self)  # モーダルウィンドウが閉じられるまで待機する

    def _resize_canvas(self, parent):
        # print("Resizing canvas:", self.width_var.get(), self.height_var.get())
        minimum_canvas_width = int(parent.scrollbar_x.winfo_width())-4
        minimum_canvas_height = int(parent.scrollbar_y.winfo_height())-4
        try:
            new_width = int(self.width_var.get())
            new_height = int(self.height_var.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid integers for width and height.")
            return

        if new_width < minimum_canvas_width or new_height < minimum_canvas_height:
            messagebox.showerror("Invalid Input", f"Width must be at least {minimum_canvas_width} and height must be at least {minimum_canvas_height}.")
            return

        parent.canvas_width = new_width
        parent.canvas_height = new_height
        parent.canvas.config(width=parent.canvas_width, height=parent.canvas_height)
        parent._draw_grid()

        self.destroy()

    def _set_minimum_size(self, checkbox_var, minimum_width, minimum_height):
        if checkbox_var.get():
            self.width_var.set(str(minimum_width))
            self.height_var.set(str(minimum_height))
            self.width_entry.config(state=tk.DISABLED)
            self.height_entry.config(state=tk.DISABLED)
        else:
            self.width_entry.config(state=tk.NORMAL)
            self.height_entry.config(state=tk.NORMAL)
