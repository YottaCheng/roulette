# bet_ui.py - v4.9 New Spin Button Design

import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque
from roulette import RouletteWheel
from bet import GameEngine 

class RouletteBettingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("💰 轮盘赌策略实验平台 (v4.9)")
        
        window_width = 850
        window_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        self.root.configure(bg="#0a4b2c")
        self.root.resizable(False, False)

        # --- Style Configuration ---
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(".", background="#0a4b2c", foreground="white", font=("Arial", 10))
        style.configure("TFrame", background="#0a4b2c")
        style.configure("TLabel", background="#0a4b2c", foreground="white")
        style.configure("TButton", font=("Arial", 10), padding=5)
        style.configure("TEntry", fieldbackground="white", foreground="black")
        style.configure("TLabelframe", background="#0f5a37", bordercolor="#1a744a")
        style.configure("TLabelframe.Label", background="#0f5a37", foreground="white", font=("Arial", 11, "bold"))
        style.configure("Red.TButton", background="#c0392b", foreground="white", font=("Arial", 10, "bold"))
        style.configure("Black.TButton", background="#34495e", foreground="white", font=("Arial", 10, "bold"))

        self.engine = GameEngine()
        self.bet_amount_var = tk.DoubleVar(value=10.0)
        self.setup_ui()
        
        self.root.after(100, self.ask_game_settings)

    def setup_ui(self):
        # --- Upper Main Content Area ---
        top_frame = ttk.Frame(self.root, padding=(10, 10))
        top_frame.pack(side="top", fill="both", expand=True)

        result_history_frame = ttk.Frame(top_frame)
        result_history_frame.pack(pady=(5,10), fill="x")
        self.result_label = ttk.Label(result_history_frame, text="--- 欢迎来到轮盘赌平台 ---", font=("Arial", 16, "bold"), anchor="center")
        self.result_label.pack()
        self.history_label = ttk.Label(result_history_frame, text="历史: []", font=("Courier", 11), wraplength=800, justify="center")
        self.history_label.pack(pady=5)
        self.bets_label = ttk.Label(result_history_frame, text="当前下注: 无", font=("Arial", 10), wraplength=800, justify="center")
        self.bets_label.pack(pady=5)

        betting_area = ttk.Frame(top_frame)
        betting_area.pack(fill="both", expand=True, pady=5)
        betting_area.grid_columnconfigure(0, weight=1)
        betting_area.grid_columnconfigure(1, weight=1)
        betting_area.grid_columnconfigure(2, weight=1)
        betting_area.grid_rowconfigure(0, weight=1)

        bets = {
            "1:1 赔率": [("1-18", "1-18"), ("奇", "Odd"), ("红", "Red", "Red.TButton"), ("黑", "Black", "Black.TButton"), ("偶", "Even"), ("19-36", "19-36")],
            "2:1 赔率": [("1-12", "1-12"), ("13-24", "13-24"), ("25-36", "25-36"), ("第1列", "Col1"), ("第2列", "Col2"), ("第3列", "Col3")]
        }
        frame_1_1 = ttk.LabelFrame(betting_area, text=list(bets.keys())[0], padding=10)
        frame_1_1.grid(row=0, column=0, sticky="nsew", padx=5)
        frame_2_1 = ttk.LabelFrame(betting_area, text=list(bets.keys())[1], padding=10)
        frame_2_1.grid(row=0, column=1, sticky="nsew", padx=5)
        special_bets_frame = ttk.LabelFrame(betting_area, text="特殊下注", padding=10)
        special_bets_frame.grid(row=0, column=2, sticky="nsew", padx=5)

        for btn_data in bets["1:1 赔率"]:
            text, bet_type, style = (btn_data[0], btn_data[1], btn_data[2]) if len(btn_data) > 2 else (btn_data[0], btn_data[1], "TButton")
            btn = ttk.Button(frame_1_1, text=text, command=lambda b=bet_type: self.handle_place_bet(b), style=style)
            btn.pack(fill="x", pady=2, expand=True)
        for btn_data in bets["2:1 赔率"]:
            text, bet_type = btn_data[0], btn_data[1]
            btn = ttk.Button(frame_2_1, text=text, command=lambda b=bet_type: self.handle_place_bet(b))
            btn.pack(fill="x", pady=2, expand=True)
        number_bet_btn = ttk.Button(special_bets_frame, text="押单个数字 (35:1)", command=self.open_number_pad)
        number_bet_btn.pack(fill="both", expand=True)

        # --- Bottom Control Bar ---
        bottom_bar = tk.Frame(self.root, bg="#0f5a37", padx=10, pady=10)
        bottom_bar.pack(side="bottom", fill="x")
        bottom_bar.grid_columnconfigure(0, weight=1)
        bottom_bar.grid_columnconfigure(1, weight=1)
        bottom_bar.grid_columnconfigure(2, weight=1)
        bottom_bar.grid_columnconfigure(3, weight=1)
        bottom_bar.grid_columnconfigure(4, weight=1)

        balance_frame = tk.Frame(bottom_bar, bg="#0f5a37")
        balance_frame.grid(row=0, column=0, sticky="w")
        tk.Label(balance_frame, text="余额:", font=("Arial", 10), bg="#0f5a37", fg="white").pack(anchor="w")
        self.balance_label = tk.Label(balance_frame, text="$0.00", font=("Arial", 14, "bold"), bg="#0f5a37", fg="#f1c40f")
        self.balance_label.pack(anchor="w")

        bet_amount_frame = tk.Frame(bottom_bar, bg="#0f5a37")
        bet_amount_frame.grid(row=0, column=1, padx=20)
        tk.Label(bet_amount_frame, text="单注金额:", bg="#0f5a37", fg="white").pack(anchor="w")
        ttk.Entry(bet_amount_frame, textvariable=self.bet_amount_var, width=10, font=("Arial", 12)).pack(anchor="w")
        
        # --- NEW SPIN BUTTON ---
        self.spin_button = tk.Button(bottom_bar, text="🔄", 
                                     font=("Arial", 20), 
                                     fg="red", 
                                     bg="black",
                                     relief="raised",
                                     borderwidth=3,
                                     width=4,
                                     command=self.handle_spin)
        self.spin_button.grid(row=0, column=2, sticky="ew", padx=20, ipady=5)
        # --- END OF NEW SPIN BUTTON ---

        clear_frame = tk.Frame(bottom_bar, bg="#0f5a37")
        clear_frame.grid(row=0, column=3, padx=10)
        self.clear_button = ttk.Button(clear_frame, text="清除所有下注", command=self.handle_clear_bets, width=15)
        self.clear_button.pack()

        reset_frame = tk.Frame(bottom_bar, bg="#0f5a37")
        reset_frame.grid(row=0, column=4, padx=10)
        self.reset_button = ttk.Button(reset_frame, text="🔄 重置游戏", command=self.ask_game_settings, width=15)
        self.reset_button.pack()

    # (All methods below are unchanged from the last complete version)
    def ask_game_settings(self):
        dialog = tk.Toplevel(self.root); dialog.title("游戏设置"); dialog.geometry("350x250"); dialog.transient(self.root); dialog.grab_set()
        window_width = 350; window_height = 250
        center_x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (window_width // 2)
        center_y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (window_height // 2)
        dialog.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        ttk.Label(dialog, text="选择轮盘类型：").pack(pady=5)
        wheel_var = tk.StringVar(value="american")
        ttk.Radiobutton(dialog, text="美式轮盘 (0+00)", variable=wheel_var, value="american").pack()
        ttk.Radiobutton(dialog, text="欧式轮盘 (只有0)", variable=wheel_var, value="european").pack()
        ttk.Label(dialog, text="输入本金：").pack(pady=5)
        balance_entry = ttk.Entry(dialog); balance_entry.pack()
        def start_game_action():
            try:
                balance = float(balance_entry.get());
                if balance <= 0: raise ValueError
                is_american = wheel_var.get() == "american"
                self.engine.start_new_game(balance, is_american)
                self.update_displays()
                dialog.destroy()
            except (ValueError, tk.TclError): messagebox.showerror("错误", "请输入有效的正数作为本金！", parent=dialog)
        ttk.Button(dialog, text="开始游戏", command=start_game_action).pack(pady=10)
        def on_closing():
            if self.engine.wheel is None: self.root.destroy()
            dialog.destroy()
        dialog.protocol("WM_DELETE_WINDOW", on_closing)

    def open_number_pad(self):
        if not self.engine.wheel: messagebox.showerror("错误", "请先开始游戏"); return
        pad = tk.Toplevel(self.root); pad.title("选择一个数字"); pad.transient(self.root); pad.grab_set(); pad.configure(bg="white")
        window_width = 280; window_height = 250
        center_x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (window_width // 2)
        center_y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (window_height // 2)
        pad.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        numbers_frame = tk.Frame(pad, padx=10, pady=10, bg="white"); numbers_frame.pack()
        numbers = self.engine.wheel.numbers
        def get_btn_color(num_str):
            color = self.engine.wheel.get_color(num_str)
            if color == "红色": return "#c0392b"
            if color == "黑色": return "#2c3e50"
            return "#27ae60"
        def select_action(selected_number): self.handle_place_bet("Number", number=selected_number); pad.destroy()
        row, col = 0, 0
        for num in sorted(numbers, key=lambda x: int(x) if x.isdigit() else -1):
            btn_color = get_btn_color(num)
            label_btn = tk.Label(numbers_frame, text=num, fg="white", bg=btn_color, width=4, font=("Arial", 10, "bold"), relief="raised", borderwidth=2, padx=5, pady=5)
            label_btn.bind("<Button-1>", lambda event, n=num: select_action(n))
            label_btn.grid(row=row, column=col, padx=2, pady=2); col += 1
            if col > 6: col = 0; row += 1

    def handle_place_bet(self, bet_type, number=None):
        try:
            amount = self.bet_amount_var.get()
            if amount <= 0: messagebox.showerror("错误", "下注金额必须为正数"); return
        except (ValueError, tk.TclError): messagebox.showerror("错误", "下注金额无效"); return
        success, message = self.engine.place_bet(bet_type, amount, number)
        if not success: messagebox.showerror("下注失败", message)
        self.update_displays()

    def handle_clear_bets(self):
        self.engine.clear_bets(); self.update_displays()

    def handle_spin(self):
        result_desc, net_profit = self.engine.spin()
        if result_desc is None: messagebox.showerror("错误", net_profit); return
        self.result_label.config(text=result_desc)
        if net_profit > 0:
            self.result_label.config(foreground="#2ecc71"); messagebox.showinfo("恭喜", f"本轮您的净利润为 ${net_profit:.2f}!")
        elif net_profit < 0:
            self.result_label.config(foreground="#e74c3c"); messagebox.showinfo("很遗憾", f"本轮您亏损了 ${abs(net_profit):.2f}。")
        else:
            self.result_label.config(foreground="white"); messagebox.showinfo("平局", "本轮没有盈亏。")
        self.root.after(2000, lambda: self.result_label.config(foreground="white"))
        self.update_displays()
        if self.engine.balance <= 0: messagebox.showinfo("游戏结束", "您的本金已用完！")

    def update_displays(self):
        self.balance_label.config(text=f"${self.engine.balance:.2f}")
        if not self.engine.bets:
            self.bets_label.config(text="当前下注: 无")
        else:
            bet_texts = [f"{key.replace('_', ' ')}: ${amount:.2f}" for key, amount in self.engine.bets.items()]
            self.bets_label.config(text="当前下注: " + ", ".join(bet_texts))
        history_list = list(self.engine.history)
        self.history_label.config(text="历史: " + " « ".join(reversed(history_list)))
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    try: from tkinter import TclError
    except ImportError: pass
    root = tk.Tk()
    app = RouletteBettingGUI(root)
    app.run()