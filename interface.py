import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from threading import Timer
from kivy.animation import Animation
from kivy.config import Config
from custom_kivi import Gauge
import light

[Config.set('graphics', x, y) for x, y in {'resizable': '0', 'width': '1280', 'height': '640'}.items()]

class Controller(FloatLayout):
    def __init__(self):
        super(Controller, self).__init__()
        self.updateGauges()

    def updateGauges(self):
        try:
            values = []
            for x in open("./data.txt", 'r').readlines()[0].split(" "):
                values.append(float(x.split(":")[1]))

            print(values)
            values[2] = 100-values[2]/10
                
            self.label1.text = '[color=2a9c9d][b]Vlaga (%d)[/b][/color]' % values[0]
            self.label2.text = '[color=B9DA6E][b]Temperatura (%d)[/b][/color]' % values[1]
            self.label3.text = '[color=f98861][b]Svetlost (%d)[/b][/color]' % values[2]

            for i in range(len(values)):
                if values[i]<-20:
                    values[i]=-20
                elif values[i]>120:
                    values[i]=120
                    
            Animation(value = values[0]).start(self.gauge1)
            Animation(value = values[1]).start(self.gauge2)
            Animation(value = values[2]).start(self.gauge3)

        except Exception as ex:
            print("error occured", ex)

        Timer(1, self.updateGauges).start()

    def btn_click(self, btn, slider, index): 
        if "ON" not in btn.text.upper():
            slider.value = float(100)  
            if index == 1:
                light.turn0On(1)
            else:
                light.turn1On(1)
        else:
            slider.value = float(0)
            if index == 1:
                light.turn0On(0)
            else:
                light.turn1On(0)
	

    def slider_drag(self, btn, slider, index):
        if slider.value > float(1):
            btn.text = "[color=888][b]ON[/b][/color]"
            btn.background_color = (.4, .8, .9, 1.0)
##            if index == 1:
##                light.turn0On(float(round(slider.value/100, 1)))
##            else:
##                light.turn1On(float(round(slider.value/100, 1)))
        else:
            btn.text = "[color=888][b]OFF[/b][/color]"
            btn.background_color = (.7, .7, .7, 1.0)
##            if index == 1:
##                light.turn0On(0)
##            else:
##                light.turn1On(0)

class InterfaceApp(App): 
    build = lambda self: Controller()

InterfaceApp().run() if __name__ == '__main__' else None
