import os
import numpy as np
import shutil

image_data = {}
for filepath, dirnames, filenames in os.walk('./image'):
    for filename in filenames:
        name = filename.split('_')[0]
        id = filepath.split("\\")[-1]
        if id not in image_data:
            image_data[id] = [name]
        else:
            image_data[id].append(name)

video_data = {}
video_name = {}
for filepath, dirnames, filenames in os.walk('./data'):
    for filename in filenames:
        name = filename.split('.')[0]
        path = os.path.join(filepath, filename)
        id = filepath.split("\\")[-1]
        v_name = id +'_'+name
        video_name[v_name] = path
        if id not in video_data:
            video_data[id] = [path]
        else:
            video_data[id].append(path)

image_video = {}
for i in image_data.keys():
    image_video[i] = np.unique(image_data[i])

fp = open("removed.txt", "w+", encoding="utf-8")
path = './remove'
for i in video_name.keys():
    x = i.split('_')
    if x[1] not in image_video[x[0]].tolist():
        print(video_name[i])
        remove = os.path.join(path,x[0])
        if not os.path.exists(remove):
            os.mkdir(remove)
        fp.write(i + ' : ' + video_name[i] + '\n')
        shutil.move(video_name[i], remove)
fp.close()

