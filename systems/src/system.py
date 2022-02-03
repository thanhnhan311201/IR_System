import os
import pickle
from PIL import Image
import numpy as np
import cv2
from scipy import spatial
import time
import glob
from tqdm import tqdm

try:
    import feature_extractor
except:
    from systems.src import feature_extractor

class CBIR_System:
    def __init__(self, dataset_path='systems/datasets/paris_dataset/', image_folder='IRsystem_WebPage/static/datasets/paris_dataset/images/'):
        self.extractor_method = 'Xception_FE'
        self.extractor = feature_extractor.Xception_FE()

        self.dataset_path = dataset_path
        self.feature_folder_path = dataset_path + 'feature_folder/'
        self.gt_folder_path = dataset_path + 'gt_files/'
        self.image_folder = image_folder

    def index_dataset(self):
        if not os.path.exists(self.feature_folder_path):
            os.mkdir(self.feature_folder_path)

        if not os.path.exists(f'{self.feature_folder_path}features_{self.extractor_method}/'):
            os.mkdir(f'{self.feature_folder_path}features_{self.extractor_method}/')

        vector_file = f'{self.feature_folder_path}features_{self.extractor_method}/feature_vectors.pkl'
        path_file = f'{self.feature_folder_path}features_{self.extractor_method}/img_paths.pkl'
        
        vectors = []
        paths = []
        for img_path in tqdm(os.listdir(self.image_folder)):
            img_path_full = os.path.join(self.image_folder + img_path)
            
            try:
                feature_vector = self.extractor.extract(img=Image.open(img_path_full))
            except:
                continue

            vectors.append(feature_vector)
            paths.append(img_path)

        pickle.dump(vectors, open(vector_file, "wb"))
        pickle.dump(paths, open(path_file, "wb"))

        return 'Done!'

    def retrieve_img(self, img, K=32):
        query_start_time = time.time()

        vector_file = f'{self.feature_folder_path}features_{self.extractor_method}/feature_vectors.pkl'
        path_file = f'{self.feature_folder_path}features_{self.extractor_method}/img_paths.pkl'
        feature_vectors = pickle.load(open(vector_file,"rb"))
        img_paths = pickle.load(open(path_file,"rb"))

        if isinstance(img, str):
            img = Image.open(img)

        query_img = self.extractor.extract(img)

        # # calculate the eculide distance
        # similarity = np.linalg.norm(feature_vectors-query_img, axis=1)
        # # select top K relevant image
        # ids = np.argsort(similarity)[:K]

        # calculate the cosine similarity
        similarity = []
        for vector in feature_vectors:
            cos_sim = 1 - spatial.distance.cosine(vector, query_img)
            similarity.append(cos_sim)
        # select top K relevant image
        ids = np.argsort(similarity)[::-1][:K]

        relevant_imgs = [(similarity[id], img_paths[id]) for id in ids]
        
        query_time = time.time() - query_start_time

        return relevant_imgs, query_time

    def query_n_display_results(self, query_image):
        relevant_imgs, query_time = self.retrieve_img(query_image)

        if isinstance(query_image, str):
            query_image = cv2.imread(query_image)

        if not isinstance(query_image, np.ndarray):
            query_image = np.array(query_image)

        cv2.imshow('Query image', query_image)
        cv2.waitKey(0)

        print('----------------RESULTS----------------')
        for img_info in relevant_imgs:
            rel_img = cv2.imread(self.image_folder + img_info[1])
            cv2.imshow('Relevant image', rel_img)
            print(f'Relevant image file: {img_info[1]}')
            cv2.waitKey(0)

        print(f'Query Time: {np.round(query_time, 2)}s')
        
        return 'Done!'

    def evaluate_system(self):
        res_folder_path = f'{self.dataset_path}evaluation_result/'
        if not os.path.exists(res_folder_path):
            os.mkdir(res_folder_path)
        res_file_path = f'{res_folder_path}eval_result_{self.extractor_method}.txt'
        if os.path.exists(res_file_path):
            os.remove(res_file_path)

        res_file = open(res_file_path, 'a')

        line = '-----------START EVALUATING THE SYSTEM-----------\n'
        res_file.write(line + '\n')
        print(line)

        eval_start_time = time.time()

        query_files = glob.glob(os.path.join(self.gt_folder_path, "*_query.txt"))
        query_files = [x.replace("\\", "/") for x in query_files]
        
        AP_score_lst = []
        for file in query_files:
            gt_imgs = []
            
            with open(file.replace("query", "good"), 'r') as gt_fi:
                gt_imgs += [x.strip() for x in gt_fi.readlines()]

            with open(file.replace("query", "ok"), 'r') as gt_fi:
                gt_imgs += [x.strip() for x in gt_fi.readlines()]

            K = len(gt_imgs)

            with open(file, 'r') as query_fi:
                img_info = query_fi.readlines()[0].strip().split(' ')
                img_name = img_info[0].replace("oxc1_", "") + ".jpg"
                x_min, y_min, x_max, y_max = [int(float(x)) for x in img_info[1:]]
                
                query_img = Image.open(self.image_folder + img_name)
                query_img = query_img.crop((x_min, y_min, x_max, y_max))

                relevant_imgs, query_time = self.retrieve_img(query_img, K)

                relevant_jugdes = []
                for img_info in relevant_imgs:
                    img_name = img_info[1].split('/')[-1].split('.')[0]

                    if img_name in gt_imgs:
                        relevant_jugdes.append(1)
                    else:
                        relevant_jugdes.append(0)
                
                if np.sum(np.array(relevant_jugdes)) == 0:
                    AP_score_lst.append(0)
                else:
                    rel_judge_count = 0
                    precision_score_lst = []
                    for i in range(len(relevant_jugdes)):
                        if relevant_jugdes[i] == 1:
                            rel_judge_count += 1
                            precision_score_lst.append(rel_judge_count / (i+1))   
                    AP_score = np.mean(np.array(precision_score_lst))
                    AP_score_lst.append(AP_score)

            line = f'- Query: {file.split("/")[-1]}'
            res_file.write(line + '\n')
            print(line)

            line = f'\tAverage Precision: {np.round(AP_score, 2)}'
            res_file.write(line + '\n')
            print(line)

            line = f'\tQuery Time: {np.round(query_time, 2)}s'
            res_file.write(line + '\n')
            print(line)

        eval_time = time.time() - eval_start_time

        line = '\n----------COMPLETE THE SYSTEM EVALUATION---------'
        res_file.write(line + '\n')
        print(line)

        MAP = np.round(np.mean(np.array(AP_score_lst)), 2)
        line = f'Mean Average Precision of system: {MAP}'
        res_file.write(line + '\n')
        print(line)

        line = f'Evaluation time: {np.round(eval_time, 2)}s'
        res_file.write(line + '\n')
        print(line)

        res_file.close()

        return MAP