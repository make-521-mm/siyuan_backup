
---

### 🇬🇧 English README

```markdown
# 📁 SiYuan Note Encryption Backup Script

This script automates the backup process for [SiYuan Note](https://b3log.org/siyuan/) data directories. It supports **7z encryption**, **WebDAV auto-upload**, and **automatic cleanup** of old backups. The script outputs logs to both the console and a local file, making it easy to troubleshoot errors when running in the background.

## 🛠️ Core Features

-   **🔒 AES-256 Encryption**: Protects your notes with a password to prevent data leaks in the cloud.
-   **☁️ WebDAV Sync**: Automatically moves the backup archive to your mounted WebDAV drive.
-   **🧹 Auto-Cleanup**: Keeps only the latest N backups and deletes old ones to save space.
-   **📝 Detailed Logging**: Records execution time, compression duration, transfer duration, and errors.

## ⚙️ Quick Start

### 1. Prerequisites
Ensure you have **Python 3.7** or higher installed.

### 2. Install Dependencies
Open a terminal (CMD/PowerShell) in the script directory and run:

```bash
pip install py7zr
