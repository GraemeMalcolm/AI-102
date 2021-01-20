# Use the Form Recognizer to train a custom model 

In this exercise, you will use the Form Recognizer service to train a custom form recognition model.  

## Clone the repository for this course

If you have not already done so, you must clone the code repository for this course:

1. Start Visual Studio Code.
2. Open the palette (SHIFT+CTRL+P) and run a `Git: Clone` command to clone the `https://github/com/GraemeMalcolm/AI-102` repository to a local folder.
3. When the repository has been cloned, open the folder in Visual Studio Code.

## Getting started 

(Case scenario setup TBD)

We want to create a custom model that will recognize the data in our industry-specific forms. To do this, we will upload a set of training data to a container, create a Form Recognizer resource, train a model, and deploy for prediction. 

### (!) Important
We can train a custom Form Recognizer model with labeled data or  data without labels. In this exercise we will train a model with data without labels. 

Next we will store a set of training data to a container. 

## Create An Azure Storage blob 

To provide your own training data to the Train Custom Model operation, you need to provide a minimum of **five** filled-in forms or an empty form (you must include the word "empty" in the file name) and two filled-in forms.

The full custom model input requirements can be found [https://docs.microsoft.com/azure/cognitive-services/form-recognizer/build-training-data-set#custom-model-input-requirements](here).    

We'll use the sample forms in the sample_forms folder and upload the set of form documents to an Azure blob storage container. To do this we'll create a container and upload a block blob.  

### Create a container 

1. In a new browser tab, open the Azure portal at [https://portal.azure.com](https://portal.azure.com), and sign in using the Microsoft account associated with your Azure subscription.

2. Expand the portal menu by clicking on the three lines at the top left hand of the screen. Click on Storage accounts, and create a **Storage Account** resource with the following settings:

    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Choose or create a resource group (if you are using a restricted subscription, you may not have permission to create a new resource group - use the one provided)*
    - **Storage account name**: *Enter a unique name*
    - **Location**: *Choose any available region*
    - **Performance**: Standard
    - **Account kind**: StorageV2 (general purpose v2)
    - **Replication**: Read-access geo-redundant stoarge (RA-GRS)

Click Review + Create.  

3. Wait for the resource to be created. Once it is ready, view the deployment details in the overview page. On the deployment details page, click on **Containers** and create a new container by clicking on **+ Container** with the following settings: 
    
    - **Name**: *Enter a unique name, lowercase* 
    - **Public access level**: Private (no anonymous access) 

You do not need to configure Advanced settings for this exercise. Select **Create** to create the container. 
 
### Upload a block blob 

We use block blobs to store data in the cloud, like files, images, and videos. Upload a block blob with your training forms to your container following these steps: 

1. Navigate to the container you just created above.  
2. Select the **Upload** button and browse your local file system. You will want to access the local folder where you cloned this repository. The path to the sample forms is 20-custom-form/...

3. Select the files and upload as a block blob by selecting **Upload**. You do not need to configure Advanced settings for this exercise. 

## Create a Form Recognizer resource

Before you can train a model, you will need to create a **Form Recognizer** Azure resource.  

1. Stay in the Microsoft account associated with your Azure subscription at [https://portal.azure.com](https://portal.azure.com).
2. Select the **&#65291;Create a resource** button, search for *Form Recognizer*, and create a **Form Recognizer** resource with the following settings:
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Choose or create a resource group (if you are using a restricted subscription, you may not have permission to create a new resource group - use the one provided)*
    - **Region**: *Choose any available region*
    - **Name**: *Enter a unique name*
    - **Pricing tier**: F0

    > **Note**: If you already have an F0 custom vision service in your subscription, select **S0** for this one.

3. Wait for the resources to be created, and then view the deployment details by navigating to the resource group where you created them.

## Train a custom model using the API

Now we will use Form Recognizer via the SDK.  

> **Note**: In this exercise, you can choose to use the API from either the **C#** or **Python** SDK. In the steps below, perform the actions appropriate for your preferred language.

1. In Visual Studio Code open the **AI-102** project, and in the **Explorer** pane, browse to the **20-custom-form** folder and expand the **C-Sharp** or **Python** folder depending on your language preference.
1. 
1. Right-click the **train-without-labels** folder and open an integrated terminal. Then install the Form Recognizer package by running the appropriate command for your language preference:

   **C#**

    ```
    dotnet add package Azure.AI.FormRecognizer --version 3.0.0 
    ```

   **Python**

   ```
   pip install azure-ai-formrecognizer
   ```

3. View the contents of the **train-without-labels** folder, and note that it contains a file for configuration settings:
    - **C#**: appsettings.json
    - **Python**: .env

    Open the configuration file. 

    ### Get Container's Shared Access Signature

    From the main menu of your Storage Account, navigate to **Storage Explorer**, select **BLOB CONTAINERS**, and right click on the container with your form training data. 
    [image here for clarity] 
     Select **Get Shared Access Signature**. Then use the following configurations: 
   
    - Access Policy: (none)
    - Start time: *leave as is for this exercise* 
    - End time: *leave as is for this exercise* 
    - Time Zone: Local 
    - Permissions: _Select **Read** and **List**_ 

    Select **Create** and copy the **URI** to the **STORAGE_URL** configuration value.

     Update the configuration values it contains to reflect the endpoint and key for your Form Recognizer resource, and container Shared Access Signature. 
  
4. Note that the **train-without-labels** folder contains a code file for the client application:

    - **C#**: Program.cs
    - **Python**: train-custom-model&period;py

    Open the code file and review the code it contains, noting the following details:
    - Namespaces from the package you installed are imported
    - The **Main** function retrieves the configuration settings, and uses the key and endpoint to create an authenticated **Client**.
    - The **Train_Model** function creates a new training iteration for the project and waits for training to complete.
5. Return the integrated terminal for the **train-without-labels** folder, and enter the following command to run the program:

    **C#**

    ```
    dotnet run
    ```

    **Python**

    ```
    python train-custom-model.py
    ```

6. Wait for the program to end. 
7. Review the model. 

## Get the custom form recognizer model ID

Now you're ready to publish your trained model so that it can be used from a client application.

## Use the custom model from a client application

Now that you've got the model ID, you can use it from a client application. Once again, you can choose to use **C#** or **Python**.

1. In Visual Studio Code, in the **AI-102** project, browse to the **20-custom-form** folder and in the folder for your preferred language (**C-Sharp** or **Python**), expand the **test-custom-form** folder.
2. Right-click the **test-custom-form** folder. Open the code file for your client application (*Program.cs* for C#, *test-custom-model&period;py* for Python) and review the code it contains, noting the following details:
    - Namespaces from the package you installed are imported
    - The **Main** function retrieves the configuration settings, and uses the key and endpoint to create an authenticated **Client**.
    
5. Return the integrated terminal for the **test-custom-form** folder, and enter the following SDK-specific command to run the program:

    **C#**

    ```
    dotnet run
    ```

    **Python**

    ```
    python test-custom-model.py
    ```

6. View the output. 

## More information

For more information about the Form Recognizer service, see the [Form Recognizer documentation](https://docs.microsoft.com/azure/cognitive-services/form-recognizer/).
