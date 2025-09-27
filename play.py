# play_ui.py

import tkinter as tk
from tkinter import ttk, messagebox
from roulette import RouletteWheel

def spin(american=True):
    """返回一次轮盘结果，如 '11 (黑色, 第2列)'"""
    wheel = RouletteWheel(american=american)
    result = wheel.spin()
    description = wheel.describe(result)
    return description

class RouletteGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎲 轮盘赌模拟器 - GUI版")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        # 初始化轮盘（默认美式）
        self.wheel = None
        self.results = []
        self.red_count = 0
        self.black_count = 0
        self.total_spins = 0

        self.setup_ui()
        self.ask_wheel_type()

    def ask_wheel_type(self):
        """弹窗让用户选择轮盘类型"""
        dialog = tk.Toplevel(self.root)
        dialog.title("选择轮盘类型")
        dialog.geometry("300x150")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="请选择轮盘类型：", font=("Arial", 12)).pack(pady=10)

        def set_american():
            self.wheel = RouletteWheel(american=True)
            dialog.destroy()
            self.update_status()

        def set_european():
            self.wheel = RouletteWheel(american=False)
            dialog.destroy()
            self.update_status()

        ttk.Button(dialog, text="美式轮盘 (0 + 00)", command=set_american).pack(pady=5)
        ttk.Button(dialog, text="欧式轮盘 (只有 0)", command=set_european).pack(pady=5)

    def setup_ui(self):
        # 顶部状态栏
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.pack(fill="x", padx=10, pady=5)

        self.round_label = ttk.Label(self.status_frame, text="当前轮次: 0", font=("Arial", 10))
        self.round_label.pack(side="left")

        self.red_label = ttk.Label(self.status_frame, text="红色: 0 (0.0%)", font=("Arial", 10))
        self.red_label.pack(side="left", padx=20)

        self.black_label = ttk.Label(self.status_frame, text="黑色: 0 (0.0%)", font=("Arial", 10))
        self.black_label.pack(side="left")

        # 中间结果显示区
        result_frame = ttk.LabelFrame(self.root, text="🎰 当前结果", padding=10)
        result_frame.pack(fill="x", padx=10, pady=10)

        self.result_label = ttk.Label(result_frame, text="--- 点击“下一局”开始 ---", font=("Arial", 16, "bold"))
        self.result_label.pack(pady=10)

        # 历史记录区
        history_frame = ttk.LabelFrame(self.root, text="📜 历史记录 (最近10局)", padding=10)
        history_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.history_text = tk.Text(history_frame, height=10, font=("Courier", 10), state="disabled")
        self.history_text.pack(fill="both", expand=True, side="left")

        scrollbar = ttk.Scrollbar(history_frame, command=self.history_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.history_text.config(yscrollcommand=scrollbar.set)

        # 底部按钮
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        self.spin_button = ttk.Button(button_frame, text="🔄 下一局", command=self.spin_once, state="disabled")
        self.spin_button.pack(side="left", padx=5)

        self.reset_button = ttk.Button(button_frame, text="🔁 重置", command=self.reset)
        self.reset_button.pack(side="left", padx=5)

        ttk.Button(button_frame, text="❌ 退出", command=self.root.quit).pack(side="left", padx=5)

    def update_status(self):
        if not self.wheel:
            return
        total = self.total_spins
        red_pct = (self.red_count / total * 100) if total > 0 else 0
        black_pct = (self.black_count / total * 100) if total > 0 else 0

        self.round_label.config(text=f"当前轮次: {total}")
        self.red_label.config(text=f"红色: {self.red_count} ({red_pct:.1f}%)")
        self.black_label.config(text=f"黑色: {self.black_count} ({black_pct:.1f}%)")

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
        self.result_label.config(text=description)
        self.update_status()
        self.update_history()

    def update_history(self):
        self.history_text.config(state="normal")
        self.history_text.delete(1.0, tk.END)
        for i, desc in enumerate(reversed(self.results[-10:]), 1):
            self.history_text.insert(tk.END, f"{i}. {desc}\n")
        self.history_text.config(state="disabled")

    def reset(self):
        self.results = []
        self.red_count = 0
        self.black_count = 0
        self.total_spins = 0
        self.result_label.config(text="--- 点击“下一局”开始 ---")
        self.update_status()
        self.update_history()
        self.spin_button.config(state="normal")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    print("🎲 轮盘赌模拟器（按回车生成下一局）")
    try:
        total_rounds = int(input("请输入总轮数: "))
    except ValueError:
        print("❌ 请输入有效数字！")
        exit()

    for i in range(total_rounds):
        input(f"\n[第 {i + 1} 局] 按回车开始...")
        result = spin()  # 调用上面的函数
        print(f"🎰 结果: {result}")