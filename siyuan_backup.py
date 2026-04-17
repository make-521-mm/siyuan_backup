import os
import py7zr
import shutil
import sys
from datetime import datetime
import logging  # 新增：导入日志模块

# --- 1. 配置路径 ---
# 你的思源笔记 data 目录路径
SIYUAN_DATA_PATH = r"D:\Users\mmake\SiYuan\data"
# WebDAV 挂载的网盘目录 (最终存放位置)
WEBDAV_DIR = r"Z:\123 云盘\back"
# 本地临时压缩目录 (建议使用 SSD 硬盘，速度快且避免锁文件)
LOCAL_TEMP_DIR = r"D:\Temp\SiyuanBackup"  # 修改为你本地的一个临时文件夹
# 备份文件前缀
BACKUP_FILE_PREFIX = "SiYuan_data_"
# 备份密码 (建议配置环境变量)
BACKUP_PASSWORD = "4iyuan"
# BACKUP_PASSWORD = os.getenv("SIYUAN_BACKUP_PWD")
# 保留最新的 N 个备份
KEEP_COUNT = 5

# --- 1.1 新增：配置日志记录 ---
# 获取当前脚本所在的目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE_PATH = os.path.join(SCRIPT_DIR, f'siyuan_backup.log')

# 配置日志，同时输出到文件和控制台
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE_PATH, encoding='utf-8'),  # 写入脚本同级目录的文件
        logging.StreamHandler(sys.stdout)  # 保持原有的控制台输出
    ]
)

# --- 2. 准备工作 ---
# 记录脚本开始的绝对时间
start_time = datetime.now()
# 确保目录存在
os.makedirs(LOCAL_TEMP_DIR, exist_ok=True)
os.makedirs(WEBDAV_DIR, exist_ok=True)

# --- 3. 备份主函数 ---
def backup_encrypted():
    # 初始化阶段变量
    compress_duration = move_duration = cleanup_duration = 0
    archive_name = None
    try:
        date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_name = f"{BACKUP_FILE_PREFIX}{date_str}.7z"
        # 1. 本地临时路径 (先在这里生成压缩包)
        local_archive_path = os.path.join(LOCAL_TEMP_DIR, archive_name)
        # 2. WebDAV 目标路径 (压缩完成后要移动到这里)
        final_archive_path = os.path.join(WEBDAV_DIR, archive_name)

        # --- 阶段 1：加密压缩 ---
        logging.info(f"🔒 开始加密压缩: {LOCAL_TEMP_DIR}")
        logging.info(f"📄 临时文件: {local_archive_path}")
        compress_start = datetime.now()
        with py7zr.SevenZipFile(local_archive_path, mode='w', password=BACKUP_PASSWORD) as archive:
            archive.writeall(SIYUAN_DATA_PATH, arcname='data')
        compress_duration = datetime.now() - compress_start
        logging.info(f"✅ 本地压缩完成: {compress_duration}")

        # --- 阶段 2：移动文件 ---
        logging.info(f"🚚 开始移动到 WebDAV...")
        move_start = datetime.now()
        # shutil.move() 在跨设备移动时实际上是“复制+删除”
        shutil.move(local_archive_path, final_archive_path)
        move_duration = datetime.now() - move_start
        logging.info(f"💾 移动完成: {move_duration}")

        # --- 阶段 3：清理旧文件 ---
        logging.info(f"🧹 开始清理旧备份...")
        cleanup_start = datetime.now()
        cleanup_old_backups(WEBDAV_DIR, KEEP_COUNT)
        cleanup_duration = datetime.now() - cleanup_start
        logging.info(f"🧹 清理完成: {cleanup_duration}")

        # --- 汇总 ---
        # 主程序中会计算总时间
        return True, archive_name, compress_duration, move_duration, cleanup_duration
    except Exception as e:
        error_msg = f"❌ 备份失败: {e}"
        logging.error(error_msg).error
        return False, str(e), compress_duration, move_duration, cleanup_duration

def cleanup_old_backups(target_dir, keep_count=5):
    """保留目标目录中最新的 N 个备份，删除旧的"""
    try:
        files = [f for f in os.listdir(target_dir) if f.startswith(BACKUP_FILE_PREFIX) and f.endswith(".7z")]
        # 按文件名降序排序 (最新的在前)
        files.sort(reverse=True)
        if len(files) > keep_count:
            logging.info(f"🧹 检测到多余备份，开始清理...")
            for old_file in files[keep_count:]:
                file_to_remove = os.path.join(target_dir, old_file)
                os.remove(file_to_remove)
                logging.info(f"🗑️ 已删除: {old_file}")
    except Exception as e:
        logging.error(f"🧹 清理旧文件时出错: {e}")

if __name__ == "__main__":
    logging.info(f"🚀 备份任务启动: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    success, detail, c_d, m_d, cl_d = backup_encrypted()
    end_time = datetime.now()
    total_duration = end_time - start_time

    # --- 输出最终日志 ---
    if success:
        logging.info("\n" + "="*50)
        logging.info("🎉 备份任务成功完成！")
        logging.info(f"📝 备份文件: {detail}")
        logging.info(f"⏱️ 总耗时: {total_duration}")
        logging.info(f" ├─ 压缩耗时: {c_d}")
        logging.info(f" ├─ 传输耗时: {m_d}")
        logging.info(f" └─ 清理耗时: {cl_d}")
    else:
        logging.info("\n" + "="*50)
        logging.info("🚨 备份任务失败")
        logging.info(f"📝 错误信息: {detail}")
        logging.info(f"⏱️ 运行时间: {total_duration} (直到出错)")

    # 防止窗口立即关闭（如果双击运行）
    # input("\n按回车键退出...")
