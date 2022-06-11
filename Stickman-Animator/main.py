import pygame, glob, os.path
from pygame.locals import *
from interface import Button, Input
from person import Person
from projectManager import ProjectManager

# Initialize program
pygame.init()

displayInfo = pygame.display.Info()
width, height = displayInfo.current_w, displayInfo.current_h-55

pygame.display.set_caption("Stickman Animator")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)
defaultPadding = (4, 4, 4, 4)

def mainMenu(mm):
    window = pygame.display.set_mode((600, 800))

    run, start = True, False
    textField = Input(pygame, window, (20, 50, 450, 30), 24, padding=defaultPadding)
    createProject = Button(pygame, window, "Create", (500, 50), 24, padding=defaultPadding)

    recentProjects = {}; row = 100
    for project in glob.glob('*.stm'):
        recentProjects[project] = Button(
            pygame, window, project[:-4], (20, row), 24,
            padding=(16, 20, 8, 225),
            backgroundColor=(255, 255, 255),
            borderColor=(50, 50, 50)
        )
        row += 60

    while run:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            elif textField.focus and event.type == pygame.KEYDOWN:
                textField.text = textField.text[:-1] if (event.key == pygame.K_BACKSPACE) else (textField.text + event.unicode)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if textField.click():
                    textField.focus = True
                elif createProject.click() and textField.text != '':
                    mm.setProject(textField.text, os.path)
                    run = textField.focus = False
                    start = True
                else:
                    for name, project in recentProjects.items():
                        if project.click():
                            mm.setProject(name[:-4], os.path)
                            run = textField.focus = False
                            start = True

        window.fill((255, 255, 255))

        label = font.render("Create new project", True, pygame.Color('Black'))
        window.blit(label, (20, 10))

        textField.show()
        createProject.show()

        for project in recentProjects.values():
            project.show()

    return start


projectManager = ProjectManager()
if mainMenu(projectManager):
    window = pygame.display.set_mode((width, height))

    frames = [] # Frames
    for frame in projectManager.getKeyFrames():
        person = Person(pygame, window, True)
        for name, part in frame.items():
            person.customPerson(name, part[0], part[1], part[2], part[3], name=="HEAD")

        person.setChildrenToTheRespectPart()
        frames.append(person)

    frames = frames if len(frames) > 0 else [Person(pygame, window)]
    person = frames[0]

    # Buttons
    createKeyFrame = Button(pygame, window, "Create keyframe", (width/2-185, height-50), 24, padding=defaultPadding)
    addKeyFrame = Button(pygame, window, "Add keyframe", (width/2, height-50), 24, padding=defaultPadding)
    play = Button(pygame, window, "Play", (width/2-60, 50), 24, padding=defaultPadding)
    pause = Button(pygame, window, "Pause", (width/2, 50), 24, padding=defaultPadding)

    # Key frames
    keyFrames = [Button(pygame, window, " . ", (width/2-100, height-100), 24)]
    keyFrames[0].select(True)
    selectedKeyFrame = [0, keyFrames[0]]

    for i in range(1, len(frames)):
        keyFrames.append(Button(pygame, window, " . ", (keyFrames[-1].x+30, keyFrames[-1].y), 24))

    # Beginning Game Loop
    animate = False; f = 0
    running = True
    while running:
        if animate:
            person = frames[f]
            f = f+1 if f+1 < len(frames) else 0
            pygame.time.delay(200)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                projectManager.storeKeyFrames(frames)
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and play.click():
                animate = True
                print('Ada')
            elif event.type == pygame.MOUSEBUTTONDOWN and pause.click():
                animate = False
                person = frames[selectedKeyFrame[0]]
            elif not animate:
                if event.type == pygame.MOUSEBUTTONDOWN and createKeyFrame.click():
                    keyFrames.append(Button(pygame, window, " . ", (keyFrames[-1].x+30, keyFrames[-1].y), 24))
                elif event.type == pygame.MOUSEBUTTONDOWN and addKeyFrame.click():
                    if  selectedKeyFrame[0] < len(frames):
                        frames[selectedKeyFrame[0]] = person
                    else:
                        frames.append(person)
                else:
                    for i, kf in enumerate(keyFrames):
                        if event.type == pygame.MOUSEBUTTONDOWN and kf.click():
                            selectedKeyFrame[1].select(False)
                            kf.select(True)
                            selectedKeyFrame = [i, kf]
                            person = frames[i] if i < len(frames) else frames[-1].copy()
                            break

                    for part in person.BODY_PARTS.values():
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and part.bone.collidepoint(event.pos):
                            part.bone.drag = True
                            mouse_x, mouse_y = event.pos
                            offset_x = part.bone.x - mouse_x
                            offset_y = part.bone.y - mouse_y
                        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                            part.bone.drag = False
                        elif event.type == pygame.MOUSEMOTION and part.bone.drag:
                            mouse_x, mouse_y = event.pos
                            part.bone.x = mouse_x + offset_x
                            part.bone.y = mouse_y + offset_y

        window.fill((255, 255, 255))

        play.show(); pause.show()
        person.draw()

        if not animate:
            createKeyFrame.show()
            addKeyFrame.show()

            for kf in keyFrames:
                kf.show()

        pygame.display.flip()

        clock.tick(30)

pygame.quit()
