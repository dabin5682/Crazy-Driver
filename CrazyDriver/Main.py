#불러오기
import pygame
import sys,os,random,time
from pygame.locals import *
#게임 색상 정의
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
paused = False
moveSpeed = 5
startSpeed = 5
moveSpeed = startSpeed
maxSpeed = 10
score = 0
eNum = -1
overlay_start_time = None
#게임경로 설정
textFonts = ['comicsansms','arial']
textSize = 48
GAME_ROOT_FOLDER = os.path.dirname(__file__)
IMAGE_FOLDER = os.path.join(GAME_ROOT_FOLDER,"Images")
#Gameover 함수
def GameOver():
    #게임종료 문자열 생성
    fontGameOver = pygame.font.SysFont(textFonts,textSize)
    textGameOver = fontGameOver.render("GameOver",True,RED)
    rectGameOver = textGameOver.get_rect()
    rectGameOver.center = (IMG_ROAD.get_width()//2,IMG_ROAD.get_height()//4)
    #스코어 생성
    fontScore = pygame.font.SysFont(textFonts,textSize)
    textScore = fontScore.render("Score : "+ str(score),True,WHITE)
    rectScore = textScore.get_rect()
    rectScore.center = (IMG_ROAD.get_width()//2,IMG_ROAD.get_height()//2)
    #검은화면에 게임오버 메세지,점수 출력
    screen.fill(BLACK)
    screen.blit(textGameOver,rectGameOver)
    screen.blit(textScore,rectScore)
    #출력 업데이트
    pygame.display.update()
    #객체제거
    player.kill()
    enemy.kill()
    #일시정지
    time.sleep(5)

    pygame.quit()
    sys.exit()
#게임 시작은 이곳에서
#파이 게임 초기화 하기
pygame.init()
#프레임 매니저 초기화하기
clock = pygame.time.Clock()
clock.tick(60)
#제목 표시줄 설정
pygame.display.set_caption("Crazy Driver")

#이미지 불러오기
IMG_ROAD =pygame.image.load(os.path.join(IMAGE_FOLDER, "Road.png"))
IMG_PLAYER =pygame.image.load(os.path.join(IMAGE_FOLDER,"Player.png"))
IMG_Oil =pygame.image.load(os.path.join(IMAGE_FOLDER,"Oil.png"))
IMG_Oil_width = 300
IMG_Oil_height = 300
IMG_Oil = pygame.transform.scale(IMG_Oil, (IMG_Oil_width, IMG_Oil_height))
#화면을 방해할 오일 위치설정
oil_x = (IMG_ROAD.get_width() - IMG_Oil_width) // 2
oil_y = (IMG_ROAD.get_height() - IMG_Oil_height) // 2
IMG_ENEMIES =[]
IMG_ENEMIES.append(pygame.image.load(os.path.join(IMAGE_FOLDER,"Enemy.png")))
IMG_ENEMIES.append(pygame.image.load(os.path.join(IMAGE_FOLDER,"Enemy2.png")))
IMG_ENEMIES.append(pygame.image.load(os.path.join(IMAGE_FOLDER,"Enemy3.png")))
IMG_ENEMIES.append(pygame.image.load(os.path.join(IMAGE_FOLDER,"IceCube.png")))
IMG_ENEMIES.append(pygame.image.load(os.path.join(IMAGE_FOLDER,"Oil.png")))
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
while True:
    clock.tick(60)
    #배경화면 설정
    pygame.display.set_caption("Crazy Driver-Score "+str(score))
    screen.blit(IMG_ROAD,(0,0))
    #캐릭터 화면 배치
    screen.blit(player.image,player.rect)
    #적 설정
    if eNum == -1:
        eNum = random.randrange(0,len(IMG_ENEMIES))
        hl= IMG_ENEMIES[eNum].get_width()//2
        hr = IMG_ROAD.get_width()-(IMG_ENEMIES[eNum].get_width()//2)    
        h = random.randrange(hl,hr)
        v=0
        #enemy 스프라이트 설정
        enemy = pygame.sprite.Sprite()
        enemy.image = IMG_ENEMIES[eNum]
        enemy.surf = pygame.Surface(IMG_ENEMIES[eNum].get_size())
        enemy.rect = enemy.surf.get_rect(center = (h,v))
    #적 배치
    screen.blit(enemy.image,enemy.rect)
    #적을 아래로 움직이기
    enemy.rect.move_ip(0,moveSpeed)
    
    if eNum == -1:
        eNum = random.randrange(0,len(IMG_ENEMIES))
        hl= IMG_ENEMIES[eNum].get_width()//2
        hr = IMG_ROAD.get_width()-(IMG_ENEMIES[eNum].get_width()//2)
        h = random.randrange(hl,hr)
        v=0
        #enemy 스프라이트
        enemy = pygame.sprite.Sprite()
        enemy.image = IMG_ENEMIES[eNum]
        enemy.surf = pygame.Surface(IMG_ENEMIES[eNum].get_size())
        enemy.rect = enemy.surf.get_rect(center = (h,v))
    if (enemy.rect.bottom > IMG_ROAD.get_height()):
        #enemy 객체없애기
        enemy.kill()
        #enemy 없는상태 확인
        eNum = -1
        score += 1
        if moveSpeed <maxSpeed:
            moveSpeed +=1
    keys = pygame.key.get_pressed()
    #일시정지
    if paused:
        if not keys[K_SPACE]:
            #일시정지 종료
            moveSpeed = tempSpeed
            paused = False
     
    else:
    #플레이어 이동설정    
        if keys[K_LEFT] and player.rect.left>0:
            player.rect.move_ip(-moveSpeed,0)
        if player.rect.left < 0:
            player.rect.left = 0
        if keys[K_RIGHT] and player.rect.right < IMG_ROAD.get_width():
            player.rect.move_ip(moveSpeed,0)
        if  player.rect.right > IMG_ROAD.get_width():
            player.rect.right = IMG_ROAD.get_width()
        if keys[K_SPACE]:
            tempSpeed = moveSpeed
            moveSpeed = 0
            paused = True
    #충돌 확인
    if eNum> 0 and pygame.sprite.collide_rect(player,enemy):
        # 얼음장애물일때
        if eNum == 3:
            moveSpeed =  startSpeed
            #충돌시 게임오버
        # 오일장애물일때
        elif eNum == 4:
            if overlay_start_time is None:
                overlay_start_time = time.time() #충돌시간 기록

            if time.time() - overlay_start_time < 5:
                screen.blit(IMG_Oil,(oil_x,oil_y))
            else:
                overlay_start_time = None           
        else: 
            GameOver()
    for event in pygame.event.get():
        #게임을 그만두나요?
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
  