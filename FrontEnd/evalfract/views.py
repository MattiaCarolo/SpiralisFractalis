from django.http import HttpRequest, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from Fractals.wsgi import string_to_transformations, transformation_to_string
from evalfract.models import ImageModel, Settings
from evalfract.serializers import ImageSerializer
from rest_framework.status import *
from Fractals.settings import *
from SaettaMcQueen.src.components.ga import *
from evalfract.SpiralisFractalis import *

# Create your views here.
import os
class ImageView(APIView):

    generation_counter = 0

    def get(self, request: HttpRequest):
        imgs_path = []
        ids = []
        imgs = ImageModel.objects.all()
        for i in imgs.iterator():
            imgs_path.append(i.image_path)
            ids.append(i.id)
        return Response(
            {"paths" : imgs_path, "ids" : ids},
            status= HTTP_200_OK
        )
    
    def post(self, request: HttpRequest):
        ids = request.data["ids"]
        evals = [int(x) for x in request.data["evaluations"]]
        if sum(evals) == 0:
            return Response(status=HTTP_400_BAD_REQUEST)
        fractals = []
        for i in range(len(ids)):
            fractals.append(
                Fractal(
                    transformations= string_to_transformations(ImageModel.objects.get(id= ids[i]).transformations),
                    score = evals[i]
                )
            )
        

        settings = Settings.objects.get(dataset_filename= os.path.join("SaettaMcQueen", "datasets", "dataset_md.json"))
        # now we have all the fractals with the score

        # evolve()
        fractals = evolve(fractals)
        # create new images
        for i, x in enumerate(fractals):
            process_file(x, settings.width, settings.height, settings.num_iteration, get_name_index(i))
        
        #zip images
        zipGeneration(
            settings.width, settings.height, settings.num_iteration, fractals, self.generation_counter
        )
        self.generation_counter += 1

        # delete all images in database
        ImageModel.objects.all().delete()

        # repopulate database with new population
        for i, fractal in enumerate(fractals):
            f = ImageModel.objects.create(
                id= i,
                image_path= os.path.join(".", "src", "IMGres", f"{i}.png"),
                transformations = transformation_to_string(fractal.transformations)
            )
            f.save()


        imgs_path = []
        ids = []
        imgs = ImageModel.objects.all()
        for i in imgs.iterator():
            imgs_path.append(i.image_path)
            ids.append(i.id)
        return Response(
            {"paths" : imgs_path, "ids" : ids},
            status= HTTP_200_OK
        )


