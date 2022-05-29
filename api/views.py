from django.shortcuts import render, redirect
from PIL import Image, ImageOps
import numpy as np


from .predictor import *
from .utils import *

def home(request):
	#print("\n\n\n\n Kaaaj kortese \n\n\n\n")
	return render(request, 'home.html')


def digit_recognizer(request):
	if request.method == 'POST':
		if request.POST['content_sumbit']:
			try:
				content_image = request.FILES["content_image"]
			except:
				content_image = None
				error = 'Please upload an image'

				
				return render(request, 'prediction.html', context={'error':error})
			if content_image:
				try:
				
					pil_image = Image.open(content_image).convert('L')
					#pil_image = ImageOps.grayscale(pil_image) # converting the image in grayscale
					img = np.array(pil_image)
					
					digit_image = segments_image(img)

					number = get_prediction(digit_image)
						
					return render(request, 'prediction.html', context={'pred':f'The number in the image is {number}'})

				except:
					error = 'Sorry, your image is invalid, please upload a valid image'

					
					return render(request, 'prediction.html', context={'error':error})

	else:
		return redirect('home')
