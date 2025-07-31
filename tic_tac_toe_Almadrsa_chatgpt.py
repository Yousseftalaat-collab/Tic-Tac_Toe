import tkinter as tk
import random
import glob

# --- Setup Window ---
root = tk.Tk()
root.title("Tic Tac Toe")
root.geometry("400x550")
root.resizable(False, False)

# --- Game State ---
player_symbol = None
computer_symbol = None
board = [""] * 9
player_score = 0
computer_score = 0
game_over = False

# --- GUI Elements ---
buttons = []
status_label = tk.Label(root, text="Choose X or O to Start", font=("Arial", 14))
score_label = tk.Label(root, text="You: 0    Computer: 0", font=("Arial", 14))
symbol_frame = tk.Frame(root)

def select_symbol(symbol):
    global player_symbol, computer_symbol
    player_symbol = symbol
    computer_symbol = "O" if symbol == "X" else "X"
    status_label.config(text=f"You are {player_symbol}", fg="black")
    for child in symbol_frame.winfo_children():
        child.config(state="disabled")
    reset_board()

# --- Reset Board (continue game, keep score) ---
def reset_board():
    global board, game_over
    board = [""] * 9
    game_over = False
    for btn in buttons:
        btn.config(text="", state="normal", bg="white")
    status_label.config(text=f"You are {player_symbol}", fg="black")

# --- Restart Game (reset score and board) ---
def restart_game():
    global player_score, computer_score, player_symbol, computer_symbol
    player_score = 0
    computer_score = 0
    update_score()
    player_symbol = None
    computer_symbol = None
    status_label.config(text="Choose X or O to Start", fg="black")
    for child in symbol_frame.winfo_children():
        child.config(state="normal")
    for btn in buttons:
        btn.config(text="", state="normal", bg="white")
    disable_all_buttons()

# --- Update Score ---
def update_score():
    score_label.config(text=f"You: {player_score}    Computer: {computer_score}")

# --- Check Winner ---
def check_winner():
    global player_score, computer_score, game_over
    win_combos = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]

    for combo in win_combos:
        line = [board[i] for i in combo]
        if line[0] != "" and all(cell == line[0] for cell in line):
            for btn in buttons:
                btn.config(bg="lightblue")  # 🟦 Full board blue if win
            if line[0] == player_symbol:
                player_score += 1
                status_label.config(text="You Win!", fg="blue")
            else:
                computer_score += 1
                status_label.config(text="Computer Wins!", fg="blue")
            update_score()
            game_over = True
            root.after(1000, reset_board)
            return

    if "" not in board:
        status_label.config(text="No Winner", fg="red")
        for btn in buttons:
            btn.config(bg="lightcoral")  # 🟥 Full board red if tie
        game_over = True
        root.after(1000, reset_board)

# --- Disable Buttons ---
def disable_all_buttons():
    for btn in buttons:
        btn.config(state="disabled")

# --- Computer Move ---
def computer_move():
    if game_over:
        return
    empty = [i for i, val in enumerate(board) if val == ""]
    if not empty:
        return
    move = random.choice(empty)
    board[move] = computer_symbol
    buttons[move].config(text=computer_symbol, state="disabled")
    check_winner()

# --- Player Move ---
def button_click(i):
    if game_over or player_symbol is None:
        return
    if board[i] == "":
        board[i] = player_symbol
        buttons[i].config(text=player_symbol, state="disabled")
        check_winner()
        if not game_over:
            root.after(500, computer_move)

# --- Check for x.png using glob ---
if not glob.glob("x.png"):
    print("x.png not found, using text symbols.")

# --- GUI Layout ---
symbol_frame.pack(pady=10)
tk.Button(symbol_frame, text="Play as X", font=("Arial", 12), width=10, command=lambda: select_symbol("X")).pack(side="left", padx=10)
tk.Button(symbol_frame, text="Play as O", font=("Arial", 12), width=10, command=lambda: select_symbol("O")).pack(side="left", padx=10)

status_label.pack(pady=10)
score_label.pack(pady=5)

frame = tk.Frame(root)
frame.pack(pady=10)

for i in range(9):
    btn = tk.Button(frame, text="", font=("Arial", 20), width=5, height=2,
                    command=lambda i=i: button_click(i))
    btn.grid(row=i//3, column=i%3)
    buttons.append(btn)

tk.Button(root, text="Restart Game", font=("Arial", 12), command=restart_game).pack(pady=20)

# Start with disabled board until symbol selected
disable_all_buttons()

root.mainloop()
