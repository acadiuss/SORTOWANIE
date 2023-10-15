import sys
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
            sorter = BubbleSort(self.data.copy(), self.update_canvas)
        elif selected_algorithm == 'Insertion Sort':
            sorter = InsertionSort(self.data.copy(), self.update_canvas)
        elif selected_algorithm == 'Selection Sort':
            sorter = SelectionSort(self.data.copy(), self.update_canvas)
        elif selected_algorithm == 'Quick Sort':
            sorter = QuickSort(self.data.copy(), self.update_canvas)
        elif selected_algorithm == 'Merge Sort':
            sorter = MergeSort(self.data.copy(), self.update_canvas)
        
        sorter.sort()

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

class SortingAlgorithm:
    def __init__(self, data, callback):
        self.data = data
        self.callback = callback

    def sort(self):
        raise NotImplementedError("Subclasses must implement the 'sort' method.")

class BubbleSort(SortingAlgorithm):
    def sort(self):
        data = self.data
        for i in range(len(data)):
            for j in range(0, len(data) - i - 1):
                if data[j] > data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]
                self.callback(data)
                time.sleep(0.1)

class InsertionSort(SortingAlgorithm):
    def sort(self):
        data = self.data
        for i in range(1, len(data)):
            key = data[i]
            j = i - 1
            while j >= 0 and key < data[j]:
                data[j + 1] = data[j]
                j -= 1
            data[j + 1] = key
            self.callback(data)
            time.sleep(0.1)

class SelectionSort(SortingAlgorithm):
    def sort(self):
        data = self.data
        for i in range(len(data)):
            min_idx = i
            for j in range(i + 1, len(data)):
                if data[j] < data[min_idx]:
                    min_idx = j
            data[i], data[min_idx] = data[min_idx], data[i]
            self.callback(data)
            time.sleep(0.1)

class QuickSort(SortingAlgorithm):
    def partition(self, low, high):
        i = low - 1
        pivot = self.data[high]
        for j in range(low, high):
            if self.data[j] < pivot:
                i += 1
                self.data[i], self.data[j] = self.data[j], self.data[i]
                self.data[i + 1], self.data[high] = self.data[high], self.data[i + 1]
        return i + 1

    def sort(self):
        self.quick_sort(0, len(self.data) - 1)

    def quick_sort(self, low, high):
        if low < high:
            pi = self.partition(low, high)
            self.quick_sort(low, pi - 1)
            self.quick_sort(pi + 1, high)
            self.callback(self.data)
            time.sleep(0.1)

class MergeSort(SortingAlgorithm):
    def merge(self, left, mid, right):
        n1 = mid - left + 1
        n2 = right - mid
        L = [0] * n1
        R = [0] * n2
        for i in range(n1):
            L[i] = self.data[left + i]
        for j in range(n2):
            R[j] = self.data[mid + 1 + j]
        i = j = 0
        k = left
        while i < n1 and j < n2:
            if L[i] <= R[j]:
                self.data[k] = L[i]
                i += 1
            else:
                self.data[k] = R[j]
                j += 1
            k += 1
        while i < n1:
            self.data[k] = L[i]
            i += 1
            k += 1
        while j < n2:
            self.data[k] = R[j]
            j += 1
            k += 1
        self.callback(self.data)

    def merge_sort(self, left, right):
        if left < right:
            mid = (left + right) // 2
            self.merge_sort(left, mid)
            self.merge_sort(mid + 1, right)
            self.merge(left, mid, right)
            self.callback(self.data)

    def sort(self):
        self.merge_sort(0, len(self.data) - 1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SortingVisualizer()
    window.show()
    app.exec()

