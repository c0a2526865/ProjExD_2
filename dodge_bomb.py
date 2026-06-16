import os
import sys
import pygame as pg
import random


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool,bool]:  # 型ヒント、関数アノテーション
    """
    引数：こうかとんRect or 爆弾Rect
    戻り値：判定結果タプル（横方向判定結果、縦方向判定結果）
    TRUE：画面内　/　FALSE：画面外
    """
    yoko,tate = True,True
    if rct.left < 0 or WIDTH < rct.right:   # 横方向の判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:   # 縦方向の判定
        tate = False
    return yoko,tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    # こうかとん初期化
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
#   爆弾初期化
    bb_img = pg.Surface((20,30))  # 爆弾用のからのSurface
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)   # 半径10の赤い丸を描画
    bb_img.set_colorkey((0, 0, 0))  # 円の周りの四角を消す
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0,WIDTH)#初期座標横
    bb_rct.centery = random.randint(0,HEIGHT)#初期座標縦
    vx,vy = 5,5

    DELTA = {
        pg.K_UP:(0,-5),#右上矢印キー
        pg.K_DOWN:(0,5),#下矢印キー
        pg.K_LEFT:(-5,0),#左矢印キー
        pg.K_RIGHT:(5,0),#右矢印キー
    }
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            print("GAME　OVER")
            return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        for key,mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]#横方向の移動量
                sum_mv[1] += mv[1]#縦方向の移動量
        
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])    # 動きをなかったことにする
        screen.blit(kk_img, kk_rct)


        bb_rct.move_ip(vx,vy)#速度の設定
        yoko,tate = check_bound(bb_rct)
        if not yoko:  # 横方向にはみ出ていたら
            vx *= -1
        if not tate:  # 縦方向にはみ出ていたら
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
