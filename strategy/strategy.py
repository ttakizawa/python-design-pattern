import numpy as np


class Hand:

    HANDNAME = {
        0: "グー",
        1: "チョキ",
        2: "パー",
    }
    
    def __init__(self, hand_value: int):
        self.hand_value = hand_value

    def is_stronger_than(self, hand):
        return self._fight(hand) == 1

    def is_weaker_than(self, hand):
        return self._fight(hand) == -1

    def _fight(self, hand):
        if (self.hand_value == hand.hand_value):
            return 0
        elif ((self.hand_value + 1) % 3 == hand.hand_value):
            return 1
        else:
            return -1

    def __str__(self) -> str:
        return self.HANDNAME[self.hand_value]


class Strategy:

    def next_hand(self) -> Hand:
        raise NotImplementedError()

    def study(self, win: bool):
        raise NotImplementedError()


class WinningStrategy(Strategy):

    def __init__(self, seed: int):
        self._r = np.random.RandomState(seed)
        self._won = False
        self._prev_hand = None


    def next_hand(self) -> Hand:
        if not self._won:
            self._prev_hand = Hand(self._r.randint(0, 2))

        return self._prev_hand

    def study(self, win: bool):
        self._won = win


class ProbStrategy(Strategy):

    def __init__(self, seed: int):
        self._r = np.random.RandomState(seed)
        self._prev_hand_value = 0
        self._current_hand_value = 0
        self._history = [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
        ]
    
    def next_hand(self) -> Hand:
        bet = self._r.randint(self.get_sum(self._current_hand_value))
        hand_value = 0

        if bet < self._history[self._current_hand_value][0]:
            hand_value = 0
        elif bet < (self._history[self._current_hand_value][0] + self._history[self._current_hand_value][1]):
            hand_value = 1
        else:
            hand_value = 2
        
        self._prev_hand_value = self._current_hand_value
        self._current_hand_value = hand_value
        return Hand(hand_value=hand_value)

    def get_sum(self, hv: int):
        sum_val = 0
        for i in range(3):
            sum_val += self._history[hv][i]

        return sum_val

    def study(self, win: bool):
        if win:
            self._history[self._prev_hand_value][self._current_hand_value] += 1
        else:
            self._history[self._prev_hand_value][(self._current_hand_value + 1) % 3] += 1
            self._history[self._prev_hand_value][(self._current_hand_value + 2) % 3] += 1


class Player:

    def __init__(self, name: str, strategy: Strategy):
        self._name = name
        self._strategy = strategy
        self._win_count = 0
        self._lose_count = 0
        self._game_count = 0

    def next_hand(self):
        return self._strategy.next_hand()

    def win(self):
        self._strategy.study(True)
        self._win_count += 1
        self._game_count += 1

    def lose(self):
        self._strategy.study(False)
        self._lose_count += 1
        self._game_count += 1

    def even(self):
        self._game_count += 1

    def __str__(self) -> str:
        return f"[ {self._name}: {self._game_count} games, {self._win_count} win, {self._lose_count} lose ]"


def main():
    player1 = Player("Taro", WinningStrategy(123))
    player2 = Player("Hana", ProbStrategy(0))
    
    for i in range(10000):
        next_hand_1 = player1.next_hand()
        next_hand_2 = player2.next_hand()

        if next_hand_1.is_stronger_than(next_hand_2):
            print("Winner " + str(player2))
            player1.win()
            player2.lose()
        elif next_hand_2.is_stronger_than(next_hand_1):
            print("Winner " + str(player1))
            player2.win()
            player1.lose()
        else:
            print("Even...")
            player2.even()
            player1.even()

    print("Total result")
    print(str(player1))
    print(str(player2))


if __name__ == "__main__":
    main()
