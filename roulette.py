# roulette.py - 修正红黑判断逻辑的最终版

import random

class RouletteWheel:
    def __init__(self, american=True):
        if american:
            self.numbers = ['0', '00'] + [str(i) for i in range(1, 37)]
        else:
            self.numbers = ['0'] + [str(i) for i in range(1, 37)]

        self.reds = {'1', '3', '5', '7', '9', '12', '14', '16', '18', '19', '21', '23', '25', '27', '30', '32', '34', '36'}

        self.columns = {
            'Col1': {1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34},
            'Col2': {2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35},
            'Col3': {3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36}
        }

    def spin(self) -> str:
        return random.choice(self.numbers)

    def get_color(self, number: str) -> str:
        if number in ('0', '00'):
            return '绿色'
        return '红色' if number in self.reds else '黑色'

    def get_column_name(self, number: str) -> str:
        if number in ('0', '00'): return 'N/A'
        n = int(number)
        for col_name, nums in self.columns.items():
            if n in nums:
                return col_name.replace('Col', '第') + "列"
        return '未知'
        
    def describe(self, number: str) -> str:
        color = self.get_color(number)
        column = self.get_column_name(number)
        return f'{number} ({color}, {column})'

    def check_bet(self, bet_type: str, outcome: str) -> bool:
        if outcome in ('0', '00'): return False

        # 【核心修正】在判断红黑时，直接使用 outcome (字符串)
        if bet_type == "Red": return outcome in self.reds
        if bet_type == "Black": return outcome not in self.reds
        
        # 对于其他判断，才需要将 outcome 转换为数字 n
        n = int(outcome)
        if bet_type == "Even": return n % 2 == 0
        if bet_type == "Odd": return n % 2 != 0
        if bet_type == "1-18": return 1 <= n <= 18
        if bet_type == "19-36": return 19 <= n <= 36
        
        if bet_type == "1-12": return 1 <= n <= 12
        if bet_type == "13-24": return 13 <= n <= 24
        if bet_type == "25-36": return 25 <= n <= 36
        if bet_type == "Col1": return n in self.columns['Col1']
        if bet_type == "Col2": return n in self.columns['Col2']
        if bet_type == "Col3": return n in self.columns['Col3']
        
        return False