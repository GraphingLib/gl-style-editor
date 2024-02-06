from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QColorDialog,
    QHBoxLayout,
    QCheckBox,
    QPushButton,
    QMainWindow,
    QWidget,
    QLabel,
    QLineEdit,
    QSlider,
    QComboBox,
)


class ColorButton(QPushButton):
    colorChanged = pyqtSignal(str)

    def __init__(self, *args, color=None, **kwargs):
        super(ColorButton, self).__init__(*args, **kwargs)
        self._color = None
        self._default = color
        self.pressed.connect(self.onColorPicker)
        self.setColor(self._default)
        self.setFixedSize(25, 25)

    def setColor(self, color):
        if color != self._color:
            self._color = color
            self.colorChanged.emit(color)
        if self._color:
            self.setStyleSheet("background-color: %s;" % self._color)
        else:
            self.setStyleSheet("")

    def color(self):
        return self._color

    def onColorPicker(self):
        dlg = QColorDialog(self)
        if self._color:
            dlg.setCurrentColor(QColor(self._color))

        # Calculate the position to move the dialog next to the button
        button_pos = self.mapToGlobal(self.pos())
        dlg.move(button_pos.x(), button_pos.y())

        if dlg.exec_():
            self.setColor(dlg.currentColor().name())

    def mousePressEvent(self, e):
        if e.button() == Qt.RightButton:  # type: ignore
            self.setColor(self._default)
        return super(ColorButton, self).mousePressEvent(e)


class ColorPickerWidget(QWidget):
    def __init__(
        self,
        window: QMainWindow,
        label="Pick a colour:",
        initial_color="#ff0000",
        param_ids=[],
        activated_on_init=True,
    ):
        super().__init__()
        self.the_window = window
        self.param_section = param_ids[0]
        self.param_labels = param_ids[1]
        self.layout = QHBoxLayout(self)  # type: ignore

        self.label = QLabel(label)
        self.colorButton = ColorButton(color=initial_color)
        self.colorEdit = QLineEdit(initial_color)
        self.colorEdit.setFixedWidth(60)  # Half the length
        self.colorButton.colorChanged.connect(self.onColorChanged)
        self.colorEdit.textChanged.connect(self.onColorEditTextChanged)

        self.copyButton = QPushButton("Copy")
        self.pasteButton = QPushButton("Paste")
        self.copyButton.setFixedWidth(65)  # Shorter copy button
        self.pasteButton.setFixedWidth(65)  # Shorter paste button
        self.copyButton.clicked.connect(
            lambda: QApplication.clipboard().setText(self.colorEdit.text())  # type: ignore
        )
        self.pasteButton.clicked.connect(
            lambda: self.colorEdit.setText(QApplication.clipboard().text())  # type: ignore
        )
        self.setEnabled(activated_on_init)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.colorButton)
        self.layout.addWidget(self.colorEdit)
        self.layout.addWidget(self.copyButton)
        self.layout.addWidget(self.pasteButton)

    def onColorChanged(self, color):
        self.colorEdit.setText(color)
        rc = {label: color for label in self.param_labels}
        self.the_window.params[self.param_section].update(rc)
        self.the_window.updateFigure()

    def onColorEditTextChanged(self, text):
        if QColor(text).isValid():
            self.colorButton.setColor(text)
            param = {label: text for label in self.param_labels}
            self.the_window.params[self.param_section].update(param)
            self.the_window.updateFigure()

    def getValue(self):
        return self.colorButton._color


class Activator(QWidget):
    def __init__(
        self,
        window: QMainWindow,
        label,
        widget,
        param_ids=[],
        condition="",
    ):
        super(Activator, self).__init__()
        self.the_window = window
        self.widget = widget
        self.param_section = param_ids[0]
        self.param_label = param_ids[1]
        self.layout = QHBoxLayout(self)
        self.condition = condition

        self.checkbox = QCheckBox(label)
        self.checkbox.setChecked(
            self.the_window.params[self.param_section][self.param_label] == condition
        )
        self.checkbox.stateChanged.connect(self.onStateChanged)
        self.layout.addWidget(widget)
        self.layout.addWidget(self.checkbox)

    def onStateChanged(self, state):
        self.widget.setEnabled(True if state != 2 else False)
        rc = {
            self.param_label: (self.condition if state == 2 else self.widget.getValue())
        }
        self.the_window.params[self.param_section].update(rc)
        self.the_window.updateFigure()


class Slider(QWidget):
    def __init__(
        self,
        window: QMainWindow,
        label,
        mini,
        maxi,
        tick_interval,
        param_ids=[],
        initial_value=0,
        activated_on_init=True,
    ):
        super(Slider, self).__init__()
        self.the_window = window
        self.param_section = param_ids[0]
        self.param_label = param_ids[1]

        self.label = QLabel(label)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(mini)
        self.slider.setMaximum(maxi)
        self.slider.setValue(initial_value * 2)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(tick_interval)
        self.slider.valueChanged.connect(self.onValueChanged)
        self.setEnabled(activated_on_init)

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.slider)

    def onValueChanged(self, value):
        rc = {self.param_label: value / 2}
        self.the_window.params[self.param_section].update(rc)
        self.the_window.updateFigure()

    def getValue(self):
        return self.slider.value() / 2


class Dropdown(QWidget):
    def __init__(
        self,
        window: QMainWindow,
        label,
        items=[],
        param_values=[],
        param_ids=[],
        initial_item=0,
        activated_on_init=True,
    ):
        super(Dropdown, self).__init__()
        self.the_window = window
        self.param_section = param_ids[0]
        self.param_label = param_ids[1]
        self.param_values = param_values

        self.label = QLabel(label)
        self.dropdown = QComboBox()
        self.dropdown.addItems(items)
        self.dropdown.setCurrentIndex(self.param_values.index(initial_item))
        self.dropdown.currentIndexChanged.connect(self.onCurrentIndexChanged)
        self.setEnabled(activated_on_init)

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.dropdown)

    def getValue(self):
        return self.dropdown.currentIndex()

    def onCurrentIndexChanged(self, index):
        rc = {self.param_label: self.param_values[index]}
        self.the_window.params[self.param_section].update(rc)
        self.the_window.updateFigure()