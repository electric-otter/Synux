import subprocess
import os
import shutil
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import docker

class DockerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
      
def browse_file():
    return filedialog.askopenfilename()

def show_installer():
    root = tk.Tk()
    root.title("AppImage Installer")

    tk.Label(root, text="Application Path:").grid(row=0, column=0, padx=10, pady=10)
    app_path_entry = tk.Entry(root, width=50)
    app_path_entry.grid(row=0, column=1, padx=10, pady=10)
    tk.Button(root, text="Browse", command=lambda: app_path_entry.insert(0, browse_file())).grid(row=0, column=2, padx=10, pady=10)

    tk.Label(root, text="Application Name:").grid(row=1, column=0, padx=10, pady=10)
    app_name_entry = tk.Entry(root, width=50)
    app_name_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(root, text="Requirements Path (optional):").grid(row=2, column=0, padx=10, pady=10)
    requirements_path_entry = tk.Entry(root, width=50)
    requirements_path_entry.grid(row=2, column=1, padx=10, pady=10)
    tk.Button(root, text="Browse", command=lambda: requirements_path_entry.insert(0, browse_file())).grid(row=2, column=2, padx=10, pady=10)

    def on_confirm():
        app_path = app_path_entry.get()
        app_name = app_name_entry.get()
        requirements_path = requirements_path_entry.get()

        if not app_path or not app_name:
            messagebox.showerror("Error", "Application path and name are required.")
            return

        if not os.path.isfile(app_path):
            messagebox.showerror("Error", "The specified application path does not exist.")
            return

        root.destroy()

        # Proceed with creating the AppImage
        create_appimage(app_path, app_name, requirements_path)

    tk.Button(root, text="Install", command=on_confirm).grid(row=3, column=1, padx=10, pady=10)
    root.mainloop()

def create_appimage(app_path, app_name, requirements_path):
    temp_dir = os.path.abspath("temp_appimage")
    os.makedirs(temp_dir, exist_ok=True)

    # Step 1: Write Dockerfile to the temporary directory
    dockerfile_content = f"""
    FROM your-base-image
    COPY {os.path.basename(app_path)} /usr/local/bin/{app_name}.exe

    # Install required packages (example: Python, pip, other packages)
    RUN apt-get update && apt-get install -y \\
        python3 \\
        python3-pip \\
        && rm -rf /var/lib/apt/lists/*

    # Copy requirements.txt if exists
    COPY requirements.txt /tmp/

    # Install Python packages from requirements.txt if it exists
    RUN if [ -f /tmp/requirements.txt ]; then pip3 install -r /tmp/requirements.txt; fi

    ENTRYPOINT ["{app_name}.exe"]
    """

    with open(os.path.join(temp_dir, 'Dockerfile'), 'w') as f:
        f.write(dockerfile_content)

    # Step 2: Copy the application and requirements.txt (if available) to the temporary directory
    shutil.copy(app_path, os.path.join(temp_dir, os.path.basename(app_path)))

    if requirements_path and os.path.isfile(requirements_path):
        shutil.copy(requirements_path, os.path.join(temp_dir, "requirements.txt"))

    # Change the working directory to the temporary directory
    os.chdir(temp_dir)

    # Step 3: Build Docker Image
    subprocess.run(["docker", "build", "-t", app_name, "."])

    # Step 4: Save Docker Image to Tar
    subprocess.run(["docker", "save", app_name, "-o", f"{app_name}.tar"])

    # Step 5: Extract Docker Image
    os.makedirs('AppDir', exist_ok=True)
    subprocess.run(["tar", "-xf", f"{app_name}.tar", "-C", "AppDir"])

    # Step 6: Create AppImage
    appimage_builder_yml = f"""
    script:
      - mkdir -p $APPDIR
      - tar -xf {app_name}.tar -C $APPDIR

    app_info:
      id: org.{app_name.lower()}
      name: {app_name}
      version: "1.0"
      exec: ./usr/local/bin/{app_name}.exe
      exec_args: $@
    """

    with open('AppImageBuilder.yml', 'w') as f:
        f.write(appimage_builder_yml)

    # Step 7: Run AppImageBuilder
    subprocess.run(["appimage-builder", "--recipe", "AppImageBuilder.yml"])

    # Clean up the temporary directory (optional)
    shutil.rmtree(temp_dir)

if __name__ == "__main__":
    show_installer()
"""


def emulator():
          self.setWindowTitle('Docker GUI Emulator')
        layout = QVBoxLayout()

        self.list_btn = QPushButton('List Containers')
        self.list_btn.clicked.connect(self.list_containers)
        layout.addWidget(self.list_btn)
        
        self.build_label = QLabel('Build Container:')
        layout.addWidget(self.build_label)
        self.build_input = QLineEdit()
        layout.addWidget(self.build_input)
        self.build_btn = QPushButton('Build')
        self.build_btn.clicked.connect(self.build_container)
        layout.addWidget(self.build_btn)
        
        self.start_label = QLabel('Start Container:')
        layout.addWidget(self.start_label)
        self.start_input = QLineEdit()
        layout.addWidget(self.start_input)
        self.start_btn = QPushButton('Start')
        self.start_btn.clicked.connect(self.start_container)
        layout.addWidget(self.start_btn)
        
        self.stop_label = QLabel('Stop Container:')
        layout.addWidget(self.stop_label)
        self.stop_input = QLineEdit()
        layout.addWidget(self.stop_input)
        self.stop_btn = QPushButton('Stop')
        self.stop_btn.clicked.connect(self.stop_container)
        layout.addWidget(self.stop_btn)

        self.setLayout(layout)
    
    def list_containers(self):
        containers = client.containers.list()
        output = "\n".join([container.name for container in containers])
        QMessageBox.information(self, 'Running Containers', output)

    def build_container(self):
        dockerfile_path = self.build_input.text()
        image, build_logs = client.images.build(path=dockerfile_path, rm=True)
        for log in build_logs:
            if 'stream' in log:
                print(log['stream'])
        QMessageBox.information(self, 'Build Status', 'Build Completed!')

    def start_container(self):
        container_name = self.start_input.text()
        container = client.containers.get(container_name)
        container.start()

    def stop_container(self):
        container_name = self.stop_input.text()
        container = client.containers.get(container_name)
        container.stop()
