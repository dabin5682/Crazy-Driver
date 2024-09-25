#불러오기
import pygame
import sys,os,random
from pygame.locals import *


#게임 색상 정의

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
moveSpeed = 5

#게임경로 설정
GAME_ROOT_FOLDER = os.path.dirname(__file__)
IMAGE_FOLDER = os.path.join(GAME_ROOT_FOLDER,"Images")
#게임 시작은 이곳에서
#파이 게임 초기화 하기
pygame.init()
#프레임 매니저 초기화하기
clock = pygame.time.Clock()
#프레임 레이트 설정하기
clock.tick(60)

#제목 표시줄 설정
pygame.display.set_caption("Crazy Driver")

#이미지 불러오기
IMG_ROAD =pygame.image.load(os.path.join(IMAGE_FOLDER, "Road.png"))
IMG_PLAYER =pygame.image.load(os.path.join(IMAGE_FOLDER,"Player.png"))
IMG_ENEMY =pygame.image.load(os.path.join(IMAGE_FOLDER,"Enemy.png"))
#게임화면 초기화하기
screen = pygame.display.set_mode(IMG_ROAD.get_size())

#게임 객체 만들기
#플레이어 초기위치 설정
h=IMG_ROAD.get_width()//2
v=IMG_ROAD.get_height()-(IMG_PLAYER.get_height()//2)

#플레이어 스프라이트 만들기
player = pygame.sprite.Sprite()
player.image = IMG_PLAYER
player.surf = pygame.Surface(IMG_PLAYER.get_size())
player.rect = player.surf.get_rect(center = (h,v))

#적
#적 초기위치 설정
hl= IMG_ENEMY.get_width()//2
hr = IMG_ROAD.get_width()-(IMG_ENEMY.get_width()//2)
h = random.randrange(hl,hr)
v=0
#적 스프라이트 설정
enemy = pygame.sprite.Sprite()
enemy.image = IMG_ENEMY
enemy.surf = pygame.Surface(IMG_ENEMY.get_size())
enemy.rect = enemy.surf.get_rect(center = (h,v))



while True:
    #배경화면
    screen.blit(IMG_ROAD,(0,0))
    #캐릭터 화면 배치
    screen.blit(player.image,player.rect)
    screen.blit(enemy.image,enemy.rect)
    keys = pygame.key.get_pressed()
    #적을 아래로 움직이기
    enemy.rect.move_ip(0,moveSpeed)
    if keys[K_LEFT] and player.rect.left>0:
        player.rect.move_ip(-moveSpeed,0)
        if player.rect.left < 0:
            player.rect.left = 0
    if keys[K_RIGHT] and player.rect.right < IMG_ROAD.get_width():
        player.rect.move_ip(moveSpeed,0)
        if player.rect.right > IMG_ROAD.get_width():
            player.rect.right = IMG_ROAD.get_width()
    for event in pygame.event.get():
        #게임을 그만두나요?
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()