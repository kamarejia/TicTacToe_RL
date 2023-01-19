import pygame
import random
import numpy as np
from pygame.locals import *
from enum import Enum
import json

pygame.init()

#BGM
pygame.mixer.music.load("tictactoe_music/tie no wa.mp3")  
pygame.mixer.music.play(-1) 

#効果音
sound_select= pygame.mixer.Sound("tictactoe_music/決定ボタンを押す30.mp3")  
sound_player=pygame.mixer.Sound("tictactoe_music/決定ボタンを押す42.mp3")
sound_agent=pygame.mixer.Sound("tictactoe_music/キャンセル6.mp3")
sound_win=pygame.mixer.Sound("tictactoe_music/可愛く輝く1.mp3")
sound_lose=pygame.mixer.Sound("tictactoe_music/クイズ不正解2.mp3")
sound_draw=pygame.mixer.Sound("tictactoe_music/決定ボタンを押す25.mp3")

#画面の基本設定
screen_width=600
screen_height=600
screen=pygame.display.set_mode((screen_width,screen_height))
bg = pygame.image.load("tictactoe_images/TicTacToe_bg.png").convert_alpha()
bg = pygame.transform.scale(bg, (600,600))
rect_bg = bg.get_rect()
bg2 = pygame.image.load("tictactoe_images/TicTacToe_bg2.png").convert_alpha()
bg2 = pygame.transform.scale(bg2, (600,600))
rect_bg2 = bg2.get_rect()
pygame.display.set_caption("tictactoe")       
    
#マークの描画
def draw_OX():
    for i,ox in enumerate(env.board,1):
        if i%2==0:
            if ox==1:
                moon_white.draw(screen,2*100*((i+2)%3),2*100*(((i+2)//3))-200)
            elif ox==-1:
                star_white.draw(screen,2*100*((i+2)%3),2*100*(((i+2)//3))-200)
                
        elif i%2==1:
            if ox==1:
                moon_blue.draw(screen,2*100*((i+2)%3),2*100*(((i+2)//3))-200)
            elif ox==-1:
                star_blue.draw(screen,2*100*((i+2)%3),2*100*(((i+2)//3))-200)

#マークのクラス
class Mark:
    def __init__(self,image,x_size, y_size):
        ### 透過変換でファイル読み込み
        self.image = pygame.image.load(image).convert_alpha()
 
        ### 画像サイズ変更
        self.image = pygame.transform.scale(self.image, (x_size,y_size))
 
        ### 画像サイズ取得
        self.width  = self.image.get_width()
        self.height = self.image.get_height()
 
    #　描画   
    def draw(self, screen,x,y):
        rect= Rect(x, y, self.width, self.height)
        screen.blit(self.image, rect)

#マークの作成
moon_blue=Mark("tictactoe_images/moon_blue.png",200,200)
moon_white=Mark("tictactoe_images/moon_white.png",200,200)
star_blue=Mark("tictactoe_images/star_blue.png",200,200)
star_white=Mark("tictactoe_images/star_white.png",200,200)

#winlose ウィンドウの作成
image_win=pygame.image.load("tictactoe_images/win.png").convert_alpha()
image_win = pygame.transform.scale(image_win, (376,276))
image_lose=pygame.image.load("tictactoe_images/lose.png").convert_alpha()
image_lose = pygame.transform.scale(image_lose, (376,276))
image_draw=pygame.image.load("tictactoe_images/draw.png").convert_alpha()
image_draw= pygame.transform.scale(image_draw, (376,276))

#手番
class TURN(Enum):
    O = 1
    X = -1

#ゲーム環境
class TicTacToeEnv():

    def __init__(self):
        self.reset()
        self.board

    def reset(self):
        self.board = [0]*9

    #どちらのターンか確認
    def check_turn(self):
        O = self.board.count(TURN.O.value)
        X = self.board.count(TURN.X.value)

        if O == X:
            return TURN.O
        else:
            return TURN.X

    #状態遷移関数
    def T(self,action):

        next_state = self.board
        #行動しようとしているマスが空ならどちらの手番か参照して更新
        if next_state[action] == 0:
            
            next_state[action] = TURN.O.value
        return next_state

    #stateをOX変換
    def board_to_string(self,state=None):
        if state == None:
            state = self.board
      
        result = ""
        for a in state:
            if a == TURN.O.value:
                result += "O"
            elif a == TURN.X.value:
                result += "X"
            else:
                result += " "
        return result

    #勝敗の確認
    def check_winner(self):
    #OorXが揃っている場合　そろった 1(O) or -1(X)を返す
        state=self.board
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
        

#難易度別にエージェントの行動価値関数のロード
with open("Q_function.json","r") as f:
    Q=json.load(f)

#エージェント
class TicTacToeAgent():

    def __init__(self):
        self.Q =Q
        self.turn = TURN.O
    
    #方策
    def policy(self):
        board_string = env.board_to_string()

        #難易度別に異なる行動価値関数を呼び出し
        #Easy
        if Difficulty==1:
                return random.randint(0,8)
        #Normal
        elif Difficulty==2:
            random_or_optimal=random.randint(0,9)
            if random_or_optimal<=3:
                return random.randint(0,8)
            else:
                if board_string in self.Q:
                    return np.argmax(self.Q[board_string])
                else:
                    return random.randint(0,8)
        #Hard
        elif Difficulty==3:
            if board_string in self.Q:
                return np.argmax(self.Q[board_string])
            else:
                return random.randint(0,8)

    #ゲームをプレイ
    def play(self):
        if env.check_turn() == self.turn:
            selected_action = self.policy()
            env.board=env.T(selected_action)
            

if __name__ == "__main__":
    #環境とエージェントインスタンス作成
    env=TicTacToeEnv()
    agent=TicTacToeAgent()


    #メインループ
    Run=True
    Game_Run=False
    #ゲーム難易度
    Difficulty=None
    #Sceneで画面遷移
    #Scene1:難易度設定
    #Scene2:ゲーム画面
    Scene=1
    while Run:
        if Scene==1:
            #画面の描画    
            screen.blit(bg, rect_bg)

        elif Scene==2:
            #ゲームスクリーン描画
            screen.blit(bg2, rect_bg2)

            #OX描画
            draw_OX()

            #ゲームの終了処理
            if env.check_winner()==1:
                if Game_Run:
                    sound_lose.play()
                screen.blit(image_lose,(112,162))
                Game_Run=False
                
            elif env.check_winner()==-1:
                if Game_Run:
                    sound_win.play()
                screen.blit(image_win,(112,162))
                Game_Run=False
                
            elif 0 not in env.board:
                if Game_Run:
                    sound_draw.play()
                screen.blit(image_draw,(112,162))
                Game_Run=False

            #ゲーム中ならエージェントがplay
            if Game_Run==True:
                agent.play()
            

        #マウスの位置からグリッド位置を計算
        mx,my=pygame.mouse.get_pos()
        gridx=mx//200
        gridy=my//200
        
        #イベント処理
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                Run=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    Run=False
            
            if event.type==pygame.MOUSEBUTTONDOWN:
                
                #ボタン区間内の領域ならその難易度のゲームに遷移
                if Scene==1 and 150<=mx and mx<462 and 235<=my and my<=315:
                    #Easyでゲーム開始
                    sound_select.play() 
                    Difficulty=1
                    Game_Run=True
                    Scene=2
                elif Scene==1 and 150<=mx and mx<462 and 334<=my and my<=414:
                    #Normalでゲーム開始
                    sound_select.play()
                    Difficulty=2
                    Game_Run=True
                    Scene=2
                elif Scene==1 and 150<=mx and mx<462 and 432<=my and my<=512:
                    #Hardでゲーム開始
                    sound_select.play()
                    Difficulty=3
                    Game_Run=True
                    Scene=2
                elif Scene==2 and env.board[gridx+3*gridy]==0 and Game_Run==True:
                    #プレイヤーのクリックした位置を反映
                    sound_player.play()
                    env.board[gridx+3*gridy]=TURN.X.value

                if Scene==2 and Game_Run==False:
                    env.reset()
                    Scene=1

        pygame.display.update()
        
    pygame.quit()