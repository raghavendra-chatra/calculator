from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon, QFont, QKeyEvent
from PyQt6.QtCore import Qt
import sys


class MyTextEdit(QTextEdit):
    keyList = {Qt.Key.Key_0.value : '0',
               Qt.Key.Key_1.value : '1',
               Qt.Key.Key_2.value : '2',
               Qt.Key.Key_3.value : '3',
               Qt.Key.Key_4.value : '4',
               Qt.Key.Key_5.value : '5',
               Qt.Key.Key_6.value : '6',
               Qt.Key.Key_7.value : '7',
               Qt.Key.Key_8.value : '8',
               Qt.Key.Key_9.value : '9',
               Qt.Key.Key_Plus.value : '+',
               Qt.Key.Key_Minus.value : '-',
               Qt.Key.Key_Asterisk.value : '*',
               Qt.Key.Key_Slash.value : '/',
               Qt.Key.Key_Percent.value : '%',
               Qt.Key.Key_Return.value : '=',
               Qt.Key.Key_Enter.value: '=',
               Qt.Key.Key_Equal.value: '=',
               Qt.Key.Key_Backspace.value: 'X'}

    def __init__(self):
        super().__init__()
        self.setCursorWidth(0)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() in self.keyList.keys():
            window.calc_functions(self.keyList.get(event.key()))
        else:
            pass


class Calculator(QWidget):
    def __init__(self):
        super(Calculator, self).__init__()
        self.setWindowTitle('Calculator')
        self.setWindowIcon(QIcon('calc.ico'))
        self.resize(600, 500)
        self.output = MyTextEdit()
        self.output.setFont(QFont('Courier New', 34))
        self.expression = ''
        self.calc_layout_structure()

    def calc_functions(self, action):
        try:
            if action == 'X':
                if self.expression != '':
                    self.expression = self.expression[:-1]
                    self.output.setText(self.expression)
                pass
            elif action == 'C':
                self.expression = ''
                self.output.setText(self.expression)
            elif action == '%':
                try:
                    if float(self.expression):
                        self.expression += '/100'
                        total = eval(self.expression)
                        self.output.setText(self.expression[:-4] + '% = ' + str(total))
                        self.expression = ''
                except:
                    pass
            elif action == 'x2':
                try:
                    if float(self.expression):
                        self.expression += '**2'
                        total = eval(self.expression)
                        self.output.setText(self.expression[:-3] + '*' + self.expression[:-3] + ' = ' + str(total))
                        self.expression = ''
                except:
                    pass
            elif self.expression == '' and action in '=*/+':
                pass
            elif self.expression != '' and action == '.':
                previous_deci = self.expression.rfind('.')  # find the index of previous decimal if any.
                if previous_deci != -1:
                    if any(o for o in '+-*/' if o in self.expression[previous_deci + 1:]):
                        self.expression += action
                        self.output.setText(self.expression)
                    else:
                        return
                else:
                    self.expression += action
                    self.output.setText(self.expression)
            elif action == '=':
                if self.expression[-1] not in ".+/-*":
                    total = eval(self.expression)
                    self.output.setText(self.expression + ' = ' + str(total))
                    self.expression = ''
                elif len(self.expression) == 1:
                    self.expression = ''
                    self.output.setText(self.expression)
                else:
                    temp = self.expression[:-1]
                    self.expression = temp
                    total = eval(self.expression)
                    self.output.setText(self.expression + ' = ' + str(total))
                    self.expression = ''
            elif self.expression != '' and action in '.+/*-' and self.expression[-1] in '.+/*-':
                pass
            else:
                self.expression += action
                self.output.setText(self.expression)
        except ZeroDivisionError:
            self.expression = 'ZeroDivisionError'
            self.output.setText(self.expression)
            self.expression = ''
            return

    def calc_layout_structure(self):
        layout = QGridLayout()
        self.setLayout(layout)

        # Position for text output
        output_position = (0, 0, 1, 0)
        layout.addWidget(self.output, * output_position)

        # Buttons
        names = ['%', 'C', 'X', 'x2',
                 '7', '8', '9', '/',
                 '4', '5', '6', '*',
                 '1', '2', '3', '+',
                 '0', '.', '=', '-']

        # Position for each button
        positions = [(i+1, j) for i in range(5) for j in range(4)]

        for position, name in zip(positions, names):
            button = QPushButton(name)
            layout.addWidget(button, *position)
            button.clicked.connect(lambda _, x=name: self.calc_functions(x))
            # clicked method fires a signal which needs a place holder, hence the underscore.
            # if a place holder parameter is not provided, it will override the x=name parameter.



app = QApplication(sys.argv)

window = Calculator()
window.show()

sys.exit(app.exec())