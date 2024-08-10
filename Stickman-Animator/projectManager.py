class ProjectManager:
    def __init__(self):
        self.project_name = ''
        self.key_frames = []

    def set_project(self, name, os_path):
        self.project_name = name + '.stm'
        if not os_path.isfile(self.project_name):
            open(self.project_name, 'w').close()

    def store_key_frames(self, frames):
        keys = ''
        for frame in frames:
            for name, part in frame.BODY_PARTS.items():
                keys += "{},{},{},{},{}\n".format(name, part.bone.x, part.bone.y, part.x, part.y)

        file = open(self.project_name, "w")
        file.write(keys)
        file.close()

    def get_key_frames(self):
        file = open(self.project_name, "r")
        keys = file.read().strip().split('\n')
        dic = {}
        for i, key in enumerate(keys):
            key = key.split(',')
            dic[key[0]] = list(map(int, key[1:len(key)]))
            if (i + 1) % 10 == 0:
                self.key_frames.append(dic)
                dic = {}

            file.close()

        return self.key_frames
