from dotenv import load_dotenv
import os
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt

# Import namespaces
from azure.cognitiveservices.vision.face import FaceClient
from azure.cognitiveservices.vision.face.models import FaceAttributeType
from msrest.authentication import CognitiveServicesCredentials

def main():

    global face_client

    try:
        # Get Configuration Settings
        load_dotenv()
        cog_endpoint = os.getenv('COG_SERVICE_ENDPOINT')
        cog_key = os.getenv('COG_SERVICE_KEY')

        # Authenticate Computer Vision client
        credentials = CognitiveServicesCredentials(cog_key)
        face_client = FaceClient(cog_endpoint, credentials)

        print('1: Detect faces\n2: Compare faces\n3: Train a facial recognition model\n4: Recognize faces\n5: Verify a face\nAny other key to quit')
        command = input('Enter a number:')
        if command == '1':
            # Detect faces in an image
            image_file = os.path.join('images','people.jpg')
            DetectFaces(image_file)
        elif command =='2':
            # Compare faces
            person_image = os.path.join('images','person1.jpg') # Also try person2.jpg
            people_image = os.path.join('images','people.jpg')
            CompareFaces(person_image, people_image)
        elif command =='3':
            # Train a people group model
            folders = ['Mary', 'Sue']
        elif command =='4':
            # Recognize faces in an image
            image_file = os.path.join('images','people.jpg')
        elif command == '5':
            person_image = os.path.join('images','person1.jpg')
            person_name = 'Sue'
            VerifyFace(person_image, person_name)
                

    except Exception as ex:
        print(ex)

def DetectFaces(image_file):
    print('Analyzing', image_file)

    # Specify facial features to be retrieved
    features = [FaceAttributeType.age,
                FaceAttributeType.emotion,
                FaceAttributeType.glasses]

    # Get faces in the image
    with open(image_file, mode="rb") as image_data:
        detected_faces = face_client.face.detect_with_stream(image=image_data,
                                                             return_face_attributes=features)

        # Get faces
        if len(detected_faces) > 0:
            print(len(detected_faces), 'faces detected.')

            # Prepare image for drawing
            fig = plt.figure(figsize=(8, 6))
            plt.axis('off')
            image = Image.open(image_file)
            draw = ImageDraw.Draw(image)
            color = 'lightgreen'

            # Draw and annotate each face
            for face in detected_faces:

                # Get face properties
                print('\nFace ID: {}'.format(face.face_id))
                detected_attributes = face.face_attributes.as_dict()
                age = 'age unknown' if 'age' not in detected_attributes.keys() else int(detected_attributes['age'])
                print(' - Age: {}'.format(age))

                if 'emotion' in detected_attributes:
                    for emotion_name in detected_attributes['emotion']:
                        print(' - {}: {}'.format(emotion_name, detected_attributes['emotion'][emotion_name]))
                
                if 'glasses' in detected_attributes:
                    print(' - Glasses:{}'.format(detected_attributes['glasses']))

                # Draw and annotate face
                r = face.face_rectangle
                bounding_box = ((r.left, r.top), (r.left + r.width, r.top + r.height))
                draw = ImageDraw.Draw(image)
                draw.rectangle(bounding_box, outline=color, width=5)
                annotation = 'Face ID: {}'.format(face.face_id)
                plt.annotate(annotation,(r.left, r.top), backgroundcolor=color)

            # Save annotated image
            plt.imshow(image)
            outputfile = 'detected_faces.jpg'
            fig.savefig(outputfile)

            print('\nResults saved in', outputfile)

def CompareFaces(image_1, image_2):
    print('Comparing faces in ', image_1, 'and', image_2)

    # Get the first image in image 1
    with open(image_1, mode="rb") as image_data:
        image_1_faces = face_client.face.detect_with_stream(image=image_data)
        image_1_face = image_1_faces[0]

        # Highlight the face in the image
        fig = plt.figure(figsize=(8, 6))
        plt.axis('off')
        image = Image.open(image_1)
        draw = ImageDraw.Draw(image)
        color = 'lightgreen'
        r = image_1_face.face_rectangle
        bounding_box = ((r.left, r.top), (r.left + r.width, r.top + r.height))
        draw = ImageDraw.Draw(image)
        draw.rectangle(bounding_box, outline=color, width=5)
        plt.imshow(image)
        outputfile = 'face_to_match.jpg'
        fig.savefig(outputfile)


    # Get all the faces in image 2
    with open(image_2, mode="rb") as image_data:
        image_2_faces = face_client.face.detect_with_stream(image=image_data)
        image_2_face_ids = list(map(lambda face: face.face_id, image_2_faces))

        # Find faces in image 2 that are similar to the one in image 1
        similar_faces = face_client.face.find_similar(face_id=image_1_face.face_id, face_ids=image_2_face_ids)
        similar_face_ids = list(map(lambda face: face.face_id, similar_faces))

        # Prepare image for drawing
        fig = plt.figure(figsize=(8, 6))
        plt.axis('off')
        image = Image.open(image_2)
        draw = ImageDraw.Draw(image)

        # Draw and annotate matching faces
        for face in image_2_faces:
            if face.face_id in similar_face_ids:
                r = face.face_rectangle
                bounding_box = ((r.left, r.top), (r.left + r.width, r.top + r.height))
                draw = ImageDraw.Draw(image)
                draw.rectangle(bounding_box, outline='lightgreen', width=10)
                plt.annotate('Match!',(r.left, r.top + r.height + 15), backgroundcolor='white')

        # Save annotated image
        plt.imshow(image)
        outputfile = 'matched_faces.jpg'
        fig.savefig(outputfile)

def TrainModel(image_folders):
    print('Training model')

def RecognizeFaces(image_file):
    print('Recognizing faces')

def VerifyFace(person_image, person_name):
    print('Verifying the person in', person_image, 'is', person_name)

if __name__ == "__main__":
    main()