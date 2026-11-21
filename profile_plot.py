import tkinter as tk

from models import RouteDepth


def plot_profile(
    route_depths: list[RouteDepth],
    maximum_depth: float,
    accumulated: bool,
) -> None:
    if not route_depths:
        print("Маршрут порожній")
        return

    root = tk.Tk()
    root.title("Профіль дна ехолота")
    canvas = tk.Canvas(root, width=1000, height=500, bg="white")
    canvas.pack(fill="both", expand=True)
    canvas.create_text(
        500,
        18,
        text=f"Профіль дна; максимальна глибина системи: {maximum_depth:.3f} м",
        fill="black",
    )

    left, right, top, bottom = 70, 970, 50, 450
    plot_width = right - left
    plot_height = bottom - top
    values = [
        item.accumulated_depth_m if accumulated else item.depth_m
        for item in route_depths
    ]
    scale_limit = maximum_depth

    canvas.create_line(left, top, left, bottom, fill="gray")
    canvas.create_line(left, bottom, right, bottom, fill="gray")
    canvas.create_line(left, top, right, top, fill="#888888", dash=(3, 3))

    points: list[tuple[int, int]] = []
    for index, value in enumerate(values):
        x = left
        if len(values) > 1:
            x = left + round(index * plot_width / (len(values) - 1))
        y = top + round(min(value / scale_limit, 1.0) * plot_height)
        points.append((x, y))

    for x, y in points:
        canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="#0066cc")
    for start, end in zip(points, points[1:]):
        canvas.create_line(*start, *end, fill="#0066cc", width=2)

    root.mainloop()
