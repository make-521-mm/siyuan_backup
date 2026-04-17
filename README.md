
---
### 🌏 语言 / Language

**[中文文档](README-zh.md)** | **[English](README.md)**

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


### 3. Configuration
Open `siyuan_back.py` in a text editor and modify the configuration section (Section 1) to match your environment:

```python
# --- 1. Configuration Paths ---
SIYUAN_DATA_PATH = r"D:\Users\mmake\SiYuan\data"  # Path to your SiYuan data folder
WEBDAV_DIR = r"Z:\123 Cloud Drive\back"           # Path to your mounted WebDAV drive
LOCAL_TEMP_DIR = r"D:\Temp\SiyuanBackup"          # Local temp folder (SSD recommended)
BACKUP_PASSWORD = "YourSecurePassword"            # Password for the 7z archive
```

### 4. Execution
You can run the script by double-clicking it or via the command line:

```bash
python siyuan_back.py
```

## 📂 Output & Logs

Upon execution, the script produces the following:

1.  **The Backup:** An encrypted `.7z` file (e.g., `SiYuan_data_20231010_120000.7z`) in your WebDAV directory.
2.  **The Log:** A `backup.log` file in the same directory as the script. This file contains the full history of runs, which is essential for debugging issues when running via Task Scheduler.

## 🗑️ Retention Policy

By default, the script keeps the **5 most recent backups**. To change this limit, locate the `KEEP_COUNT` parameter.

## 🐞 Troubleshooting

If the script fails or stops unexpectedly, please check the `backup.log` file. Common issues include:

-   **Path Errors:** Ensure paths do not contain invalid characters or use raw strings (`r"..."`).
-   **Drive Connection:** Ensure the WebDAV drive (e.g., Z:) is successfully mounted before the script runs.
-   **File Locking:** Ensure SiYuan Note is closed or files are not locked by other processes during backup.
```
