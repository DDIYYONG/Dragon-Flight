import pygame
import random as r
import time
import fontTools

pygame.init()       #파이게임 초기화(필수)

icon = pygame.image.load("images\\시작화면.png")        #윈도우 프레임 아이콘
pygame.display.set_icon(icon)

end_game = False            #게임종료시 불린으로 빠져나가기

screen_width = 740              #프레임세팅
screen_height = 986
screen= pygame.display.set_mode((screen_width,screen_height)) 
pygame.display.set_caption("드래곤 플라이트")
clock = pygame.time.Clock()     #FPS세팅

def ready():                #준비화면 메소드
    global end_game
    
    icon = pygame.image.load("images\\시작화면.png")
    ico=pygame.transform.scale(icon,(580,804))
    ico_rect = ico.get_rect()
    ico_y_pos = 50
    ico_x_pos = 80
    ico_to_y = 0
    ico_speed = 0.1
    ico_count = 0
    count = 0
    ico_check= True
    
    logo = pygame.image.load("images\\로고.png")
    log=pygame.transform.scale(logo,(370,220))
    
    background = pygame.image.load("images\\드래곤플라이트배경.png")
    bg = pygame.transform.scale(background, (740,986))
    
    font2 = pygame.font.Font('images\\Maplestory Bold.ttf', 50)
    text2 = font2.render("Press SPACE BAR to Play",True,(255,255,255))
    
    ready_sound = pygame.mixer.Sound("images\\ready.mp3")
    click_sound = pygame.mixer.Sound("images\\선택.mp3")
    
    running =True
    
    while running:                         
        dt = clock.tick(60)         #FPS60으로 세팅
        ready_sound.play(-1)        #음악재생
        
        for event in pygame.event.get():      #이벤트 키 
            if event.type == pygame.QUIT: 
                end_game = True
                running = False
            if event.type == pygame.KEYDOWN: 
                if event.key== pygame.K_SPACE:
                    ready_sound.stop()
                    time.sleep(0.1)
                    click_sound.play()
                    running = False
                    time.sleep(0.5)
                    game()                          #게임속으로 슈웃~!
                elif event.key == pygame.K_ESCAPE:
                    running= False
        
        if ico_check:           #준비화면 용이 와리가리
            if count < 5 :
                ico_to_y -= ico_speed
                ico_check = False
                count+=1
            elif count == 5:
                ico_to_y = 0
                count+=1
            elif count == 11:
                ico_to_y = 0
                ico_check = False
                count = 0
            elif count > 5:
                ico_to_y -= -ico_speed
                ico_check = False
                count+=1
            
            
        if not ico_check:
            if ico_count < 30:
                ico_count += 1
            else:
                ico_count = 0
                ico_check = True
        
        ico_y_pos += ico_to_y
        
        ico_rect = ico.get_rect()
        ico_rect.left = ico_x_pos
        ico_rect.top = ico_y_pos
        
        screen.blit(bg,(0,0))                       #화면 깔아주는 곳
        screen.blit(ico,(ico_x_pos,ico_y_pos))
        screen.blit(log,(90,40))
        screen.blit(text2,(65,850))
        
        pygame.display.update()         #디스플레이를 다시 세팅해주는 메소드

        
def game():                     #게임시작
    global end_game
    
    background = pygame.image.load("images\\드래곤플라이트배경.png")
    bg = pygame.transform.scale(background, (740,986))

    i=0

    character= pygame.image.load("images\\나.png")
    character_size = character.get_rect().size              #터틀과 다른점 소환한 객체마다 사이즈를 구해야함
    character_width = character_size[0]
    character_height = character_size[1]
    character_x_pos = screen_width / 2 - character_width /2
    character_y_pos = screen_height - character_height-30
    to_x = 0

    #이동속도
    character_speed = 0.6

    enemy = pygame.image.load("images\\드래곤플라이트 enemy.png")
    enemy_size = enemy.get_rect().size
    enemy_width= enemy_size[0]
    enemy_height = enemy_size[1]
    enemy_x_pos= r.randint(0,screen_width- enemy_width)
    enemy_y_pos=0-enemy_height
    enemy_speed=8

    weapon= pygame.image.load("images\\1단계 투사체.png")
    weapon_size = weapon.get_rect().size
    weapon_width = weapon_size[0]
    weapons = []            #무기 발사를 키를 입력한대로 계속 하려면 리스트에 넣어주고 뽑아줘야함
    weapon_speed = 10
    
    boom_sound = pygame.mixer.Sound("images\\쥬금.mp3")
    weapon_sound = pygame.mixer.Sound("images\\투사체.mp3")

    font1 = pygame.font.Font("images\\Maplestory Light.ttf", 80)
    
    global score
    score = 0
    
    running = True
    
    while running:
        dt = clock.tick(60)

        for event in pygame.event.get():      
            if event.type == pygame.QUIT: 
                running = False
                end_game = True
            if event.type == pygame.KEYDOWN: 
                if event.key== pygame.K_LEFT:
                    to_x -= character_speed
                elif event.key == pygame.K_RIGHT:
                    to_x +=character_speed
                elif event.key == pygame.K_SPACE:
                    weapon_x_pos = character_x_pos + (character_width/2) - (weapon_width/2)         #무기발사 위치(좌표)
                    weapon_y_pos = character_y_pos
                    weapons.append([weapon_x_pos,weapon_y_pos])                 #리스트에 추가
                    weapon_sound.play()
                    
            if event.type == pygame.KEYUP:                          #키를 안누른상태에서는 캐릭터가 그자리에 정지
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    to_x = 0
                    
        character_x_pos += to_x *dt                 #내 캐릭터에게 FPS부여

        if character_x_pos < 0 :                        #캐릭터들이 옆 울타리 밖으로 못나가게 함 
            character_x_pos = 0
        elif character_x_pos > screen_width - character_width:
            character_x_pos = screen_width - character_width

        enemy_y_pos += enemy_speed

        if enemy_y_pos > screen_height:
            enemy_y_pos=0-enemy_height
            enemy_x_pos=r.randint(0,screen_width- enemy_width)
            
        character_rect = character.get_rect()           #충돌을 위한 각 캐릭터들의 위치
        character_rect.left = character_x_pos
        character_rect.top = character_y_pos

        enemy_rect = enemy.get_rect()
        enemy_rect.left = enemy_x_pos
        enemy_rect.top = enemy_y_pos

        weapons = [[w[0],w[1]-weapon_speed] for w in weapons]           #리스트에 넣을때  레이저의 y값을 계속 빼줌으로써 무기가 위로 올라가도록
        weapons = [[w[0],w[1]] for w in weapons if w[1] > 0]                #레이저가 천장에 닿으면 사라짐
        
        screen.blit(bg, (0,i))                                          #공중에 나는 효과를 주기위해서 배경을 무한으로 루프돌림
        screen.blit(bg,(0,-screen_height+i))
        if i == screen_height:
            screen.blit(bg, (0,-screen_height+i))
            i=0
        i += 2

        for weapon_x_pos, weapon_y_pos in weapons:                          #레이저 발사~
            screen.blit(weapon,(weapon_x_pos, weapon_y_pos))
            
        for x in weapons:
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_x_pos
            weapon_rect.top= weapon_y_pos
            if enemy_rect.colliderect(weapon_rect):                     #레이저가 적에게 닿았을때 적을 새로 랜덤한 위치에서 생성
                weapons.clear()
                score += 100                                                                #동시에 점수 100점씩올라감
                boom_sound.play()
                enemy_y_pos=0-enemy_height
                enemy_x_pos=r.randint(0,screen_width- enemy_width)
        
        if score ==2000:                                                                    #점수2000점 돌파시 무기강화 및 적 속도 빨라짐
            weapon= pygame.image.load("images\\2단계 투사체.png")
            enemy_speed =enemy_speed+(score/50000)
        elif score == 4000:                                                                 #점수4000점 돌파시 무기강화 및 적 속도 더 빨라짐
            weapon= pygame.image.load("images\\3단계 투사체.png")
            enemy_speed =enemy_speed +(score/30000)

        if character_rect.colliderect(enemy_rect):              #적과 내가 부딪혔을때 게임오버(메소드로 넘어감)
            running = False
            #game_sound.stop()
            game_over()           
        
        text2 = font1.render("score: "+str(score),True,(255,255,255))
        
        screen.blit(text2,(10,10))    
        screen.blit(character, (character_x_pos,character_y_pos))
        screen.blit(enemy,(enemy_x_pos,enemy_y_pos))   

        pygame.display.update()


def game_over():
    global end_game
   
    background = pygame.image.load("images\\드래곤플라이트배경.png")
    bg = pygame.transform.scale(background, (740,986))
    
    font = pygame.font.Font("images\\Maplestory Light.ttf", 100)
    font1 = pygame.font.Font("images\\Maplestory Light.ttf", 60)
    font2 = pygame.font.Font("images\\Maplestory Bold.ttf", 50)
    text = font.render("GAME OVER",True,(255,255,255))
    text1 = font1.render("Score: " + str(score),True,(255,255,255))
    text2 = font2.render("Press SPACE BAR to Replay",True,(255,255,255))
    
    gameover_sound = pygame.mixer.Sound("images\\gameover.mp3")
    click_sound = pygame.mixer.Sound("images\\선택.mp3")

    running=True
    
    while running:
        gameover_sound.play(-1)
        
        for event in pygame.event.get():      
            if event.type == pygame.QUIT: 
                running = False
                end_game = True
            if event.type == pygame.KEYDOWN: 
                if event.key== pygame.K_SPACE:
                    gameover_sound.stop()
                    time.sleep(0.1)
                    click_sound.play()
                    running = False
                    ready()
                elif event.key == pygame.K_ESCAPE:
                    running = False
                    end_game = True
        
        screen.blit(bg,(0,0))                                               #게임오버 글과 점수가 표시되고 스페이스바를 누르면 초기화면으로 돌아감
        screen.blit(text, (85,450))
        screen.blit(text1, (180,300))
        screen.blit(text2, (42,850))
        
        pygame.display.update()
    
if end_game: pygame.quit()                              #게임종료를 위한 불린
    
if __name__ == '__main__':
    ready()

