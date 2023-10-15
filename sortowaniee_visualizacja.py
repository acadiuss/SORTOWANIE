import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QComboBox, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from threading import Thread
import time

class SortingVisualizer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Sorting Visualizer')
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.canvas = PlotCanvas(self, width=5, height=4)
        self.layout.addWidget(self.canvas)

        self.sort_button = QPushButton('Sort', self)
        self.sort_button.clicked.connect(self.visualize_sorting)
        self.layout.addWidget(self.sort_button)

        self.sorting_algorithms = ['Bubble Sort', 'Insertion Sort', 'Selection Sort']
        self.sort_combobox = QComboBox(self)
        self.sort_combobox.addItems(self.sorting_algorithms)
        self.layout.addWidget(self.sort_combobox)

        self.lst = np.random.randint(0, 100, 10)
        self.x = np.arange(0, 10, 1)

        self.sorting_thread = None

    def visualize_sorting(self):
        if self.sorting_thread is not None and self.sorting_thread.is_alive():
            return

        selected_algorithm = self.sort_combobox.currentText()
        self.sorting_thread = Thread(target=self.sorting_worker, args=(selected_algorithm,))
        self.sorting_thread.start()

    def sorting_worker(self, selected_algorithm):
        if selected_algorithm == 'Bubble Sort':
            self.bubble_sort()
        elif selected_algorithm == 'Insertion Sort':
            self.insertion_sort()
        elif selected_algorithm == 'Selection Sort':
            self.selection_sort()

    def bubble_sort(self):
        for i in range(10):
            for j in range(0, 10 - i - 1):
                self.canvas.clear()
                self.lst, swapped = self.bubble_step(self.lst)
                self.canvas.bar(self.x, self.lst, color='orange')
                self.canvas.draw()
                time.sleep(0.1)
                if not swapped:
                    return

    def bubble_step(self, arr):
        n = len(arr)
        swapped = False
        for i in range(n - 1):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
        return arr, swapped

    def insertion_sort(self):
        for j in range(10 - 1, 0, -1):
            x = self.lst[j]
            ip = j
            ik = 10 + 1
            while ik - ip > 1:
                i = (ip + ik) // 2
                if x <= self.lst[i]:
                    ik = i
                else:
                    ip = i
            for i in range(j, ip - 1, -1):
                self.lst[i] = self.lst[i - 1]
            self.lst[ip] = x
            self.canvas.clear()
            self.canvas.bar(self.x, self.lst, color='orange')
            self.canvas.draw()
            time.sleep(0.1)

    def selection_sort(self):
        for j in range(10 - 1, 0, -1):
            min_idx = j
            for i in range(j):
                if self.lst[i] < self.lst[min_idx]:
                    min_idx = i
            self.lst[j], self.lst[min_idx] = self.lst[min_idx], self.lst[j]
            self.canvas.clear()
            self.canvas.bar(self.x, self.lst, color='orange')
            self.canvas.draw()
            time.sleep(0.1)

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)
        
    def bar(self, x, y, **kwargs):
        self.ax.bar(x, y, **kwargs)
        
    def clear(self):
        self.ax.clear()

if __name__ == '__main__':
    app = QApplication([])
    window = SortingVisualizer()
    window.show()
    app.exec_()
