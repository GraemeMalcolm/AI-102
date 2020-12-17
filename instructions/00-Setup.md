# Lab Environment Setup

These exercises are designed to be completed ion a hosted lab environment. However, if you want to complete them on your own computer, you can do so by installing the following software. You may experience unexpected dialogs and behavior when using your own environment.

> **Note**: The instructions below are for a Windows 10 computer. You can also use Linux or MacOS.

## Base Operating System (Windows 10)

### Windows 10

Install Windows 10 and apply all updates.

### Edge

Install [Edge (Chromium)](https://microsoft.com/edge)

### WSL 2 

1. Open PowerShell as Administrator and run the following commands: 

```
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart 

dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```

2. Restart Windows and sign in again. 

3. Download and install the [x64](https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi) or [ARM64](https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_arm64.msi) version of WSL 2, depending on your hardware architecture. 

4. Reopen PowerShell as Administrator and run the following command: 

```
wsl --set-default-version 2 
```
 
## Docker 

1. Download **Docker Desktop** from https://www.docker.com/get-started 
2. Run setup
3. Sign out and in again

Docker will start automatically.

(If you use a non-Admin user for development, add your user account to **docker-users** group)

## .NET Core SDK

1. Download and install from https://dotnet.microsoft.com/download (download .NET Core SDK - not just the runtime)

## Node.JS

1. Download the latest LTS version from https://nodejs.org/en/download/ 
2. Install using the default options

## Python (and required packages)

1. Download version 3.8 from https://docs.conda.io/en/latest/miniconda.html 
2. Run setup to install - **Important**: Select the options to add Miniconda to the PATH variable and to register Miniconda as the default Python environment.
3. After installation, open the Anaconda prompt and enter the following command to install packages: 

```
pip install flask requests python-dotenv pylint matplotlib pillow 
```

## Azure CLI

1. Download from https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest 
2. Install using the default options

## Visual Studio Code (and extensions)

1. Download from https://code.visualstudio.com/Download 
2. Install using the default options 
3. After installation, start Visual Studio Code and on the **Extensions** tab (CTRL+SHIFT+X), search for and install the following extensions from Microsoft:
    - Python
    - C#
    - Azure Functions

## Bot Framework Emulator

Follow the instructions at https://github.com/Microsoft/BotFramework-Emulator/blob/master/README.md to diwnload and install the latest stable version of the Bot Framework Emulator for your operating system.

## Bot Framework Composer

Install from https://docs.microsoft.com/en-us/composer/install-composer.

