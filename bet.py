# bet.py - 带有诊断功能的完整版

import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque
from roulette import RouletteWheel

# ---------------------------------------------------
# 游戏引擎 (GameEngine Class)
# ---------------------------------------------------
class GameEngine:
    PAYOUT_RATIOS = { "Red": 1, "Black": 1, "Even": 1, "Odd": 1, "1-18": 1, "19-36": 1, "1-12": 2, "13-24": 2, "25-36": 2, "Col1": 2, "Col2": 2, "Col3": 2, "Number": 35 }
    def __init__(self):
        self.balance = 0.0
        self.bets = {}
        self.wheel = None
        self.history = deque(maxlen=10)
    def start_new_game(self, balance, is_american):
        self.balance = float(balance); self.wheel = RouletteWheel(american=is_american); self.history.clear(); self.bets.clear(); return True
    def place_bet(self, bet_type, amount, number=None):
        if amount > self.balance: return False, "余额不足以支付此注"
        bet_key = f"{bet_type}_{number}" if number is not None else bet_type
        self.balance -= amount; self.bets[bet_key] = self.bets.get(bet_key, 0) + amount; return True, ""
    def clear_bets(self):
        total_bet_amount = sum(self.bets.values()); self.balance += total_bet_amount; self.bets.clear(); return True

    # 【核心修正】恢复对“押数字”的专门判断
    def spin(self):
        print("\n" + "="*40)
        print("【诊断信息】开始新一轮旋转...")
        
        if not self.bets:
            print("【诊断信息】错误：没有检测到任何下注。")
            return None, "错误: 请先下注"

        total_bet_amount = sum(self.bets.values())
        print(f"【诊断信息】本轮总下注额: ${total_bet_amount:.2f}")
        print(f"【诊断信息】当前下注详情: {self.bets}")
        
        total_return = 0
        result_num = self.wheel.spin()
        result_description = self.wheel.describe(result_num)
        print(f"【诊断信息】轮盘开奖结果: {result_description}")

        for bet_key, amount in self.bets.items():
            parts = bet_key.split('_')
            bet_type = parts[0]
            win = False
            
            print(f"  - 正在检查下注 '{bet_key}'...")
            
            # --- START OF FIX ---
            # 恢复对“押数字”的特别判断
            if bet_type == "Number":
                target_num = parts[1]
                if result_num == target_num:
                    win = True
            # 其他类型的下注，则调用通用的check_bet
            else:
                if self.wheel.check_bet(bet_type, result_num):
                    win = True
            # --- END OF FIX ---

            if win:
                print(f"    - 结果: ✅ 赢了!")
                payout_ratio = self.PAYOUT_RATIOS.get(bet_type, 0)
                profit = amount * payout_ratio
                stake_return = amount
                total_return += (profit + stake_return)
                print(f"    - 赢得: ${profit:.2f}, 返还本金: ${stake_return:.2f}")
            else:
                print(f"    - 结果: ❌ 输了。")
        
        print(f"【诊断信息】本轮总返还金额: ${total_return:.2f}")
        self.balance += total_return
        
        net_profit = total_return - total_bet_amount
        print(f"【诊断信息】本轮净利润: ${net_profit:.2f}")
        print(f"【诊断信息】旋转后最终余额: ${self.balance:.2f}")
        print("="*40 + "\n")

        self.history.append(result_description)
        self.bets.clear()
        
        return result_description, net_profit

# ---------------------------------------------------
# 用户图形界面 (GUI Class)
# ---------------------------------------------------
class RouletteBettingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("💰 轮盘赌策略实验平台 (诊断版)")
        self.root.geometry("800x650")
        
        self.engine = GameEngine()
        self.bet_amount_var = tk.DoubleVar(value=10.0)
        self.setup_ui()
        
        self.root.after(100, self.ask_game_settings)

    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg="#0a4b2c")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        top_frame = tk.Frame(main_frame, bg="#0a4b2c")
        top_frame.pack(fill="x", pady=5)
        self.balance_label = tk.Label(top_frame, text="余额: $0.00", font=("Arial", 12), bg="#0a4b2c", fg="gold")
        self.balance_label.pack(side="left", padx=10)
        self.bets_label = tk.Label(top_frame, text="当前下注: 无", font=("Arial", 10), bg="#0a4b2c", fg="white", wraplength=400, justify="left")
        self.bets_label.pack(side="left", padx=20)

        self.mid_frame = tk.Frame(main_frame, bg="#0a4b2c")
        self.mid_frame.pack(fill="both", expand=True, pady=10)
        
        self.placeholder_label = tk.Label(self.mid_frame, text="--- 请通过“重置游戏”来开始 ---", font=("Arial", 16), bg="#0a4b2c", fg="white")
        self.placeholder_label.pack(expand=True)

        bottom_frame = tk.Frame(main_frame, bg="#0a4b2c")
        bottom_frame.pack(pady=10, fill="x")

        control_frame = tk.Frame(bottom_frame, bg="#0a4b2c")
        control_frame.pack(side="left", padx=10)
        
        ttk.Label(control_frame, text="单注金额:", background="#0a4b2c", foreground="white").pack(pady=2)
        ttk.Entry(control_frame, textvariable=self.bet_amount_var, width=10).pack(pady=2)
        self.spin_button = tk.Button(control_frame, text="▶️ 旋转", command=self.handle_spin, bg="gold", fg="black", font=("Arial", 12))
        self.spin_button.pack(pady=5)
        self.clear_button = tk.Button(control_frame, text="清除所有下注", command=self.handle_clear_bets)
        self.clear_button.pack(pady=5)
        ttk.Button(control_frame, text="🔄 重置游戏", command=self.ask_game_settings).pack(pady=5)

        history_frame = tk.Frame(bottom_frame, bg="#0a4b2c")
        history_frame.pack(side="left", expand=True, fill="x", padx=20)
        self.result_label = tk.Label(history_frame, text="--- 请下注后旋转 ---", font=("Arial", 14, "bold"), bg="#0a4b2c", fg="white")
        self.result_label.pack(pady=5)
        self.history_label = tk.Label(history_frame, text="历史: []", font=("Courier", 10), bg="#0a4b2c", fg="lightgray", wraplength=500, justify="left")
        self.history_label.pack(pady=5)

    def ask_game_settings(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("游戏设置")
        dialog.geometry("350x250")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="选择轮盘类型：").pack(pady=5)
        wheel_var = tk.StringVar(value="american")
        ttk.Radiobutton(dialog, text="美式轮盘 (0+00)", variable=wheel_var, value="american").pack()
        ttk.Radiobutton(dialog, text="欧式轮盘 (只有0)", variable=wheel_var, value="european").pack()

        ttk.Label(dialog, text="输入本金：").pack(pady=5)
        balance_entry = ttk.Entry(dialog)
        balance_entry.pack()

        def start_game_action():
            try:
                balance = float(balance_entry.get())
                if balance <= 0: raise ValueError
                is_american = wheel_var.get() == "american"
                
                self.engine.start_new_game(balance, is_american)
                self.update_displays()
                self.create_bet_buttons()
                dialog.destroy()
            except (ValueError, tk.TclError):
                messagebox.showerror("错误", "请输入有效的正数作为本金！", parent=dialog)

        ttk.Button(dialog, text="开始游戏", command=start_game_action).pack(pady=10)
        
        def on_closing():
            if self.engine.wheel is None:
                self.root.destroy()
            dialog.destroy()
        dialog.protocol("WM_DELETE_WINDOW", on_closing)

    def create_bet_buttons(self):
        if hasattr(self, 'placeholder_label'):
            self.placeholder_label.destroy()
            del self.placeholder_label

        for widget in self.mid_frame.winfo_children(): widget.destroy()
        
        bet_options_1_1 = [("红", "Red"), ("黑", "Black"), ("奇", "Odd"), ("偶", "Even"), ("1-18", "1-18"), ("19-36", "19-36")]
        bet_options_2_1_dozens = [("1-12", "1-12"), ("13-24", "13-24"), ("25-36", "25-36")]
        bet_options_2_1_cols = [("第1列", "Col1"), ("第2列", "Col2"), ("第3列", "Col3")]

        frame_1_1 = ttk.LabelFrame(self.mid_frame, text="1:1 赔率", labelanchor="n")
        frame_1_1.pack(side="left", padx=10, pady=5, fill="both", expand=True)
        
        frame_2_1 = ttk.LabelFrame(self.mid_frame, text="2:1 赔率", labelanchor="n")
        frame_2_1.pack(side="left", padx=10, pady=5, fill="both", expand=True)

        for text, bet_type in bet_options_1_1:
            btn = ttk.Button(frame_1_1, text=text, command=lambda b=bet_type: self.handle_place_bet(b))
            btn.pack(pady=3, padx=5, fill="x")

        for text, bet_type in bet_options_2_1_dozens:
            btn = ttk.Button(frame_2_1, text=text, command=lambda b=bet_type: self.handle_place_bet(b))
            btn.pack(pady=3, padx=5, fill="x")

        ttk.Separator(frame_2_1, orient='horizontal').pack(pady=5, fill='x')

        for text, bet_type in bet_options_2_1_cols:
            btn = ttk.Button(frame_2_1, text=text, command=lambda b=bet_type: self.handle_place_bet(b))
            btn.pack(pady=3, padx=5, fill="x")
        special_bets_frame = ttk.LabelFrame(self.mid_frame, text="特殊下注", labelanchor="n")
        special_bets_frame.pack(side="left", padx=10, pady=5, fill="both", expand=True)
        
        number_bet_btn = ttk.Button(special_bets_frame, text="押单个数字 (35:1)", command=self.open_number_pad)
        number_bet_btn.pack(pady=3, padx=5, fill="x")


    def handle_place_bet(self, bet_type, number=None):
        try:
            amount = self.bet_amount_var.get()
            if amount <= 0:
                messagebox.showerror("错误", "下注金额必须为正数")
                return
        except (ValueError, tk.TclError):
            messagebox.showerror("错误", "下注金额无效")
            return
        
        success, message = self.engine.place_bet(bet_type, amount, number)
        if not success:
            messagebox.showerror("下注失败", message)
        self.update_displays()

    def handle_clear_bets(self):
        self.engine.clear_bets()
        self.update_displays()

    def handle_spin(self):
        result_desc, net_profit = self.engine.spin()
        if result_desc is None:
            messagebox.showerror("错误", net_profit)
            return

        self.result_label.config(text=result_desc)
        if net_profit > 0:
            self.result_label.config(fg="lightgreen")
            messagebox.showinfo("恭喜", f"本轮您的净利润为 ${net_profit:.2f}!")
        else:
            self.result_label.config(fg="tomato")
            messagebox.showinfo("很遗憾", f"本轮您亏损了 ${abs(net_profit):.2f}。")
        
        self.root.after(1500, lambda: self.result_label.config(fg="white"))
        
        self.update_displays()
        if self.engine.balance <= 0:
            messagebox.showinfo("游戏结束", "您的本金已用完！")



    def open_number_pad(self):
        if not self.engine.wheel:
            messagebox.showerror("错误", "请先开始游戏")
            return

        pad = tk.Toplevel(self.root)
        pad.title("选择一个数字")
        pad.transient(self.root)
        pad.grab_set()
        # 设置一个背景色，避免透明
        pad.configure(bg="white")

        numbers_frame = tk.Frame(pad, padx=10, pady=10, bg="white")
        numbers_frame.pack()
        numbers = self.engine.wheel.numbers

        def get_btn_color(num_str):
            color = self.engine.wheel.get_color(num_str)
            if color == "红色": return "#c0392b"  # Red
            if color == "黑色": return "#2c3e50"  # Black
            return "#27ae60"  # Green

        def select_action(selected_number):
            self.handle_place_bet("Number", number=selected_number)
            pad.destroy()

        row, col = 0, 0
        for num in sorted(numbers, key=lambda x: int(x) if x.isdigit() else -1):
            btn_color = get_btn_color(num)
            
            # 使用 Label 代替 Button
            # relief="raised" 让它看起来有立体感，像个按钮
            label_btn = tk.Label(numbers_frame, text=num, 
                                 fg="white", bg=btn_color, 
                                 width=4, font=("Arial", 10, "bold"),
                                 relief="raised", borderwidth=2,
                                 padx=5, pady=5)
            
            # 绑定鼠标点击事件
            label_btn.bind("<Button-1>", lambda event, n=num: select_action(n))
            
            label_btn.grid(row=row, column=col, padx=2, pady=2)
            col += 1
            if col > 6:
                col = 0
                row += 1

    def update_displays(self):
        self.balance_label.config(text=f"余额: ${self.engine.balance:.2f}")
        
        if not self.engine.bets:
            self.bets_label.config(text="当前下注: 无")
        else:
            bet_texts = [f"{key.replace('_', ' ').replace('Col', '第')}列: ${amount:.2f}" for key, amount in self.engine.bets.items()]
            self.bets_label.config(text="当前下注: " + ", ".join(bet_texts))
            
        history_list = list(self.engine.history)
        self.history_label.config(text="历史: " + " « ".join(reversed(history_list)))
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    try:
        from tkinter import TclError
    except ImportError:
        pass
    root = tk.Tk()
    app = RouletteBettingGUI(root)
    app.run()