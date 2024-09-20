#불러오기
import pygame

#게임 색상 정의

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)

#게임 시작은 이곳에서
#파이 게임 초기화 하기
pygame.init()
#프레임 매니저 초기화하기
clock = pygame.time.Clock()
#프레임 레이트 설정하기
clock.tick(60)

#제목 표시줄 설정
pygame.display.set_caption("Crazy Driver")

screen = pygame.display.set_mode((500,800))
screen.fill(WHITE)
pygame.display.update()