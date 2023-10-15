
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

        self.sorting_algorithms = ['Bubble Sort', 'Insertion Sort', 'Selection Sort', 'Quick Sort', 'Merge Sort']
        self.sort_combobox = QComboBox(self)
        self.sort_combobox.addItems(self.sorting_algorithms)
        self.layout.addWidget(self.sort_combobox)

        self.data = np.random.randint(0, 100, 10)
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
        elif selected_algorithm == 'Quick Sort':
            self.quick_sort(self.data, 0, len(self.data) - 1)
        elif selected_algorithm == 'Merge Sort':
            self.data #= self.merge_sort(self.data)

    def bubble_sort(self):
        data = self.data.copy()
        for i in range(len(data)):
            for j in range(0, len(data) - i - 1):
                if data[j] > data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]
                self.update_canvas(data)
                time.sleep(0.1)

    def insertion_sort(self):
        data = self.data.copy()
        for i in range(1, len(data)):
            key = data[i]
            j = i - 1
            while j >= 0 and key < data[j]:
                data[j + 1] = data[j]
                j -= 1
            data[j + 1] = key
            self.update_canvas(data)
            time.sleep(0.1)

    def selection_sort(self):
        data = self.data.copy()
        for i in range(len(data)):
            min_idx = i
            for j in range(i + 1, len(data)):
                if data[j] < data[min_idx]:
                    min_idx = j
            data[i], data[min_idx] = data[min_idx], data[i]
            self.update_canvas(data)
            time.sleep(0.1)

    def partition(self, arr, low, high):
        i = low - 1
        pivot = arr[high]
        for j in range(low, high):
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    def quick_sort(self, arr, low, high):
        if low < high:
            pi = self.partition(arr, low, high)
            self.quick_sort(arr, low, pi - 1)
            self.quick_sort(arr, pi + 1, high)
            self.update_canvas(arr)

    def merge(self, arr, left, mid, right):
        n1 = mid - left + 1
        n2 = right - mid
        L = [0] * n1
        R = [0] * n2
        for i in range(n1):
            L[i] = arr[left + i]
        for j in range(n2):
            R[j] = arr[mid + 1 + j]
        i = j = 0
        k = left
        while i < n1 and j < n2:
            if L[i] <= R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
        while i < n1:
            arr[k] = L[i]
            i += 1
            k += 1
        while j < n2:
            arr[k] = R[j]
            j += 1
            k += 1

    def merge_sort(self, arr):
        if len(arr) > 1:
            mid = len(arr) // 2
            L = arr[:mid]
            R = arr[mid:]
            self.merge_sort(L)
            self.merge_sort(R)
            i = j = k = 0
            while i < len(L) and j < len(R):
                if L[i] < R[j]:
                    arr[k] = L[i]
                    i += 1
                else:
                    arr[k] = R[j]
                    j += 1
                k += 1
            while i < len(L):
                arr[k] = L[i]
                i += 1
                k += 1
            while j < len(R):
                arr[k] = R[j]
                j += 1
                k += 1
            self.update_canvas(arr)
        return arr

    def update_canvas(self, data):
        self.canvas.clear()
        self.canvas.bar(self.x, data, color='orange')
        self.canvas.draw()

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
    app.exec()
