import sys
from PySide6.QtWidgets import QApplication, QLabel
from main_window import MainWindow
from PySide6.QtGui import QIcon
from variables import WINDOW_ICON_PATH


def temp_label(texto):
    label1 = QLabel(texto)
    label1.setStyleSheet('font-size: 150px')

    return label1


if __name__ == '__main__':
    # Cria a aplicação
    app = QApplication(sys.argv)
    window = MainWindow()

    # Define o ícone
    icon = QIcon(str(WINDOW_ICON_PATH))
    window.setWindowIcon(icon)

    # Define o ícone na taskbar
    if sys.platform.startswith('win'):
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            u'CompanyName.ProductName.SubProduct.VersionInformation')

    window.addWidgetToVLayout(temp_label('label 1'))

    # Executa tudo
    window.adjustFixedSize()
    window.show()
    app.exec()
