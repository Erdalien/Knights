'''
Rules:
    Each player has a chess knight (that moves in "L") on a chessboard.
    Each turn the player moves the knight to any tile that hasn't been
    occupied by a knight before. The first player that cannot move loses.
Authors:
    Adam Tomporowski, s16740
    Piotr Baczkowski, s16621
'''
# To run the game you just have to import below modules
import numpy as np
from easyAI import TwoPlayerGame, Human_Player, AI_Player, Negamax

# directions in which a knight can move
DIRECTIONS = list(
    map(
        np.array,
        [[1, 2], [-1, 2], [1, -2], [-1, -2], [2, 1], [2, -1], [-2, 1], [-2, -1]],
    )
)

# functions to convert "D8" into (3,7) and back...
pos2string = lambda ab: "ABCDEFGH"[ab[0]] + str(ab[1] + 1)
string2pos = lambda s: np.array(["ABCDEFGH".index(s[0]), int(s[1]) - 1])


class Knights(TwoPlayerGame):
    def __init__(self, players, board_size):
        """
        Main function of the game, better not to touch anything here.
        All that matters you can set when calling the class.
        :param players: You can set two players as you wish, 2xAI, 2x Human player. It's up to you...
        :param board_size: Tells the board size
        """
        self.players = players
        self.board_size = board_size
        self.board = np.zeros(board_size, dtype=int)
        self.board[0, 0] = 1
        self.board[board_size[0] - 1, board_size[1] - 1] = 2
        players[0].pos = np.array([0, 0])  # starting position of player one, top left corner
        players[1].pos = np.array(
            [board_size[0] - 1, board_size[1] - 1])  # starting position of player two, bottom right corner
        self.current_player = 1  # player 1 starts.

    def possible_moves(self):
        """Functions showing you all possible for current moment moves, they are restricted

        :return: Function returns all possible moves for player
        """
        endings = [self.player.pos + d for d in DIRECTIONS]
        return [
            pos2string(e)
            for e in endings  # all positions
            if (e[0] >= 0)
               and (e[1] >= 0)
               and (e[0] < self.board_size[0])
               and (e[1] < self.board_size[1])
               and self.board[e[0], e[1]] == 0  # inside the board
        ]  # and not blocked

    def make_move(self, pos):
        """You need to move your knight and this function let's to do it after you choose available field. You can use
        command 'show moves' to see tip

        :param pos: Player choose what move will make
        :return: Players move
        """
        pi, pj = self.player.pos
        self.board[pi, pj] = 3  # 3 means blocked
        self.player.pos = string2pos(pos)
        pi, pj = self.player.pos
        self.board[pi, pj] = self.current_player  # place player on board

    def ttentry(self):
        """We need to remember which fields were occupied by knights, function saves it in form of entry

        :return: Saves all occupied fields
        """
        e = [tuple(row) for row in self.board]
        e.append(pos2string(self.players[0].pos))
        e.append(pos2string(self.players[1].pos))
        return tuple(e)

    def ttrestore(self, entry):
        """Useful for players is to remember which fields were occupied, what helps during prepering good strategy
        against our opponent

        :param entry: Parameter saving informations about previously occupied fields
        :return: Entry of occupied fields
        """
        for x, row in enumerate(entry[: self.board_size[0]]):
            for y, n in enumerate(row):
                self.board[x, y] = n
        self.players[0].pos = string2pos(entry[-2])
        self.players[1].pos = string2pos(entry[-1])

    def show(self):
        """Chess table have own wasy to sign, function shows proper chess fields

        :return: Function shows chess fileds
        """
        print(
            "\n"
            + "\n".join(
                ["  1 2 3 4 5 6 7 8"]
                + [
                    "ABCDEFGH"[k]
                    + " "
                    + " ".join(
                        [
                            [".", "1", "2", "X"][self.board[k, i]]
                            for i in range(self.board_size[0])
                        ]
                    )
                    for k in range(self.board_size[1])
                ]
                + [""]
            )
        )

    def lose(self):
        """Rules are simple, if you cannot move your knight you lose. Remember that only one person can win

        :return: If have no possible moves, you lose
        """
        return self.possible_moves() == []

    def scoring(self):
        """All games needs some kond of reward, even if this is not real one. Scores helps to keep who is winning

        :return: If you lose, you are losing 100 points
        """
        return -100 if (self.possible_moves() == []) else 0

    def is_over(self):
        """Games are simple, if you lose, you lose. Simple right? This function shows when game ends

        :return: You losed, so game is over
        """
        return self.lose()


if __name__ == "__main__":
    # Below you can specific AI complex
    ai_algo = Negamax(11)
    game = Knights([AI_Player(ai_algo), Human_Player()], (8, 8))
    game.play()
    print("player %d loses" % (game.current_player))