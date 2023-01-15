N = 10

class Board:
    def __init__(self,board_raw=None,debug_board=False):
        if board_raw:
            self.rows = [board_raw[i:i+N] for i in range(0, len(board_raw), N)]
        elif debug_board:
            self.rows = [[i*10+j for j in range(N)] for i in range(N)]
        else:
            self.rows = [[0 for j in range(N)] for i in range(N)]
        self.N = 0
        
    def __repr__(self):
        res = ""
        d = ['O','.', 'X', '#']
        for row in self.rows:
            res += " ".join([f'{d[x+1]: >2}' for x in row])
            res += "\n"
        return res
    
    @property
    def cols(self):
        for i in range(N):
            col = []
            for j in range(N):
                col.append(self.rows[j][i])
            yield col
    
    @property    
    def groups(self):
        # Horizontal groups
        for row in self.rows:
            for i in range(N-4):
                yield row[i:i+5]
        
        # Vertical groups
        for col in self.cols:
            for i in range(N-4):
                yield col[i:i+5]
        
        # Diagonal groups
        for i in range(0,N-4):
            for j in range(0,N-4):
                yield [self.rows[i+k][j+k] for k in range(5)]
                yield [self.rows[i+k][N-j-k-1] for k in range(5)]
    
    @property
    def score(self):
        total = 0
        
        for group in self.groups:
            figures = set(group)
            if figures == set([0]) or len(figures) > 2:
                # Nothing in this group yet, or mixed figures: ignore
                continue
            elif figures == set([1]):
                # 1 wins
                total += 1_000_000
                continue
            elif figures == set([-1]):
                # -1 wins
                total += -1_000_000
                continue
            
            total += sum(group)**3
            
        return total
    
    @property
    def possible_moves(self):
        for i in range(N):
            for j in range(N):
                if self.rows[i][j] == 0:
                    yield (j, i)
    
    
    def ordered_possible_moves(self, maximizing=True):
        return sorted(self.possible_moves,
                        key=lambda move:self.move_score(move, maximizing=maximizing),
                        reverse = maximizing)
        
    
    def move_score(self, move, maximizing=True):
        i,j = move
        assert self.rows[j][i] == 0
        self.rows[j][i] = 1 if maximizing else -1
        s = self.score
        self.rows[j][i] = 0
        return s
    
    
    def minimax(self, maximizing: bool = True, level = 0, alpha = -10_000_000, beta = 10_000_000):
        
        self.N = self.N + 1
        if self.N % 10000 == 0:
            print(self.N)
        
        curr_score = self.score
        if level <= 0 or abs(curr_score)>=100_000:
            return None, curr_score
        
        if maximizing:
            best_score = -10_000_000
        else:
            best_score = 10_000_000
            
        best_move = None
        
        for x,y in self.ordered_possible_moves(maximizing=maximizing):
            self.rows[y][x] = 1 if maximizing else -1
            
            _, curr_score = self.minimax(maximizing = not maximizing, level = level-1, alpha=alpha, beta=beta)

            if maximizing:
                if curr_score > best_score:
                    best_score = curr_score
                    best_move = (x,y)
                alpha = max(alpha, curr_score)
            else:
                if curr_score < best_score:
                    best_score = curr_score
                    best_move = (x,y)
                beta = min(beta, curr_score)
            
            self.rows[y][x] = 0
            
            if maximizing:
                if curr_score >= beta:
                    break
            else:
                if curr_score <= alpha:
                    break
            

        return best_move, best_score