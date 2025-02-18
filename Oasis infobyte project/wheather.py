import sys
import asyncio
import aiohttp
import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout
from PyQt5.QtCore import Qt, QThread, pyqtSignal

API_KEY = "6ddec2f560686e41e571e8cd7fe99e48"
LAT = "28.6139"  # Example: New Delhi Latitude
LON = "77.2090"  # Example: New Delhi Longitude

class WorkerThread(QThread):
    data_fetched = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)

    async def get_past_temperatures(self):
        temperatures = []
        today = datetime.datetime.now()

        async with aiohttp.ClientSession() as session:
            for i in range(5):
                past_date = today - datetime.timedelta(days=i + 1)
                timestamp = int(past_date.timestamp())
                print("Time:",timestamp)
                url = f"https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={LAT}&lon={LON}&dt={timestamp}&appid=17cb6e99c3d0250f8a996d4f68e2bafa&units=metric"
                print(url)
                try:

                    async with session.get(url) as response:
                        data = await response.json()
                        print(data)
                        if "current" in data:
                            temp = data["current"]["temp"]
                            temperatures.append((past_date.strftime("%Y-%m-%d"), temp))
                        else:
                            temperatures.append((past_date.strftime("%Y-%m-%d"), "Retry-gotu"))
                except Exception as e:
                    print(f"Error fetching data: {e}")
                    temperatures.append((past_date.strftime("%Y-%m-%d"), "Retry-gotu"))
        return temperatures

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        temperatures = loop.run_until_complete(self.get_past_temperatures())
        self.data_fetched.emit(temperatures)

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Past 5 Days Temperature")
        self.setGeometry(100, 100, 600, 400)

        # Create layout
        layout = QVBoxLayout()

        # Title Label
        title_label = QLabel("Temperature for Last 5 Days")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title_label)

        # Create Table
        self.table = QTableWidget(0, 2)  # 2 columns (Date and Temperature)
        self.table.setHorizontalHeaderLabels(["Date", "Temperature (°C)"])
        layout.addWidget(self.table)

        # Fetch Data Button
        fetch_button = QPushButton("Fetch Data")
        fetch_button.clicked.connect(self.fetch_data)
        layout.addWidget(fetch_button)

        # Set layout
        self.setLayout(layout)

        # Create WorkerThread for async data fetching
        self.worker_thread = WorkerThread()
        self.worker_thread.data_fetched.connect(self.update_table)

    def fetch_data(self):
        self.worker_thread.start()  # Start the worker thread

    def update_table(self, temperatures):
        self.table.setRowCount(len(temperatures))  # Set the number of rows
        for row, (date, temp) in enumerate(temperatures):
            self.table.setItem(row, 0, QTableWidgetItem(date))
            self.table.setItem(row, 1, QTableWidgetItem(str(temp)))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
