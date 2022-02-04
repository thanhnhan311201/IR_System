from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import Template, Context
from django.views.decorators.csrf import csrf_exempt

import cv2
import json
import numpy as np
from PIL import Image
import os

from systems.src.system import CBIR_System

my_system = CBIR_System()
results = None
query_image_file = None

@csrf_exempt
def index(request, *args, **kwargs):
    global results
    global query_image_file

    if request.method == "POST":
        try:
            file = request.FILES['file']
        except:
            return redirect('/')

        result_number = int(request.POST.get('result_number'))
        image_file = file.read()
        image = cv2.imdecode(np.frombuffer(image_file, dtype=np.uint8), -1)
        query_img = Image.fromarray(np.uint8(image)).convert('RGB')

        relevant_imgs, query_time = my_system.retrieve_img(query_img, result_number)
        results = relevant_imgs

        if not os.path.exists('IRsystem_WebPage/static/query_images/'):
            os.mkdir('IRsystem_WebPage/static/query_images/')

        query_image_file = '/static/query_images/query_img.jpg'
        cv2.imwrite('IRsystem_WebPage' + query_image_file, image)

        response_data = {}
        response_data['query_image'] = query_image_file
        response_data['relevant_imgs'] = relevant_imgs
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    
    return render(request, 'index.html')

# def result(request):
#     if request.method == 'GET':
#         if not results == None:
#             relevant_imgs = []
#             for img_infor in results:
#                 relevant_imgs.append(img_infor[1])

#             context = {
#                 'query_img': query_image_file,
#                 'relevant_imgs': relevant_imgs,
#             }

#     return render(request, 'result.html', context)