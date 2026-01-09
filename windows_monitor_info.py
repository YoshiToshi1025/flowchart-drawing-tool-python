import ctypes
from ctypes import wintypes
import tkinter as tk
import platform

user32 = ctypes.windll.user32
shcore = ctypes.windll.shcore

MONITOR_DEFAULTTONEAREST = 2
MDT_EFFECTIVE_DPI = 0

# DPI aware（拡大率や座標が正しく取れるように）
try:
    shcore.SetProcessDpiAwareness(1) if shcore is not None else None  # Per-monitor DPI aware
except Exception:
    pass

class MONITOR_INFO_EX(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.DWORD),
        ("rcMonitor", wintypes.RECT),
        ("rcWork", wintypes.RECT),
        ("dwFlags", wintypes.DWORD),
        ("szDevice", wintypes.WCHAR * 32),
    ]

def get_monitor_from_tk_window(canvas):
    hwnd = wintypes.HWND(canvas.winfo_id())  # tkのウィンドウハンドル
    hmon = user32.MonitorFromWindow(hwnd, MONITOR_DEFAULTTONEAREST)
    if not hmon:
        raise RuntimeError("MonitorFromWindow failed")

    info = MONITOR_INFO_EX()
    info.cbSize = ctypes.sizeof(MONITOR_INFO_EX)
    ok = user32.GetMonitorInfoW(hmon, ctypes.byref(info))
    if not ok:
        raise RuntimeError("GetMonitorInfoW failed")

    # モニタのDPI（拡大率）
    dpi_x = wintypes.UINT()
    dpi_y = wintypes.UINT()
    hr = shcore.GetDpiForMonitor(hmon, MDT_EFFECTIVE_DPI, ctypes.byref(dpi_x), ctypes.byref(dpi_y))
    if hr != 0:
        # 失敗したらNone扱い（環境によっては取れないことがある）
        dpi_x_val = None
        scale_percent = None
    else:
        dpi_x_val = dpi_x.value
        scale_percent = round(dpi_x_val / 96 * 100, 2)

    rc = info.rcMonitor
    monitor_rect = (rc.left, rc.top, rc.right, rc.bottom)
    monitor_width = rc.right - rc.left
    monitor_height = rc.bottom - rc.top

    return {
        "hwnd": hwnd.value,
        "device": info.szDevice,              # \\.\DISPLAY1 等
        "monitor_rect": monitor_rect,         # (L, T, R, B)
        "monitor_width": monitor_width,     # 横幅
        "monitor_height": monitor_height,     # 高さ
        "dpi_x": dpi_x_val,
        "scale_percent": scale_percent,
    }

def get_system_dpi_x(canvas):
    m = get_monitor_from_tk_window(canvas)
    dpi_x = m["dpi_x"]
    return dpi_x

def get_system_scale_percent(canvas):
    if platform.system() == "Windows":
        m = get_monitor_from_tk_window(canvas)
        scale_percent = m["scale_percent"]
    else:
        scale_percent = 100.0
    return scale_percent

def _draw_grid(canvas):
    """グリッドを再描画"""
    canvas.delete("grid")
    w = canvas.winfo_width()
    h = canvas.winfo_height()
    if w <= 0 or h <= 0:
        return
    step = 15 # グリッド間隔
    for x in range(0, w, step):
        canvas.create_line(x, 0, x, h, fill="lightgray", tags=("grid",))
    for y in range(0, h, step):
        canvas.create_line(0, y, w, y, fill="lightgray", tags=("grid",))
    # グリッドを最背面へ
    canvas.tag_lower("grid")

def test(canvas):
    """テスト用関数"""
    m = get_monitor_from_tk_window(canvas)
    print("HWND          :", m["hwnd"])
    print("Device        :", m["device"])
    print("Monitor Rect  :", m["monitor_rect"])
    print("Monitor Width :", m["monitor_width"])
    print("Monitor Height:", m["monitor_height"])
    print("DPI           :", m["dpi_x"])
    print("Scale         :", m["scale_percent"], "%")
    print(f"Canvas Size   : {canvas.winfo_width()} x {canvas.winfo_height()}\n")

# ---- 動作確認UI ----
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x400")
    root.title("Which monitor am I on?")

    # root.update_idletasks()

    print("Initial window size:", root.winfo_width(), "x", root.winfo_height())
    
    container = tk.Frame(root)
    container.pack(fill=tk.BOTH, expand=True)
    # container.update_idletasks()
    print("container size:", container.winfo_width(), "x", container.winfo_height())

    toolbar = tk.Frame(container)
    toolbar.pack(side=tk.TOP, fill=tk.X, pady=4)
    # toolbar.update_idletasks()
    tk.Button(toolbar, text="TEST", command=lambda: test(canvas)).pack(side=tk.LEFT, padx=1)
    print("toolbar size:", toolbar.winfo_width(), "x", toolbar.winfo_height())

    main_panel = tk.Frame(container)
    main_panel.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    # main_panel.update_idletasks()
    print("main_panel size:", main_panel.winfo_width(), "x", main_panel.winfo_height())

    canvas = tk.Canvas(main_panel, bg="white")
    canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    # canvas.grid(row=0, column=0, sticky="nsew")
    # canvas.update_idletasks()
    print("canvas size:", canvas.winfo_width(), "x", canvas.winfo_height())

    _draw_grid(canvas)   # 初期グリッド描画

    label = tk.Label(canvas, text="", justify="left", font=("Consolas", 11))
    label.pack(padx=12, pady=12, anchor="ne")

    def refresh():
        m = get_monitor_from_tk_window(canvas)
        _draw_grid(canvas)  # グリッド再描画
        label.config(text=
            f"HWND          : {m['hwnd']}\n"
            f"Device        : {m['device']}\n"
            f"Monitor Rect  : {m['monitor_rect']}\n"
            f"Monitor Width : {m['monitor_width']}\n"
            f"Monitor Height: {m['monitor_height']}\n"
            f"DPI           : {m['dpi_x']}\n"
            f"Scale         : {m['scale_percent']} %\n"
            f"Canvas Size   : ({canvas.winfo_rootx()}, {canvas.winfo_rooty()}), {canvas.winfo_width()} x {canvas.winfo_height()}\n"
        )
        root.after(300, refresh)  # 0.3秒ごとに更新（移動しても追従）

    refresh()
    root.mainloop()
