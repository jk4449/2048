from BaseAI import BaseAI
from Displayer import Displayer
from Grid import Grid
import time
import random

class IntelligentAgent(BaseAI):
    def getMove(self, grid):
        self.timeLimit = 0.2
        self.reactionTime = 0.02
        self.startTime = time.process_time()
        self.max_depth = 4
        best_move = None
        _, _, move = self.maximize(grid, 0, float('-inf'), float('inf'))
        return move

    def minimize(self, grid, depth, alpha, beta):
        possibility = [2, 4]
        tile_value = possibility[random.random() > 0.9]
        possibleCells = grid.getAvailableCells()
        timeElapsed = time.process_time() - self.startTime
        
        if depth >= self.max_depth or possibleCells == None or timeElapsed > self.timeLimit:
            return None, self.utility(grid)
        minChild, minUtility = None, float('inf')

        for cell in possibleCells:
            gridCopy2 = grid.clone()
            gridCopy2.insertTile(cell, 2)
            _, utility2, _ = self.maximize(gridCopy2, depth+1, alpha, beta)

            gridCopy4 = grid.clone()
            gridCopy4.insertTile(cell, 4)
            _, utility4, _ = self.maximize(gridCopy4, depth+1, alpha, beta)

            utility = 0.9*utility2 + 0.1*utility4

            if utility < minUtility:
                chance = random.random() > 0.9
                if chance:
                    minChild, minUtility = gridCopy4, utility
                else:
                    minChild, minUtility = gridCopy2, utility
            if minUtility <= alpha:
                break
            if minUtility <= beta:
                beta = minUtility
        return minChild, minUtility
           
    def maximize(self, grid, depth, alpha, beta):
        possibleMoves = grid.getAvailableMoves()
        timeElapsed = time.process_time() - self.startTime

        if depth >= self.max_depth or len(possibleMoves)==0 or timeElapsed > self.timeLimit:
            return None, self.utility(grid), None
        
        maxChild, maxUtility = None, float('-inf')
        prevMove = possibleMoves[0][0]
        for item in possibleMoves:
            _, utility = self.minimize(item[1], depth+1, alpha, beta)

            if utility > maxUtility:
                maxChild, maxUtility, prevMove = item[1], utility, item[0]
            if maxUtility >= beta:
                break
            if maxUtility > alpha:
                alpha = maxUtility
        return maxChild, maxUtility, prevMove
           
    def utility(self, grid):
        maxtile_position_reward = pow(10, 10)
        empty = len(grid.getAvailableCells())
        position = self.max_tile_position(grid, maxtile_position_reward)
        weighted_sum = self.weighted_sum(grid)
        mergability = self.mergability(grid)
        emptyness = -1000 if 0 == (empty+mergability) else -1000/(empty+mergability)
        
        return position*maxtile_position_reward + weighted_sum
    
    def max_tile_position(self, grid, reward):
        if grid.getCellValue((0,0)) == grid.getMaxTile():
            return 1
        else:
            return -1

    def weighted_sum(self, grid):
        reward = 0
        weight_matrix = [
            [4**9, 4**8, 4**7, 4**6],
            [4**2, 4**3, 4**4, 4**5],
            [4, 4, 4, 4],
            [4, 4, 4, 4]]
        for i in range(grid.size):
            for j in range(grid.size):
                reward += grid.getCellValue((i, j)) * weight_matrix[i][j]
        return reward

    
    def mergability(self, grid):
        reward = 0
        for i in range(grid.size - 1):
            for j in range(grid.size - 1):
                if grid.getCellValue((i, j)) == grid.getCellValue((i, j+1)):
                    reward += 1
                if grid.getCellValue((i, j)) == grid.getCellValue((i+1, j)):
                    reward += 1 
        return reward

    
