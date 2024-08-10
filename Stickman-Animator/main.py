import glob
import os.path
import pygame
from pygame.locals import *

from interface import Button, Input
from person import Person
from projectManager import ProjectManager

pygame.init()

displayInfo = pygame.display.Info()
# width, height = displayInfo.current_w, displayInfo.current_h - 55
width, height = 1200, 900

pygame.display.set_caption("Stick-Man Animator")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)
defaultPadding = (4, 4, 4, 4)


def main_menu(mm):
    main_menu_window = pygame.display.set_mode((600, 800))

    run, start = True, False
    text_field = Input(pygame, main_menu_window, (20, 50, 450, 30), 24, padding=defaultPadding)
    create_project = Button(pygame, main_menu_window, "Create", (500, 50), 24, padding=defaultPadding)

    recent_projects = {}
    row = 100
    for project in glob.glob('Stickman-Animator/*.stm'):
        print(project)
        recent_projects[project] = Button(
            pygame, main_menu_window, project[18:-4], (20, row), 24,
            padding=(16, 20, 8, 225),
            background_color=(255, 255, 255),
            border_color=(50, 50, 50)
        )
        row += 60

    while run:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            elif text_field.focus and event.type == pygame.KEYDOWN:
                text_field.text = text_field.text[:-1] if (event.key == pygame.K_BACKSPACE) else (
                            text_field.text + event.unicode)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if text_field.click():
                    text_field.focus = True
                elif create_project.click() and text_field.text != '':
                    mm.setProject(text_field.text, os.path)
                    run = text_field.focus = False
                    start = True
                else:
                    for name, project in recent_projects.items():
                        if project.click():
                            mm.set_project(name[:-4], os.path)
                            run = text_field.focus = False
                            start = True

        main_menu_window.fill((255, 255, 255))

        label = font.render("Create new project", True, pygame.Color('Black'))
        main_menu_window.blit(label, (20, 10))

        text_field.show()
        create_project.show()

        for project in recent_projects.values():
            project.show()

    return start


projectManager = ProjectManager()
if main_menu(projectManager):
    window = pygame.display.set_mode((width, height))

    frames = []  # Frames
    for frame in projectManager.get_key_frames():
        person = Person(pygame, window, True)
        for name, part in frame.items():
            person.custom_person(name, part[0], part[1], part[2], part[3], name == "HEAD")

        person.set_children_to_the_respect_part()
        frames.append(person)

    frames = frames if len(frames) > 0 else [Person(pygame, window)]
    person = frames[0]

    # Buttons
    createKeyFrame = Button(pygame, window, "Create keyframe", (width / 2 - 185, height - 50), 24,
                            padding=defaultPadding)
    add_key_frame = Button(pygame, window, "Add keyframe", (width / 2, height - 50), 24, padding=defaultPadding)
    play = Button(pygame, window, "Play", (width / 2 - 60, 50), 24, padding=defaultPadding)
    pause = Button(pygame, window, "Pause", (width / 2, 50), 24, padding=defaultPadding)

    # Key frames
    key_frames = [Button(pygame, window, " . ", (width / 2 - 100, height - 100), 24)]
    key_frames[0].select(True)
    selected_key_frame = [0, key_frames[0]]

    for i in range(1, len(frames)):
        key_frames.append(Button(pygame, window, " . ", (key_frames[-1].x + 30, key_frames[-1].y), 24))

    # Beginning Game Loop
    animate = False
    f = 0
    running = True
    while running:
        if animate:
            person = frames[f]
            f = f + 1 if f + 1 < len(frames) else 0
            pygame.time.delay(200)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                projectManager.store_key_frames(frames)
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and play.click():
                animate = True
            elif event.type == pygame.MOUSEBUTTONDOWN and pause.click():
                animate = False
                person = frames[selected_key_frame[0]]
            elif not animate:
                if event.type == pygame.MOUSEBUTTONDOWN and createKeyFrame.click():
                    key_frames.append(Button(pygame, window, " . ", (key_frames[-1].x + 30, key_frames[-1].y), 24))
                elif event.type == pygame.MOUSEBUTTONDOWN and add_key_frame.click():
                    if selected_key_frame[0] < len(frames):
                        frames[selected_key_frame[0]] = person
                    else:
                        frames.append(person)
                else:
                    for i, kf in enumerate(key_frames):
                        if event.type == pygame.MOUSEBUTTONDOWN and kf.click():
                            selected_key_frame[1].select(False)
                            kf.select(True)
                            selected_key_frame = [i, kf]
                            person = frames[i] if i < len(frames) else frames[-1].copy()
                            break

                    for part in person.BODY_PARTS.values():
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and part.bone.collidepoint(
                                event.pos):
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

        play.show()
        pause.show()
        person.draw()

        if not animate:
            createKeyFrame.show()
            add_key_frame.show()

            for kf in key_frames:
                kf.show()

        pygame.display.flip()

        clock.tick(30)

pygame.quit()
