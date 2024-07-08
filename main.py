import pygame
from Button import*
from Texts import*
from TxtEntry import*

pygame.init()
pygame.mixer.pre_init(48000,-16,2,512)

#setup window
sw,sh = 650,500
screen = pygame.display.set_mode((sw,sh))
pygame.display.set_caption("Pomodoro-Timer")
pygame.display.set_icon(pygame.image.load("assets/pomodoro.png"))

#game loop variables
clock = pygame.time.Clock()
on = True
app_state = "running"

#fonts
app_XL_font = pygame.font.Font("BebasNeue-Regular.ttf",150)
app_M_font = pygame.font.Font("BebasNeue-Regular.ttf",80)
app_S_font = pygame.font.Font("BebasNeue-Regular.ttf",40)

#timer variables
period = "focus"
Minutes = 25
Seconds = 0
focusTime = 25
restTime = 5
FOM,FOS,RM,RS = focusTime,0,restTime,0
Fakesecondcounter = 10
paused = True
caption1,caption2 = "focus","rest"
current_caption = caption1
period_caption = app_M_font.render(current_caption,True,(139, 232, 229))

#switch button
off_b_img = pygame.image.load("assets/off-button.png")
on_b_img = pygame.image.load("assets/switch.png")
switchButton_image = off_b_img
switchButton_rect = switchButton_image.get_rect(topleft=(sw//2-switchButton_image.get_width()//2,period_caption.get_height()))

#pause button
pause_img = pygame.image.load("assets/pause.png")
continue_img = pygame.image.load("assets/play.png")
PaCoButton_image = continue_img
PaCoButton_rect = PaCoButton_image.get_rect(topleft=(sw//2,sh-110))

#add 1 minute button
plus_img = pygame.image.load("assets/plus.png")
plus_rect = plus_img.get_rect(topleft=(30,sh//2-plus_img.get_height()//2))

#minus 1 minute button
minus_img = pygame.image.load("assets/minus.png")
minus_rect = minus_img.get_rect(topleft=(sw-minus_img.get_width()-30,sh//2-minus_img.get_height()//2))

#setting button
setting_img = pygame.image.load("assets/setting.png")
setting_rect = setting_img.get_rect(topleft=(sw-setting_img.get_width()-30,30))

#reset button
reset_img = pygame.image.load("assets/redo.png")
reset_rect = reset_img.get_rect(topleft=(sw//2-reset_img.get_width()-10,sh-110))

#back button
back_img = pygame.image.load("assets/previous.png")
back_rect = back_img.get_rect(topleft=(10,sh-back_img.get_height()-10))

#save button
save_img = pygame.image.load("assets/checked.png")
save_rect = save_img.get_rect(topleft=(sw-save_img.get_width()-10,sh-save_img.get_height()-10))

#labels
Labels = [
    app_M_font.render("Settings",True,(216, 217, 218)),
    app_S_font.render("Period's Caption",True,(0,0,0)),
    app_S_font.render("Minutes",True,(0,0,0)),
    app_S_font.render("Seconds",True,(0,0,0))
]

#text inputs
entrys = [
    Entry(30,Labels[0].get_height()+Labels[1].get_height()+20,300,50,app_M_font),
    Entry(350,Labels[0].get_height()+Labels[1].get_height()+20,110,50,app_M_font),
    Entry(480,Labels[0].get_height()+Labels[1].get_height()+20,110,50,app_M_font),
    Entry(30,Labels[0].get_height()*1.7+Labels[1].get_height()+20,300,50,app_M_font),
    Entry(350,Labels[0].get_height()*1.7+Labels[1].get_height()+20,110,50,app_M_font),
    Entry(480,Labels[0].get_height()*1.7+Labels[1].get_height()+20,110,50,app_M_font)
]
selected_entry = None

#sounds
ringtone = pygame.mixer.Sound("assets/marimba.mp3")

#added minutes
ADMin = []

#reset variable to initiate values
def reset_vars():
    for e in entrys:
        e.text = ""

def resetT():
    global Minutes,Seconds,paused,PaCoButton_image,period_caption
    period_caption = app_M_font.render(current_caption,True,(139, 232, 229))
    try:
        Minutes = FOM if period=="focus"else RM
    except:Minutes = 25 if period=="focus" else 5
    try:
        Seconds = FOS if period=="focus"else RS
    except:Seconds = 0
    paused = True
    PaCoButton_image = continue_img

#game loop
while on:

    #mouse position
    mouse_pos = pygame.mouse.get_pos()

    #background color
    if period == "focus":
        screen.fill((111, 97, 192))
    else:
        screen.fill((159, 13, 127))

    #handle main app interface
    if app_state == "running":
        #display timer
        secstoDisplay = str(Seconds)
        minstoDisplay = str(Minutes)
        if len(str(Minutes))<2:
            minstoDisplay = "0"+str(Minutes)
        if len(str(Seconds))<2:
            secstoDisplay = "0"+str(Seconds)
        timer_surf = app_XL_font.render(minstoDisplay+" : "+secstoDisplay,True,(255,255,255))
        screen.blit(timer_surf,(sw//2-timer_surf.get_width()//2,sh//2-timer_surf.get_height()//2))
        screen.blit(period_caption,(sw//2-period_caption.get_width()//2,20))
        screen.blit(setting_img,setting_rect)
        screen.blit(PaCoButton_image,PaCoButton_rect)
        screen.blit(switchButton_image,switchButton_rect)
        screen.blit(plus_img,plus_rect)
        screen.blit(minus_img,minus_rect)
        screen.blit(reset_img,reset_rect)

        #handle pause
        if not paused:
            #timer logic
            Fakesecondcounter -= 0.15
            if Fakesecondcounter <= 0:
                Seconds -= 1
                Fakesecondcounter = 10
            if Seconds <= 0:
                Minutes -= 1
                Seconds = 59

            if Minutes < 0:
                if period == "focus":
                    period = "rest"
                    current_caption = caption2
                    Minutes = RM
                    Seconds = RS
                    switchButton_image = on_b_img
                else:
                    period = "focus"
                    current_caption = caption1
                    Minutes = FOM
                    Seconds = FOS
                    switchButton_image = off_b_img
                period_caption = app_M_font.render(current_caption,True,(139, 232, 229))
                pygame.mixer.Sound.play(ringtone)
                pygame.time.wait(5000)
                pygame.mixer.Sound.play(ringtone)
                pygame.time.wait(5000)

        #draw added minutes
        if len(ADMin)>=1:
            for am in ADMin:
                am.draw(screen)
                am.y -= 1
                if am.valpha <= 0:
                    ADMin.remove(am)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                on = False

            #handle mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                #check if left mose button was clicked
                if event.button == 1:
                    #check if pause/continue button was clicked
                    if PaCoButton_rect.collidepoint(mouse_pos):
                        if paused:
                            paused = False
                            PaCoButton_image = pause_img
                        else:
                            paused = True
                            PaCoButton_image = continue_img
                    #check if switch period button was clicked
                    if switchButton_rect.collidepoint(mouse_pos):
                        if period == "focus":
                            switchButton_image = on_b_img
                            current_caption = caption2
                            period = "rest"
                            resetT()
                        else:
                            switchButton_image = off_b_img
                            current_caption = caption1
                            period = "focus"
                            resetT()

                    #check if +1 minute button was clicked
                    if plus_rect.collidepoint(mouse_pos):
                        Minutes += 1
                        ADMin.append(Text("+1",mouse_pos[0],mouse_pos[1],(213, 255, 228),app_M_font))
                    #check if -1 minute button was clicked
                    if minus_rect.collidepoint(mouse_pos):
                        Minutes -= 1
                        ADMin.append(Text("-1",mouse_pos[0],mouse_pos[1],(213, 255, 228),app_M_font))

                    #check if reset button was clicked
                    if reset_rect.collidepoint(mouse_pos):
                        resetT()

                    #check if settings button was clicked
                    if setting_rect.collidepoint(mouse_pos):
                        app_state = "settings"
                        paused = True
                        pygame.display.set_caption("Pomodoro-Settings")


    #handle settings interface
    if app_state == "settings":

        #place back and save buttons
        screen.blit(back_img,back_rect)
        screen.blit(save_img,save_rect)

        screen.blit(Labels[0],(sw//2-Labels[0].get_width()//2,10))
        pygame.draw.line(screen,(39, 40, 41),(30,Labels[0].get_height()+10),(sw-30,Labels[0].get_height()+10),2)

        for e in entrys:
            e.draw(screen)

        screen.blit(Labels[1],(40,Labels[1].get_height()*2+20))
        screen.blit(Labels[2],(350,Labels[1].get_height()*2+20))
        screen.blit(Labels[3],(480,Labels[1].get_height()*2+20))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                on = False
            #check if any key was pressed
            if event.type == pygame.KEYDOWN:
                #check if any text input is selected
                try:
                    if selected_entry.on_focus:
                        #check if backspace was pressed
                        if event.key == pygame.K_BACKSPACE:
                            #delete last caracter of the text input
                            selected_entry.text = selected_entry.text[:-1]
                        #check the rest of the keys
                        else:
                            if selected_entry not in (entrys[0],entrys[3]):
                                #check if length of the input is less than 3 numbers
                                if len(selected_entry.text)<3:
                                    #check if input is digits only
                                    if event.unicode.isnumeric():
                                        selected_entry.text += event.unicode
                            else:
                                selected_entry.text += event.unicode
                        #display text of the input after update
                        selected_entry.text_surface = app_S_font.render(selected_entry.text,True,(0,0,0))
                except:pass

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    #check if back button was clicked
                    if back_rect.collidepoint(mouse_pos):
                        app_state = "running"
                        pygame.display.set_caption("Pomodoro-Timer")

                    #check if save button was clicked
                    if save_rect.collidepoint(mouse_pos):
                        #check if inputs have values so update the variables
                        if entrys[0].text != "":
                            caption1 = entrys[0].text
                        if entrys[1].text != "":
                            FOM = int(entrys[1].text)
                            Minutes = FOM
                            if entrys[2].text != "":
                                FOS = int(entrys[2].text)
                        if entrys[3].text != "":
                            caption2 = entrys[3].text
                        if entrys[4].text != "":
                            RM = int(entrys[4].text)
                            if entrys[5].text != "":
                                RS = int(entrys[5].text)
                        period = "focus"
                        current_caption = caption1
                        resetT()
                        app_state = "running"
                        pygame.display.set_caption("Pomodoro-Timer")
                        switchButton_image = off_b_img
                        #reset_vars()


                    #check if clicked on text input
                    for e in entrys:
                        if e.rect.collidepoint(mouse_pos):
                            e.on_focus = not(e.on_focus)
                            e.update()
                            selected_entry = e
                        else:
                            e.on_focus = False
                            e.update()


    #update screen
    pygame.display.update()
    #framerate (FPS)
    clock.tick(60)

#closes the app by the end of the loop (red X on top is pressed)
pygame.quit()


