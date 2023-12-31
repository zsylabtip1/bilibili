import os
import json
import re
import argparse
import random
import string

global FFmpeg
global NewFolder
global Danmuku
# 命令行解析
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--ffmpeg', type=str,
                    default="ffmpeg", help="FFmpeg的路径，默认为当前目录")
parser.add_argument('-folder', action='store_true',
                    default=False, help="是否每一个视频一个文件夹")
parser.add_argument('-danmaku', action='store_true',
                    default=False, help="是否转换.xml到弹幕文件.aas")
parser.add_argument('-file', default='D:/Data/temp'+'\\', metavar='FILE',help='b站缓存文件文件夹')
parser.add_argument('-s', '--save', type=str,
                    default='D:/Data/Bili'+'\\', help='释放的位置，默认为本脚本所在目录')

args = parser.parse_args()

# 初始化
FFmpeg = args.ffmpeg
NewFolder = args.folder
Danmaku = args.danmaku
File = args.file
Save = args.save
Danmaku2Ass='danmaku2ass.exe' if os.path.exists('danmaku2ass.exe') else 'python danmaku2ass.py'
AddAuthorMsg=False # 个人的需求，可以在文件夹下方生成Author.txt，方便查看原作者


# 生成一个随机字符串，用于在标题中添加随机数
def generate_random_string(length=4):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

# 利用os.walk仅查找目录，返回列表
def DirFolder(n): return [
    n+'/'+i if not os.path.isdir(os.path.realpath((n+i))) else n+i for i in os.listdir(n)]

# 标题中的非法字符过滤
def Filter(t): return re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]', "", t)

# 搜索文件
def SearchFile(name: str, s: str):
    Filelist = []
    for home, dirs, files in os.walk(name):
        for filename in files:
            if os.path.join(home, filename).find(s) != -1:
                Filelist.append(os.path.join(home, filename))
    return Filelist[0] if len(Filelist) == 1 else Filelist


def ReadJson(n: str):
    try:
        with open(os.path.realpath(n), 'r', encoding='utf-8') as load_f:
            load_dict = json.load(load_f)
        return load_dict
    except:
        return None

# 有的json没有part，只有title
def ReadTitle(load_dict: dict):
    if 'part' not in load_dict['page_data']:
        return Filter(load_dict['title'])
    else:
        return Filter(load_dict['title'])

# 生成指令list
def MergeVideo(fn):
    ffmpeg = []
    title_set = set()  # 用于存储已经生成过的标题
    for i in DirFolder(fn):
        jsonData = ReadJson(SearchFile(i, 'entry.json'))
        if NewFolder:
            fl = Save + '\\' + Filter(jsonData['title']) + '\\' + Filter(ReadTitle(jsonData))
            folder = Save + '\\' + Filter(jsonData['title']) + '\\'
            if not os.path.exists(folder):
                os.mkdir(folder)
            ffmpeg.append('{} -i "{}" -i "{}" -c copy "{}.mp4"'.format(FFmpeg, SearchFile(i, 'video.m4s'), SearchFile(i, 'audio.m4s'), fl))
            if AddAuthorMsg:
                with open(folder + 'author.txt', 'w+') as f:
                    f.write(jsonData['owner_name'] + '\n' + str(jsonData['owner_id']) + '\n' + jsonData['bvid'] + '\n' + (jsonData['owner_avatar'] if 'owner_avatar' in jsonData else ''))
            if Danmaku:
                ffmpeg.append('{} "{}" -s {}x{} -fn "微软雅黑" -fs 48 -a 0.8 -dm 5 -ds 5 -o "{}"'.format(Danmaku2Ass, SearchFile(i, 'danmaku.xml'), jsonData['page_data']['width'], jsonData['page_data']['height'], fl + '.ass'))
        else:
            if jsonData['type_tag'] == '64':
                fl = Save + '\\' + Filter(ReadTitle(jsonData))
            else:
                # 检查标题是否重复
                title = Filter(ReadTitle(jsonData))
                while title in title_set:
                    # 如果标题重复，加上一个随机数，直到标题唯一为止
                    title = title + '_' + generate_random_string()
                title_set.add(title)
                fl = Save + '\\' + title
            # 检查视频文件是否已经存在
            index = 1
            while os.path.exists(fl + '.mp4'):
                # 如果视频文件已经存在，添加索引数字
                fl = Save + '\\' + title + f'_{index}'
                index += 1
            ffmpeg.append('{} -i "{}" -i "{}" -c copy "{}.mp4"'.format(FFmpeg, SearchFile(i, 'video.m4s'), SearchFile(i, 'audio.m4s'), fl))
            if Danmaku:
                ffmpeg.append('{} "{}" -s {}x{} -fn "微软雅黑" -fs 48 -a 0.8 -dm 5 -ds 5 -o "{}"'.format(Danmaku2Ass, SearchFile(i, 'danmaku.xml'), jsonData['page_data']['width'], jsonData['page_data']['height'], fl + '.ass'))

    return ffmpeg


for i in DirFolder(File):
    buffer = MergeVideo(i)
    for ii in buffer:
     os.system(ii)

