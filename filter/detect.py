import cv2
import os
from facenet_pytorch import  InceptionResnetV1, fixed_image_standardization
import torch
from PIL import Image
from torchvision import transforms,get_image_backend
import numpy as np
import math

size_m = 30
size_n = 30

os.environ["CUDA_VISIBLE_DEVICES"] = '1'
workers = 0 if os.name == 'nt' else 8

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
print('Running on device: {}'.format(device))

resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)

trans = transforms.Compose([
    transforms.Resize((160,160)),
    np.float32,
    transforms.ToTensor(),
    fixed_image_standardization
])

def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30),
                                     flags=cv2.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:, 2:] += rects[:, :2]
    return rects

def pil_loader(path):
    with open(path, 'rb') as f:
        with Image.open(f) as img:
            return img.convert('RGB')

def distance(embeddings1, embeddings2, distance_metric=1):
    if distance_metric==0:
        # Euclidian distance
        diff = np.subtract(embeddings1, embeddings2)
        dist = np.sum(np.square(diff),1)
    elif distance_metric==1:
        # Distance based on cosine similarity
        dot = np.sum(np.multiply(embeddings1, embeddings2), axis=1)
        norm = np.linalg.norm(embeddings1, axis=1) * np.linalg.norm(embeddings2, axis=1)
        similarity = dot / norm
        dist = np.arccos(similarity) / math.pi
    else:
        raise 'Undefined distance metric %d' % distance_metric

    return dist

def filter():
    classes = {}
    enroll = {}
    for filepath, dirnames, filenames in os.walk('./enroll'):
        for filename in filenames:
            enroll_path = os.path.join(filepath, filename)
            id = filepath.split("\\")[-1]
            if id not in enroll:
                enroll[id] = [enroll_path]
            else:
                enroll[id].append(enroll_path)

    for i in (enroll.keys()):
        classes.update({i: []})

    with torch.no_grad():
        for id in enroll.keys():
            for path in enroll[id]:
                tb = pil_loader(path)
                tb = trans(tb)
                tb = tb.to(device)
                tb = torch.unsqueeze(tb, dim=0)
                embedt = resnet(tb)
                classes[id].append(embedt.to('cpu').numpy())
            classes.update({id: np.mean(np.array(classes[id]), 0)})
    return classes

classes = filter()

def detect2(img,name,path):
    cascade = cv2.CascadeClassifier("./haarcascade_frontalface_alt2.xml")
    dst = img
    rects = detect(dst, cascade)
    # print(rects)
    n=0
    image = {}
    for x1, y1, x2, y2 in rects:
        # 调整人脸截取的大小。横向为x,纵向为y
        roi = dst[y1 + 10:y2 + 20, x1 + 10:x2]
        img_roi = roi
        n+=1
        re_roi = cv2.resize(img_roi, (size_m, size_n))
        # print(name+'_'+str(n))
        # print(path)
        image_name = name+'_'+str(n)+'.jpg'
        image_path = os.path.join(path,image_name)
        image[image_path] = re_roi
        # with torch.no_grad():
        #     tb = Image.fromarray(np.uint8(re_roi)).convert('RGB')
        #     tb = trans(tb)
        #     tb = tb.to(device)
        #     tb = torch.unsqueeze(tb, dim=0)
        #     embedt = resnet(tb)
        # if distance(classes[path[-7:]],embedt.to('cpu').numpy()) < 0.4:
        #     print(distance(classes[path[-7:]],embedt.to('cpu').numpy()))
        #     print(image_path)
        #     cv2.imwrite(image_path, re_roi)
    dis = {}
    if len(image.keys()) == 0:
        print('pass')
    elif len(image.keys()) == 1:
        for i in image:
            with torch.no_grad():
                tb = Image.fromarray(np.uint8(image[i])).convert('RGB')
                tb = trans(tb)
                tb = tb.to(device)
                tb = torch.unsqueeze(tb, dim=0)
                embedt = resnet(tb)
            x = distance(classes[path[-7:]], embedt.to('cpu').numpy())
            if x < 0.4:
                print(i)
                cv2.imwrite(i, image[i])
    else:
        for i in image:
            with torch.no_grad():
                tb = Image.fromarray(np.uint8(image[i])).convert('RGB')
                tb = trans(tb)
                tb = tb.to(device)
                tb = torch.unsqueeze(tb, dim=0)
                embedt = resnet(tb)
            dis[i]=distance(classes[path[-7:]],embedt.to('cpu').numpy())
        corpath=min(dis.items(),key=lambda x:x[1])[0]
        if dis[corpath] < 0.4:
            print(corpath)
            cv2.imwrite(corpath, image[corpath])
