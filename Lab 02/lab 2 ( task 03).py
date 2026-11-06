class ClassroomAgent:

    def __init__(self):
        self.old_mode = None
    def act(self, temp, occupied):
        if occupied == False:
            mode = "ECO"
        elif temp > 26:
            mode = "COOL"
        elif temp < 20:
            mode = "WARM"
        else:
            mode = "IDLE"
        if mode != self.old_mode:
            command = "SEND COMMAND"
        else:
            command = "NO COMMAND"
        previous = self.old_mode
        self.old_mode = mode
        return previous, mode, command
agent = ClassroomAgent()
percepts = [
    (29, True),
    (29, True),
    (20, True),
    (26, True),
    (19, True),
    (29, False)
]
