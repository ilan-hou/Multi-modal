import cv2
import os
from detect import detect2
def trans(filepath,filename):
    path=os.path.join(filepath,filename)
    cap=cv2.VideoCapture(path)
    fps=cap.get(cv2.CAP_PROP_FPS)
    if cap.isOpened():
        ret,frame=cap.read()
    else:
        ret = False
    delayFrame=fps
    c=0
    x=1
    while ret :
         ret,frame=cap.read()
         if(c%delayFrame==0):
             name = filename[:-4]+'_'+str(x)
             save_path = os.path.join('./image/',filepath.split('\\')[-1])
             if not os.path.exists(save_path):
                 os.mkdir(save_path)
             # print(save_path)
             try:
                 #cv2.imwrite(save_path,frame)
                 # print("--------------")
                 detect2(frame,name,save_path)
             except:
                 print("----------------------")

             # cv2.imwrite(filename.strip(".mp4") + '_' + str(x) + '.jpg', frame)
             x+=1
         c+=1
         cv2.waitKey(1)
    cap.release()
    cv2.destroyAllWindows()

"""for filepath,dirnames,filenames in os.walk('./data/entertainment-01-001.mp4'):
    for filename in filenames:
        print(os.path.join(filepath,filename))
        trans(filepath,dirnames,filename)"""
if __name__ == '__main__':
    # trans("./data/",'entertainment-01-001.mp4')
    for filepath, dirnames, filenames in os.walk('./data'):
        for filename in filenames:
            print(os.path.join(filepath, filename))
            trans(filepath, filename)