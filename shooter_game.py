from random import *
from pygame import *
win_height = 700
win_width = 500
x1=350
y1=390
y2=-10
window=display.set_mode((700,500))
clock = time.Clock()
FPS=60
display.set_caption("ASTROPAWS")
background=transform.scale(image.load("galaxy.jpg"),(win_height,win_width))
window.blit(background,(0,0))
monsters =sprite.Group()
bullets=sprite.Group()
cucumbers=sprite.Group()
fishes=sprite.Group()
font.init()
fontl=font.Font(None, 36)
lost=0
total=0
lifes=1
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, height, weight):
        super().__init__()
        self.image=transform.scale(image.load(player_image), (height,weight))
        self.speed=player_speed
        self.rect = self.image.get_rect()
        self.rect.x=player_x
        self.rect.y=player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        global lost
        global total
        global lifes
        if total<5 and lost<3 and lifes>0:
            keys_pressed=key.get_pressed()
            if keys_pressed[K_a] and self.rect.x >-50:
                self.rect.x -=self.speed
            if keys_pressed[K_d] and self.rect.x <595:
                self.rect.x +=self.speed
            if keys_pressed[K_w] and self.rect.y >5:
                self.rect.y -=self.speed
            if keys_pressed[K_s] and self.rect.y <395:
                self.rect.y +=self.speed
        
class Enemy(GameSprite):
    def update(self):
        global lost
        global total
        global lifes
        if total>=5 or lost>=3 or lifes<=0:
            self.kill()
        self.rect.y+=self.speed
        if self.rect.y==500:
            lost+=1
        
        

class Bullet(GameSprite):
    def update(self):
        global lost
        global total
        global lifes
        if total>=5 or lost>=3 or lifes<=0:
            self.kill()
        self.rect.y-=self.speed
            
class Heal(GameSprite):
    def update(self):
        global lost
        global total
        global lifes
        if total>=5 or lost>=3 or lifes<=0:
            self.kill()
        self.rect.y+=self.speed
        

class Kill(GameSprite):
    def update(self):
        global lost
        global total
        global lifes
        if total>5 or lost>3 or lifes<=0:
            self.kill()
        self.rect.y+=self.speed
        

cat =Player('memecat.png', x1, y1,4, 90,110)
font.init()
font = font.Font(None, 70)
win = font.render('YOU WIN!', True, (255,0,0))
lose = font.render('YOU LOSE!', True, (255,0,0))
death=font.render('YOU DIED!', True, (169,0,0))
game=True
finish = False
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

wait=120
wait2=120
wait0=240
wait3=360
while game:
    for e in event.get():
        if e.type == QUIT:
            game=False
    window.blit(background,(0,0))
    cat.reset()
    cat.update()
    if finish!=True:
        if wait==0:
            wait=120
            monsters.add(Enemy('memec.png', randint(5,550), y2, randint(2,4),150,100))
        else:
            wait-=1
        #for i in monsters:
            #i.reset()
            #i.update()
            #if wait !=0:
        if wait0==0:
            wait0=240
            cucumbers.add(Kill('cucumber2.png', randint(5,550), y2, randint(3,7),90,90))
        else:
            wait0-=1
        if wait3==0:
            wait3=360
            fishes.add(Heal('downloadf.png', randint(5,550), y2, randint(3,5),80,50))
        else:
            wait3-=1
        monsters.draw(window)
        cucumbers.draw(window)
        fishes.draw(window)
        bullets.draw(window)
        for e in event.get():
            if e.type == QUIT:
                game=False
            elif e.type == KEYDOWN:
                if e.key==K_e:
                    mixer.music.load('fire.ogg')
                    mixer.music.play()
                    bullets.add(Bullet('bullet.png', cat.rect.x+20, cat.rect.y, 7,50,50))
        text_lose=fontl.render("lost:"+str(lost), 1,(255,255,255))
        text_win=fontl.render("total:"+str(total),1,(255,255,255))
        text_lifes=fontl.render(str(lifes),1,(255,0,0))
        window.blit(text_lose,(2,2))
        window.blit(text_win,(2,30))
        window.blit(text_lifes,(680,1))
    if total==5:
        window.blit(win,(200,200))
        finish=True
        if wait2 == 0:
            wait2 = 120
            lost=0
            total=0
            lifes=1
            finish=False
        else:
            wait2-=1
    if lost==3:
        finish=True
        window.blit(lose,(200,200))
        if wait2 == 0:
            wait2 = 120
            lost=0
            total=0
            lifes=1
            finish=False
        else:
            wait2-=1
    if lifes==0:
        finish=True
        window.blit(death,(200,200))
        if wait2 == 0:
            wait2 = 120
            lost=0
            lifes=1
            total=0
            finish=False
        else:
            wait2-=1
    sprite_list=sprite.groupcollide(bullets, monsters,True,True)
    sprite_list2=sprite.spritecollide(cat, fishes,True)
    sprite_list3=sprite.spritecollide(cat, cucumbers,True)
    for f in sprite_list2: 
        lifes+=1
    for s in sprite_list: 
        total+=1
    for d in sprite_list3: 
        lifes-=1
    monsters.update()
    bullets.update()
    cucumbers.update()
    fishes.update()
    
    display.update()
    clock.tick(FPS)
