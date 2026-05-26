import tkinter as tk
import tkinter.font as tkfont


class StickyNote:
    def __init__(self, canvas, x, y, w, h, text):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text

        self.padding = 10
        self.font = tkfont.Font(family="Meiryo", size=12)

        self.rect_id = None
        self.text_id = None
        self.editor = None
        self.editor_window_id = None

        self.draw()

    def wrap_text(self, text, max_width):
        lines = []

        for raw_line in text.split("\n"):
            current = ""
            for char in raw_line:
                test = current + char
                if self.font.measure(test) <= max_width:
                    current = test
                else:
                    lines.append(current)
                    current = char
            lines.append(current)

        return lines

    def get_display_text(self):
        text_width = self.w - self.padding * 2
        text_height = self.h - self.padding * 2

        lines = self.wrap_text(self.text, text_width)

        line_height = self.font.metrics("linespace")
        max_lines = max(1, text_height // line_height)

        if len(lines) > max_lines:
            lines = lines[:max_lines]
            while self.font.measure(lines[-1] + "...") > text_width and lines[-1]:
                lines[-1] = lines[-1][:-1]
            lines[-1] += "..."

        return "\n".join(lines)

    def draw(self):
        self.rect_id = self.canvas.create_rectangle(
            self.x, self.y, self.x + self.w, self.y + self.h,
            fill="#FFF4A3",
            outline="#D6B94D",
            width=2
        )

        self.text_id = self.canvas.create_text(
            self.x + self.padding,
            self.y + self.padding,
            text=self.get_display_text(),
            anchor="nw",
            font=self.font,
            fill="#333333",
            width=self.w - self.padding * 2
        )

        self.canvas.tag_bind(self.rect_id, "<Double-Button-1>", self.start_edit)
        self.canvas.tag_bind(self.text_id, "<Double-Button-1>", self.start_edit)

    def start_edit(self, event=None):
        if self.editor is not None:
            return

        # 表示中の文字を一時的に隠す
        self.canvas.itemconfigure(self.text_id, state="hidden")

        self.editor = tk.Text(
            self.canvas,
            font=self.font,
            wrap="char",
            bd=0,
            padx=2,
            pady=2,
            bg="#FFF4A3",
            fg="#333333",
            highlightthickness=1,
            highlightbackground="#D6B94D"
        )

        self.editor.insert("1.0", self.text)

        self.editor_window_id = self.canvas.create_window(
            self.x + self.padding,
            self.y + self.padding,
            anchor="nw",
            width=self.w - self.padding * 2,
            height=self.h - self.padding * 2,
            window=self.editor
        )

        self.editor.focus_set()

        # Ctrl+Enter または フォーカスアウトで確定
        self.editor.bind("<Control-Return>", self.finish_edit)
        self.editor.bind("<FocusOut>", self.finish_edit)

    def finish_edit(self, event=None):
        if self.editor is None:
            return

        self.text = self.editor.get("1.0", "end-1c")

        self.canvas.delete(self.editor_window_id)
        self.editor.destroy()

        self.editor = None
        self.editor_window_id = None

        self.canvas.itemconfigure(
            self.text_id,
            text=self.get_display_text(),
            state="normal"
        )


root = tk.Tk()
root.title("Editable Sticky Note Sample")

canvas = tk.Canvas(root, width=600, height=400, bg="white")
canvas.pack(fill="both", expand=True)

StickyNote(
    canvas,
    50, 50, 240, 150,
    "ダブルクリックすると、この付箋の文字を編集できます。"
)

StickyNote(
    canvas,
    330, 80, 190, 120,
    "文字が多い場合は、表示時に省略されます。"
)

root.mainloop()