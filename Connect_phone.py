import subprocess

def download_file_by_path(device_path, local_file_path):
    try:
        # 使用 gmtp 命令行工具下载文件
        subprocess.run(["gmtp", "-c", device_path, "-local", local_file_path])
        print(f"文件已下载到：{local_file_path}")
    except Exception as e:
        print(f"下载文件时发生错误：{e}")

def main():
    # 指定路径
    target_path = 'Xiaomi 12:/内部存储设备/Android/data/tv.danmaku.bili/download'

    # 下载文件到本地
    local_file_path = 'D:/Data/Bili'+'\\'  # 修改为本地保存的文件路径
    download_file_by_path(target_path, local_file_path)

if __name__ == "__main__":
    main()
