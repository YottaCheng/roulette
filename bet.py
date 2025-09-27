# bet.py - 纯逻辑引擎 (v3.1)

from collections import deque
from roulette import RouletteWheel

class GameEngine:
    PAYOUT_RATIOS = { "Red": 1, "Black": 1, "Even": 1, "Odd": 1, "1-18": 1, "19-36": 1, "1-12": 2, "13-24": 2, "25-36": 2, "Col1": 2, "Col2": 2, "Col3": 2, "Number": 35 }
    
    def __init__(self):
        self.balance = 0.0
        self.bets = {}
        self.wheel = None
        self.history = deque(maxlen=10)

    def start_new_game(self, balance, is_american):
        self.balance = float(balance)
        self.wheel = RouletteWheel(american=is_american)
        self.history.clear()
        self.bets.clear()
        return True

    def place_bet(self, bet_type, amount, number=None):
        if amount > self.balance: return False, "余额不足以支付此注"
        bet_key = f"{bet_type}_{number}" if number is not None else bet_type
        self.balance -= amount
        self.bets[bet_key] = self.bets.get(bet_key, 0) + amount
        return True, ""

    def clear_bets(self):
        total_bet_amount = sum(self.bets.values())
        self.balance += total_bet_amount
        self.bets.clear()
        return True

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
            
            if bet_type == "Number":
                target_num = parts[1]
                if result_num == target_num:
                    win = True
            else:
                if self.wheel.check_bet(bet_type, result_num):
                    win = True

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