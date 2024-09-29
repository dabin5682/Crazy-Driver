#불러오기
import pygame
import sys,os,random,time
from pygame.locals import *
#게임 색상 정의
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
#변수 초기화
paused = False
moveSpeed = 5
startSpeed = 10
moveSpeed = startSpeed
maxSpeed = 20
score = 0
oil_display_time = 5
start_time = None
#적의 변수 초기화
enemy_count = 1
enemies = []
#게임경로 설정
textFonts = ['comicsansms','arial']
textSize = 48
GAME_ROOT_FOLDER = os.path.dirname(__file__)
IMAGE_FOLDER = os.path.join(GAME_ROOT_FOLDER,"Images")
#Gameover 함수 점수와 게임오버 화면출력               
    #게임종료 문자열 생성
def GameOver():
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
#게임 설정 초기화
pygame.init()
clock = pygame.time.Clock()

#이미지 불러오기
IMG_ROAD =pygame.image.load(os.path.join(IMAGE_FOLDER, "Road.png"))
IMG_PLAYER =pygame.image.load(os.path.join(IMAGE_FOLDER,"Player.png"))
IMG_Oil =pygame.image.load(os.path.join(IMAGE_FOLDER,"Oil.png"))
#화면을 가릴 오일 이미지 사이즈 설정
IMG_Oil_width = 400
IMG_Oil_height = 400
IMG_Oil = pygame.transform.scale(IMG_Oil, (IMG_Oil_width, IMG_Oil_height))
#화면을 방해할 오일 위치설정
oil_x = (IMG_ROAD.get_width() - IMG_Oil_width) // 2
oil_y = (IMG_ROAD.get_height() - IMG_Oil_height) //2-200
#게임 적 이미지 불러오기
IMG_ENEMIES =[]
IMG_ENEMIES.append(pygame.image.load(os.path.join(IMAGE_FOLDER,"Enemy.png")))
IMG_ENEMIES.append(pygame.image.load(os.path.join(IMAGE_FOLDER,"Enemy2.png")))
IMG_ENEMIES.append(pygame.image.load(os.path.join(IMAGE_FOLDER,"Enemy3.png")))
IMG_ENEMIES.append(pygame.image.load(os.path.join(IMAGE_FOLDER,"IceCube.png")))
IMG_ENEMIES.append(pygame.image.load(os.path.join(IMAGE_FOLDER,"Oil.png")))

#배경화면 초기화하기
screen = pygame.display.set_mode(IMG_ROAD.get_size())
#플레이어 초기위치 설정
h=IMG_ROAD.get_width()//2
v=IMG_ROAD.get_height()-(IMG_PLAYER.get_height()//2)
#플레이어 스프라이트 만들기
player = pygame.sprite.Sprite()
player.image = IMG_PLAYER
player.surf = pygame.Surface(IMG_PLAYER.get_size())
player.rect = player.surf.get_rect(center = (h,v))

while True:
    #틱설정
    clock.tick(60)
    #배경화면 설정
    pygame.display.set_caption("Crazy Driver-Score "+str(score))
    screen.blit(IMG_ROAD,(0,0))
    #캐릭터 화면 배치
    screen.blit(player.image,player.rect)
    # 점수에 따라 적의 수 변경
    if score >= 20:
        enemy_count = 3 
    elif score >= 10:
        enemy_count = 2  
    else:
        enemy_count = 1
    # 적 생성 및 배치
    while len(enemies) < enemy_count: # enemy_count 개수만큼 위에서 적을 생성
        eNum = random.randrange(0, len(IMG_ENEMIES))
        hl = IMG_ENEMIES[eNum].get_width() // 2
        hr = IMG_ROAD.get_width() - (IMG_ENEMIES[eNum].get_width() // 2)
        h = random.randrange(hl, hr)
        v = 0 

        # enemy 스프라이트 설정
        enemy = pygame.sprite.Sprite()
        enemy.image = IMG_ENEMIES[eNum]
        enemy.surf = pygame.Surface(IMG_ENEMIES[eNum].get_size())
        enemy.rect = enemy.surf.get_rect(center=(h, v))
        enemies.append(enemy)  

    #적의 이동 설정 moveSpeed로 이동
    for enemy in enemies[:]: 
        screen.blit(enemy.image, enemy.rect)
        enemy.rect.move_ip(0, moveSpeed)

        #적이 무사히 넘어가면 1점증가
        if enemy.rect.bottom > IMG_ROAD.get_height():
            enemies.remove(enemy)  
            score += 1  
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
           
        # 오일장애물일때
        elif eNum == 4:
            if start_time is None:
                start_time = time.time()    
        else: 
            GameOver() #충돌시 게임오버 함수출력
    # 오일 표시 처리
    if start_time is not None:
        if time.time() - start_time < oil_display_time:
            screen.blit(IMG_Oil, (oil_x, oil_y))
        else:
            overlay_start_time = None  

    for event in pygame.event.get():
        #게임을 종료하나요?
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
  