class ProjectManager:
    def __init__(self):
        self.projectName = ''
        self.keyFrames = []

    def setProject(self, name, osPath):
        self.projectName = name+'.stm'
        if not osPath.isfile(self.projectName):
            open(self.projectName, 'w').close()

    def storeKeyFrames(self, frames):
        keys = ''
        for frame in frames:
            for name, part in frame.BODY_PARTS.items():
                keys += "{},{},{},{},{}\n".format(name, part.bone.x, part.bone.y, part.x, part.y)

        file = open(self.projectName, "w")
        file.write(keys)
        file.close()

    def getKeyFrames(self):
        file = open(self.projectName, "r")
        keys = file.read().strip().split('\n')
        dic = {}
        for i, key in enumerate(keys):
            key = key.split(',')
            dic[key[0]] = list(map(int, key[1:len(key)]))
            if (i+1)%10 == 0:
                self.keyFrames.append(dic)
                dic = {}

            file.close()

        return self.keyFrames
