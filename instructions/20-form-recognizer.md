# Use the Form Recognizer to train a custom model 

**Form Recognizer** is a cognitive service that can extract key, value pairs of information from documents using optical character recognition (OCR). Form Recognizer has pre-built models for recognizing invoices, receipts, and business cards. The service also gives you the capability to create custom models, trained for your industry-specific forms. In this exercise, you will use the Form Recognizer service to train and test custom form recognition models, first using training forms **without** labels, then using training forms **with** labels. 

We can train a custom Form Recognizer model with labeled data or data without labels. We will first train a model using forms without labels and test it. Then we will train a model using forms with labels and test that model.  

## Clone the repository for this course

If you have not already done so, you must clone the code repository for this course:

1. Start Visual Studio Code.
2. Open the palette (SHIFT+CTRL+P) and run a `Git: Clone` command to clone the `https://github/com/MicrosoftLearning/AI-102-AIEngineer` repository to a local folder.
3. When the repository has been cloned, open the folder in Visual Studio Code.

3. Wait for the resources to be created, and then view the deployment details by navigating to the resource group where you created them.

## Custom Form Case: Hero Limited

Suppose the company Hero Limited sends out invoices. Although the forms are sent digitally, an employee at Hero Limited is still manually transferring the data in the forms to a database. 

We want to create a custom model that will recognize the data in our industry-specific forms and give an output of accurate key, value pairs in a JSON file, which can be used to automate the process. In order to create a custom model, we will upload a set of training documents to a container, create a Form Recognizer resource, train a model, and test the model. 

## Gather training data 

![An image of a Hero Limited invoice.](../20-custom-form/sample-forms/Form_1.jpg)

Take a look at the files in **20-custom-form/sample-forms/train**. We will be using these sample forms to train two models, one with labels, and one without labels. The **sample-forms** file contains all the forms we will need to train both models.  

Notice there are four types of files: 
- **.json**
- **.jpg**
- **.jpg.labels.json**
- **jpg.ocr.json**

When we train a model without labels we will only uses the **.jpg** files. When we a train a model with labels we will use both the **.jpg** and the **.json** files.

## Store training data

To provide your own training data to the Train Custom Model operation, you need to provide a minimum of **five** filled-in forms or an empty form (you must include the word "empty" in the file name) and two filled-in forms.

The full custom model input requirements can be found [https://docs.microsoft.com/azure/cognitive-services/form-recognizer/build-training-data-set#custom-model-input-requirements](here).    

We'll use the sample forms in the **sample-forms** folder and upload the set of form documents to an Azure blob storage container. To do this we'll create a container and upload a block blob.  

### Create a container 

1. In a new browser tab, open the Azure portal at [https://portal.azure.com](https://portal.azure.com), and sign in using the Microsoft account associated with your Azure subscription.

2. Expand the portal menu by clicking on the three lines at the top left hand of the screen. Click on Storage accounts, and create a **Storage Account** resource with the following settings:

    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Choose or create a resource group (if you are using a restricted subscription, you may not have permission to create a new resource group - use the one provided)*
    - **Storage account name**: *Enter a unique name*
    - **Location**: *Choose any available region*
    - **Performance**: Standard
    - **Account kind**: StorageV2 (general purpose v2)
    - **Replication**: Read-access geo-redundant storage (RA-GRS)

Click Review + Create.  

3. Wait for the resource to be created. Once it is ready, view the deployment details in the overview page. On the deployment details page, click on **Containers** and create a new container by clicking on **+ Container** with the following settings: 
    
    - **Name**: *Enter a unique name, lowercase* 
    - **Public access level**: Private (no anonymous access) 

You do not need to configure Advanced settings for this exercise. Select **Create** to create the container. 
 
### Upload a block blob 

We use block blobs to store data in the cloud, like files, images, and videos. Upload a block blob with your training forms to your container following these steps: 

1. Navigate to the container you just created above.  
2. Select the **Upload** button and browse your local file system. You will want to access the local folder where you cloned this repository. Select the pdf forms located in the **20-custom-form/sample-forms/train** folder. 

3. Upload the files as a block blob by selecting **Upload**. You do not need to configure Advanced settings for this exercise. 

## Train a model **without labels** using the API

Now we will use Form Recognizer via the SDK.  

> **Note**: In this exercise, you can choose to use the API from either the **C#** or **Python** SDK. In the steps below, perform the actions appropriate for your preferred language.

1. In Visual Studio Code open the **AI-102** project, and in the **Explorer** pane, browse to the **20-custom-form** folder and expand the **C-Sharp** or **Python** folder depending on your language preference.
 
2. Right-click the **train-without-labels** folder and open an integrated terminal. Then install the Form Recognizer package by running the appropriate command for your language preference:

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

    Open the configuration file. We will need a key, endpoint, and the URI for our stored sample forms.  
    
    ## Create a Form Recognizer resource and get Key and Endpoint

    You will need to create a **Form Recognizer** Azure resource.  
    
    1. Navigate to the Microsoft account associated with your Azure subscription at [https://portal.azure.com](https://portal.azure.com).
    2. Select the **&#65291;Create a resource** button, search for *Form Recognizer*, and create a **Form Recognizer** resource with the following settings:
        - **Subscription**: *Your Azure subscription*
        - **Resource group**: *Choose or create a resource group (if you are using a restricted subscription, you may not have permission to create a new resource group - use the one provided)*
        - **Region**: *Choose any available region*
        - **Name**: *Enter a unique name*
        - **Pricing tier**: F0

    > **Note**: If you already have an F0 custom vision service in your subscription, select **S0** for this one.

    3. Select **Keys and Endpoint** on the left hand panel. Copy the key and endpoint into the configuration file. 
    
    Now we will obtain our storage blob's URI.  

    ### Get Container's Shared Access Signature

    From the main menu of your Storage Account, navigate to **Storage Explorer**, select **BLOB CONTAINERS**, and right click on the container with your form training data. 

    ![Visual of how to get shared access signature.](../20-custom-form/shared_access_sig.jpg)
 
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
    - **Python**: train-model-without-labels&period;py

    Open the code file and review the code it contains, noting the following details:
    - Namespaces from the package you installed are imported
    - The **Main** function retrieves the configuration settings, and uses the key and endpoint to create an authenticated **Client**.

5. Return the integrated terminal for the **train-without-labels** folder, and enter the following command to run the program:

    **C#**

    ```
    dotnet run
    ```

    **Python**

    ```
    python train-model-without-labels.py
    ```

6. Wait for the program to end. 
7. Review the model. 
8. Copy the Model ID in the terminal output. You will use your Model ID when analyzing new forms.  

## Analyze new forms 

Now you're ready use your trained model. Notice how we trained our model using files from a storage container URI. We could also have trained our model using local files. Similarly, we can test our model using forms from a URI or from local files. We will test our form model with a local file using the **StartRecognizeCustomForms** method. However, you can also analyze new forms from a URI using the **StartRecognizeCustomFormsFromUri** method. 

## Test the model 

Now that you've got the model ID, you can use it from a client application. Once again, you can choose to use **C#** or **Python**.

1. In Visual Studio Code, in the **AI-102** project, browse to the **20-custom-form** folder and in the folder for your preferred language (**C-Sharp** or **Python**), expand the **test-without-labels** folder.
2. Right-click the **test-without-labels** folder. Open the code file for your client application (*Program.cs* for C#, *test-model-without-labels&period;py* for Python) and review the code it contains, noting the following details:
    - Namespaces from the package you installed are imported
    - The **Main** function retrieves the configuration settings, and uses the key and endpoint to create an authenticated **Client**.
    
5. Return the integrated terminal for the **test-without-labels** folder, and enter the following SDK-specific command to run the program:

    **C#**

    ```
    dotnet run
    ```

    **Python**

    ```
    python test-model-without-labels.py
    ```

6. View the output. 

Now we will train a model using labels. 



## Train a model with labels using the API

Now suppose we have labels for the same forms we used to train a model above, and want to train a new custom model with labeled data. We will be using labeled forms this time. We have already uploaded all the image files. If you have not done so, please return to the top of the page and follow instructions to upload the sample form files to a Storage Blob. 

> **Note**: In this exercise, you can choose to use the API from either the **C#** or **Python** SDK. In the steps below, perform the actions appropriate for your preferred language.

1. In Visual Studio Code open the **AI-102** project, and in the **Explorer** pane, browse to the **20-custom-form** folder and expand the **C-Sharp** or **Python** folder depending on your language preference.
 
2. Right-click the **train-with-labels** folder and open an integrated terminal. If you have not already done so, install the Form Recognizer package by running the appropriate command for your language preference:

   **C#**

    ```
    dotnet add package Azure.AI.FormRecognizer --version 3.0.0 
    ```

   **Python**

   ```
   pip install azure-ai-formrecognizer
   ```

3. We will create another Azure Blob in our container and upload our labeled form files from the **20-custom-form/forms-with-labels/train** folder. 

4. View the contents of the **train-with-labels** folder, and note that it contains a file for configuration settings:
    - **C#**: appsettings.json
    - **Python**: .env

    Open the configuration file. 

    ### Get Container's Shared Access Signature

    From the main menu of your Storage Account, navigate to **Storage Explorer**, select **BLOB CONTAINERS**, and right click on the container with your form training data. 

    ![Visual of how to get shared access signature.](../20-custom-form/shared_access_sig.jpg)
 
     Select **Get Shared Access Signature**. Then use the following configurations: 
   
    - Access Policy: (none)
    - Start time: *leave as is for this exercise* 
    - End time: *leave as is for this exercise* 
    - Time Zone: Local 
    - Permissions: _Select **Read** and **List**_ 

    Select **Create** and copy the **URI** to the **STORAGE_URL** configuration value.

     Update the configuration values it contains to reflect the endpoint and key for your Form Recognizer resource, and container Shared Access Signature. 
  
5. Note that the **train-with-labels** folder contains a code file for the client application:

    - **C#**: Program.cs
    - **Python**: train-model-with-labels&period;py

    Open the code file and review the code it contains, noting the following details:
    - Namespaces from the package you installed are imported
    - The **Main** function retrieves the configuration settings, and uses the key and endpoint to create an authenticated **Client**.
    
6. Return the integrated terminal for the **train-with-labels** folder, and enter the following command to run the program:

    **C#**

    ```
    dotnet run
    ```

    **Python**

    ```
    python train-model-with-labels.py
    ```

7. Wait for the program to end. 
8. Review the model output. 
9. Copy the Model ID in the terminal output. You will use your Model ID when analyzing new forms.  

## Test the model

Now that you've got the model ID, test out the model. Once again, you can choose to use **C#** or **Python**.

1. In Visual Studio Code, in the **AI-102** project, browse to the **20-custom-form** folder and in the folder for your preferred language (**C-Sharp** or **Python**), expand the **test-with-labels** folder.
2. Right-click the **test-with-labels** folder. Open the code file for your client application (*Program.cs* for C#, *test-model-with-labels&period;py* for Python) and review the code it contains, noting the following details:
    - Namespaces from the package you installed are imported
    - The **Main** function retrieves the configuration settings, and uses the key and endpoint to create an authenticated **Client**.
    
5. Return the integrated terminal for the **test-with-labels** folder, and enter the following SDK-specific command to run the program:

    **C#**

    ```
    dotnet run
    ```

    **Python**

    ```
    python test-model-with-labels.py
    ```

6. View the output and notice the prediction confidence scores.   

## More information

For more information about the Form Recognizer service, see the [Form Recognizer documentation](https://docs.microsoft.com/azure/cognitive-services/form-recognizer/).
