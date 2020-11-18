class player(object):
    def __init__(self, name, num, pos, color):
        self.name = name
        self.IS_AI = False
        self.num = 0
        self.pos = pos
        self.color = color
class chunk(object):
	def __init__(self):
		self.explored = False
		self.seized = None
		self.troops = 0