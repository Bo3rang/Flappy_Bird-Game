import pygame, sys, random

def draw_floor():                                                           # Hàm 2 floor
    screen.blit(floor, (floor_x_pos, 650))
    screen.blit(floor, (floor_x_pos + 432, 650))

# Ham tạo Pipe
def create_pipe():
    pipe_random_pos = random.choice(pipe_height)
    bottom_pipe = pipe.get_rect(midtop = (500, pipe_random_pos))
    top_pipe = pipe.get_rect(midtop = (500, pipe_random_pos - 650))
    return bottom_pipe, top_pipe

# Hàm di chuyển Pipe
def move_pipe(pipes):
    for p in pipes:
        p.centerx -= 5                                                      # Di chuyển Pipe sang bên trái
    return pipes

# Hàm vẽ Pipe
def draw_pipe(pipes):
    for p in pipes:
        if p.bottom >= 600:
            screen.blit(pipe, p)
        else:
            flip_pipe = pygame.transform.flip(pipe, False, True)    
            screen.blit(flip_pipe, p)

# Hàm xử lí va chạm
def check_collision(pipes):
    for p in pipes:
        if bird_rect.colliderect(p):
            sound_hit.play()
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
        sound_hit.play()
        return False
    return True

# Hàm xoay Bird
def rotate_bird(birds):
    new_bird = pygame.transform.rotozoom(birds, - bird_movement * 3, 1)
    return new_bird

# Hàm đập cánh cho Bird
def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect

# Hàm hiển thị Score
def score_display(game_state):
    if game_state == 'Main game':
        score = game_font.render(str(int(score_game)), True, (255,255,255))
        score_rect = score.get_rect(center = (216, 100))
        screen.blit(score, score_rect)
    if game_state == "Game over":
        score = game_font.render(f'Score: {int(score_game)}', True, (255,255,255))
        score_rect = score.get_rect(center = (216, 100))
        screen.blit(score, score_rect)

        hight = game_font.render(f'Hight Score: {int(hight_score)}', True, (255,255,255))
        hight_rect = score.get_rect(center = (160, 630))
        screen.blit(hight, hight_rect)

# Hàm Hight_Score
def update_score(score_game, hight_score):
    if score_game > hight_score:
        hight_score = score_game
    return hight_score

pygame.init                                                                 # Bắt đầu pygame.
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
screen =  pygame.display.set_mode((432, 768))                               # Hiển thị cửa sổ pygame.
clock = pygame.time.Clock()                                                 # Khởi tạo FPS.
game_font = pygame.font.init()
game_font = pygame.font.Font("FileGame/04B_19.TTF", 40)

# Chèn Background
bg = pygame.image.load('FileGame/assets/background-night.png').convert()    # .convert dùng để đổi file hình ảnh nhẹ hơn => load nhanh hơn
bg = pygame.transform.scale2x(bg)                                           # X2 background để đầy màn.
# Chèn Floor.
floor = pygame.image.load('FileGame/assets/floor.png').convert()
floor = pygame.transform.scale2x(floor)  
floor_x_pos = 0                                                             # Đặt vị trí x ban đầu bằng 0.
# Chèn Bird.
bird_down = pygame.transform.scale2x(pygame.image.load('FileGame/assets/yellowbird-downflap.png')).convert_alpha()
bird_mid = pygame.transform.scale2x(pygame.image.load('FileGame/assets/yellowbird-midflap.png')).convert_alpha()
bird_up = pygame.transform.scale2x(pygame.image.load('FileGame/assets/yellowbird-upflap.png')).convert_alpha()
bird_list = [bird_down, bird_mid, bird_up]          
bird_index = 0
bird = bird_list[bird_index]
bird_rect = bird.get_rect(center = (100, 384))                              # Tạo hình chữ nhật xung quanh Bird.
gravity = 0.25                                                              # Tạo ra trọng lực.
bird_movement = 0                                                           # Tạo sự di chuyển, = 0 vì lúc đầu Bird chưa di chuyển.
# Tạo timmer cho Bird
bird_flap = pygame.USEREVENT + 1
pygame.time.set_timer(bird_flap, 200)

# Chèn Pipe
pipe = pygame.image.load('FileGame/assets/pipe-green.png').convert()
pipe = pygame.transform.scale2x(pipe)
pipe_list = []
pipe_height = [200, 300, 400]
# Tạo SpawnPipe
spawnpipe = pygame.USEREVENT                                                # Làm cho xuất hiện Pipe liên tục 
pygame.time.set_timer(spawnpipe, 1200)                                      # Set 1.2s sẽ xuất hiện 
# Biến game
game_active = True
score_game = 0
hight_score = 0

# Tạo màn hình kết thúc game
game_over = pygame.transform.scale2x(pygame.image.load('FileGame/assets/message.png')).convert_alpha()
game_over_rect = game_over.get_rect(center = (216,384))

# Chèn Sound
sound_flap = pygame.mixer.init()
sound_flap = pygame.mixer.Sound('FileGame/sound/sfx_wing.wav')
sound_hit = pygame.mixer.Sound('FileGame/sound/sfx_hit.wav')
sound_die = pygame.mixer.Sound('FileGame/sound/sfx_die.wav')
sound_score = pygame.mixer.Sound('FileGame/sound/sfx_point.wav')


# While loop của trò chơi
while True:
    for event in pygame.event.get():
        # Sự kiên tắt, đóng
        if event.type == pygame.QUIT:
            pygame.quit()  
            sys.exit()

        # Sự kiện nhấn phím Space di chuyển Bird
        if event.type == pygame.KEYDOWN:            
            if event.key == pygame.K_SPACE and game_active:
                # Di chuyển Bird lên trên.
                bird_movement = 0
                bird_movement = -10
                sound_flap.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 384)
                bird_movement = -10
                score_game = 0

        # Sự kiện xuất hiện Pipe
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())
        
        # Sự kiện Flap cho Bird
        if event.type == bird_flap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()

    # Hiển thị Background
    screen.blit(bg, (0, 0))

    if game_active:
        # Hiển thị Pipe
        pipe_list = move_pipe(pipe_list)                                    # Lấy tất cả ống trong Pipe list trả về xong di chyển Pipe mới
        draw_pipe(pipe_list)
        game_active = check_collision(pipe_list)
        
        # Hiển thị Bird
        rotate_birded = rotate_bird(bird)
        screen.blit(rotate_birded, bird_rect)
        bird_movement += gravity                                            # Bird càng di chuyển thì Gravity càng tăng
        bird_rect.centery += bird_movement                                  # Di chuyển Bird và Rect đi xuống
        
        # Hiển thị Score
        score_game += 0.01
        score_display('Main game')
    else: 
        hight_score = update_score(score_game, hight_score)
        score_display('Game over')
        screen.blit(game_over, game_over_rect)

    # Hiển thị Floor
    floor_x_pos -= 1                                                        # Di chuyển Floor lùi về phía sau 
    draw_floor()  
    # Lặp đi lặp lại floor
    if floor_x_pos <= -432:                         
        floor_x_pos = 0
    
    pygame.display.update()                     
    clock.tick(120)                                                         # FPS là 120.