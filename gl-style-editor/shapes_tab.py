from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QScrollArea, QTabWidget, QVBoxLayout, QWidget

from .widgets import Activator, CheckBox, ColorPickerWidget, Dropdown, Slider


def create_shapes_tab(window):
    layout = QVBoxLayout()
    tabWidget = QTabWidget()

    # circle tab
    circleTabLayout = create_circle_tab(window)
    circleTab = QWidget()
    circleTab.setLayout(circleTabLayout)
    circleTabScrollArea = QScrollArea()
    circleTabScrollArea.setWidgetResizable(True)
    circleTabScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    circleTabScrollArea.setWidget(circleTab)
    tabWidget.addTab(circleTabScrollArea, "Circle")

    # create rectangle tab
    rectangleTabLayout = create_rectangle_tab(window)
    rectangleTab = QWidget()
    rectangleTab.setLayout(rectangleTabLayout)
    rectangleTabScrollArea = QScrollArea()
    rectangleTabScrollArea.setWidgetResizable(True)
    rectangleTabScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    rectangleTabScrollArea.setWidget(rectangleTab)
    tabWidget.addTab(rectangleTabScrollArea, "Rectangle")

    # Example stubs for each sub-tab
    arrowTab = QWidget()
    tabWidget.addTab(arrowTab, "Arrow")
    lineTab = QWidget()
    tabWidget.addTab(lineTab, "Line")

    layout.addWidget(tabWidget)
    window.shapesTab.setLayout(layout)


def create_circle_tab(window):
    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignTop)

    # create fill checkbox
    fill = CheckBox(window, "Fill", ["Circle", "fill"])
    layout.addWidget(fill)

    # create fill_alpha slider
    fill_alpha = Slider(
        window,
        "Fill Opacity",
        0,
        100,
        5,
        ["Circle", "fill_alpha"],
        conversion_factor=100,
    )
    layout.addWidget(fill_alpha)

    # create line_width slider
    line_width = Slider(
        window,
        "Line Width",
        0,
        10,
        1,
        ["Circle", "line_width"],
        conversion_factor=1,
    )
    layout.addWidget(line_width)

    # create line_style dropdown
    line_style = Dropdown(
        window,
        "Line Style",
        ["Solid", "Dashed", "Dotted", "Dash-Dot", "None"],
        ["-", "--", ":", "-.", "None"],
        ["Circle", "line_style"],
    )
    layout.addWidget(line_style)

    color = ColorPickerWidget(
        window,
        "Color",
        param_ids=["Circle", ["color"]],
        activated_on_init=(False if window.params["Circle"]["color"] == "" else True),
    )
    color_picker_widget = Activator(
        window,
        widget=color,
        param_ids=["Circle", "color"],
        check_label="Use color cycle",
        param_if_checked=None,
    )
    layout.addWidget(color_picker_widget)

    return layout


def create_rectangle_tab(window):
    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignTop)

    # create fill checkbox
    fill = CheckBox(window, "Fill", ["Rectangle", "fill"])
    layout.addWidget(fill)

    # create fill_alpha slider
    fill_alpha = Slider(
        window,
        "Fill Opacity",
        0,
        100,
        5,
        ["Rectangle", "fill_alpha"],
        conversion_factor=100,
    )
    layout.addWidget(fill_alpha)

    # create line_width slider
    line_width = Slider(
        window,
        "Line Width",
        0,
        10,
        1,
        ["Rectangle", "line_width"],
        conversion_factor=1,
    )
    layout.addWidget(line_width)

    # create line_style dropdown
    line_style = Dropdown(
        window,
        "Line Style",
        ["Solid", "Dashed", "Dotted", "Dash-Dot", "None"],
        ["-", "--", ":", "-.", "None"],
        ["Rectangle", "line_style"],
    )
    layout.addWidget(line_style)

    color = ColorPickerWidget(
        window,
        "Color",
        param_ids=["Rectangle", ["color"]],
        activated_on_init=(
            False if window.params["Rectangle"]["color"] == "" else True
        ),
    )
    color_picker_widget = Activator(
        window,
        widget=color,
        param_ids=["Rectangle", "color"],
        check_label="Use color cycle",
        param_if_checked=None,
    )
    layout.addWidget(color_picker_widget)

    return layout
