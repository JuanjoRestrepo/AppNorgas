from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.image import Image
from database import DataBase


class CreateAccountWindow(Screen):
    nombre = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def crearCuenta(self):
        if self.nombre.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
            if self.password != "":
                db.add_user(self.email.text, self.password.text, self.nombre.text)

                self.reset()

                sm.current = "login"
            else:
                validarRequeridos()
        else:
            validarRequeridos()

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.nombre.text = ""


class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        if db.validar(self.email.text, self.password.text):
            MainWindow.current = self.email.text
            self.reset()
            sm.current = "main"
        else:
            validarDatos()

    def createBtn(self):
        self.reset()
        sm.current = "create"

    def reset(self):
        self.email.text = ""
        self.password.text = ""


class MainWindow(Screen):
    namen = ObjectProperty(None)
    created = ObjectProperty(None)
    email = ObjectProperty(None)
    current = ""

    def salir(self):
        sm.current = "login"

    def on_enter(self, *args):
        password, name, created = db.get_user(self.current)
        self.namen.text = "Nombre Cuenta: " + name
        self.email.text = "Email: " + self.current
        self.created.text = "Creada en: " + created


class WindowManager(ScreenManager):
    pass


def validarDatos():
    pop = Popup(title='Validar Datos',
                  content=Label(text='Usuario o Contraseña no validos.'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()


def validarRequeridos():
    pop = Popup(title='Validar Requeridos',
                  content=Label(text='Por favor, llene completa y\n correctamente los datos solicitados.'),
                  size_hint=(None, None), size=(400, 400))

    pop.open()


kv = Builder.load_file("my.kv")

sm = WindowManager()
db = DataBase("usuarios.txt")

screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"),MainWindow(name="main")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"


class MyMainApp(App):
    def build(self):

        Window.clearcolor = (0, 0.65, 255, 1)
        #Window.clearcolor = (240, 255, 0, 1)
        return sm


if __name__ == "__main__":
    MyMainApp().run()
