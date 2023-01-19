import numpy as np
import random
from enum import Enum
from collections import defaultdict
import copy
import math
import json

#手番
class TURN(Enum):
    O = 1
    X = -1

#環境
class TicTacToeEnv():

    # 0:empty
    # 1:"O"
    # -1:"X"
    #
    # board
    # 0 1 2
    # 3 4 5
    # 6 7 8

    def __init__(self):
        self.reset()
        self.penalty = -0.2
    
    #stateをOX変換
    def board_to_string(self,state=None):
        if state == None:
            state = self.board
      
        result = ""
        for a in state:
            if a == TURN.O:
                result += "O"
            elif a == TURN.X:
                result += "X"
            else:
                result += " "
        return result

    #環境リセット
    def reset(self):
        self.board = [0]*9

    def __len__(self):
        return len(self.board)
    
    #報酬の計算
    def calc_reward(self,state):

        #boardが無変化のときルール違反でペナルティ
        if self.board == state and state.count(0) != 0:
            return self.penalty

        #OorXが揃っている場合　そろった 1(O) or -1(X)を返す
        #縦
        for c in range(0,3):
            if 0 != state[c] and state[c] == state[3+c] == state[6+c]:
                return state[c]
        #横
        for r in range(0,3):
            if 0 != state[r*3] and state[r*3] == state[r*3+1] == state[r*3+2]:
                return state[r*3]
        #斜め
        if 0 != state[0] and state[0] == state[4] == state[8]:
            return state[0]
        if 0 != state[2] and state[2] == state[4] == state[6]:
            return state[2]
        return 0
    
    #1step 状態変化
    def step(self, action):
        #状態遷移関数から次の状態を取得
        next_state, reward, done = self.T(self.board,action)

        #状態更新
        self.board = next_state

        return next_state, reward, done
    
    #状態遷移関数
    def T(self,state,action):

        reward, done = self.R(state)

        #ゲームが終了しているか確認　終了の場合は遷移なし
        if done == True:
            return state, reward, done

        next_state = copy.copy(state)
        #行動しようとしているマスが空ならどちらの手番か参照して更新
        if next_state[action] == 0:
            next_state[action] = self.check_turn()

        reward, done = self.R(next_state)
        return next_state, reward, done
    
    #報酬関数
    def R(self,state):
        reward = self.calc_reward(state)
        
        # 勝ち/負け
        if reward == TURN.O or reward == TURN.X:
            done = True
            return reward.value, done
        
        # 引き分け
        elif state.count(0) == 0:
            done = True
            return reward, done
        
        # ゲーム続行
        else:
            done = False
            return reward, done

    #どちらの手番かを確認
    def check_turn(self):
        O = self.board.count(TURN.O)
        X = self.board.count(TURN.X)
        if O == X:
            return TURN.O
        else:
            return TURN.X

#エージェント
class TicTacToeAgent():

    def __init__(self, env, epsilon, min_alpha, learning=True):
        #ハイパーパラメータ
        self.epsilon = epsilon
        self.min_alpha = min_alpha
        
        self.N = defaultdict(lambda: [0] * len(env))
        self.Q = defaultdict(lambda: [0] * len(env))
        self.env = env
        
        self.prev_state = [0] * len(self.env)
        self.prev_action = -1
        
        self.turn = TURN.O
        self.learning = learning
    
    #方策
    def policy(self):

        #ランダム値がε以上ならQ値に従って行動
        if self.learning and random.random() < self.epsilon:
            return random.randint(0,8)
        else:
            board_string = env.board_to_string()
            if board_string in self.Q:
                return np.argmax(self.Q[board_string])
            else:
                return random.randint(0,8)
  
    def play(self):
        env.reset()
        if random.randint(0,1)==0:
            self.turn = TURN.O
        else:
            self.turn = TURN.X
    
        done = False
        next_state = -1
        reward = -1
        
        rewards = []
        experience = []
    
        # ゲームを最後までプレイ
        while not done:
            #エージェントの手番
            if env.check_turn() == self.turn:
            
                if self.prev_action != -1:
                    experience.append({"state": env.board_to_string(self.prev_state), "action": self.prev_action, "reward": reward})
                    rewards.append(reward)
            
                selected_action = self.policy()
                self.prev_state = copy.copy(env.board)
                self.prev_action = selected_action
            
                next_state, reward, done = env.step(selected_action)
            
                if done == True:
                    experience.append({"state": env.board_to_string(self.prev_state), "action": self.prev_action, "reward": reward})
                    rewards.append(reward)

            
            else:
                #selected_action=self.policy()
                selected_action = random.randint(0,8)
                env.step(selected_action)
        
    # 価値を計算して、行動価値関数を更新
        for i, x in enumerate(experience):
            s, a = x["state"], x["action"]
            G, t = 0, 0
            for j in range(i, len(experience)):
                G += math.pow(0.9, t) * experience[j]["reward"]
                t += 1
            self.N[s][a] += 1
            alpha = 1 / self.N[s][a]
            alpha = max(alpha,self.min_alpha)
            self.Q[s][a] += alpha * (G - self.Q[s][a])
        self.prev_action = -1
        
        return rewards  



def print_tictactoe_board(env):
    count = 0
    for b in env.board:
        if b == TURN.O:
            print("○",end="")
        if b == TURN.X:
            print("×",end="")    
        if b == 0:
            print(" ",end="")
        if count % 3 == 2 :
            print("")
        count += 1


if __name__ == "__main__":
    env = TicTacToeEnv()
    agent = TicTacToeAgent(env, epsilon=0.05, min_alpha = 0.005)
    
    win = 0
    game = 0
  
    for i in range(10000001):
        rewards = agent.play()
        
        if rewards[-1] == 1 or rewards[-1] == 0:
            win += 1
            game += 1
        else:
            game += 1
        
        if i % 10000 == 0:
            print_tictactoe_board(env)
            print(str(i) + "th play",rewards)
            print("win %:",win/game*100)
            win = 0
            game = 0
            
            Qs = agent.Q[env.board_to_string([0,0,0,0,0,0,0,0,0])]
            
            for a in range(0,3):
                
                print(Qs[a*3],Qs[a*3+1],Qs[a*3+2])
        
    # check learned
    agent.learning = False
  
    for i in range(10001):
        rewards = agent.play()
        
        if rewards[-1] == 1 or rewards[-1] == 0:
            win += 1
            game += 1
        else:
            game += 1
        
        if i % 10000 == 0:
            print_tictactoe_board(env)
            print(str(i) + "th play(test)",rewards)
            print("win %:",win/game*100)
            win = 0
            game = 0
        
            Qs = agent.Q[env.board_to_string([0,0,0,0,0,0,0,0,0])]
            for a in range(0,3):
                print(Qs[a*3],Qs[a*3+1],Qs[a*3+2])
    print("Last play",rewards)
    
    with open("Q.json","w") as f:
        json.dump(agent.Q,f)