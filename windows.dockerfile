# Use the Windows Server core image as the base
FROM mcr.microsoft.com/windows/servercore:ltsc2022

# Set the working directory
WORKDIR /app

# Define build arguments with default values
ARG APP_NAME=YourApplication.exe
ARG ADDITIONAL_FEATURES=""

# Copy the application files to the container
COPY . /app

# Install any necessary dependencies (example: .NET) and additional features
RUN powershell -Command \
    Install-WindowsFeature -Name Web-Server -IncludeManagementTools; \
    if ($env:ADDITIONAL_FEATURES -ne "") { Install-WindowsFeature -Name $env:ADDITIONAL_FEATURES }

# Define the entry point for the application using the build argument
ENTRYPOINT ["cmd.exe", "/c", "%APP_NAME%"]
