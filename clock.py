import tkinter as tk
import math
import time


CLOCK_SIZE = 400
CENTER = CLOCK_SIZE // 2
RADIUS = CENTER - 20
FACE_COLOR = "#1a1a2e"
RIM_COLOR = "#e0e0e0"
TICK_COLOR = "#e0e0e0"
HOUR_HAND_COLOR = "#ffffff"
MINUTE_HAND_COLOR = "#aaaaff"
SECOND_HAND_COLOR = "#ff4444"
NUMBER_COLOR = "#e0e0e0"
CENTER_DOT_COLOR = "#ff4444"


def hand_coords(angle_deg, length, cx, cy):
    """Return (x, y) tip of a clock hand given angle (0=12 o'clock) and length."""
    angle_rad = math.radians(angle_deg - 90)
    x = cx + length * math.cos(angle_rad)
    y = cy + length * math.sin(angle_rad)
    return x, y


class AnalogClock(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("clack – Analog Clock")
        self.resizable(False, False)
        self.configure(bg="#0d0d1a")

        self.canvas = tk.Canvas(
            self,
            width=CLOCK_SIZE,
            height=CLOCK_SIZE,
            bg="#0d0d1a",
            highlightthickness=0,
        )
        self.canvas.pack(padx=20, pady=20)

        self._draw_static_face()
        self._tick()

    def _draw_static_face(self):
        c = self.canvas
        cx, cy = CENTER, CENTER

        # Outer rim glow
        c.create_oval(
            cx - RADIUS - 4,
            cy - RADIUS - 4,
            cx + RADIUS + 4,
            cy + RADIUS + 4,
            outline="#555588",
            width=2,
        )
        # Clock face
        c.create_oval(
            cx - RADIUS,
            cy - RADIUS,
            cx + RADIUS,
            cy + RADIUS,
            fill=FACE_COLOR,
            outline=RIM_COLOR,
            width=3,
        )

        # Hour markers and numbers
        for hour in range(1, 13):
            angle = math.radians(hour * 30 - 90)
            cos_a = math.cos(angle)
            sin_a = math.sin(angle)

            # Tick marks
            inner = RADIUS - 20
            outer = RADIUS - 6
            x1 = cx + inner * cos_a
            y1 = cy + inner * sin_a
            x2 = cx + outer * cos_a
            y2 = cy + outer * sin_a
            c.create_line(x1, y1, x2, y2, fill=TICK_COLOR, width=3, capstyle=tk.ROUND)

            # Numbers
            num_r = RADIUS - 38
            nx = cx + num_r * cos_a
            ny = cy + num_r * sin_a
            c.create_text(
                nx, ny,
                text=str(hour),
                fill=NUMBER_COLOR,
                font=("Helvetica", 14, "bold"),
            )

        # Minute tick marks (skip positions already covered by hour marks)
        for minute in range(60):
            if minute % 5 == 0:
                continue
            angle = math.radians(minute * 6 - 90)
            inner = RADIUS - 10
            outer = RADIUS - 4
            x1 = cx + inner * math.cos(angle)
            y1 = cy + inner * math.sin(angle)
            x2 = cx + outer * math.cos(angle)
            y2 = cy + outer * math.sin(angle)
            c.create_line(x1, y1, x2, y2, fill="#888888", width=1)

    def _draw_hands(self, hours, minutes, seconds):
        c = self.canvas
        cx, cy = CENTER, CENTER

        for tag in ("hour_hand", "minute_hand", "second_hand", "center_dot"):
            c.delete(tag)

        # Hour hand  (shorter, thicker)
        hour_angle = (hours % 12) * 30 + minutes * 0.5 + seconds * (0.5 / 60)
        hx, hy = hand_coords(hour_angle, RADIUS * 0.5, cx, cy)
        c.create_line(
            cx, cy, hx, hy,
            fill=HOUR_HAND_COLOR, width=6, capstyle=tk.ROUND, tags="hour_hand",
        )

        # Minute hand (longer, medium thickness)
        minute_angle = minutes * 6 + seconds * 0.1
        mx, my = hand_coords(minute_angle, RADIUS * 0.75, cx, cy)
        c.create_line(
            cx, cy, mx, my,
            fill=MINUTE_HAND_COLOR, width=4, capstyle=tk.ROUND, tags="minute_hand",
        )

        # Second hand (longest, thin)
        second_angle = seconds * 6
        sx, sy = hand_coords(second_angle, RADIUS * 0.85, cx, cy)
        # Counterweight tail
        tail_x, tail_y = hand_coords(second_angle + 180, RADIUS * 0.15, cx, cy)
        c.create_line(
            tail_x, tail_y, sx, sy,
            fill=SECOND_HAND_COLOR, width=2, capstyle=tk.ROUND, tags="second_hand",
        )

        # Center dot
        dot_r = 7
        c.create_oval(
            cx - dot_r, cy - dot_r, cx + dot_r, cy + dot_r,
            fill=CENTER_DOT_COLOR, outline="white", width=1, tags="center_dot",
        )

    def _tick(self):
        now = time.localtime()
        self._draw_hands(now.tm_hour, now.tm_min, now.tm_sec)
        self.after(1000, self._tick)


if __name__ == "__main__":
    app = AnalogClock()
    app.mainloop()
