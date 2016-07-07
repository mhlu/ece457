import random
import copy
import sys

class Game:
    def __init__(self, depth):
        # Initialize 4x4 board with 10 stones for each player
        self.board = [[() for i in range(4)] for j in range(4)]
        self.board[3][0] = (10, 'b')
        self.board[3][3] = (10, 'w')
        self.turn = 'b'
        self.depth = depth
        self.visited_nodes = 0

    def printState(self):
        print '\n' + '-' * 25
        for row in self.board:
            print '|',
            for elem in row:
                print "%3s" % (str(elem[0]) + elem[1]) if len(elem) else "   ",
                print '|', 
            print '\n' + '-' * 25

    def nextMove(self):
        if not self._valid_moves():
            return 

        # Player 1 (minimax)
        if self.turn == 'b':
            self._minimax()
        # Random Agent
        else:
            self._random()
        self.turn = 'b' if self.turn == 'w' else 'w'

    def over(self):
        return not self._valid_moves()

    def winner(self):
        # If last turn was player 1, then player 2 is winner (vice-versa)
        return "Player 1" if self.turn == 'w' else "Player 2"

    def visited(self):
        return self.visited_nodes

    # Checks if current player has any moves
    def _valid_moves(self, board=None, player=None):
        if not board:
            board = self.board
        if not player:
            player = self.turn
        for i in range(4):
            for j in range(4):
                if len(board[i][j]) and board[i][j][1] == player:
                    # Check if any moves are available from here
                    if self._movable(i, j, board, player):
                        return True
        return False
                    
    # Checks if current player can move from position (x,y)
    def _movable(self, x, y, board=None, player=None):
        if not board:
            board = self.board
        if not player:
            player = self.turn
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if self._check_bounds(x+i, y+j):
                    if not len(board[x+i][y+j]) or board[x+i][y+j][1] == player:
                        return True
        return False

    def _minimax(self):
        # Player 1 (black) is the max and Player 2 is the min
        best = self._do_minimax(self.board, self.turn, self.depth, None, None)
        self.board = best[1]

    def _do_minimax(self, board, player, depth, a, b):
        self.visited_nodes += 1
        if depth == 0 or not self._valid_moves(board, player):
            return (self._evaluate(board), board)

        potential_moves = []
        for i in range(4):
            for j in range(4):
                if len(board[i][j]) and board[i][j][1] == player and self._movable(i, j, board, player):
                    potential_moves.append((i, j))
        potential_directions = [(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1)]
        random.shuffle(potential_moves)

        if player == 'b':
            # Max player
            bestValue = None
            bestBoard = None
            for pos in potential_moves:
                for direction in potential_directions:
                    if self._valid_next(pos[0] + direction[0], pos[1] + direction[1], board, player): 
                        new_board = copy.deepcopy(board)
                        self._move(pos[0], pos[1], direction, new_board, player)
                        value = self._do_minimax(new_board, 'w', depth - 1, a, b)
                        a = max(a, value[0]) if a is not None else value[0]
                        if a and b and b <= a:
                            break
                        if bestValue is None or value[0] > bestValue:
                            bestValue, bestBoard = value[0], new_board
            return (bestValue, bestBoard)
        else:
            # Min player
            bestValue = None
            bestBoard = None
            for pos in potential_moves:
                for direction in potential_directions:
                    if self._valid_next(pos[0] + direction[0], pos[1] + direction[1], board, player): 
                        new_board = copy.deepcopy(board)
                        self._move(pos[0], pos[1], direction, new_board, player)
                        value = self._do_minimax(new_board, 'b', depth - 1, a, b)
                        b = min(b, value[0]) if b is not None else value[0]
                        if a and b and b <= a:
                            break
                        if bestValue is None or value[0] < bestValue:
                            bestValue, bestBoard = value[0], new_board
            return (bestValue, bestBoard)

    def _evaluate(self, board):
        score = 0
        directions = [(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1)]
        potential_moves = []
        for i in range(4):
            for j in range(4):
                if len(board[i][j]) and board[i][j][1] == 'b':
                    score += 1
                    if self._movable(i, j, board, 'b'):
                        score += 1
        for i in range(4):
            for j in range(4):
                if len(board[i][j]) and board[i][j][1] == 'w':
                    score -= 1
                    if self._movable(i, j, board, 'w'):
                        score -= 1
        return score

    def _random(self):
        potential_moves = []
        for i in range(4):
            for j in range(4):
                if len(self.board[i][j]) and self.board[i][j][1] == self.turn and self._movable(i, j):
                    potential_moves.append((i, j))
        
        pos = random.choice(potential_moves)
        potential_directions = [(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1)]
        direction = random.choice(potential_directions)
        while not self._valid_next(pos[0] + direction[0], pos[1] + direction[1]):
            direction = random.choice(potential_directions)

        self._move(pos[0], pos[1], direction)

    def _check_bounds(self, x, y):
        return x >= 0 and x < 4 and y >= 0 and y < 4

    def _valid_next(self, x, y, board=None, player=None):
        if not board:
            board = self.board
        if not player:
            player = self.turn

        if not self._check_bounds(x, y):
            return False
        return (not len(board[x][y]) or board[x][y][1] == player)

    def _move(self, x, y, direction, board=None, player=None):
        if not board:
            board = self.board
        if not player:
            player = self.turn
        stones = board[x][y][0]
        board[x][y] = ()
        dir_x, dir_y = direction

        for i in range(1, 4):
            new_x = x + dir_x * i
            new_y = y + dir_y * i
            old = board[new_x - dir_x][new_y - dir_y]
            if not self._check_bounds(new_x, new_y):
                board[new_x - dir_x][new_y - dir_y] = (old[0] + stones, old[1])
                return
            if len(board[new_x][new_y]) and board[new_x][new_y][1] != player:
                board[new_x - dir_x][new_y - dir_y] = (old[0] + stones, old[1])
                return

            old = board[new_x][new_y]
            if stones <= i or i == 3:
                board[new_x][new_y] = (stones + (old[0] if len(old) else 0), player)
                return
            else:
                board[new_x][new_y] = (i + (old[0] if len(old) else 0), player)
                stones -= i

if __name__ == "__main__":
    iterations = 0
    game = Game(int(sys.argv[1]))
    game.printState()

    while not game.over():
        iterations += 1
        game.nextMove()
        game.printState()

    print game.winner(), "wins the game"
    print "Iterations:", iterations
    print "Nodes Visited:", game.visited()
    print "Depth:", sys.argv[1]
