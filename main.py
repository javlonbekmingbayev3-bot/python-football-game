import tkinter as tk
from tkinter import messagebox

class FootballGame:
    # --- PHYSICAL BOUNDARIES (Class Constants) ---
    X_MIN, X_MAX = 20, 980
    Y_MIN, Y_MAX = 20, 700

    def __init__(self, window):
        """Initializes the game window, state, and visual assets."""
        self.window = window
        self.window.geometry("1000x1000")
        self.window.title("Python Canvas Football")

        # --- GAME STATE (Instance Variables) ---
        self.score = 0
        self.time_left = 60
        self.game_active = True
        self.goalie_direction = 1
        self.goalie_speed = 8

        # --- SETUP COMPONENTS ---
        self.setup_canvas()
        self.draw_scenery()
        self.setup_ball()
        self.bind_controls()

        # --- START GAME LOOPS ---
        self.update_timer()
        self.animate_goalkeeper()

    def setup_canvas(self):
        """Creates and packs the main game canvas."""
        self.canvas = tk.Canvas(master=self.window, height=1000, width=1000, bg="green")
        self.canvas.pack(fill="both")
        self.canvas.propagate(False)

    def draw_scenery(self):
        """Draws static field elements, text labels, and the goalkeeper."""
        # Border line
        self.canvas.create_line(0, 700, 1000, 700, fill="lightgrey", width=5)

        # Dynamic Displays (saved as properties to update later)
        self.score_text_item = self.canvas.create_text(900, 50, text="Score: 0", font="Arial 15 bold", fill="white")
        self.timer_text_item = self.canvas.create_text(100, 50, text="Time: 60s", font="Arial 15 bold", fill="white")

        # Goal and Goal Area text
        points_gate = [333, 600, 666, 700]
        self.gates = self.canvas.create_rectangle(points_gate, outline="white", width=4, dash=(20, 10))
        self.canvas.create_text(499, 650, text="Goal Area!", font="Arial 20 bold", fill="white")
        self.canvas.create_text(499, 770, text="Move to the goal!", font="Arial 30 bold italic", fill="white")

        # Goalkeeper
        self.goalie_item = self.canvas.create_rectangle(450, 610, 550, 630, fill="red", outline="yellow", width=2)

    def setup_ball(self):
        """Loads the image asset and initializes the ball placement."""
        self.ball_image = tk.PhotoImage(file="ball_f.png")
        self.ball_image_small = self.ball_image.subsample(4, 4)
        
        self.ball_item = self.canvas.create_image(500, 60, image=self.ball_image_small, anchor="center")
        self.canvas.image = self.ball_image_small  # Keeps garbage collection from wiping the image

    def bind_controls(self):
        """Binds directional arrow keys to movement methods."""
        self.canvas.bind("<Up>", self.move_up)
        self.canvas.bind("<Down>", self.move_down)
        self.canvas.bind("<Left>", self.move_left)
        self.canvas.bind("<Right>", self.move_right)
        self.canvas.focus_set()

    # --- GAME MECHANICS & LOOPS ---

    def reset_ball(self):
        """Resets the ball to the starting kickoff position."""
        self.canvas.coords(self.ball_item, 500, 60)

    def update_timer(self):
        """Background countdown clock loop."""
        if self.time_left > 0:
            self.time_left -= 1
            self.canvas.itemconfig(self.timer_text_item, text=f"Time: {self.time_left}s")
            self.window.after(1000, self.update_timer)
        else:
            self.game_active = False
            messagebox.showinfo(title="Game Over!", message=f"Time's up! ⏱️\nFinal Score: {self.score} goals.")

    def animate_goalkeeper(self):
        """Background frame animation loop for the moving opponent."""
        if not self.game_active:
            return

        x1, y1, x2, y2 = self.canvas.coords(self.goalie_item)

        if x2 >= 666:
            self.goalie_direction = -1
        elif x1 <= 333:
            self.goalie_direction = 1

        self.canvas.move(self.goalie_item, self.goalie_speed * self.goalie_direction, 0)
        self.window.after(20, self.animate_goalkeeper)

    def is_goalie_collision(self, ball_x, ball_y):
        """Collision helper detecting overlapping bounding boxes."""
        gx1, gy1, gx2, gy2 = self.canvas.coords(self.goalie_item)
        return gx1 <= ball_x <= gx2 and gy1 <= ball_y <= gy2

    # --- INPUT ACTIONS ---

    def move_up(self, event):
        if not self.game_active: return
        x, y = self.canvas.coords(self.ball_item)
        if y - 10 >= self.X_MIN:
            self.canvas.move(self.ball_item, 0, -10)

    def move_down(self, event):
        if not self.game_active: return
        x, y = self.canvas.coords(self.ball_item)
        
        if self.is_goalie_collision(x, y):
            self.canvas.move(self.ball_item, 0, -40)
            return

        if y >= 600 and 333 < x < 666:
            self.score += 1
            self.canvas.itemconfig(self.score_text_item, text=f"Score: {self.score}")
            messagebox.showinfo(title="Goal!", message=f"GOAL! 🎉\nYour score is now: {self.score}")
            self.reset_ball()
        elif y + 10 <= self.Y_MAX:
            self.canvas.move(self.ball_item, 0, 10)

    def move_left(self, event):
        if not self.game_active: return
        x, y = self.canvas.coords(self.ball_item)
        if self.is_goalie_collision(x - 10, y): return
        if x - 10 >= self.X_MIN:
            self.canvas.move(self.ball_item, -10, 0)

    def move_right(self, event):
        if not self.game_active: return
        x, y = self.canvas.coords(self.ball_item)
        if self.is_goalie_collision(x + 10, y): return
        if x + 10 <= self.X_MAX:
            self.canvas.move(self.ball_item, 10, 0)


# --- APPLICATION ENTRY POINT ---
if __name__ == "__main__":
    root = tk.Tk()
    game = FootballGame(root)
    root.mainloop()
