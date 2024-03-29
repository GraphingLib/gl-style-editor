from typing import Optional

from matplotlib.colors import is_color_like, to_hex
from PyQt5.QtCore import QSortFilterProxyModel, QStringListModel, Qt, pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QColorDialog,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListView,
    QMainWindow,
    QPushButton,
    QSlider,
    QSpinBox,
    QVBoxLayout,
    QWidget,
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
        if self.colorEdit.text() == "" or (
            color != self.colorEdit.text() and color != to_hex(self.colorEdit.text())
        ):
            self.colorEdit.setText(color)
            self.the_window.update_params(self.param_section, self.param_labels, color)

    def onColorEditTextChanged(self, text):
        if QColor(text).isValid():
            self.colorButton.setColor(text)
            self.the_window.update_params(self.param_section, self.param_labels, text)
        elif is_color_like(text):
            # get the hex value of the color using matplotlib
            text = to_hex(text)
            self.colorButton.setColor(text)
            self.the_window.update_params(self.param_section, self.param_labels, text)

    def getValue(self):
        return self.colorButton._color


class Activator(QWidget):
    def __init__(
        self,
        window: QMainWindow,
        widget,
        param_ids=[],
        check_label="",
        param_if_checked: Optional[str] = "",
    ):
        super(Activator, self).__init__()
        self.the_window = window
        self.widget = widget
        self.param_section = param_ids[0]
        self.param_label = param_ids[1]
        self.layout = QHBoxLayout(self)  # type: ignore
        self.check_label = check_label
        self.param_if_checked = param_if_checked

        self.checkbox = QCheckBox(self.check_label)
        if (
            self.the_window.params[self.param_section][self.param_label]
            == param_if_checked
        ):

            is_checked = True
        else:
            is_checked = False
        self.checkbox.setChecked(is_checked)
        self.checkbox.stateChanged.connect(self.onStateChanged)
        self.widget.setEnabled(not is_checked)
        self.layout.addWidget(widget)
        self.layout.addWidget(self.checkbox)

    def onStateChanged(self, state):
        self.widget.setEnabled(True if state != 2 else False)
        if state == 2:
            new_param = self.param_if_checked
        else:
            new_param = self.widget.getValue()
        self.the_window.update_params(self.param_section, self.param_label, new_param)


class Slider(QWidget):
    def __init__(
        self,
        window: QMainWindow,
        label,
        mini,
        maxi,
        tick_interval,
        param_ids=[],
        conversion_factor=2,
    ):
        super(Slider, self).__init__()
        self.the_window = window
        self.param_section = param_ids[0]
        self.param_label = param_ids[1]
        self.factor = conversion_factor

        self.label = QLabel(label)
        self.slider = QSlider(Qt.Horizontal)  # type: ignore
        self.slider.wheelEvent = lambda event: event.ignore()  # type: ignore
        self.slider.setMinimum(mini)
        self.slider.setMaximum(maxi)
        if isinstance(
            self.the_window.params[self.param_section][self.param_label], str
        ):
            initial_value = 0
        else:
            initial_value = self.the_window.params[self.param_section][self.param_label]
        self.slider.setValue(int(initial_value * self.factor))
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(tick_interval)
        self.slider.valueChanged.connect(self.onValueChanged)
        self.setEnabled(
            not isinstance(
                self.the_window.params[self.param_section][self.param_label], str
            )
        )

        self.layout = QHBoxLayout(self)  # type: ignore
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.slider)

    def onValueChanged(self, value):
        new_value = value / self.factor
        # turn into int if it's a whole number
        if new_value == int(new_value):
            new_value = int(new_value)
        self.the_window.update_params(self.param_section, self.param_label, new_value)

    def getValue(self):
        return self.slider.value() / self.factor


class Dropdown(QWidget):
    def __init__(
        self,
        window: QMainWindow,
        label,
        items=[],
        param_values=[],
        param_ids=[],
    ):
        super(Dropdown, self).__init__()
        self.the_window = window
        self.param_section = param_ids[0]
        self.param_label = param_ids[1]
        self.param_values = param_values

        self.label = QLabel(label)
        self.dropdown = QComboBox()
        self.dropdown.addItems(items)
        if (
            isinstance(
                self.the_window.params[self.param_section][self.param_label], str
            )
            and "same as"
            in self.the_window.params[self.param_section][self.param_label]
        ):
            initial_index = 0
        else:
            initial_index = self.param_values.index(
                self.the_window.params[self.param_section][self.param_label]
            )
        self.dropdown.setCurrentIndex(initial_index)
        self.dropdown.currentIndexChanged.connect(self.onCurrentIndexChanged)
        if (
            isinstance(
                self.the_window.params[self.param_section][self.param_label], str
            )
            and "same as"
            in self.the_window.params[self.param_section][self.param_label]
        ):
            is_enabled = False
        else:
            is_enabled = True
        self.setEnabled(is_enabled)

        self.layout = QHBoxLayout(self)  # type: ignore
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.dropdown)

    def getValue(self):
        return self.dropdown.currentIndex()

    def onCurrentIndexChanged(self, index):
        self.the_window.update_params(
            self.param_section, self.param_label, self.param_values[index]
        )


class CheckBox(QWidget):
    def __init__(self, window: QMainWindow, label, param_ids=[]):
        super(CheckBox, self).__init__()
        self.checkbox = QCheckBox(label)
        self.the_window = window
        self.param_section = param_ids[0]
        self.param_label = param_ids[1]

        self.checkbox.setChecked(
            self.the_window.params[self.param_section][self.param_label]
        )
        self.checkbox.stateChanged.connect(self.onStateChanged)
        self.layout = QHBoxLayout(self)  # type: ignore
        self.layout.addWidget(self.checkbox)

    def onStateChanged(self, state):
        value = True if state == 2 else False
        self.the_window.update_params(self.param_section, self.param_label, value)


class IntegerBox(QWidget):
    def __init__(self, window: QMainWindow, label, param_ids=[]):
        super(IntegerBox, self).__init__()
        self.the_window = window
        self.param_section = param_ids[0]
        self.param_label = param_ids[1]

        self.label = QLabel(label)
        initial_value = self.the_window.params[self.param_section][self.param_label]
        initial_value = 0 if isinstance(initial_value, str) else int(initial_value)
        self.spinbox = QSpinBox()
        self.spinbox.setValue(initial_value)
        self.spinbox.valueChanged.connect(self.onValueChanged)

        self.layout = QHBoxLayout(self)  # type: ignore
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.spinbox)

    def onValueChanged(self, value):
        self.the_window.update_params(self.param_section, self.param_label, value)

    def getValue(self):
        return self.spinbox.value()


class ListOptions(QWidget):
    def __init__(self, window: QMainWindow, label, options=[], param_ids=[]):
        super(ListOptions, self).__init__()
        self.the_window = window
        self.param_section = param_ids[0]
        self.param_label = param_ids[1]

        self.labelWidget = QLabel(label)
        self.filterLineEdit = QLineEdit()
        self.filterLineEdit.setPlaceholderText("Type to filter options...")
        self.listView = QListView()

        self.model = QStringListModel(options)

        self.proxyModel = QSortFilterProxyModel(self)
        self.proxyModel.setFilterCaseSensitivity(Qt.CaseInsensitive)  # type: ignore
        self.proxyModel.setSourceModel(self.model)
        self.listView.setModel(self.proxyModel)

        # Connect the QLineEdit's textChanged signal to update the filter
        self.filterLineEdit.textChanged.connect(self.proxyModel.setFilterFixedString)

        self.layout = QVBoxLayout(self)  # type: ignore
        self.layout.addWidget(self.labelWidget)
        self.layout.addWidget(self.filterLineEdit)
        self.layout.addWidget(self.listView)

        # Connect the listView selection change to handle selection
        self.listView.selectionModel().selectionChanged.connect(self.onSelectionChanged)

    def onSelectionChanged(self, selected, deselected):
        # Assuming the parameter needs the text of the selected option
        selectedIndexes = self.listView.selectedIndexes()
        if selectedIndexes:
            selectedText = self.model.data(selectedIndexes[0], Qt.DisplayRole)  # type: ignore
            self.the_window.update_params(
                self.param_section, self.param_label, selectedText
            )

    def getCurrentSelection(self):
        selectedIndexes = self.listView.selectedIndexes()
        if selectedIndexes:
            return self.model.data(selectedIndexes[0], Qt.DisplayRole)  # type: ignore
        return None
