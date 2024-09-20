#불러오기
import pygame
import sys,os
from pygame.locals import *


#게임 색상 정의

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)

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
#게임화면 초기화하기
screen = pygame.display.set_mode(IMG_ROAD.get_size())

while True:
    screen.blit(IMG_ROAD,(0,0))
    for event in pygame.event.get():
        #게임을 그만두나요?
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()