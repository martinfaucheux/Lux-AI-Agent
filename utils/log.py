LOG_FILE = "log.txt"


class Logger:
    def __init__(self):
        self.path = LOG_FILE

        # reset file
        with open(self.path, "w") as f:
            f.write("")

    def log(self, message):
        with open(self.path, "a") as f:
            f.write(message)
