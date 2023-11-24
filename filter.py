import os
import re

# 过滤非汉字、英文字母和数字字符
def FilterTitle(text):
    filtered_text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]', '', text)
    return filtered_text

# 删除标题中的重复文本
def RemoveDuplicates(text):
    words = text.split('_')  # 将标题拆分成单词或短语
    unique_words = list(dict.fromkeys(words))  # 找到不重复的部分
    new_title = '_'.join(unique_words)  # 将不重复的部分连接起来
    return new_title

# 遍历目录下的所有mp4视频文件
def process_videos(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.mp4'):
                video_path = os.path.join(root, file)
                new_title = FilterTitle(os.path.splitext(file)[0])
                new_title = RemoveDuplicates(new_title)
                new_filename = new_title + '.mp4'
                new_video_path = os.path.join(root, new_filename)
                os.rename(video_path, new_video_path)
                print(f"Renamed: {video_path} to {new_video_path}")

# 指定目录进行处理
target_directory = 'D:/Data/Videos_temp'
process_videos(target_directory)
