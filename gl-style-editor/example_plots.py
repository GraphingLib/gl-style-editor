import graphinglib as gl
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np


class GLCanvas(FigureCanvas):
    def __init__(self, params: dict, width=5, height=4):
        self.params = params
        self.gl_fig = gl.Figure(size=(width, height), figure_style="dark")
        self.compute_curve_figure()

        self.axes = self.gl_fig._axes
        self.fig = self.gl_fig._figure
        super(GLCanvas, self).__init__(self.fig)

    def compute_curve_figure(self):
        curve = gl.Curve([0, 1, 2, 3, 4], [2, 1, 2.5, 3, 4]) + 1.5
        curve.add_errorbars(y_error=0.5)
        curve2 = gl.Curve.from_function(
            lambda x: np.sin(3 * x) + 1, 0, 4, number_of_points=50
        )
        curve2.get_area_between(2, 4, fill_under=True)
        self.gl_fig.add_elements(curve, curve2)
        self.gl_fig._prepare_figure(default_params=self.params)
