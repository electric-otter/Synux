import sys
import os
import shutil
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox
import docker

class DockerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.client = docker.from_env()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Docker and AppImage Manager')
        layout = QVBoxLayout()

        # List Containers
        self.list_btn = QPushButton('List Containers')
        self.list_btn.clicked.connect(self.list_containers)
        layout.addWidget(self.list_btn)

        # Build Container
        self.build_label = QLabel('Dockerfile Path:')
        layout.addWidget(self.build_label)
        self.build_input = QLineEdit()
        layout.addWidget(self.build_input)
        self.build_btn = QPushButton('Build Container')
        self.build_btn.clicked.connect(self.build_container)
        layout.addWidget(self.build_btn)

        # Start Container
        self.start_label = QLabel('Container to Start:')
        layout.addWidget(self.start_label)
        self.start_input = QLineEdit()
        layout.addWidget(self.start_input)
        self.start_btn = QPushButton('Start Container')
        self.start_btn.clicked.connect(self.start_container)
        layout.addWidget(self.start_btn)

        # Stop Container
        self.stop_label = QLabel('Container to Stop:')
        layout.addWidget(self.stop_label)
        self.stop_input = QLineEdit()
        layout.addWidget(self.stop_input)
        self.stop_btn = QPushButton('Stop Container')
        self.stop_btn.clicked.connect(self.stop_container)
        layout.addWidget(self.stop_btn)

        # AppImage Creation
        self.app_path_btn = QPushButton('Select Application File')
        self.app_path_btn.clicked.connect(self.select_app_file)
        layout.addWidget(self.app_path_btn)

        self.setLayout(layout)

    def list_containers(self):
        containers = self.client.containers.list()
        output = "\n".join([container.name for container in containers])
        QMessageBox.information(self, 'Running Containers', output)

    def build_container(self):
        dockerfile_path = self.build_input.text()
        if not os.path.isdir(dockerfile_path):
            QMessageBox.warning(self, 'Error', 'Invalid Dockerfile path.')
            return
        image, build_logs = self.client.images.build(path=dockerfile_path, rm=True)
        for log in build_logs:
            if 'stream' in log:
                print(log['stream'])
        QMessageBox.information(self, 'Build Status', 'Build Completed!')

    def start_container(self):
        container_name = self.start_input.text()
        try:
            container = self.client.containers.get(container_name)
            container.start()
            QMessageBox.information(self, 'Success', f'Container {container_name} started.')
        except docker.errors.NotFound:
            QMessageBox.warning(self, 'Error', f'Container {container_name} not found.')

    def stop_container(self):
        container_name = self.stop_input.text()
        try:
            container = self.client.containers.get(container_name)
            container.stop()
            QMessageBox.information(self, 'Success', f'Container {container_name} stopped.')
        except docker.errors.NotFound:
            QMessageBox.warning(self, 'Error', f'Container {container_name} not found.')

    def select_app_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Application File", "", "All Files (*)", options=options)
        if file_path:
            QMessageBox.information(self, 'Selected File', f'You selected: {file_path}')
            # Proceed with AppImage creation logic here

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DockerApp()
    ex.show()
    sys.exit(app.exec_())
