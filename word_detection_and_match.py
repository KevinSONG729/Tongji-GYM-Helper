import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from PIL import Image, ImageFont, ImageDraw
FLANN_INDEX_KDTREE = 0

def get_coordinate(target_word_list, img_filename):
    
    res_list = []
    used_flag = [0,0,0,0]
    
    # 获取mask
    img = cv.imread(img_filename)
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    low_hsv, high_hsv = np.array([0,0,0]), np.array([0,0,0])
    mask = cv.inRange(hsv, lowerb=low_hsv, upperb=high_hsv)

    # 图像腐蚀获得更好的聚类结果
    kernel = np.ones((2,2), np.uint8)
    mask_erode = cv.erode(mask, kernel)
    mask_idx = np.transpose(np.nonzero(mask_erode))
    cluster = KMeans(n_clusters=4, random_state=0, n_init='auto').fit(mask_idx)

    # 刨除聚类离群点，再做一次聚类
    new_mask_idx = []
    for label, point in zip(cluster.labels_, mask_idx):
        if(np.sqrt(np.sum((point - cluster.cluster_centers_[label])**2)) < 20):
            new_mask_idx.append(point)
    new_mask_idx = np.array(new_mask_idx)
    cluster = KMeans(n_clusters=4, random_state=0, n_init='auto').fit(new_mask_idx)

    # 获得文字对应图像，并用SIFT做匹配
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)
    flann = cv.FlannBasedMatcher(index_params,search_params)
    sift = cv.SIFT.create(100000)
    
    sorted_cluster_centers = sorted(cluster.cluster_centers_, key=lambda cluster: cluster[1])

    for word in target_word_list:
        im = Image.new("RGB", (40, 40), (0,0,0))
        dr = ImageDraw.Draw(im)
        font = ImageFont.truetype("STZHONGS.TTF", 30)
        dr.text((5,-2), word, font=font, align="center")
        target_data = np.array(list(im.convert("1").getdata())).reshape(40, 40)
        cv.imwrite('cache.png', target_data)
        kp_target, fe_target = sift.detectAndCompute(cv.imread('cache.png'),None) # 目标文字图像SIFT特征
        feature_list = []
        for point in sorted_cluster_centers:
            score = 0
            # print(point)
            mask_pre = mask[max(0, int(point[0])-20):int(point[0])+20, max(0, int(point[1])-20):int(point[1])+20]
            kp, fe = sift.detectAndCompute(mask_pre, None) # 检测图像中文字对应区域SIFT
            matches = flann.knnMatch(fe, fe_target, k = 2)
            for m, n in matches: # 计算匹配率，选择最高
                if m.distance <= 0.6*n.distance:
                    score += 1
            feature_list.append(score)
        sorted_idx = np.argsort(feature_list)[::-1]
        # print(sorted_idx)
        for idx in sorted_idx:
            if used_flag[idx] == 0:
                res_list.append([int(sorted_cluster_centers[idx][0]), int(sorted_cluster_centers[idx][1])])
                used_flag[idx] = 1
                break
            else:
                continue
    
    # for point in cluster.cluster_centers_:
    #     print(point)
    #     # mask = cv.drawMarker(mask, position=(int(point[1]), int(point[0])), color=(128,0,0), markerSize=50, markerType=cv.MARKER_CROSS, thickness=5)
    #     mask = cv.rectangle(mask, (int(point[1])-20, int(point[0])-20), (int(point[1])+20, int(point[0])+20), (255,0,0), 2)

    # cv.imshow("img",mask)
    # cv.waitKey(0)
    
    return res_list

if __name__ == "__main__":
    target_word_list = ['孑','孥','忶']
    c = get_coordinate(target_word_list, '1.png')
    print(c)