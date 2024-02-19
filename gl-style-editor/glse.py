import sys

import graphinglib as gl
from matplotlib.pyplot import close
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSplitter,
    QTabWidget,
    QVBoxLayout,
    QWidget,
    QScrollArea,
    QHBoxLayout,
    QLabel,
)
import numpy as np

from .plotting_1d_tab import create_plotting_1d_tab
from .plotting_2d_tab import create_plotting_2d_tab
from .figure_tab import create_figure_tab
from .fits_tab import create_fits_tab
from .shapes_tab import create_shapes_tab
from .other_gl_tab import create_other_gl_tab
from .example_plots import GLCanvas


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Updatable parameters
        self.params = gl.file_manager.FileLoader("plain").load()

        # Main widget and layout
        self.mainWidget = QWidget(self)
        self.mainLayout = QVBoxLayout(self.mainWidget)

        # header widget and layout
        self.headerWidget = QWidget(self)
        self.headerLayout = QHBoxLayout(self.headerWidget)
        self.headerLayout.setAlignment(Qt.AlignLeft)

        # Add a field for the figure style name
        figureStyleNameWidget = QWidget()
        figureStyleNameLayout = QVBoxLayout()
        figureStyleNameLabel = QLabel("Enter a name for your figure style:")
        figureStyleNameLayout.addWidget(figureStyleNameLabel)
        self.figureStyleName = QLineEdit(self)
        self.figureStyleName.setText("my_style")
        self.figureStyleName.setFixedWidth(200)
        figureStyleNameLayout.addWidget(self.figureStyleName)
        figureStyleNameWidget.setLayout(figureStyleNameLayout)
        self.headerLayout.addWidget(figureStyleNameWidget)

        # Add save button
        self.saveButton = QPushButton("Save", self)
        self.saveButton.clicked.connect(self.save)
        self.saveButton.setFixedWidth(100)
        self.mainLayout.addWidget(self.saveButton)

        # add header in main layout

        # Create a horizontal splitter to contain the tab widget and canvas
        self.splitter = QSplitter(Qt.Horizontal)  # type: ignore

        # Create and add the tab widget and canvas
        self.tabWidget = QTabWidget()
        self.canvas = GLCanvas(width=5, height=5, params=self.params)
        self.splitter.addWidget(self.tabWidget)
        self.splitter.addWidget(self.canvas)

        # Set the splitter as the main layout widget
        self.mainLayout.addWidget(self.splitter)

        # Combined Figure and Axes tab
        self.figureTab = QWidget()
        figureTabLayout = create_figure_tab(self)
        self.figureTab.setLayout(figureTabLayout)
        self.figureTabScrollArea = QScrollArea()
        self.figureTabScrollArea.setWidgetResizable(True)
        self.figureTabScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.figureTabScrollArea.setWidget(self.figureTab)
        self.tabWidget.addTab(self.figureTabScrollArea, "Figure")

        # 1D Plotting tab with nested tabs
        self.plotting1DTab = QWidget()
        self.tabWidget.addTab(self.plotting1DTab, "1D Plotting")
        create_plotting_1d_tab(self)

        # 2D Plotting tab with nested tabs
        self.plotting2DTab = QWidget()
        self.tabWidget.addTab(self.plotting2DTab, "2D Plotting")
        create_plotting_2d_tab(self)

        # Fits tab with nested tabs
        self.fitsTab = QWidget()
        self.tabWidget.addTab(self.fitsTab, "Fits")
        create_fits_tab(self)

        # Shapes tab with nested tabs
        self.shapesTab = QWidget()
        self.tabWidget.addTab(self.shapesTab, "Shapes")
        create_shapes_tab(self)

        # Other GL Objects tab with nested tabs
        self.otherGLTab = QWidget()
        self.tabWidget.addTab(self.otherGLTab, "Other GL Objects")
        create_other_gl_tab(self)

        # Set the main widget
        self.setCentralWidget(self.mainWidget)

    def updateFigure(self):
        # self.canvas.deleteLater()
        close()
        canvas = GLCanvas(width=5, height=4, params=self.params)
        self.splitter.replaceWidget(1, canvas)
        self.canvas = canvas

    def save(self):
        # get the figure style name
        name = self.figureStyleName.text()
        gl.file_manager.FileSaver(name, self.params).save()


def run():
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
