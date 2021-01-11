from dotenv import load_dotenv
import os
from array import array
from PIL import Image, ImageDraw
import sys
import time
from matplotlib import pyplot as plt
import numpy as np

# Import namespaces
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

def main():
    global cv_client

    try:
        # Get Configuration Settings
        load_dotenv()
        cog_endpoint = os.getenv('COG_SERVICE_ENDPOINT')
        cog_key = os.getenv('COG_SERVICE_KEY')

        # Authenticate Computer Vision client
        credential = CognitiveServicesCredentials(cog_key) 
        cv_client = ComputerVisionClient(cog_endpoint, credential)

        # Get image
        image_file = os.path.join('images','satya.jpg')

        # Analyze image
        AnalyzeImage(image_file)

        # Generate thumbnail
        GenerateThumbnail(image_file)

    except Exception as ex:
        print(ex)

def AnalyzeImage(image_file):

    # Get image features (categories)
    features = ["description", "tags","categories", "brands", "objects", "adult"]
    
    with open(image_file, mode="rb") as image_data:
        analysis = cv_client.analyze_image_in_stream(image_data , features)

    if (len(analysis.description.captions) == 0):
        print("No description detected.")
    else:
        for caption in analysis.description.captions:
            print("Description: '{}' (confidence: {:.2f}%)".format(caption.text, caption.confidence * 100))

    
    if (len(analysis.tags) > 0):
        print("Tags: ")
        for tag in analysis.tags:
            print(" -'{}' (confidence: {:.2f}%)".format(tag.name, tag.confidence * 100))

    if (len(analysis.categories) > 0):
        print("Categories:")
        landmarks = []
        celebrities = []
        for category in analysis.categories:
            print(" -'{}' (confidence: {:.2f}%)".format(category.name, category.score * 100))
            if category.detail:
                if category.detail.landmarks:
                    for landmark in category.detail.landmarks:
                        if landmark not in landmarks:
                            landmarks.append(landmark)
                if category.detail.celebrities:
                    for celebrity in category.detail.celebrities:
                        if celebrity not in celebrities:
                            celebrities.append(celebrity)
        if len(landmarks) > 0:
            print("Landmarks:")
            for landmark in landmarks:
                print(" -'{}' (confidence: {:.2f}%)".format(landmark.name, landmark.confidence * 100))
        if len(celebrities) > 0:
            print("Celebrities:")
            for celebrity in celebrities:
                print(" -'{}' (confidence: {:.2f}%)".format(celebrity.name, celebrity.confidence * 100))

    if (len(analysis.brands) > 0):
        print("Brands: ")
        for brand in analysis.brands:
            print(" -'{}' (confidence: {:.2f}%)".format(brand.name, brand.confidence * 100))

    if len(analysis.objects) > 0:
        print("Objects in image:")
        fig = plt.figure(figsize=(8, 8))
        plt.axis('off')
        image = Image.open(image_file)
        draw = ImageDraw.Draw(image)
        color = 'cyan'
        for detected_object in analysis.objects:
            print(" -{} (confidence: {:.2f}%)".format(detected_object.object_property, detected_object.confidence * 100))
            r = detected_object.rectangle
            bounding_box = ((r.x, r.y), (r.x + r.w, r.y + r.h))
            draw.rectangle(bounding_box, outline=color, width=3)
            plt.annotate(detected_object.object_property,(r.x, r.y), backgroundcolor=color)
        plt.imshow(image)
        outputfile = 'objects.jpg'
        fig.savefig(outputfile)
        print('  Results saved in', outputfile)

        ratings = 'Ratings:\n - Adult: {}\n - Racy: {}\n - Gore: {}'.format(analysis.adult.is_adult_content,
                                                                            analysis.adult.is_racy_content,
                                                                            analysis.adult.is_gory_content)
        print(ratings)

        

def GenerateThumbnail(image_file):

    with open(image_file, mode="rb") as image_data:
        thumbnail_stream = cv_client.generate_thumbnail_in_stream(100, 100, image_data, True)

    thumbnail_file_name = 'thumbnail.png'
    with open(thumbnail_file_name, "wb") as thumbnail_file:
        for chunk in thumbnail_stream:
            thumbnail_file.write(chunk)

    print('Thumbnail saved in.', thumbnail_file_name)

if __name__ == "__main__":
    main()