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
        return (self.x-self.radius <= pos[0] <= self.x+self.radius) and (self.y-self.radius <= pos[1] <= self.y+self.radius)


class BodyPart:
    def __init__(self, pygame, win, bone, pos, head):
        self.pygame = pygame
        self.window = win
        self.bone = bone
        self.x, self.y = pos
        self.parent, self.children = None, []
        self.distanceX = self.distanceY = 0
        self.isHead = head

    def setDistance(self):
        if self.parent:
            self.distanceX = self.parent.bone.x - self.bone.x
            self.distanceY = self.parent.bone.y - self.bone.y

    def setChildren(self):
        for child in self.children:
            if child.parent:
                child.bone.x = self.bone.x-child.distanceX
                child.bone.y = self.bone.y-child.distanceY
                child.setChildren()

    def draw(self):
        boneX, boneY = self.bone.x, self.bone.y
        blackColor, thickness = (0, 0, 0), 7
        if self.isHead:
            radius = 45
            self.pygame.draw.circle(self.window, blackColor, (boneX, boneY-radius), radius, thickness)
        else:
            start = end = (boneX, boneY)
            if self.parent:
                end = (self.parent.bone.x, self.parent.bone.y)
            else:
                head = self.children[0]
                start = (head.bone.x, head.bone.y)

            self.pygame.draw.line(self.window, blackColor, start, end, thickness)

        if self.bone.drag:
            self.setChildren()
        else:
            for child in self.children:
                child.setDistance()

        self.bone.draw()


class Person:
    def __init__(self, pygame, win, custom=True):
        self.pygame = pygame
        self.window = win
        self.BODY_PARTS = {}
        if custom:
            self.BODY_PARTS["LEFT_HAND"] = self.createBodyPart(130, 350)
            self.BODY_PARTS["RIGHT_HAND"] = self.createBodyPart(370, 350)
            self.BODY_PARTS["LEFT_LEG"] = self.createBodyPart(170, 500)
            self.BODY_PARTS["RIGHT_LEG"] = self.createBodyPart(330, 500)
            self.BODY_PARTS["LEFT_ARM"] = self.createBodyPart(170, 250)
            self.BODY_PARTS["RIGHT_ARM"] = self.createBodyPart(330, 250)
            self.BODY_PARTS["LEFT_THIGH"] = self.createBodyPart(200, 410)
            self.BODY_PARTS["RIGHT_THIGH"] = self.createBodyPart(300, 410)
            self.BODY_PARTS["BODY"] = self.createBodyPart(250, 350, 0, 155)
            self.BODY_PARTS["HEAD"] = self.createBodyPart(250, 195, head=True)

            self.setChildrenToTheRespectPart()

    def createBodyPart(self, boneX, boneY, x=0, y=0, head=False):
        return BodyPart(self.pygame, self.window, Bone(self.pygame, self.window, (boneX, boneY)), (x, y), head)

    def setChildrenToTheRespectPart(self):
        self.setChildren("BODY", ["HEAD", "LEFT_THIGH", "RIGHT_THIGH"])
        self.setChildren("HEAD", ["LEFT_ARM", "RIGHT_ARM"])
        self.setChildren("LEFT_ARM", ["LEFT_HAND"])
        self.setChildren("RIGHT_ARM", ["RIGHT_HAND"])
        self.setChildren("LEFT_THIGH", ["LEFT_LEG"])
        self.setChildren("RIGHT_THIGH", ["RIGHT_LEG"])

    def setChildren(self, obj, children):
        obj = self.BODY_PARTS[obj]
        for child in children:
            child = self.BODY_PARTS[child]
            obj.children.append(child); child.parent = obj
            child.setDistance()

    def draw(self):
        for part in self.BODY_PARTS.values():
            part.draw()

    def customPerson(self, name, boneX, boneY, x, y, head):
        self.BODY_PARTS[name] = self.createBodyPart(boneX, boneY, x, y, head)

    def copy(self):
        person = Person(self.pygame, self.window, custom=True)
        for name, part in self.BODY_PARTS.items():
            person.customPerson(name, part.bone.x, part.bone.y, part.x, part.y, name=="HEAD")

        person.setChildrenToTheRespectPart()
        return person
