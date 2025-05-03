import json
import random
import pyxel

# 音楽のパス
MUSIC_FILE = "music/music"

# シーン番号の定義
SNO_TITLE = 0
SNO_STAGESET = 10
SNO_PLAY = 11
SNO_SFINISH = 12
SNO_END = 20

scene = SNO_TITLE  # ゲームの進行を管理する変数
tmr = 0  # シーン内でカウントするタイマー変数

# イヌの状態 0:通常 1:提供
ply_state = 0
PLY_ANIM_NORMAL = 0
PLY_ANIM_TEIKYO = 1

# アニメーション管理用
animation_timer = 0
ply_ani = 0
FRAME_INTERVAL = 15

PLY_ANIM = [(0, 16), (16, 16)]
PLY_END_ANIM = [(0, 32), (16, 32)]

# カーソル位置
cursor_pos = 0

# カーソル座標
CURSOR_POS_LIST = [
    (0, 64),
    (16, 64),
    (32, 64),
    (48, 64),
    (0, 80),
    (16, 80),
    (32, 80),
    (48, 80),
    (0, 96),
    (16, 96),
    (32, 96),
    (48, 96),
    (0, 112),
    (16, 112),
    (32, 112),
    (48, 112),
]

# 選択した材料
select_element = [0, 0, 0]

# 客の注文
customer_order = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
# 客の見た目 0～3
customer_type = [0, 1, 2, 3]
# 客の注文の状態 0:注文無し 1:注文あり 2:提供済み
order_state = [0, 0, 0]
# 捌いた客
customer_point = 0

# 制限時間
TIME_LIMIT = 60

# デバッグモード
DEBUG_MODE = False


class App:
    def __init__(self):
        # ここで起動時の処理をします
        pyxel.init(64, 128, title="bowkery")
        pyxel.load("bowkery.pyxres")
        # pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def update(self):
        # ここで毎フレームの更新作業をします
        global scene, tmr, animation_timer, ply_ani, cursor_pos, customer_order, order_state, customer_type, ply_state, customer_point
        tmr += 1

        if scene == SNO_TITLE:
            ply_ani += 1

            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
                scene = SNO_STAGESET
                # scene = SNO_PLAY
                customer_point = 0
                cursor_pos = 0
                select_element[0] = 0
                select_element[1] = 0
                select_element[2] = 0
                order_state[0] = 0
                order_state[1] = 0
                order_state[2] = 0
                customer_order = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
                ply_ani = 0
                tmr = 0

        elif scene == SNO_STAGESET:
            if tmr == 1:
                pyxel.play(3, 6)
                ply_ani = 0

            # カウントダウン
            if 30 * 3 == tmr:
                pyxel.play(3, 7)
            elif 30 * 2 == tmr:
                pyxel.play(3, 6)
            elif 30 * 1 == tmr:
                pyxel.play(3, 6)

            if 30 * 4 < tmr:
                tmr = 0
                scene = SNO_PLAY

                with open(f"./{MUSIC_FILE}.json", "rt") as fin:
                    self.music = json.loads(fin.read())

                for ch, sound in enumerate(self.music):
                    pyxel.sounds[ch].set(*sound)
                    pyxel.play(ch, ch, loop=True)
                pyxel.load("bowkery.pyxres")

        elif scene == SNO_PLAY:
            # 注文生成
            for index, wkOrder in enumerate(customer_order):
                if order_state[index] == 0:
                    customer_type.append(random.randint(0, 3))
                    wkOrder[0] = random.randint(1, 4)
                    wkOrder[1] = random.randint(1, 4)
                    wkOrder[2] = random.randint(1, 4)
                    order_state[index] = 1

                # 注文の生成を途中でやめる
                if index == 0:
                    break

            # カーソル移動
            # 上
            if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
                # カーソル位置を-4する 負の数になるなら処理しない
                if (cursor_pos - 4) >= 0:
                    cursor_pos = cursor_pos - 4

            # 下
            if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(
                pyxel.GAMEPAD1_BUTTON_DPAD_DOWN
            ):
                # カーソル位置を+4する 15以上または左下右下になるなら処理しない
                if (
                    (cursor_pos + 4) != 12
                    and (cursor_pos + 4) != 15
                    and (cursor_pos + 4) <= 15
                ):
                    cursor_pos = cursor_pos + 4

            # 右
            if pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(
                pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT
            ):
                # カーソル位置を+1する 現在位置が右端なら処理しない
                if (
                    (cursor_pos != 3)
                    and (cursor_pos != 7)
                    and (cursor_pos != 11)
                    and (cursor_pos != 15)
                    and (cursor_pos + 1) != 15
                ):
                    cursor_pos = cursor_pos + 1

            # 左
            if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(
                pyxel.GAMEPAD1_BUTTON_DPAD_LEFT
            ):
                # カーソル位置を-1する 現在位置が左端なら処理しない
                if (
                    (cursor_pos != 0)
                    and (cursor_pos != 4)
                    and (cursor_pos != 8)
                    and (cursor_pos != 12)
                    and (cursor_pos - 1) != 12
                ):
                    cursor_pos = cursor_pos - 1

            # 材料選択
            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):

                if cursor_pos <= 3:
                    # チョコ
                    if select_element[0] == 0:
                        select_element[0] = cursor_pos + 1
                        pyxel.play(3, 0)

                elif cursor_pos <= 7:
                    # 型
                    if select_element[1] == 0:
                        select_element[1] = (cursor_pos - 4) + 1
                        pyxel.play(3, 0)

                elif cursor_pos <= 11:
                    # トッピング
                    if select_element[2] == 0:
                        select_element[2] = (cursor_pos - 8) + 1
                        pyxel.play(3, 0)

                elif cursor_pos == 13:
                    # 提供
                    for index, wkOrder in enumerate(customer_order):
                        # 提供済みならスルー
                        if order_state[index] == 2:
                            continue

                        # 選択した素材が完全一致なら提供
                        if (
                            (select_element[0] == wkOrder[0])
                            and (select_element[1] == wkOrder[1])
                            and (select_element[2] == wkOrder[2])
                        ):
                            select_element[0] = 0
                            select_element[1] = 0
                            select_element[2] = 0
                            order_state[index] = 2

                            # 提供状態のスプライトに変更
                            ply_state = PLY_ANIM_TEIKYO
                            # カーソル位置を初期位置へ
                            cursor_pos = 0
                            # ポイントアップ
                            customer_point += 1
                            pyxel.play(3, 1)

                            # 注文無し以外なくなったら次の注文へ
                            if all(x in {0, 2} for x in order_state):
                                customer_order = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
                                order_state = [0, 0, 0]
                                customer_type.pop(0)
                                break
                            else:
                                break

                elif cursor_pos == 14:
                    # ゴミ箱
                    select_element[0] = 0
                    select_element[1] = 0
                    select_element[2] = 0
                    # カーソル位置を初期位置へ
                    cursor_pos = 0
                    pyxel.play(3, 8)

            if ply_state != PLY_ANIM_NORMAL:
                animation_timer += 1
                if animation_timer >= FRAME_INTERVAL:
                    animation_timer = 0
                    ply_state = PLY_ANIM_NORMAL  # アニメーション終了

            # 終了判定
            if TIME_LIMIT == (tmr // 30) and ply_state == PLY_ANIM_NORMAL:
                scene = SNO_SFINISH
                tmr = 0

        elif scene == SNO_SFINISH:
            if ply_state == PLY_ANIM_NORMAL:
                if FRAME_INTERVAL == tmr:
                    pyxel.stop()
                    pyxel.play(3, 2)

                # 5秒経過後にステージ更新(1秒30フレームなので3倍待つ)
                if 30 * 5 < tmr:
                    scene = SNO_END
                    tmr = 0

        elif scene == SNO_END:
            ply_ani += 1

            if tmr == 1:
                pyxel.playm(0)

            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
                scene = SNO_TITLE
                pyxel.stop()
                ply_ani = 0
                tmr = 0
        pass

    def draw(self):
        # ここで毎フレームの描画作業をします
        pyxel.cls(0)

        if scene == SNO_TITLE:
            # pyxel.blt(30, 16, 1, 0, 0, 64, 32, 0)

            pyxel.blt(8, 16, 1, 0, 0, 64, 32, 0)
            u, v = PLY_ANIM[pyxel.frame_count // 15 % 2]
            pyxel.blt(22, 35, 0, u, v, 16, 16, 0)
            pyxel.text(5, 61, "PRESS [SPACE]", 7)
            pyxel.text(5, 69, "GAME START", 7)

            pyxel.text(5, 85, "2025", 7)
            pyxel.text(5, 92, "OSUSHI TABEZO", 7)

        if scene == SNO_STAGESET or scene == SNO_PLAY or scene == SNO_SFINISH:

            # 材料リストの表示
            pyxel.bltm(0, 0, 0, 0, 0, 64, 128)

            # カーソルの表示
            cursor_x, cursor_y = CURSOR_POS_LIST[cursor_pos]
            pyxel.blt(cursor_x, cursor_y, 0, 16, 0, 16, 16, 0)

            # イヌ
            u, v = PLY_ANIM[pyxel.frame_count // 15 % 2]
            if ply_state == PLY_ANIM_TEIKYO:
                pyxel.blt(2, 30, 0, 32, 16, 16, 16, 0)
            else:
                pyxel.blt(2, 30, 0, u, v, 16, 16, 0)

            # 吹き出し
            pyxel.blt(14, 10, 0, 16, 128, 48, 16, 0)
            pyxel.blt(27, 26, 0, 0, 128, 16, 16, 0)
            # 客
            for index, wkCustomer in enumerate(customer_type):
                pyxel.blt(
                    34 + (11 * index),
                    30,
                    0,
                    (wkCustomer * 2 * 8),
                    144,
                    -16,
                    16,
                    0,
                )

            # 客の注文表示
            for index, wkOrder in enumerate(customer_order):
                # 注文がないなら何もしない
                if order_state[index] == 0:
                    continue

                # チョコ
                customer_choco = wkOrder[0]
                if customer_choco > 0:
                    pyxel.blt(
                        (20 * (index + 1)),
                        10,
                        0,
                        (((customer_choco - 1) * 2) * 8),
                        48,
                        16,
                        16,
                        0,
                    )

                # 型
                customer_mold = wkOrder[1]
                if customer_mold > 0:
                    pyxel.blt(
                        (20 * (index + 1)),
                        10,
                        0,
                        (((customer_mold - 1) * 2) * 8),
                        112,
                        16,
                        16,
                        0,
                    )

                # トッピング
                customer_topping = wkOrder[2]
                if customer_topping > 0:
                    pyxel.blt(
                        (20 * (index + 1)),
                        10,
                        0,
                        (((customer_topping - 1) * 2) * 8),
                        80,
                        16,
                        16,
                        0,
                    )

                # チェックマーク 提供済みなら表示
                if order_state[index] == 2:
                    pyxel.blt((16 * (index + 1)), 10, 0, 32, 0, 16, 16, 0)

            # 選択したものの表示
            # チョコ
            select_choco = select_element[0]
            if select_choco > 0:
                pyxel.blt(24, 47, 0, (((select_choco - 1) * 2) * 8), 48, 16, 16, 0)

            # 型
            select_mold = select_element[1]
            if select_mold > 0:
                pyxel.blt(24, 47, 0, (((select_mold - 1) * 2) * 8), 96, 16, 16, 1)

            # トッピング
            select_topping = select_element[2]
            if select_topping > 0:
                pyxel.blt(24, 47, 0, (((select_topping - 1) * 2) * 8), 80, 16, 16, 0)

            # 開始時のカウントダウン
            if scene == SNO_STAGESET:
                if tmr > 30 * 3:
                    pyxel.text(5, 53, "AM 9:00 OPEN!!", 7)
                elif tmr > 30 * 2:
                    pyxel.text(5, 53, "AM 8:59", 7)
                elif tmr > 30 * 1:
                    pyxel.text(5, 53, "AM 8:58", 7)
                else:
                    pyxel.text(5, 53, "AM 8:57", 7)

            # 制限時間
            if scene == SNO_PLAY:
                pyxel.text(0, 2, "TIME:" + str(TIME_LIMIT - (tmr // 30)), 7)

            if scene == SNO_SFINISH:
                pyxel.text(5, 53, "PM 6:00 CLOSE!!", 7)

        if scene == SNO_END:

            u, v = PLY_END_ANIM[ply_ani // 15 % 2]
            pyxel.text(7, 16, "RESULT", 7)
            pyxel.text(16, 28, "POINT " + str(customer_point), 7)

            pyxel.blt(25, 60, 0, u, v, 16, 16, 0)

            pyxel.text(8, 42, "PRESS [SPACE]", 7)
            pyxel.text(7, 50, "BACK TO TITLE", 7)

        # デバッグ用
        if DEBUG_MODE:
            pyxel.text(
                0, 0, "mouse x:" + str(pyxel.mouse_x) + "y:" + str(pyxel.mouse_y), 7
            )

            # if scene == SNO_SFINISH:
            #     pyxel.text(0, 40, "FINISH", 7)


App()
