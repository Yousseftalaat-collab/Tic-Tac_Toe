import tkinter as tk
from PIL import Image, ImageTk
import random

window = tk.Tk()
window.title("Tic_Tac_Toe Almadrsa")
window.geometry("400x550")
window.resizable(True,True)

window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=1)

score_frame = tk.Frame(window)
score_frame.grid(row=0, column=1, pady=20)

you_label = tk.Label(score_frame, text="You:   ", font=("Arial",14))
you_label.grid(row=0, column=0, padx=20)

computer_label = tk.Label(score_frame, text="computer:   ", font=("Arial",14))
computer_label.grid(row=0, column=1, padx=20)

result_label = tk.Label(window, text="", font=("Arial", 16))

def update_result(winner):
    global player_score, computer_score

    if winner == player_symbol:
        player_score += 1
        result_label.config(text="You win!", fg="blue", font=("Arial", 20))
    elif winner == computer_symbol:
        computer_score += 1
        result_label.config(text="Computer wins!", fg="blue", font=("Arial", 20))
    elif winner == "tie":
        result_label.config(text="No Winner!", fg="red", font=("Arial", 20))

    you_label.config(text=f"You: {player_score}")
    computer_label.config(text=f"Computer: {computer_score}")

    if not result_label.winfo_ismapped():
        result_label.grid(row=1, column=0, columnspan=3, pady=10)

    color = "blue" if winner in [player_symbol, computer_symbol] else "red"
    for row in cells:
        for btn in row:
            btn.config(bg=color)

    window.after(2000, reset_board_only)


def reset_board_only():
    global current_turn
    current_turn = "player"
    for row in cells:
        for btn in row:
            btn.config(image=empty_photo, state="normal",bg="white")
            btn.image = empty_photo
            btn.symbol = None
    result_label.config(text="")


def restart_game():
    global current_turn, player_score, computer_score, cells, player_symbol, computer_symbol

    player_score = 0
    computer_score = 0
    you_label.config(text="You: 0")
    computer_label.config(text="Computer: 0")

    result_label.config(text="")

    for row in cells:
        for btn in row:
            btn.destroy()  
    cells = []  
    player_symbol = None
    computer_symbol = None
    current_turn = None

    choose_frame.grid(row=3, column=0, columnspan=3, pady=10)


Restart_button = tk.Button(window, text="Restart", font=("Arial", 14), padx=20, pady=5, command=restart_game)
Restart_button.grid(row=2, column=0, columnspan=3, pady=20)

x_image = Image.open("x.png").resize((80, 80), Image.Resampling.LANCZOS)
o_image = Image.open("o.png").resize((80, 80), Image.Resampling.LANCZOS)
empty_image = Image.new("RGBA", (80, 80), (255, 255, 255, 0))

x_photo = ImageTk.PhotoImage(x_image)
o_photo = ImageTk.PhotoImage(o_image)
empty_photo = ImageTk.PhotoImage(empty_image)

player_score = 0
computer_score = 0

player_symbol = None
computer_symbol = None
current_turn = None
cells = []

board_frame = tk.Frame(window)
board_frame.grid(row=4, column=0, columnspan=3)


def check_winner():
    for i in range(3):
        if cells[i][0].symbol == cells[i][1].symbol == cells[i][2].symbol and cells[i][0].symbol:
            return cells[i][0].symbol
        if cells[0][i].symbol == cells[1][i].symbol == cells[2][i].symbol and cells[0][i].symbol:
            return cells[0][i].symbol
    if cells[0][0].symbol == cells[1][1].symbol == cells[2][2].symbol and cells[0][0].symbol:
        return cells[0][0].symbol
    if cells[0][2].symbol == cells[1][1].symbol == cells[2][0].symbol and cells[0][2].symbol:
        return cells[0][2].symbol

    if all(c.symbol for row in cells for c in row):
        return "tie"
    return None


def handle_click(row, col):
    global current_turn
    button = cells[row][col]
    if button.symbol is None and current_turn == "player":
        button.symbol = player_symbol
        button.config(image=x_photo if player_symbol == "x" else o_photo)
        current_turn = "computer"
        winner = check_winner()
        if winner:
            update_result(winner)
        else:
            window.after(500, computer_move)


def computer_move():
    global current_turn
    empty_cells = [(r, c) for r in range(3) for c in range(3) if cells[r][c].symbol is None]
    if empty_cells:
        row, col = random.choice(empty_cells)
        btn = cells[row][col]
        btn.symbol = computer_symbol
        btn.config(image=x_photo if computer_symbol == "x" else o_photo)
        current_turn = "player"
        winner = check_winner()
        if winner:
            update_result(winner)


def build_board():
    for row in range(3):
        row_buttons = []
        for col in range(3):
            btn = tk.Button(board_frame, image=empty_photo, relief="ridge")
            btn.grid(row=row, column=col, padx=5, pady=5)
            btn.config(command=lambda r=row, c=col: handle_click(r, c))
            btn.symbol = None
            btn.image = empty_photo
            row_buttons.append(btn)
        cells.append(row_buttons)


def start_game(symbol):
    global player_symbol, computer_symbol, current_turn
    player_symbol = symbol
    computer_symbol = "o" if symbol == "x" else "x"
    current_turn = "player"
    choose_frame.grid_forget()  
    build_board()


choose_frame = tk.Frame(window)
choose_frame.grid(row=3, column=0, columnspan=3, pady=10)

choose_label = tk.Label(choose_frame, text="Choose your symbol:", font=("Arial", 14))
choose_label.pack(pady=5)

symbols_frame = tk.Frame(choose_frame)
symbols_frame.pack()

x_button = tk.Button(symbols_frame, text="X", font=("Arial", 14), width=6, command=lambda: start_game("x"))
x_button.pack(side="left", padx=10)

o_button = tk.Button(symbols_frame, text="O", font=("Arial", 14), width=6, command=lambda: start_game("o"))
o_button.pack(side="left", padx=10)

 
window.mainloop()