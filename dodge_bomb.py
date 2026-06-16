import os
import sys
import time
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


    # 演習課題１
def gameover(screen: pg.Surface) -> None:
    """
    引数：screenSurface
    戻り値：なし
    処理：暗い画面、ゲームオーバーの文字、泣いてるこうかとんを表示
    """
    gam_ovr_img = pg.Surface((WIDTH,HEIGHT))
    gam_ovr_img.set_alpha(200)
    rec_ob = pg.Rect(0,0,WIDTH,HEIGHT)    
    pg.draw.rect(gam_ovr_img,(0,0,0),rec_ob)
    
    fonto = pg.font.Font(None,80)
    txt = fonto.render("Game　Over",True,(255,255,255))
    gam_ovr_img.blit(txt,(WIDTH/2,HEIGHT/2-40))

    kk_naki_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    gam_ovr_img.blit(kk_naki_img,(200,HEIGHT/2-40))

    screen.blit(gam_ovr_img,(0,0))

    pg.display.update()
    time.sleep(5)


# def init_bb_imgs(bb_imgs,bb_accs) -> tuple[list[pg.Surface],list[int]]:
#     """
#     引数： or 爆弾Rect
#     戻り値：判定結果タプル（横方向判定結果、縦方向判定結果）
#     TRUE：画面内　/　FALSE：画面外
#     """
#     for r in range(1,11):
#         bb_img = pg.Surface((20*r,20*r))
#         pg.draw.circle(bb_img,(255,0,0),(10*r,10*r),10*r)
#         bb_imgs.append(bb_img)
#     bb_accs = [a for a in range(1,11)]
#     return bb_img,bb_accs


# 演習課題３
def get_kk_imgs() -> dict[tuple[int,int],pg.Surface]:
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    # kk_rct = kk_img.get_rect()
    kk_imgs = {
    (0, 0): kk_img,
    (+5, 0): pg.transform.flip(kk_img, True, False), # 右
    (-5, 0): kk_img, # 左
    (0, -5): pg.transform.rotozoom(kk_img, -90, 1.0), # 上
    (0, +5): pg.transform.rotozoom(kk_img, 90, 1.0), # 下
    (+5, -5): pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), 45, 1.0), # 右上
    (+5, +5): pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), -45, 1.0), # 右下
    (-5, -5): pg.transform.rotozoom(kk_img, -45, 1.0), # 左上
    (-5, +5): pg.transform.rotozoom(kk_img, 45, 1.0), # 左下
    }
    return kk_imgs


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
    # count = 0

    # 加速と大きさの設定
    # bb_imgs = []
    # bb_accs = []
    
    # init_bb_imgs(bb_imgs,bb_accs)
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
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
        
        kk_imgs = get_kk_imgs()
        kk_img = kk_imgs[(0,0)]

        
        for key,mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]#横方向の移動量
                sum_mv[1] += mv[1]#縦方向の移動量

        if tuple(sum_mv) in kk_imgs:
            kk_img = kk_imgs[tuple(sum_mv)]

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])    # 動きをなかったことにする
            get_kk_imgs()

        screen.blit(kk_img, kk_rct)

        # if tmr == 250  or tmr == 500 or tmr == 750:
        #     bb_imgs_youso = bb_imgs[count]
        #     bb_rct.width = bb_imgs_youso.get_rect().width
        #     count+=1

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
