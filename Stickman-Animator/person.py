class Bone:
    def __init__(self, pygame, win, pos):
        self.pygame = pygame
        self.window = win
        self.x, self.y = pos
        self.drag = False
        self.radius = 5

    def draw(self):
        self.pygame.draw.circle(self.window, (255, 0, 0), (self.x, self.y), self.radius, 0)

    def collidepoint(self, pos):
        return (self.x - self.radius <= pos[0] <= self.x + self.radius) and (
                    self.y - self.radius <= pos[1] <= self.y + self.radius)


class BodyPart:
    def __init__(self, pygame, win, bone, pos, head):
        self.pygame = pygame
        self.window = win
        self.bone = bone
        self.x, self.y = pos
        self.parent, self.children = None, []
        self.distanceX = self.distanceY = 0
        self.isHead = head

    def set_distance(self):
        if self.parent:
            self.distanceX = self.parent.bone.x - self.bone.x
            self.distanceY = self.parent.bone.y - self.bone.y

    def set_children(self):
        for child in self.children:
            if child.parent:
                child.bone.x = self.bone.x - child.distanceX
                child.bone.y = self.bone.y - child.distanceY
                child.set_children()

    def draw(self):
        bone_x, bone_y = self.bone.x, self.bone.y
        black_color, thickness = (0, 0, 0), 7
        if self.isHead:
            radius = 45
            self.pygame.draw.circle(self.window, black_color, (bone_x, bone_y - radius), radius, thickness)
        else:
            start = end = (bone_x, bone_y)
            if self.parent:
                end = (self.parent.bone.x, self.parent.bone.y)
            else:
                head = self.children[0]
                start = (head.bone.x, head.bone.y)

            self.pygame.draw.line(self.window, black_color, start, end, thickness)

        if self.bone.drag:
            self.set_children()
        else:
            for child in self.children:
                child.set_distance()

        self.bone.draw()


class Person:
    def __init__(self, pygame, win, custom=True):
        self.pygame = pygame
        self.window = win
        self.BODY_PARTS = {}
        if custom:
            self.BODY_PARTS["LEFT_HAND"] = self.create_body_part(130, 350)
            self.BODY_PARTS["RIGHT_HAND"] = self.create_body_part(370, 350)
            self.BODY_PARTS["LEFT_LEG"] = self.create_body_part(170, 500)
            self.BODY_PARTS["RIGHT_LEG"] = self.create_body_part(330, 500)
            self.BODY_PARTS["LEFT_ARM"] = self.create_body_part(170, 250)
            self.BODY_PARTS["RIGHT_ARM"] = self.create_body_part(330, 250)
            self.BODY_PARTS["LEFT_THIGH"] = self.create_body_part(200, 410)
            self.BODY_PARTS["RIGHT_THIGH"] = self.create_body_part(300, 410)
            self.BODY_PARTS["BODY"] = self.create_body_part(250, 350, 0, 155)
            self.BODY_PARTS["HEAD"] = self.create_body_part(250, 195, head=True)

            self.set_children_to_the_respect_part()

    def create_body_part(self, bone_x, bone_y, x=0, y=0, head=False):
        return BodyPart(self.pygame, self.window, Bone(self.pygame, self.window, (bone_x, bone_y)), (x, y), head)

    def set_children_to_the_respect_part(self):
        self.set_children("BODY", ["HEAD", "LEFT_THIGH", "RIGHT_THIGH"])
        self.set_children("HEAD", ["LEFT_ARM", "RIGHT_ARM"])
        self.set_children("LEFT_ARM", ["LEFT_HAND"])
        self.set_children("RIGHT_ARM", ["RIGHT_HAND"])
        self.set_children("LEFT_THIGH", ["LEFT_LEG"])
        self.set_children("RIGHT_THIGH", ["RIGHT_LEG"])

    def set_children(self, obj, children):
        obj = self.BODY_PARTS[obj]
        for child in children:
            child = self.BODY_PARTS[child]
            obj.children.append(child)
            child.parent = obj
            child.set_distance()

    def draw(self):
        for part in self.BODY_PARTS.values():
            part.draw()

    def custom_person(self, name, bone_x, bone_y, x, y, head):
        self.BODY_PARTS[name] = self.create_body_part(bone_x, bone_y, x, y, head)

    def copy(self):
        person = Person(self.pygame, self.window, custom=True)
        for name, part in self.BODY_PARTS.items():
            person.custom_person(name, part.bone.x, part.bone.y, part.x, part.y, name == "HEAD")

        person.set_children_to_the_respect_part()
        return person
