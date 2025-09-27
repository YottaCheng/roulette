# test.py - Final version with comprehensive edge case testing

import unittest
from roulette import RouletteWheel
from bet import GameEngine

class TestGameEngine(unittest.TestCase):

    def setUp(self):
        """This method is called before each test."""
        self.engine = GameEngine()
        # Default to a European wheel for most tests unless specified otherwise
        self.engine.start_new_game(balance=1000, is_american=False)

    # --- Basic Win/Loss Tests ---
    def test_bet_on_red_win(self):
        self.engine.wheel.spin = lambda: '7' # Force Red
        self.engine.place_bet('Red', 10)
        desc, net_profit = self.engine.spin()
        self.assertEqual(net_profit, 10)

    def test_bet_on_black_lose(self):
        self.engine.wheel.spin = lambda: '7' # Force Red
        self.engine.place_bet('Black', 10)
        desc, net_profit = self.engine.spin()
        self.assertEqual(net_profit, -10)

    def test_bet_on_dozen_win(self):
        self.engine.wheel.spin = lambda: '7'
        self.engine.place_bet('1-12', 10)
        desc, net_profit = self.engine.spin()
        self.assertEqual(net_profit, 20)

    def test_bet_on_column_win(self):
        self.engine.wheel.spin = lambda: '7'
        self.engine.place_bet('Col1', 10)
        desc, net_profit = self.engine.spin()
        self.assertEqual(net_profit, 20)

    def test_bet_on_number_win(self):
        self.engine.wheel.spin = lambda: '7'
        self.engine.place_bet('Number', 10, number='7')
        desc, net_profit = self.engine.spin()
        self.assertEqual(net_profit, 350)

    # --- Combination Bet Tests ---
    def test_combination_bet_win_and_lose(self):
        self.engine.wheel.spin = lambda: '7' # Red, Odd
        self.engine.place_bet('Red', 10)    # Should win (+10 profit)
        self.engine.place_bet('Even', 5)    # Should lose (-5 profit)
        desc, net_profit = self.engine.spin()
        self.assertEqual(net_profit, 5)

    def test_multiple_wins_combination(self):
        self.engine.wheel.spin = lambda: '7' # Red, Odd, 1-12, Col1
        self.engine.place_bet('Red', 10)    # Profit: 10
        self.engine.place_bet('Odd', 10)    # Profit: 10
        self.engine.place_bet('1-12', 10)   # Profit: 20
        self.engine.place_bet('Col1', 10)   # Profit: 20
        desc, net_profit = self.engine.spin()
        self.assertEqual(net_profit, 60)

    def test_multiple_losses_combination(self):
        self.engine.wheel.spin = lambda: '7' # Red, Odd
        self.engine.place_bet('Black', 10)
        self.engine.place_bet('Even', 10)
        self.engine.place_bet('19-36', 10)
        desc, net_profit = self.engine.spin()
        self.assertEqual(net_profit, -30)

    # --- NEW EDGE CASE TESTS ---

    def test_bet_on_zero_and_win(self):
        """Test the user-suggested case: winning a bet on '0'."""
        self.engine.wheel.spin = lambda: '0'
        self.engine.place_bet('Number', 10, number='0')
        desc, net_profit = self.engine.spin()
        
        # Expected profit for a 10 bet on 35:1 is 350
        self.assertEqual(net_profit, 350)
        self.assertEqual(self.engine.balance, 1350)

    def test_zero_outcome_loses_all_outside_bets(self):
        """Test that a '0' outcome makes all outside bets lose."""
        self.engine.wheel.spin = lambda: '0'
        bets_to_place = [
            'Red', 'Black', 'Odd', 'Even', '1-18', '19-36',
            '1-12', '13-24', '25-36', 'Col1', 'Col2', 'Col3'
        ]
        for bet_type in bets_to_place:
            self.engine.place_bet(bet_type, 1) # Bet $1 on each
        desc, net_profit = self.engine.spin()
        self.assertEqual(net_profit, -12)

    def test_double_zero_outcome_loses_all_outside_bets(self):
        """Test that a '00' outcome on an American wheel also loses all outside bets."""
        # Re-initialize the engine for this specific test with an American wheel
        self.engine.start_new_game(balance=1000, is_american=True)
        self.engine.wheel.spin = lambda: '00'
        
        bets_to_place = [
            'Red', 'Black', 'Odd', 'Even', '1-18', '19-36',
            '1-12', '13-24', '25-36', 'Col1', 'Col2', 'Col3'
        ]
        for bet_type in bets_to_place:
            self.engine.place_bet(bet_type, 1)
        desc, net_profit = self.engine.spin()
        self.assertEqual(net_profit, -12)

    def test_bet_exact_balance_and_lose(self):
        """Test the financial edge case of betting the entire balance."""
        # Set a specific balance for this test
        self.engine.balance = 50.0
        self.engine.wheel.spin = lambda: '35' # 35 is Black        
        # Bet the entire balance on a losing outcome
        self.engine.place_bet('Red', 50.0)
        self.assertEqual(self.engine.balance, 0) # Balance should be 0 after placing the bet
        
        desc, net_profit = self.engine.spin()
        
        self.assertEqual(net_profit, -50)
        self.assertEqual(self.engine.balance, 0) # Balance should remain 0 after losing

if __name__ == '__main__':
    unittest.main()