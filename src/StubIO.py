class StubIO:
    def __init__(self):
        self.input = []
        self.output = []

    def lue(self, teksti=""):
        self.output.append(teksti)
        if self.input:
            return self.input.pop(0)
        return ""

    def kirjoita(self, teksti):
        return self.output.append(teksti)
