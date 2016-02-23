import eventBasedAnimation # requires version 1.10 or later
import random

class Dot(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = random.randint(20,50)
        self.fill = random.choice(["pink","orange","yellow","green",
                                   "cyan","purple"])
        self.clickCount = 0

    def containsPoint(self, x, y):
        d = ((self.x - x)**2 + (self.y - y)**2)**0.5
        return (d <= self.r)

    def draw(self, canvas):
        canvas.create_oval(self.x-self.r, self.y-self.r,
                           self.x+self.r, self.y+self.r,
                           fill=self.fill)
        canvas.create_text(self.x, self.y, text=str(self.clickCount))

class BestDotsDemo(eventBasedAnimation.Animation):
    def onInit(self):
        self.dots = [ ]
        self.aboutText = self.windowTitle = "bestDotsDemo (click in/out dots)"

    def onMouse(self, event):
        for dot in reversed(self.dots):
            if (dot.containsPoint(event.x, event.y)):
                dot.clickCount += 1
                return
        self.dots.append(Dot(event.x, event.y))

    def onDraw(self, canvas):
        for dot in self.dots:
            dot.draw(canvas)

BestDotsDemo().run()
