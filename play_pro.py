# play_pro.py —— 修正版：0 单独左列，红/黑/绿颜色正确显示

import tkinter as tk
from tkinter import ttk
from roulette import RouletteWheel

class RouletteProGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎲 轮盘赌模拟器 - Pro版")
        self.root.geometry("720x600")
        self.root.resizable(False, False)

        # 初始化轮盘
        self.wheel = None
        self.results = []
        self.red_count = 0
        self.black_count = 0
        self.total_spins = 0

        # 创建UI
        self.setup_ui()
        self.ask_wheel_type()

    def ask_wheel_type(self):
        """弹窗选择轮盘类型"""
        dialog = tk.Toplevel(self.root)
        dialog.title("选择轮盘类型")
        dialog.geometry("300x150")
        dialog.transient(self.root)
        dialog.grab_set()

        def set_american():
            self.wheel = RouletteWheel(american=True)
            dialog.destroy()
            self.update_stats()

        def set_european():
            self.wheel = RouletteWheel(american=False)
            dialog.destroy()
            self.update_stats()

        ttk.Label(dialog, text="请选择轮盘类型：", font=("Arial", 12)).pack(pady=10)
        ttk.Button(dialog, text="美式轮盘 (0 + 00)", command=set_american).pack(pady=5)
        ttk.Button(dialog, text="欧式轮盘 (只有 0)", command=set_european).pack(pady=5)

    def setup_ui(self):
        # 主容器（绿色桌面）
        main_frame = tk.Frame(self.root, bg="#0a4b2c")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # 顶部信息栏
        top_frame = tk.Frame(main_frame, bg="#0a4b2c")
        top_frame.pack(fill="x", pady=5)

        self.round_label = tk.Label(top_frame, text="轮次: 0", font=("Arial", 10), bg="#0a4b2c", fg="white")
        self.round_label.pack(side="left", padx=10)

        self.stats_label = tk.Label(top_frame, text="红:0 (0.0%) / 黑:0 (0.0%)", font=("Arial", 10), bg="#0a4b2c", fg="white")
        self.stats_label.pack(side="left", padx=20)

        # 中间下注区（分两部分：左侧0，右侧1-36）
        board_frame = tk.Frame(main_frame, bg="#0a4b2c")
        board_frame.pack(fill="both", expand=True, pady=10)

        # --- 左侧：0 和 00 ---
        left_frame = tk.Frame(board_frame, bg="#0a4b2c")
        left_frame.pack(side="left", padx=5)

        # 0 按钮
        self.btn_0 = tk.Button(left_frame, text="0", width=4, height=8, font=("Arial", 10, "bold"),
                               bg="green", fg="white", relief="raised", bd=2)
        self.btn_0.pack(pady=2)

        # 00 按钮（初始隐藏，美式轮盘时显示）
        self.btn_00 = tk.Button(left_frame, text="00", width=4, height=8, font=("Arial", 10, "bold"),
                                bg="green", fg="white", relief="raised", bd=2)
        self.btn_00.pack(pady=2)
        self.btn_00.pack_forget()  # 默认隐藏

        # --- 右侧：1-36 数字网格 ---
        right_frame = tk.Frame(board_frame, bg="#0a4b2c")
        right_frame.pack(side="left", fill="both", expand=True)

        # 创建 3 行 x 12 列的按钮网格（1-36）
        self.buttons = {}
        for i in range(1, 37):
            row = (i - 1) % 3      # 0,1,2 → 3行
            col = (i - 1) // 3     # 0-11 → 12列
            color = self.get_number_color(i)
            btn = tk.Button(right_frame, text=str(i), width=4, height=2, font=("Arial", 9, "bold"),
                            bg=color, fg="white", relief="raised", bd=2)
            btn.grid(row=row, column=col, padx=1, pady=1)
            self.buttons[i] = btn

        # 控制区
        control_frame = tk.Frame(main_frame, bg="#0a4b2c")
        control_frame.pack(pady=10)

        self.spin_button = tk.Button(control_frame, text="▶️ 开始", command=self.spin_once,
                                     bg="gold", fg="black", font=("Arial", 11, "bold"), width=10)
        self.spin_button.pack(side="left", padx=10)

        self.result_label = tk.Label(control_frame, text="--- 点击开始 ---", font=("Arial", 11),
                                     bg="#0a4b2c", fg="white", width=30)
        self.result_label.pack(side="left", padx=10)

        reset_btn = tk.Button(control_frame, text="🔄 重置", command=self.reset,
                              bg="red", fg="white", font=("Arial", 11, "bold"), width=8)
        reset_btn.pack(side="left", padx=10)

    def get_number_color(self, num):
        """获取1-36数字的颜色"""
        red_numbers = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
        return "red" if num in red_numbers else "black"

    def spin_once(self):
        if not self.wheel:
            return

        result = self.wheel.spin()
        description = self.wheel.describe(result)

        # 更新统计
        color = self.wheel.get_color(result)
        if color == "红色":
            self.red_count += 1
        elif color == "黑色":
            self.black_count += 1

        self.total_spins += 1
        self.results.append(description)

        # 更新界面
        self.result_label.config(text=f"结果: {description}")
        self.update_stats()

        # 高亮中奖数字
        if result == '0':
            self.highlight_button(self.btn_0)
        elif result == '00':
            self.highlight_button(self.btn_00)
        elif result.isdigit():
            num = int(result)
            if 1 <= num <= 36:
                self.highlight_button(self.buttons[num])

    def highlight_button(self, btn):
        """高亮按钮（凹陷1秒）"""
        btn.config(relief="sunken", bd=4)
        self.root.after(1000, lambda: btn.config(relief="raised", bd=2))

    def update_stats(self):
        red_pct = (self.red_count / self.total_spins * 100) if self.total_spins > 0 else 0
        black_pct = (self.black_count / self.total_spins * 100) if self.total_spins > 0 else 0
        self.round_label.config(text=f"轮次: {self.total_spins}")
        self.stats_label.config(text=f"红:{self.red_count} ({red_pct:.1f}%) / 黑:{self.black_count} ({black_pct:.1f}%)")

    def reset(self):
        self.results = []
        self.red_count = 0
        self.black_count = 0
        self.total_spins = 0
        self.result_label.config(text="--- 点击开始 ---")
        self.update_stats()
        # 重置所有按钮状态
        self.btn_0.config(relief="raised", bd=2)
        self.btn_00.config(relief="raised", bd=2)
        for btn in self.buttons.values():
            btn.config(relief="raised", bd=2)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = RouletteProGUI(root)
    app.run()