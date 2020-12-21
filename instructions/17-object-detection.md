# Detect Objects in Images with Custom Vision

In this exercise, you will use the Custom Vision service to train an *object detection* model that can detect and locate three classes of fruit (apple, banana, and orange) in an image.

## Clone the repository for this course

If you have not already done so, you must clone the code repository for this course:

1. Start Visual Studio Code.
2. Open the palette (SHIFT+CTRL+P) and run a `Git: Clone` command to clone the `https://github/com/GraemeMalcolm/AI-102` repository to a local folder.
3. When the repository has been cloned, open the folder in Visual Studio Code.

## Create Custom Vision resources

You should have created **Custom Vision** resources for training and prediction in a previous exercise, but of not (or if you have deleted them), use the following instructions to create them.

1. In a new browser tab, open the Azure portal at [https://portal.azure.com](https://portal.azure.com), and sign in using the Microsoft account associated with your Azure subscription.
2. Select the **&#65291;Create a resource** button, search for *custom vision*, and create a **Custom Vision** resource with the following settings:
    - **Create options**: Both
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Choose or create a resource group (if you are using a restricted subscription, you may not have permission to create a new resource group - use the one provided)*
    - **Name**: *Enter a unique name*
    - **Training location**: *Choose any available region*
    - **Training pricing tier**: F0
    - **Prediction location**: *The same region as the training resource*
    - **Prediction pricing tier**: F0

    > **Note**: If you already have an F0 custom vision service in your subscription, select **S0** for this one.

3. Wait for the resources to be created, and then view the deployment details and note that two Custom Vision resources are provisioned; one for training, and another for prediction. You can view these by navigating to the resource group where you created them.

> **Important**: Each resource has its own *endpoint* and *keys*, which are used to manage access from your code. To train an image classification model, your code must use the *training* resource (with its endpoint and key); and to use the trained model to predict image classes, your code must use the *prediction* resource (with its endpoint and key).

## Create a Custom Vision project

To train an object detection model, you need to create a Custom Vision project based on your training resource. To do this, you'll use the Custom Vision portal.

1. In a new browser tab, open the Custom Vision portal at [https://customvision.ai](https://customvision.ai), and sign in using the Microsoft account associated with your Azure subscription.
2. Create a new project with the following settings:
    - **Name**: Detect Fruit
    - **Description**: Object detection for fruit.
    - **Resource**: *The Custom Vision resource you created previously*
    - **Project Types**: Object Detection
    - **Domains**: General
3. Wait for the project to be created and opened in the browser.

## Add and tag images

To train an object detection model, you need to upload images that contain the classes you want the model to identify, and tag them to indicate bounding boxes for each object instance.

1. View the training images in the **object-detection/training-images** folder where you cloned the AI-102 repository. This folder contains images of fruit.
2. In the Custom Vision portal, in your object detection project, select **Add images** and upload all of the images in the extracted folder.
3. After the images have been uploaded, select the first one to open it.
4. Hold the mouse over any object in the image until an automatically detected region is displayed like the image below. Then select the object, and if necessary resize the region to surround it.

![The default region for an object](./images/object-region.jpg)

Alternatively, you can simply drag around the object to create a region.

5. When the region surrounds the object, add a new tag with the appropriate object type (*apple*, *banana*, or *orange*) as shown here:

![A tagged object in an image](./images/object-tag.jpg)

6. Select and tag each other object in the image, resizing the regions and adding new tags as required.

![Two tagged objects in an image](./images/object-tags.jpg)

7. Use the **>** link on the right to go to the next image, and tag its objects. Then just keep working through the entire image collection, tagging each apple, banana, and orange.

8. When you have finished tagging the last image, close the **Image Detail** editor and on the **Training Images** page, under **Tags**, select **Tagged** to see all of your tagged images:

![Tagged images in a project](./images/tagged-images.jpg)

## Use the Training API to upload images

You can use the graphical tool in the Custom Vision portal to tag your images, but many AI development teams use other tools that generate files containing information about tags and object regions in images. In scenarios like this, you can use the Custom Vision training API to upload tagged images to the project.

> **Note**: In this exercise, you can choose to use the API from either the **C#** or **Python** SDK. In the steps below, perform the actions appropriate for your preferred language.

1. Click the *settings* (&#9881;) icon at the top right of the **Training Images** page in the Custom Vision portal to view the project settings.
2. Under **General** (on the left), note the **Project Id** that uniquely identifies this project.
3. On the left, under **Resources** note that the details for the *training* resource, including its key and endpoint are shown (you can also obtain this information by viewing the resource in the Azure portal).
4. In Visual Studio Code open the **AI-102** project, and in the **Explorer** pane, browse to the **object-detection** folder and expand the **C-Sharp** or **Python** folder depending on your language preference.
5. Right-click the **train-detector** folder and open an integrated terminal. Then install the Custom Vision Training package by running the appropriate command for your language preference:

   **C#**

    ```
    dotnet add package Microsoft.Azure.CognitiveServices.Vision.CustomVision.Training --version 2.0.0
    ```

   **Python**

   ```
   pip install azure-cognitiveservices-vision-customvision==2.0.0
   ```

6. View the contents of the **train-detector** folder, and note that it contains a file named **tagged-images.json**. Open this file and examine the JSON it contains. The JSON defines a list of images, each containing one or more tagged regions. Each tagged region includes a tag name, and the top and left coordinates and width and height dimensions of the bounding box containing the tagged object.

    > **Note**: The coordinates and dimensions in this file indicate relative points on the image. For example, a *height* value of 0.7 indicates a box that is 70% of the height of the image. Some tagging tools generate other formats of file in which the coordinate and dimension values represent pixels, inches, or other units of measurements.

7. Note that the **train-detector** folder contains a subfolder in which the image files referenced in the JSON file are stored.

8. View the contents of the **train-detector** folder, and note that it contains a file for configuration settings:
    - **C#**: appsettings.json
    - **Python**: .env

    Open the configuration file and update the configuration values it contains to reflect the endpoint and key for your Custom Vision *training* resource, and the project ID for the classification project you created previously. Save your changes.
9. Note that the **train-detector** folder contains a code file for the client application:

    - **C#**: Program.cs
    - **Python**: train-detector&period;py

    Open the code file and review the code it contains, noting the following details:
    - Namespaces from the package you installed are imported
    - The **Main** function retrieves the configuration settings, and uses the key and endpoint to create an authenticated **CustomVisionTrainingClient**, which is then used with the project ID to create a **Project** reference to your project.
    - The **Upload_Images** function extracts the tagged region information from the JSON file and uses it to create a batch of images with regions, which it then uploads to the project.
10. Return the integrated terminal for the **train-detector** folder, and enter the following command to run the program:

    **C#**

    ```
    dotnet run
    ```

    **Python**

    ```
    python train-detector.py
    ```

11. Wait for the program to end. Then return to your browser and view the **Training Images** page for your project in the Custom Vision portal (refreshing the browser if necessary).
12. Verify that some new tagged images have been added to the project.

## Train and test a model

Now that you've tagged the images in your project, you're ready to train a model.

1. In the Custom Vision project, click **Train** to train an object detection model using the tagged images. Select the **Quick Training** option.
2. Wait for training to complete (it might take ten minutes or so), and then review the *Precision*, *Recall*, and *mAP* performance metrics - these measure the prediction accuracy of the classification model, and should all be high.
3. At the top right of the page, click **Quick Test**, and then in the **Image URL** box, enter `https://aka.ms/apple-orange` and view the prediction that is generated. Then close the **Quick Test** window.

## Publish the image classification model

Now you're ready to publish your trained model so that it can be used from a client application.

1. In the Custom Vision portal, on the **Performance** page,  click **&#128504; Publish** to publish the trained model with the following settings:
    - **Model name**: fruit-detector
    - **Prediction Resource**: *The **prediction** resource you created previously (<u>not</u> the training resource)*.
2. At the top left of the **Project Settings** page, click the *Projects Gallery* (&#128065;) icon to return to the Custom Vision portal home page, where your project is now listed.
3. On the Custom Vision portal home page, at the top right, click the *settings* (&#9881;) icon to view the settings for your Custom Vision service. Then, under **Resources**, expand your *prediction* resource (<u>not</u> the training resource) to see its **Key** and **Endpoint** values (you can also obtain this information by viewing the resource in the Azure portal).

## Use the image classifier from a client application

Now that you've published the image classification model, you can use it from a client application. Once again, you can choose to use **C#** or **Python**.

1. In Visual Studio Code, in the **AI-102** project, browse to the **image-detection** folder and in the folder for your preferred language (**C-Sharp** or **Python**), expand the **test-detector** folder.
2. Right-click the **test-detector** folder and open an integrated terminal. Then enter the following SDK-specific command to install the Custom Vision Prediction package:

    **C#**

    ```
    dotnet add package Microsoft.Azure.CognitiveServices.Vision.CustomVision.Prediction --version 2.0.0
    ```

     **Python**

   ```
   pip install azure-cognitiveservices-vision-customvision==2.0.0
   ```

   > **Note**: The Python SDK package includes both training and prediction packages, and may already be installed.

3. Open the configuration file for your client application (*appsettings.json* for C# or *.env* for Python) and update the configuration values it contains to reflect the endpoint and key for your Custom Vision *prediction* resource, the project ID for the classification project, and the name of your published model (which should be *fruit-detector*). Save your changes.
4. Open the code file for your client application (*Program.cs* for C#, *test-detector&period;py* for Python) and review the code it contains, noting the following details:
    - Namespaces from the package you installed are imported
    - The **Main** function retrieves the configuration settings, and uses the key and endpoint to create an authenticated **CustomVisionPredictionClient**.
    - The prediction client object is used to get object detection predictions for the **produce.jpg** image, specifying the project ID and model name in the request. The predicted tagged regions are then drawn on the image, and the result is saved as **output.jpg**.
5. Return the integrated terminal for the **test-detector** folder, and enter the following SDK-specific command to run the program:

    **C#**

    ```
    dotnet run
    ```

    **Python**

    ```
    python test-detector.py
    ```

6. After the program has completed, view the resulting **output.jpg** file to see the detected objects in the image.

## More information

For more information about object detection with the Custom Vision service, see the [Custom Vision documentation](https://docs.microsoft.com/azure/cognitive-services/custom-vision-service/).
