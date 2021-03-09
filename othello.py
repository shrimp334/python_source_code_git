import numpy as np

EMPTY = 0
WHITE = -1
BLACK = 1
WALL = 2 #ボードの仕切り
HORIZONTAL_WALL = [1,2,3,4,5,6,7,8]
VERTICAL_WALL = [1,2,3,4,5,6,7,8]
BOARD_SIZE = 8 #縦横8x8

#相手の石を裏返せる方向。
#2進数で考える。
LEFT = 1 #00000001、左
LEFT_UPPER = 2 #00000010、左上
UPPER = 2**2 #00000100、上
RIGHT_UPPER = 2**3 #00001000、右上
RIGHT = 2**4 #00010000、右
RIGHT_DOWN = 2**5 #00100000、右下
DOWN = 2**6 #01000000、下
LEFT_DOWN = 2**7 #10000000、左下


class Othello:
    def __init__(self):
        #オセロ盤
        self.board = np.zeros((BOARD_SIZE + 2,BOARD_SIZE + 2),dtype=int)
        #裏返せる方向を示す盤
        self.moveable_dir = np.zeros((BOARD_SIZE + 2,BOARD_SIZE + 2),dtype=int)
        #置けるかどうかの判断を示す盤
        #Trueだと置ける。Falseだと置けないとする。
        self.moveable_position = np.zeros((BOARD_SIZE + 2,BOARD_SIZE + 2),dtype=int)
        #ターン数
        self.turns = 0
        #最初は黒番
        self.current_color = BLACK
        #パスの回数。
        self.pass_count = 0

        #壁埋め
        self.board[0,:] = WALL
        self.board[:,0] = WALL
        self.board[BOARD_SIZE + 1,:] = WALL
        self.board[:,BOARD_SIZE + 1] = WALL

        self.board[4,4] = WHITE
        self.board[5,5] = WHITE
        self.board[4,5] = BLACK
        self.board[5,4] = BLACK

        self.init_moveable()

    #引数x,yでボード状の座標を指定。xは横軸、yは縦軸。
    def move(self,x,y):
        if x < 1 or BOARD_SIZE < x:
            print("Horizontal axis is out of size\n")
            return False
        if y < 1 or BOARD_SIZE < y:
            print("Vertical axis is out of size\n")
            return False
        #石が置けるかどうかの確認。
        if self.moveable_position[y,x] == False:
            print("{} can not be placed\n".format((x,y)))
            return False

        #石を裏返すメソッド。
        self.flip(x,y)
        #ターンを一つすすめる。
        self.turns += 1
        #手番の変更
        self.current_color = -self.current_color
        #moveable_positionとmoveable_dirの更新
        self.init_moveable()

        self.display()

        return True

    #石を裏返すメソッド。
    def flip(self,x,y):
        self.board[y,x] = self.current_color
        #石を置くマスの裏返せる方向の情報を取得
        dir = self.moveable_dir[y,x]
        #マスの左上方向に裏返せるかどうかを確認。
        #その方向の2進数の値と論理積をとる。0でなければ裏返すことができる。
        if dir & LEFT_UPPER:
            y_tmp = y - 1
            x_tmp = x - 1
            #裏返せる方向で相手の石がある限り裏返す。
            while self.board[y_tmp,x_tmp] == -self.current_color:
                self.board[y_tmp,x_tmp] = self.current_color
                y_tmp -= 1
                x_tmp -= 1

        #マスの左方向に裏返せるかどうかを確認。
        if dir & LEFT:
            y_tmp = y
            x_tmp = x - 1
            #裏返せる方向で相手の石がある限り裏返す。
            while self.board[y_tmp,x_tmp] == -self.current_color:
                self.board[y_tmp,x_tmp] = self.current_color
                x_tmp -= 1

        #マスの上方向に裏返せるかどうかを確認。
        if dir & UPPER:
            y_tmp = y - 1
            x_tmp = x
            #裏返せる方向で相手の石がある限り裏返す。
            while self.board[y_tmp,x_tmp] == -self.current_color:
                self.board[y_tmp,x_tmp] = self.current_color
                y_tmp -= 1

        #マスの右上方向に裏返せるかどうかを確認。
        if dir & RIGHT_UPPER:
            y_tmp = y - 1
            x_tmp = x + 1
            #裏返せる方向で相手の石がある限り裏返す。
            while self.board[y_tmp,x_tmp] == -self.current_color:
                self.board[y_tmp,x_tmp] = self.current_color
                y_tmp -= 1
                x_tmp += 1

        #マスの右方向に裏返せるかどうかを確認。
        if dir & RIGHT:
            y_tmp = y
            x_tmp = x + 1
            #裏返せる方向で相手の石がある限り裏返す。
            while self.board[y_tmp,x_tmp] == -self.current_color:
                self.board[y_tmp,x_tmp] = self.current_color
                x_tmp += 1

        #マスの右下方向に裏返せるかどうかを確認。
        if dir & RIGHT_DOWN:
            y_tmp = y + 1
            x_tmp = x + 1
            #裏返せる方向で相手の石がある限り裏返す。
            while self.board[y_tmp,x_tmp] == -self.current_color:
                self.board[y_tmp,x_tmp] = self.current_color
                y_tmp += 1
                x_tmp += 1

        #マスの下方向に裏返せるかどうかを確認。
        if dir & DOWN:
            y_tmp = y + 1
            x_tmp = x
            #裏返せる方向で相手の石がある限り裏返す。
            while self.board[y_tmp,x_tmp] == -self.current_color:
                self.board[y_tmp,x_tmp] = self.current_color
                y_tmp += 1

        #マスの左下方向に裏返せるかどうかを確認。
        if dir & LEFT_DOWN:
            y_tmp = y + 1
            x_tmp = x - 1
            #裏返せる方向で相手の石がある限り裏返す。
            while self.board[y_tmp,x_tmp] == -self.current_color:
                self.board[y_tmp,x_tmp] = self.current_color
                y_tmp += 1
                x_tmp -= 1

    #どの方向を裏返せるかを確認するメソッド。返値は対象のマスの裏返せる方向(dir)
    def check_moveable(self,x,y,color):
        #対象のマスが、どの方向に裏返せるかを一時格納。
        dir = 0

        if self.board[y,x] != EMPTY:
            return False

        #マスの左を調べる。
        if self.board[y,x-1] == -color:
            y_tmp = y
            x_tmp = x - 2
            #相手の石がある限り回す。
            while self.board[y_tmp,x_tmp] == -color:
                x_tmp -=1
            #相手の石をはさんで自分の石があればdirを更新
            if self.board[y_tmp,x_tmp] == color:
                dir |= LEFT

        #マスの左上を調べる。
        if self.board[y-1,x-1] == -color:
            y_tmp = y - 2
            x_tmp = x - 2
            #相手の石がある限り回す。
            while self.board[y_tmp,x_tmp] == -color:
                y_tmp -= 1
                x_tmp -= 1
            #相手の石をはさんで自分の石があればdirを更新
            if self.board[y_tmp,x_tmp] == color:
                dir |= LEFT_UPPER

        #マスの上を調べる。
        if self.board[y-1,x] == -color:
            y_tmp = y - 2
            x_tmp = x
            #相手の石がある限り回す。
            while self.board[y_tmp,x_tmp] == -color:
                y_tmp -= 1
            #相手の石をはさんで自分の石があればdirを更新
            if self.board[y_tmp,x_tmp] == color:
                dir |= UPPER

        #マスの右上を調べる。
        if self.board[y-1,x+1] == -color:
            y_tmp = y - 2
            x_tmp = x + 2
            #相手の石がある限り回す。
            while self.board[y_tmp,x_tmp] == -color:
                y_tmp -= 1
                x_tmp += 1
            #相手の石をはさんで自分の石があればdirを更新
            if self.board[y_tmp,x_tmp] == color:
                dir |= RIGHT_UPPER

        #マスの右を調べる。
        if self.board[y,x+1] == -color:
            y_tmp = y
            x_tmp = x + 2
            #相手の石がある限り回す。
            while self.board[y_tmp,x_tmp] == -color:
                x_tmp += 1
            #相手の石をはさんで自分の石があればdirを更新
            if self.board[y_tmp,x_tmp] == color:
                dir |= RIGHT

        #マスの右下を調べる。
        if self.board[y+1,x+1] == -color:
            y_tmp = y + 2
            x_tmp = x + 2
            #相手の石がある限り回す。
            while self.board[y_tmp,x_tmp] == -color:
                y_tmp += 1
                x_tmp += 1
            #相手の石をはさんで自分の石があればdirを更新
            if self.board[y_tmp,x_tmp] == color:
                dir |= RIGHT_DOWN

        #マスの下を調べる。
        if self.board[y+1,x] == -color:
            y_tmp = y + 2
            x_tmp = x
            #相手の石がある限り回す。
            while self.board[y_tmp,x_tmp] == -color:
                y_tmp += 1
            #相手の石をはさんで自分の石があればdirを更新
            if self.board[y_tmp,x_tmp] == color:
                dir |= DOWN

        #マスの左下を調べる。
        if self.board[y+1,x-1] == -color:
            y_tmp = y + 2
            x_tmp = x - 2
            #相手の石がある限り回す。
            while self.board[y_tmp,x_tmp] == -color:
                y_tmp += 1
                x_tmp -= 1
            #相手の石をはさんで自分の石があればdirを更新
            if self.board[y_tmp,x_tmp] == color:
                dir |= LEFT_DOWN

        return dir

    #moveable_positionとmoveable_dirの更新するメソッド。
    def init_moveable(self):
        #Trueだと置ける。Falseだと置けないとする。
        self.moveable_position[:,:] = False
        #壁以外の全マスの裏返せる方向の更新。
        for x in range(1,BOARD_SIZE+1):
            for y in range(1,BOARD_SIZE+1):
                dir = self.check_moveable(x,y,self.current_color)
                #ここ重要
                self.moveable_dir[y,x] = dir
                #dirが0でない。つまり裏返せる方向が存在する。つまり置ける。
                if dir != 0:
                    self.moveable_position[y,x] = True

    #石と盤を表示するメソッド。
    def display(self):
        print(" ",end="")
        for k in range(0,8):
            print("{:>3}".format(HORIZONTAL_WALL[k]),end=" ")
        print(" ")
        n = 0
        for i in range(1,BOARD_SIZE+1):
            print(VERTICAL_WALL[n],end="")
            n += 1
            for j in range(1,BOARD_SIZE+1):
                if self.board[i,j] == EMPTY:
                    print("{:^3}".format("□"),end = "")
                elif self.board[i,j] == WHITE:
                     print("{:^3}".format("●"),end = "")
                else:
                    print("{:^3}".format("〇"),end = "")
            print(" ")
        print(" ")

    #終了したかどうかを判定するメソッド。
    #オセロの終了条件は以下の3つが存在。
    #1、全マスが石で埋まる場合。
    #2、互いがパスしあう場合。パス→パスで終了。 これはmain関数で実装。
    #3、全マスが埋まる前に片方の石のみになった場合。
    def identify_end(self):
        count_empty = 0
        count_white = 0
        count_black = 0

        if self.pass_count == 2:
            for i in range(1,BOARD_SIZE+1):
                for j in range(1,BOARD_SIZE+1):
                    if self.board[i,j] == WHITE:
                        count_white += 1
                    elif self.board[i,j] == BLACK:
                        count_black += 1
            print("Black = {} , White = {}\n".format(count_black,count_white))
            print("Game end!")
            return True

        for i in range(1,BOARD_SIZE+1):
            for j in range(1,BOARD_SIZE+1):
                if self.board[i,j] == EMPTY:
                    count_empty += 1
                elif self.board[i,j] == WHITE:
                    count_white += 1
                else:
                    count_black += 1
        if count_empty == 0 or count_white == 0 or count_black == 0:
            print("Black = {}, White = {}".format(count_black,count_white))
            print("Game end!")
            return True
        else:
            return False

    #パスするメソッド。
    def player_pass(self):
        player = {-1:"White",1:"Black"}
        print("{} passes\n".format(player[self.current_color]))
        self.current_color = -self.current_color
        #print("Next palyer is {}\n".format(player[self.current_color]))

        self.turns += 1
        self.init_moveable()


#main関数
def main():
     player_color = {-1:"White",1:"Black"}
     my_othello = Othello()

     my_othello.display()
     while not my_othello.identify_end():
        print("Now player is {}".format(player_color[my_othello.current_color]))
        select = int(input("Enter number; 0:Pass , 1:Put Disc> "))

        if select == 1:
            y,x = map(int,input("Enter coordinate (x,y)> ").split())
            my_othello.move(y,x)
            my_othello.pass_count = 0
        elif select == 0:
            my_othello.pass_count += 1
            my_othello.player_pass()


if __name__ == "__main__":
    main()

    """説明"""
    """ゲームを開始したら自分の行動を選択。
    その後、石を置く座標を選択。横軸から先に選ぶ。
    横軸はx、縦軸はy。(x,y)と定義。
    ゲーム終了までやる。"""
