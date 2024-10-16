import pygame
import random
import math

pygame.init()
pygame.font.init()
pygame.display.set_caption("Dot Placer")

Screen_Width = 1280
Screen_Height = 720
Screen = pygame.display.set_mode((Screen_Width, Screen_Height))

Sans_MS = pygame.font.SysFont("Comic Sans MS", 50, True)

Running = True
Lost = False
Score = 0

Player_Dot_Coordinates = -100, -100
Player_Place = False
Player_Played = False
Player_Dot_Size = 15

Random_Dots = []
Random_Dots_Radius = []
Random_Dots_Number = 10
Random_Dots_Maximal_Size = 150

# Check if Random Dot Maximal Size is not lesser than Minimal
if Random_Dots_Maximal_Size < Player_Dot_Size:
    Random_Dots_Maximal_Size = Player_Dot_Size + Random_Dots_Maximal_Size

Score_File = open("Score File.txt", "a")
Score_Saved = False
Difficulty = int((Player_Dot_Size*(Random_Dots_Number*0.9*(math.pi*pow(Random_Dots_Maximal_Size,1.5))))/(Screen_Height*Screen_Width)*100)



print(Difficulty)

def Randomize_Dot_Coordinates():
    return (random.randint(0, Screen_Width), random.randint(0, Screen_Height))



while True:
    # Keys definition
    # Quit, Space, Mouse
    if Running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Running = False
                    print("Running is False")

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                Random_Dots.clear()
                Random_Dots_Radius.clear()
                for i in range(Random_Dots_Number):
                    Random_Dots.append(Randomize_Dot_Coordinates())
                    Random_Dots_Radius.append(random.randint(Player_Dot_Size, Random_Dots_Maximal_Size))
                    print(f"[{i+1}] random Dot Coordinate => {Random_Dots[i]}", end=" ")
                    if i % 3 == 0:
                        print("")
                if not Lost:
                    Score += 1
                
                Player_Dot_Coordinates = pygame.mouse.get_pos()
                print(f"Player Dot coordinates => {Player_Dot_Coordinates}")
                Player_Place = True

        Screen.fill("#CFDAE5")
        Player_Dot = pygame.draw.circle(Screen, "#3051E3", Player_Dot_Coordinates, Player_Dot_Size, Player_Dot_Size)
        Score_Text = Sans_MS.render(f"Score: {Score}", 0, "#3051E3")

        # Dot Creation
        for i, Dot in enumerate(Random_Dots):
            pygame.draw.circle(Screen, "#30E38D", Dot, Random_Dots_Radius[i], Random_Dots_Radius[i])
            distance = ((Player_Dot_Coordinates[0] - Dot[0])**2 + (Player_Dot_Coordinates[1] - Dot[1])**2)**0.5

        # Check for collision
            if distance < Player_Dot_Size + Random_Dots_Radius[i]:
                Running = False
                Lost = True
                print("Lose")
        Screen.blit(Score_Text, (0, 0))
    # Death Screen
    else:
        if Lost:
            if not Score_Saved:
                Score_File.write(f" Player Dot Size => {Player_Dot_Size}\n Random Dots Max Size => {Random_Dots_Maximal_Size}\n Random Dots Count => {Random_Dots_Number}\n Score => {Score}\n Difficulty => {Difficulty}\n------------------------------------\n")
                Score_Saved = True
                print("Running is False")
            Score = 0
            Lost_Message = Sans_MS.render("You\'ve lost!", 0, "#3051E3")
            Start_New_Game_Text = Sans_MS.render("To start a new game, press \"Space\"", 0, "#3051E3")
            Screen.blit(Lost_Message,(Screen_Width/2-(Screen_Width/10),Screen_Height/2))
            Screen.blit(Start_New_Game_Text,(200,Screen_Height/1.5))
        else:
            Pause_Text = Sans_MS.render("You\'ve paused the game", 0, "#3051E3")
            Screen.blit(Pause_Text,(400,Screen_Height/2))
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                Random_Dots.clear()
                Player_Dot_Coordinates = -100, -100
                Running = True
                print("Running is True")
                Lost = False
                Score_Saved = False

    # Draw the player's dot regardless of the value of Running
    pygame.display.flip()
