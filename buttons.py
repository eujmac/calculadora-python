import math
from PySide6.QtWidgets import QPushButton, QGridLayout
from PySide6.QtCore import Slot

# Import variáveis
from variables import MEDIUM_FONT_SIZE

from utils import isEmpty, isNumOrDot, isValidNumber
from display import Display

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from display import Display
    from info import Info


class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        # self.setStyleSheet(f'font-size: {MEDIUM_FONT_SIZE}px')
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        # font.setItalic(True)
        # font.setBold(True)
        self.setFont(font)
        self.setMinimumSize(50, 50)


class ButtonsGrid(QGridLayout):
    def __init__(self, display: 'Display', info: 'Info', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._gridMask = [
            ['C', 'D', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '', '.', '='],
        ]
        self.display = display
        self.info = info
        self._equation = ''
        self._equationInitialValue = 'Sua conta'
        self._left = None
        self._right = None
        self._op = None

        self.equation = self._equationInitialValue
        self._makeGrid()

    @property
    def equation(self):
        return self._equation

    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText(value)

    def _makeGrid(self):
        for i, row in enumerate(self._gridMask):
            for j, buttonText in enumerate(row):
                button = Button(buttonText)

                if not isNumOrDot(buttonText):
                    button.setProperty('cssClass', 'specialButton')
                    self._configSpecialButton(button)

                if buttonText == '':
                    continue

                if buttonText == '0':
                    self.addWidget(button, i, j, 0, 2)

                self.addWidget(button, i, j)
                slot = self._makeSlot(
                    self._insertButtonTextToDisplay, button)
                self._connectButtonClicked(button, slot)

    def _connectButtonClicked(self, button, slot):
        button.clicked.connect(slot)

    def _configSpecialButton(self, button):
        text = button.text()
        if text == 'C':
            self._connectButtonClicked(button, self._clear)

        if text in 'D':
            self._connectButtonClicked(button, self.display.backspace)

        if text in '+-/*^':
            self._connectButtonClicked(
                button, self._makeSlot(self._operatorClicked, button))

        if text in '=':
            self._connectButtonClicked(button, self._eq)

    def _makeSlot(self, func, *args, **kwargs):
        @Slot(bool)
        def realSlot(_):
            func(*args, **kwargs)

        return realSlot

    def _insertButtonTextToDisplay(self, button):
        buttonText = button.text()
        newDisplayValue = self.display.text() + buttonText

        if not isValidNumber(newDisplayValue):
            return

        self.display.insert(buttonText)

    def _clear(self):
        self._left = None
        self._right = None
        self._op = None
        self.equation = self._equationInitialValue

        self.display.clear()

    def _operatorClicked(self, button):
        buttonText = button.text()  # +-*/
        displayText = self.display.text()  # Deverá ser meu número _left
        self.display.clear()  # limpa o display

        # Se a pessoa clicou em um operador sem digitar nenhum número antes
        if not isValidNumber(displayText) and self._left is None:
            print('não tem nada para colocar no valor da esquerda')
            return

        # Se houver algo no número da esquerda, não fazemos nada. Aguardemos o número da direita
        if self._left is None:
            self._left = float(displayText)

        self._op = buttonText
        self.equation = f'{self._left} {self._op} ??'
        # print(buttonText)

    def _eq(self):
        displayText = self.display.text()

        if not isValidNumber(displayText):
            print('Sem nada para a direita')
            return

        self._right = float(displayText)
        self.equation = f'{self._left} {self._op} {self._right}'
        result = 'error'

        try:
            if '^' in self.equation and isinstance(self._left, float):
                result = math.pow(self._left, self._right)
            else:
                result = eval(self.equation)
        except ZeroDivisionError:
            print('Zero Division Error')
        except OverflowError:
            print('OverFlowError')

        self.display.clear()
        self.info.setText(f'{self.equation} = {result}')
        self._left = result
        self._right = None

        if result == 'error':
            self._left = None
