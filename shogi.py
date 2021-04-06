""" Shogi code with python completed version 2021/4/6"""

import numpy as np

BOARD_SIZE = 9

PROMOTO = 100
ENEMY = 200

num_coordinate = [1,2,3,4,5,6,7,8,9]

"""FU 歩, TO と
KY 香車, NKY 成香
KE 桂馬, NKE 成桂
GI 銀, NGI 成銀
KI 金
KK 角, UMA 馬
HI 飛車, RYU 竜
OU 王、玉
"""

sente_koma = {"FU":1,"KY":2,"KE":3,"GI":4,"KI":5,"KK":6,"HI":7,"OU":8
             ,"TO":101,"NKY":102,"NKE":103,"NGI":104,"UMA":106,"RYU":107}

gote_koma = {"EFU":201,"EKY":202,"EKE":203,"EGI":204,"EKI":205,"EKK":206,"EHI":207,"EOU":208
            ,"ETO":301,"ENKY":302,"ENKE":303,"ENGI":304,"EUMA":306,"ERYU":307}

koma = ["  . ","歩","香","桂","銀","金","角","飛","玉"]
nari_koma_dict = {1:"と",2:"杏",3:"圭",4:"全",6:"馬",7:"竜"}

#index0から上、右上、右、右下...左上、桂馬左、桂馬右。
#1は１マスだけ、８は動けなくなるまで動ける。
koma_dir_dis = [[1,0,0,0,0,0,0,0,0,0] #歩
               ,[8,0,0,0,0,0,0,0,0,0] #香
               ,[0,0,0,0,0,0,0,0,1,1] #桂
               ,[1,0,0,0,0,0,0,0,0,0] #銀
               ,[1,1,1,0,1,0,1,1,0,0] #金
               ,[0,8,0,8,0,8,0,8,0,0] #角
               ,[8,0,8,0,8,0,8,0,0,0] #飛
               ,[1,1,1,1,1,1,1,1,0,0]] #玉

narikoma_dir_dis = {"TO":[1,1,1,0,1,0,1,1,0,0] #と
                   ,"NKY":[1,1,1,0,1,0,1,1,0,0] #成香
                   ,"NKE":[1,1,1,0,1,0,1,1,0,0] #成桂
                   ,"NGI":[1,1,1,0,1,0,1,1,0,0] #成銀
                   ,"UMA":[1,8,1,8,1,8,1,8,0,0] #馬
                   ,"RYU":[8,1,8,1,8,1,8,1,0,0]} #竜

#将棋盤及びゲームに関するクラス
class Shogi_play:
    def __init__(self):
        #将棋盤
        #行を表す縦軸をy，列を表す横軸をxとする．
        self.board = [[Empty("EMPTY",0,0,0,"e")]*(BOARD_SIZE+2) for i in range(BOARD_SIZE+2)]

        #ターン数
        self.turns = 0

        #最初は先手番。Trueが先手番、Falseが後手番。
        self.current_player = True

        #駒台クラス．駒を駒台から盤に打つときに使用する．
        self.sente_koma_dai = Koma_dai("s")
        self.gote_koma_dai = Koma_dai("g")

        #将棋盤にコマを配置。#３つ目の引数の座標は[y,x]で格納されている．
        self.board[1][5] = OU("EOU",gote_koma["EOU"],koma_dir_dis[7],[1,5],"g")
        self.board[9][5] = OU("OU",sente_koma["OU"],koma_dir_dis[7],[9,5],"s")

        self.board[1][4] = KIN("EKI",gote_koma["EKI"],koma_dir_dis[4],[1,4],"g")
        self.board[1][6] = KIN("EKI",gote_koma["EKI"],koma_dir_dis[4],[1,6],"g")
        self.board[9][4] = KIN("KI",sente_koma["KI"],koma_dir_dis[4],[9,4],"s")
        self.board[9][6] = KIN("KI",sente_koma["KI"],koma_dir_dis[4],[9,6],"s")

        self.board[1][3] = GIN("EGI",gote_koma["EGI"],koma_dir_dis[3],[1,3],"g")
        self.board[1][7] = GIN("EGI",gote_koma["EGI"],koma_dir_dis[3],[1,7],"g")
        self.board[9][3] = GIN("GI",sente_koma["GI"],koma_dir_dis[3],[9,3],"s")
        self.board[9][7] = GIN("GI",sente_koma["GI"],koma_dir_dis[3],[9,7],"s")

        self.board[1][2] = KEIMA("EKE",gote_koma["EKE"],koma_dir_dis[2],[1,2],"g")
        self.board[1][8] = KEIMA("EKE",gote_koma["EKE"],koma_dir_dis[2],[1,8],"g")
        self.board[9][2] = KEIMA("KE",sente_koma["KE"],koma_dir_dis[2],[9,2],"s")
        self.board[9][8] = KEIMA("KE",sente_koma["KE"],koma_dir_dis[2],[9,8],"s")

        self.board[1][1] = KYO("EKY",gote_koma["EKY"],koma_dir_dis[1],[1,1],"g")
        self.board[1][9] = KYO("EKY",gote_koma["EKY"],koma_dir_dis[1],[1,9],"g")
        self.board[9][1] = KYO("KY",sente_koma["KY"],koma_dir_dis[1],[9,1],"s")
        self.board[9][9] = KYO("KY",sente_koma["KY"],koma_dir_dis[1],[9,9],"s")

        self.board[2][2] = HISYA("EHI",gote_koma["EHI"],koma_dir_dis[6],[2,8],"g")
        self.board[8][2] = KAKU("KK",sente_koma["KK"],koma_dir_dis[5],[8,2],"s")
        self.board[2][8] = KAKU("EKK",gote_koma["EKK"],koma_dir_dis[5],[2,2],"g")
        self.board[8][8] = HISYA("HI",sente_koma["HI"],koma_dir_dis[6],[8,8],"s")

        for i in range(1,BOARD_SIZE+1):
            self.board[3][i] = FU("EFU",gote_koma["EFU"],koma_dir_dis[0],[3,i],"g")
            self.board[7][i] = FU("FU",sente_koma["FU"],koma_dir_dis[0],[7,i],"s")

        for i in range(BOARD_SIZE+2):
            self.board[0][i] = Wall("WALL",0,0,0,"w")
            self.board[i][0] = Wall("WALL",0,0,0,"w")
            self.board[BOARD_SIZE+1][i] = Wall("WALL",0,0,0,"w")
            self.board[i][BOARD_SIZE+1] = Wall("WALL",0,0,0,"w")

    #表示メソッド。
    def display_board(self):
        player_teban = {True:"先手",False:"後手"}
        print("\n{}の手番です．\n".format(player_teban[self.current_player]))

        print(" ",end="")
        for k in range(BOARD_SIZE):
            print("{:^5}".format(num_coordinate[k]),end="")
        print("")

        for i in range(1,BOARD_SIZE+1):
            print(num_coordinate[i-1],end="")
            for j in range(1,BOARD_SIZE+1):

                if self.board[i][j].num != 0:
                    if self.board[i][j].num < 200:
                        print("△{:^3}".format(koma[self.board[i][j].num]),end="") if self.board[i][j].num < 100 else print("△{:^3}".format(nari_koma_dict[self.board[i][j].num-100]),end="")
                    else:
                        print("▼{:^3}".format(koma[self.board[i][j].num-200]),end="") if self.board[i][j].num < 300 else print("▼{:^3}".format(nari_koma_dict[self.board[i][j].num-300]),end="")
                else:
                    print("{:^5}".format(koma[self.board[i][j].num]),end="")

            print(" ")

    #コマを動かすメソッド。
    #nx,nyは動かしたいコマの現在の座標。
    def move(self,nx,ny):
        #駒台クラスのretain_komaメソッドで使うdict
        koma_kanji = {"FU":"歩","KY":"香","KE":"桂","GI":"銀","KI":"金","KK":"角","HI":"飛","TO":"歩","NKY":"香","NKE":"桂","NGI":"銀","UMA":"角","RYU":"飛"}

        #動かしたいコマの数値を格納
        wanna_move_koma = self.board[ny][nx]

        #動かしたいコマが、動かしたい座標まで動かせるかどうかの判定。
        ls = wanna_move_koma.check_move(self,wanna_move_koma,nx,ny)
        if ls:
            #動かしたい先座標が空でなく駒が存在していたら
            if not isinstance(self.board[ls[1]][ls[0]],Empty):
                #先手
                if self.current_player:
                    self.sente_koma_dai.retain_koma(koma_kanji[self.board[ls[1]][ls[0]].name[1:]])
                #後手
                else:
                    self.gote_koma_dai.retain_koma(koma_kanji[self.board[ls[1]][ls[0]].name])

            #ls[1]はy軸，ls[0]はx軸． ls = [x,y]
            self.board[ls[1]][ls[0]] = wanna_move_koma
            self.board[ls[1]][ls[0]].coordinate = [ls[1],ls[0]]
            #print(self.board[ls[1]][ls[0]].coordinate)
            self.board[ny][nx] = Empty("EMPTY",0,0,0,"e")
        else:
            print("({},{}) {} はそこに動かせません．\n".format(nx,ny,wanna_move_koma.name))
            return

        #成るかどうかの確認．
        if self.current_player and self.board[ls[1]][ls[0]].coordinate[0] <= 3:
            #コマを成るメソッド．
            self.board[ls[1]][ls[0]].promote_koma(self,ls)

        elif not self.current_player and self.board[ls[1]][ls[0]].coordinate[0] >= 7:
            self.board[ls[1]][ls[0]].promote_koma(self,ls)

        self.turns += 1
        self.current_player = not self.current_player

    #終了判定．とりあえず投了したかどうか．
    def touryo(self):
        player_teban = {True:"先手",False:"後手"}
        print("{} が投了しました．{}の勝ちです．".format(player_teban[self.current_player],player_teban[not self.current_player]))
        return True


class Shogi_koma:
    def __init__(self,name,num,dir_dis,coord,ally_flag):
        #コマの名前。
        self.name = name
        #コマの識別数値。
        self.num = num
        #コマがその方向に何マス進めるかを格納する配列。index０からUPPER,RIGHT_UPPER...最後は桂馬用の斜め。
        self.dir_distance = dir_dis
        #コマが存在してる座標。
        self.coordinate = coord
        #先手後手のフラグ．"s"だと先手番，"g"だと後手番,"e"だとEmpty,"w"だと壁．
        self.ally_flag = ally_flag

    #動かしたいコマが動かしたい座標にまで動かせるかどうかの判定。
    #動かしたいコマの座標を指定し、そのコマがどこに動かせるかの座標を表示。座標たちを配列に入れておき、
    #動かす先として選択した座標がその配列に属していなければ再度選ばせる。
    def check_move(self,game,koma,nx,ny):
        #現在動けるマス
        current_moveable = []
        for i in range(len(koma.dir_distance)): #len(koma_dir_distance) == 10
            square = koma.dir_distance[i]
            koma.check_current_move(game,koma.dir_distance,nx,ny,i,current_moveable)

        #移動可能座標の一覧を表示．
        #current_moveableは二次元配列．各要素は動かすことのできる座標．
        #print(current_moveable)
        for i in current_moveable:
            print(i)

        input_x,input_y = map(int,input("動かしたい座標を入力してください ").split())
        if [input_x,input_y] in current_moveable:
            return [input_x,input_y]
        else:
            return False

    #現在、動くことのできるマス目を探す関数
    #gameはShogi_playのインスタンス,moveableは対象のコマが動ける方向が格納された配列,nx,nyは現在の座標，currentは動ける先の座標を格納する配列．
    def check_current_move(self,game,moveable,nx,ny,i,current):
        #先手，上．
        if i == 0 and game.current_player:
            y_tmp = ny - 1
            x_tmp = nx
            if moveable[i] == 1:
                if isinstance(game.board[y_tmp][x_tmp],Empty) or game.board[y_tmp][x_tmp].ally_flag == "g":
                    current.append([x_tmp,y_tmp])
            elif moveable[i] == 8:
                while isinstance(game.board[y_tmp][x_tmp],Empty) or game.board[y_tmp][x_tmp].ally_flag == "g":
                    current.append([x_tmp,y_tmp])
                    if game.board[y_tmp][x_tmp].ally_flag == "g":
                        return
                    y_tmp -= 1
        #後手，上．
        elif i == 0 and not game.current_player:
            y_tmp = ny + 1
            x_tmp = nx
            if moveable[i] == 1:
                if isinstance(game.board[y_tmp][x_tmp],Empty) or game.board[y_tmp][x_tmp].ally_flag == "s":
                    current.append([x_tmp,y_tmp])
            elif moveable[i] == 8:
                while isinstance(game.board[y_tmp][x_tmp],Empty) or game.board[y_tmp][x_tmp].ally_flag == "s":
                    current.append([x_tmp,y_tmp])
                    if game.board[y_tmp][x_tmp].ally_flag == "s":
                        return
                    y_tmp += 1

        #先手，右上．
        if i == 1 and game.current_player:
            y_tmp = ny - 1
            x_tmp = nx + 1
            if moveable[i] == 1:
                if isinstance(game.board[y_tmp][x_tmp],Empty) or game.board[y_tmp][x_tmp].ally_flag == "g":
                    current.append([x_tmp,y_tmp])
            elif moveable[i] == 8:
                while isinstance(game.board[y_tmp][x_tmp],Empty) or game.board[y_tmp][x_tmp].ally_flag == "g":
                    current.append([x_tmp,y_tmp])
                    if game.board[y_tmp][x_tmp].ally_flag == "g":
                        return
                    y_tmp -= 1
                    x_tmp += 1
        #後手，右上．
        elif i == 1 and not game.current_player:
            y_tmp = ny + 1
            x_tmp = nx - 1
            if moveable[i] == 1:
                if isinstance(game.board[y_tmp][x_tmp],Empty) or game.board[y_tmp][x_tmp].ally_flag == "s":
                    current.append([x_tmp,y_tmp])
            elif moveable[i] == 8:
                while isinstance(game.board[y_tmp][x_tmp],Empty) or game.board[y_tmp][x_tmp].ally_flag == "s":
                    current.append([x_tmp,y_tmp])
                    if game.board[y_tmp][x_tmp].ally_flag == "s":
                        return
                    y_tmp += 1
                    x_tmp -= 1

        #先手，右
        if i == 2 and game.current_player:
            y_tmp = ny
            x_tmp = nx + 1
            if moveable[i] == 1:
                if isinstance(game.board[y_tmp][x_tmp],Empty) or game.board[y_tmp][x_tmp].ally_flag == "g":
                    current.append([x_tmp,y_tmp])
            elif moveable[i] == 8:
                while isinstance(game.board[y_tmp][x_tmp],Empty)  or game.board[y_tmp][x_tmp].ally_flag == "g":
                    current.append([x_tmp,y_tmp])
                    if game.board[y_tmp][x_tmp].ally_flag == "g":
                        return
                    x_tmp += 1
        #後手，右
        elif i == 2 and not game.current_player:
            y_tmp = ny
            x_tmp = nx - 1
            if moveable[i] == 1:
                if isinstance(game.board[y_tmp][x_tmp],Empty) or game.board[y_tmp][x_tmp].ally_flag == "s":
                    current.append([x_tmp,y_tmp])
            elif moveable[i] == 8:
                while isinstance(game.board[y_tmp][x_tmp],Empty) or game.board[y_tmp][x_tmp].ally_flag == "s":
                    current.append([x_tmp,y_tmp])
                    if game.board[y_tmp][x_tmp].ally_flag == "s":
                        return
                    x_tmp -= 1

        #先手，右下．
        if i == 3 and game.current_player:
            y_tmp = ny + 1
            x_tmp = nx + 1
            if moveable[i] == 1:
                if isinstance(game.board[y_tmp][x_tmp],Empty) or game.board[y_tmp][x_tmp].ally_flag == "g":
                    current.append([x_tmp,y_tmp])
            elif moveable[i] == 8:
                while isinstance(game.board[y_tmp][x_tmp],Empty) or game.board[y_tmp][x_tmp].ally_flag == "g":
                    current.append([x_tmp,y_tmp])
                    if game.board[y_tmp][x_tmp].ally_flag == "g":
                        return
                    y_tmp += 1
                    x_tmp += 1
        #後手，右下．
        elif i == 3 and not game.current_player:
            y_tmp = ny - 1
            x_tmp = nx - 1
            if moveable[i] == 1:
                if isinstance(game.board[y_tmp][x_tmp],Empty) or game.board[y_tmp][x_tmp].ally_flag == "s":
                    current.append([x_tmp,y_tmp])
            elif moveable[i] == 8:
                while isinstance(game.board[y_tmp][x_tmp],Empty) or game.board[y_tmp][x_tmp].ally_flag == "s":
                    current.append([x_tmp,y_tmp])
                    if game.board[y_tmp][x_tmp].ally_flag == "s":
                        return
                    y_tmp -= 1
                    x_tmp -= 1

        #先手，下．
        if i == 4 and game.current_player:
            y_tmp = ny + 1
            x_tmp = nx
            if moveable[i] == 1:
                if isinstance(game.board[y_tmp][x_tmp],Empty) or game.board[y_tmp][x_tmp].ally_flag == "g":
                    current.append([x_tmp,y_tmp])
            elif moveable[i] == 8:
                while isinstance(game.board[y_tmp][x_tmp],Empty) or game.board[y_tmp][x_tmp].ally_flag == "g":
                    current.append([x_tmp,y_tmp])
                    if game.board[y_tmp][x_tmp].ally_flag == "g":
                        return
                    y_tmp += 1
        #後手，下．
        elif i == 4 and not game.current_player:
            y_tmp = ny - 1
            x_tmp = nx
            if moveable[i] == 1:
                if isinstance(game.board[y_tmp][x_tmp],Empty) or game.board[y_tmp][x_tmp].ally_flag == "s":
                    current.append([x_tmp,y_tmp])
            elif moveable[i] == 8:
                while isinstance(game.board[y_tmp][x_tmp],Empty) or game.board[y_tmp][x_tmp].ally_flag == "s":
                    current.append([x_tmp,y_tmp])
                    if game.board[y_tmp][x_tmp].ally_flag == "s":
                        return
                    y_tmp -= 1

        #先手，左下．
        if i == 5 and game.current_player:
            y_tmp = ny + 1
            x_tmp = nx - 1
            if moveable[i] == 1:
                if isinstance(game.board[y_tmp][x_tmp],Empty) or game.board[y_tmp][x_tmp].ally_flag == "g":
                    current.append([x_tmp,y_tmp])
            elif moveable[i] == 8:
                while isinstance(game.board[y_tmp][x_tmp],Empty) or game.board[y_tmp][x_tmp].ally_flag == "g":
                    current.append([x_tmp,y_tmp])
                    if game.board[y_tmp][x_tmp].ally_flag == "g":
                        return
                    y_tmp += 1
                    x_tmp -= 1
        #後手，左下．
        elif i == 5 and not game.current_player:
            y_tmp = ny - 1
            x_tmp = nx + 1
            if moveable[i] == 1:
                if isinstance(game.board[y_tmp][x_tmp],Empty) or game.board[y_tmp][x_tmp].ally_flag == "s":
                    current.append([x_tmp,y_tmp])
            elif moveable[i] == 8:
                while isinstance(game.board[y_tmp][x_tmp],Empty) or game.board[y_tmp][x_tmp].ally_flag == "s":
                    current.append([x_tmp,y_tmp])
                    if game.board[y_tmp][x_tmp].ally_flag == "s":
                        return
                    y_tmp -= 1
                    x_tmp += 1

        #先手，左．
        if i == 6 and game.current_player:
            y_tmp = ny
            x_tmp = nx - 1
            if moveable[i] == 1:
                if isinstance(game.board[y_tmp][x_tmp],Empty) or game.board[y_tmp][x_tmp].ally_flag == "g":
                    current.append([x_tmp,y_tmp])
            elif moveable[i] == 8:
                while isinstance(game.board[y_tmp][x_tmp],Empty) or game.board[y_tmp][x_tmp].ally_flag == "g":
                    current.append([x_tmp,y_tmp])
                    if game.board[y_tmp][x_tmp].ally_flag == "g":
                        return
                    x_tmp -= 1
        #後手，左．
        elif i == 6 and not game.current_player:
            y_tmp = ny
            x_tmp = nx + 1
            if moveable[i] == 1:
                if isinstance(game.board[y_tmp][x_tmp],Empty) or game.board[y_tmp][x_tmp].ally_flag == "s":
                    current.append([x_tmp,y_tmp])
            elif moveable[i] == 8:
                while isinstance(game.board[y_tmp][x_tmp],Empty) or game.board[y_tmp][x_tmp].ally_flag == "s":
                    current.append([x_tmp,y_tmp])
                    if game.board[y_tmp][x_tmp].ally_flag == "s":
                        return
                    x_tmp += 1

        #先手，左上．
        if i == 7 and game.current_player:
            y_tmp = ny - 1
            x_tmp = nx - 1
            if moveable[i] == 1:
                if isinstance(game.board[y_tmp][x_tmp],Empty) or game.board[y_tmp][x_tmp].ally_flag == "g":
                    current.append([x_tmp,y_tmp])
            elif moveable[i] == 8:
                while isinstance(game.board[y_tmp][x_tmp],Empty) or game.board[y_tmp][x_tmp].ally_flag == "g":
                    current.append([x_tmp,y_tmp])
                    if game.board[y_tmp][x_tmp].ally_flag == "g":
                        return
                    y_tmp -= 1
                    x_tmp -= 1
        #後手，左上．
        elif i == 7 and not game.current_player:
            y_tmp = ny + 1
            x_tmp = nx + 1
            if moveable[i] == 1:
                if isinstance(game.board[y_tmp][x_tmp],Empty) or game.board[y_tmp][x_tmp].ally_flag == "s":
                    current.append([x_tmp,y_tmp])
            elif moveable[i] == 8:
                while isinstance(game.board[y_tmp][x_tmp],Empty) or game.board[y_tmp][x_tmp].ally_flag == "s":
                    current.append([x_tmp,y_tmp])
                    if game.board[y_tmp][x_tmp].ally_flag == "s":
                        return
                    y_tmp += 1
                    x_tmp += 1

        #先手，桂馬左．
        if i == 8 and game.current_player and moveable[i] == 1:
            y_tmp = ny - 2
            x_tmp = nx - 1
            if isinstance(game.board[y_tmp][x_tmp],Empty) or game.board[y_tmp][x_tmp].ally_flag == "g":
                current.append([x_tmp,y_tmp])
        #後手，桂馬左．
        elif i == 8 and not game.current_player and moveable[i] == 1:
            y_tmp = ny + 2
            x_tmp = nx + 1
            if isinstance(game.board[y_tmp][x_tmp],Empty) or game.board[y_tmp][x_tmp].ally_flag == "s":
                current.append([x_tmp,y_tmp])

        #先手，桂馬右．
        if i == 9 and game.current_player and moveable[i] == 1:
            y_tmp = ny - 2
            x_tmp = nx + 1
            if isinstance(game.board[y_tmp][x_tmp],Empty) or game.board[y_tmp][x_tmp].ally_flag == "g":
                current.append([x_tmp,y_tmp])
        #後手，桂馬右．
        elif i == 9 and not game.current_player and moveable[i] == 1:
            y_tmp = ny + 2
            x_tmp = nx - 1
            if isinstance(game.board[y_tmp][x_tmp],Empty) or game.board[y_tmp][x_tmp].ally_flag == "s":
                current.append([x_tmp,y_tmp])

        #コマを成るかどうかのメソッド．
        #gameにはShogi_playのインスタンスが，to_coordinateには成るかどうかの対象となるコマの移動先座標配列が入る．
    def promote_koma(self,game,to_coordinate):
        promote_ans = int(input("{} を成りますか?  0:成らない 1:成る ".format(game.board[to_coordinate[1]][to_coordinate[0]].name)))
        sente_nari_koma = {"FU":"TO","KY":"NKY","KE":"NKE","GI":"NGI","KK":"UMA","HI":"RYU"}
        gote_nari_koma = {"EFU":"ETO","EKY":"ENKY","EKE":"ENKE","EGI":"ENGI","EKK":"EUMA","EHI":"ERYU"}

        #成りコマのクラスを値に持つdict
        nari_koma_class = {"TO":TO,"NKY":NKY,"NKE":NKE,"NGI":NGI,"UMA":UMA,"RYU":RYU}

        if promote_ans == 1 and game.current_player:
            nari_koma = sente_nari_koma[game.board[to_coordinate[1]][to_coordinate[0]].name]
            game.board[to_coordinate[1]][to_coordinate[0]] = nari_koma_class[nari_koma](nari_koma,sente_koma[nari_koma],narikoma_dir_dis[nari_koma],[to_coordinate[1],to_coordinate[0]],"s")

        elif promote_ans == 1 and not game.current_player:
            nari_koma = gote_nari_koma[game.board[to_coordinate[1]][to_coordinate[0]].name]
            game.board[to_coordinate[1]][to_coordinate[0]] = nari_koma_class[nari_koma[1:]](nari_koma,gote_koma[nari_koma],narikoma_dir_dis[nari_koma[1:]],[to_coordinate[1],to_coordinate[0]],"g")


class FU(Shogi_koma):
    def __init__(self,name,num,dir_dis,coord,ally_flag):
        super().__init__(name,num,dir_dis,coord,ally_flag)


class KYO(Shogi_koma):
    def __init__(self,name,num,dir_dis,coord,ally_flag):
        super().__init__(name,num,dir_dis,coord,ally_flag)


class KEIMA(Shogi_koma):
    def __init__(self,name,num,dir_dis,coord,ally_flag):
        super().__init__(name,num,dir_dis,coord,ally_flag)


class GIN(Shogi_koma):
    def __init__(self,name,num,dir_dis,coord,ally_flag):
        super().__init__(name,num,dir_dis,coord,ally_flag)


class KIN(Shogi_koma):
    def __init__(self,name,num,dir_dis,coord,ally_flag):
        super().__init__(name,num,dir_dis,coord,ally_flag)


class KAKU(Shogi_koma):
    def __init__(self,name,num,dir_dis,coord,ally_flag):
        super().__init__(name,num,dir_dis,coord,ally_flag)


class HISYA(Shogi_koma):
    def __init__(self,name,num,dir_dis,coord,ally_flag):
        super().__init__(name,num,dir_dis,coord,ally_flag)


class OU(Shogi_koma):
    def __init__(self,name,num,dir_dis,coord,ally_flag):
        super().__init__(name,num,dir_dis,coord,ally_flag)


class TO(Shogi_koma):
    def __init__(self,name,num,dir_dis,coord,ally_flag):
        super().__init__(name,num,dir_dis,coord,ally_flag)


class NKY(Shogi_koma): #成香
    def __init__(self,name,num,dir_dis,coord,ally_flag):
        super().__init__(name,num,dir_dis,coord,ally_flag)


class NKE(Shogi_koma): #成桂
    def __init__(self,name,num,dir_dis,coord,ally_flag):
        super().__init__(name,num,dir_dis,coord,ally_flag)


class NGI(Shogi_koma): #成銀
    def __init__(self,name,num,dir_dis,coord,ally_flag):
        super().__init__(name,num,dir_dis,coord,ally_flag)


class UMA(Shogi_koma):
    def __init__(self,name,num,dir_dis,coord,ally_flag):
        super().__init__(name,num,dir_dis,coord,ally_flag)


class RYU(Shogi_koma):
    def __init__(self,name,num,dir_dis,coord,ally_flag):
        super().__init__(name,num,dir_dis,coord,ally_flag)


class Empty(Shogi_koma):
    def __init__(self,name,num,dir_dis,coord,ally_flag):
        super().__init__(name,num,dir_dis,coord,ally_flag)


class Wall(Shogi_koma):
    def __init__(self,name,num,dir_dis,coord,ally_flag):
        super().__init__(name,num,dir_dis,coord,ally_flag)


#駒台クラス．先手用と後手用を作成する．
class Koma_dai:
    def __init__(self,teban):
        #とった駒を保持しておく配列．
        self.koma_dai = []

        #プレイヤーの手番．
        #"s"が先手，"g"が後手.
        self.teban = teban

    #駒を駒台に置くメソッド．
    #引数koma_nameには駒台に置く駒の名前が入る．
    def retain_koma(self,koma_name):
        self.koma_dai.append(koma_name)

    #駒を盤に打つメソッド．
    #引数gameはShogi_playのインスタンスを格納する．
    def put_koma(self,game):
        sente_koma_kanji = {"歩":"FU","香":"KY","桂":"KE","銀":"GI","金":"KI","角":"KK","飛":"HI"}
        gote_koma_kanji = {"歩":"EFU","香":"EKY","桂":"EKE","銀":"EGI","金":"EKI","角":"EKK","飛":"EHI"}

        koma_class = {"歩":FU,"香":KYO,"桂":KEIMA,"銀":GIN,"金":KIN,"角":KAKU,"飛":HISYA}

        print("{} の持ち駒です．".format("先手")) if self.teban == "s" else print("{} の持ち駒です．".format("後手"))
        for i in self.koma_dai:
            print(i,end="")
        print("\n")

        #駒の名前を漢字で入力
        n = input("どれを打ちますか．駒の名前を入力してください．> ")
        x,y = map(int,input("どこに打ちますか．座標を入力してください．(x,y)> ").split())
        if isinstance(game.board[y][x],Empty):
            if self.teban == "s":
                if n == "歩":
                    if y <= 1 or self.ni_fu(game,[x,y]):
                        print("({},{}) に歩は打てません．(y座標が1か，二歩です.)".format(x,y))
                        return
                if n == "香":
                    if y <= 1:
                        print("({},{}) に香は打てません．（y座標が1です．）".format(x,y))
                        return
                if n == "桂":
                    if y <= 2:
                        print("({},{}) に桂は打てません．（y座標が2以下です．）".format(x,y))
                        return

                game.board[y][x] = koma_class[n](sente_koma_kanji[n],sente_koma[sente_koma_kanji[n]],koma_dir_dis[sente_koma[sente_koma_kanji[n]]],[y,x],"s")
                self.koma_dai.remove(n)
                game.current_player = not game.current_player
                game.turns += 1

            elif self.teban == "g":
                if n == "歩":
                    if y >= 9 or self.ni_fu(game,[x,y]):
                        print("({},{}) に歩は打てません．(y座標が9か，二歩です.)".format(x,y))
                        return
                if n == "香":
                    if y >= 9:
                        print("({},{}) に香は打てません．(y座標が9です．)".format(x,y))
                        return
                if n == "桂":
                    if y >= 8:
                        print("({},{}) に桂は打てません．（y座標が8以上です．）".format(x,y))
                        return

                game.board[y][x] = koma_class[n](gote_koma_kanji[n],gote_koma[gote_koma_kanji[n]],koma_dir_dis[gote_koma[gote_koma_kanji[n]]-200],[y,x],"g")
                self.koma_dai.remove(n)
                game.current_player = not game.current_player
                game.turns += 1
        else:
            print("({},{}) に {} はおけません．".format(x,y,n))

    #引数gameにはShogi_playのインスタンスが入る．
    #二歩のチェック． coordinateには動かしたい先の座標が入る.coordinate = [x,y]
    #二歩だったらTrueを返す．
    def ni_fu(self,game,coordinate):
        if self.teban == "s":
            #上方向．
            y_tmp = coordinate[1] - 1
            x_tmp = coordinate[0]
            while y_tmp >= 1:
                if isinstance(game.board[y_tmp][x_tmp],FU) and game.board[y_tmp][x_tmp].ally_flag == "s":
                    return True
                y_tmp -= 1

            #下方向．
            y_tmp = coordinate[1] + 1
            x_tmp = coordinate[0]
            while y_tmp <= 9:
                if isinstance(game.board[y_tmp][x_tmp],FU) and game.board[y_tmp][x_tmp].ally_flag == "s":
                    return True
                y_tmp += 1

            return False

        elif self.teban == "g":
            #上方向
            y_tmp = coordinate[1] + 1
            x_tmp = coordinate[0]
            while y_tmp <= 9:
                if isinstance(game.board[y_tmp][x_tmp],FU) and game.board[y_tmp][x_tmp].ally_flag == "g":
                    return True
                y_tmp += 1

            #下方向．
            y_tmp = coordinate[1] - 1
            x_tmp = coordinate[0]
            while y_tmp >= 1:
                if isinstance(game.board[y_tmp][x_tmp],FU) and game.board[y_tmp][x_tmp].ally_flag == "g":
                    return True
                y_tmp -= 1

            return False


#main関数
def main():
    game = Shogi_play()

    while 1:
        game.display_board()
        select = int(input("数字を選んでください. 1:駒を動かす 2:駒を打つ 3:投了> "))
        if select == 1:
            x,y = map(int,input("動かしたい駒の座標を入力してください．(x,y)> ").split())
            game.move(x,y)
        if select == 2:
            if game.current_player:
                game.sente_koma_dai.put_koma(game)
            elif not game.current_player:
                game.gote_koma_dai.put_koma(game)
        if select == 3:
            game.touryo()
            break


if __name__ == "__main__":
    main()
