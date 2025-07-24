import tkinter as tk

def select_region_for_blurring():
    region = []
    root = tk.Tk()
    root.attributes('-alpha', 0.3)
    root.attributes('-fullscreen', True)
    root.title("드래그로 블러 영역 선택")
    canvas = tk.Canvas(root, cursor="cross")
    canvas.pack(fill="both", expand=True)
    rect = [None]
    start = [None]

    def on_press(event):
        start[0] = (event.x, event.y)
        rect[0] = canvas.create_rectangle(event.x, event.y, event.x, event.y, outline='red', width=2)

    def on_drag(event):
        if rect[0]:
            canvas.coords(rect[0], start[0][0], start[0][1], event.x, event.y)

    def on_release(event):
        x1, y1 = start[0]
        x2, y2 = event.x, event.y
        region.extend([min(x1, x2), min(y1, y2), abs(x2-x1), abs(y2-y1)])
        root.destroy()

    canvas.bind("<ButtonPress-1>", on_press)
    canvas.bind("<B1-Motion>", on_drag)
    canvas.bind("<ButtonRelease-1>", on_release)
    root.mainloop()
    return tuple(region) if region else None