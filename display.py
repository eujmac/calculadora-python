from utils import isEmpty
from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeyEvent

# Import variáveis
from variables import BIG_FONT_SIZE, TEXT_MARGIN, MINIMUM_WIDTH


class Display(QLineEdit):
    eqPressed = Signal()
    delPressed = Signal()
    clearPressed = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        self.setStyleSheet(f'font-size: {BIG_FONT_SIZE}px')

        self.setMinimumHeight(BIG_FONT_SIZE * 2)
        self.setMinimumWidth(MINIMUM_WIDTH)

        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setTextMargins(*[TEXT_MARGIN for _ in range(4)])

    def keyPressEvent(self, event: QKeyEvent) -> None:
        text = event.text().strip()
        key = event.key()
        KEYS = Qt.Key

        isEnter = key in [KEYS.Key_Enter, KEYS.Key_Return]
        isDelete = key in [KEYS.Key_Backspace, KEYS.Key_Delete]
        isEsc = key in [KEYS.Key_Escape]

        if isEnter:
            print('isEnter pressionado, sinal emitido', type(self).__name__)
            self.eqPressed.emit()
            return event.ignore()

        if isDelete:
            print('isDelete pressionado, sinal emitido', type(self).__name__)
            self.delPressed.emit()
            return event.ignore()

        if isEsc:
            print('isEsc pressionado, sinal emitido', type(self).__name__)
            self.clearPressed.emit()
            return event.ignore()

        # não passar daqui se não tiver texto
        if isEmpty(text):
            return event.ignore()

        print('Texto ', text)
