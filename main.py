import sys
# Import pyside
from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtGui import QIcon
import qdarktheme

# Import minhas classes
from main_window import MainWindow
from display import Display
from info import Info
from styles import setupTheme
from buttons import Button

# Import variáveis
from variables import WINDOW_ICON_PATH


if __name__ == '__main__':
    # Cria a aplicação
    app = QApplication(sys.argv)
    setupTheme()

    window = MainWindow()

    # Define o ícone
    icon = QIcon(str(WINDOW_ICON_PATH))
    window.setWindowIcon(icon)

    # Define o ícone na taskbar
    if sys.platform.startswith('win'):
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            u'CompanyName.ProductName.SubProduct.VersionInformation')

    # Info
    info = Info('2.0 ^ 10.0 = 1024')
    window.addWidgetToVLayout(info)

    # Display
    display = Display()
    # display.setPlaceholderText('Digite algo')
    window.addWidgetToVLayout(display)

    # Button
    button = Button('Texto do button')
    window.addWidgetToVLayout(button)

    button2 = Button('Texto do button2')
    window.addWidgetToVLayout(button2)

    # Executa tudo
    window.adjustFixedSize()
    window.show()
    app.exec()
