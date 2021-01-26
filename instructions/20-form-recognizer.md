# Build custom models with the Form Recognizer service 

**Form Recognizer** is a cognitive service that enables users to build automated data processing software. This software can extract text, key/value pairs, and tables from form documents using optical character recognition (OCR). Form Recognizer has pre-built models for recognizing invoices, receipts, and business cards. The service also provides the capability to train custom models. In this exercise, we will focus on building custom models.

## Clone the repository for this course

If you have not already done so, you must clone the code repository for this course:

1. Start Visual Studio Code.
2. Open the palette (SHIFT+CTRL+P) and run a `Git: Clone` command to clone the `https://github/com/MicrosoftLearning/AI-102-AIEngineer` repository to a local folder.
3. When the repository has been cloned, open the folder in Visual Studio Code.

<a id="getform"></a>

## Create a Form Recognizer resource

1. Navigate to the Azure Portal [https://portal.azure.com](https://portal.azure.com), and sign in using the Microsoft account associated with your Azure subscription.
2. Select the **&#65291;Create a resource** button, search for *Form Recognizer*, and create a **Form Recognizer** resource with the following settings:
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Choose or create a resource group (if you are using a restricted subscription, you may not have permission to create a new resource group - use the one provided)*
    - **Region**: *Choose any available region*
    - **Name**: *Enter a unique name*
    - **Pricing tier**: F0

> **Note**: If you already have an F0 custom vision service in your subscription, select **S0** for this one.

3. When the resource has been deployed, go to it and view its **Keys and Endpoint** page. You will need the endpoint and one of the keys from this page to manage access from your code later on.

## Case: Automating Hero Limited's data entry process

Suppose the company Hero Limited asks you to automate a data entry process. Currently an employee at Hero Limited manually reads a purchase order and enters the data into a database. You want to build a model that will use a machine learning model to read the form and produce structured data that can be used to automatically update a database.   

You will use Form Recognizer to train and test custom form recognition models. First you'll train a model **without** labeled sample forms, then train a model **with** labeled sample forms.  

Overview of next steps: 
- Gather and upload training documents to an Azure Storage Blob
- Configure program environment variables
- Run a program to train a model without labels 
- Run a program to test the model trained without labels
- Repeat process to train and test a model with labels  

## Gather documents for training

![An image of a Hero Limited invoice.](../20-custom-form/sample-forms/train/Form_1.jpg)  

You'll use the sample forms in the **20-custom-form/sample-forms** folder in this repo, which contain all the files you'll need to train a model with labels and without labels. 

>**Important**: Take a look at the files in the folder. In the **AI-102** project, and in the **Explorer** pane, select the **20-custom-form** folder and expand the **sample-forms** folder. Notice there are files ending in **.json** and **.jpg**.    

>**Now**: You will use the **.jpg** files to train your first model _without_ labels.  

>**Later**: You will use the files ending in **.json** and **.jpg** to train your second model _with_ labels. The **.json** files contain special label information. To train with labels, you need to have special label information files (<mark>&lt;filename&gt;.jpg.labels.json</mark>) in your blob storage container alongside the forms.

You can learn more about custom model input requirements [here](https://docs.microsoft.com/azure/cognitive-services/form-recognizer/build-training-data-set#custom-model-input-requirements).

<a id="blob"></a>

## Store training data in an Azure blob storage container 

1. Return to the Azure portal at [https://portal.azure.com](https://portal.azure.com).
2. View the **Resource groups** in your subscription.
3. If you are using a restricted subscription in which a resource group has been provided for you, select the resource group to view its properties. Otherwise, create a new resource group with a name of your choice, and go to it when it has been created.
4. On the **Overview** page for your resource group, note the **Subscription ID** and **Location**. You will need these values, along with the name of the resource group in subsequent steps.
5. In Visual Studio Code, in the **AI-102** project, expand the **20-custom-form** folder and select **setup.cmd**. You will use this batch script to run the Azure command line interface (CLI) commands required to create the Azure resources you need.
6. Right-click the the **20-custom-form** folder and select **Open in Integrated Terminal**.
7. In the terminal pane, enter the following command to establish an authenticated connection to your Azure subscription.

    ```bash
    az login --output none
    ```

8. When prompted, open `https://microsoft.com/devicelogin`, enter the provided code, and sign into your Azure subscription. Then return to Visual Studio Code and wait for the sign-in process to complete.
9. Run the following command to list Azure locations.

    ```bash
    az account list-locations -o table
    ```

10. In the output, find the **Name** value that corresponds with the location of your resource group (for example, for *East US* the corresponding name is *eastus*).
11. In the **setup.cmd** script, modify the **subscription_id**, **resource_group**, and **location** variable declarations with the appropriate values for your subscription ID, resource group name, and location name. Then save your changes.
12. In the terminal for the **20-custom-form** folder, enter the following command to run the script:

    ```bash
    setup
    ```
13. When the script completes, review the displayed output and note your Azure resource's Storage account name. 

14. In the Azure portal, refresh the resource group and verify that it contains the Azure Storage account just created and a container with the **sampleforms** blob. The blob should contain all the forms from your local **20-custom-form/sample-forms** folder. 

![Screenshot of sampleforms container.](../20-custom-form/container_img.jpg)

## Train a model **without labels** using the client library

You will use the Form Recognizer SDK to train and test a custom model.  

> **Note**: In this exercise, you can choose to use the API from either the **C#** or **Python** SDK. In the steps below, perform the actions appropriate for your preferred language.

1. Browse to the **20-custom-form** folder and expand the **C-Sharp** or **Python** folder depending on your language preference.
 
2. Right-click the **train-without-labels** folder and open an integrated terminal.
<a id="package"></a>
Install the Form Recognizer package by running the appropriate command for your language preference:

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

    Open the configuration file. You will need a Form Recognizer key and endpoint, and the URI of your blob container for the configuration file.
    
    ### Get the Form Recognizer keys and endpoint 
    
    1. Navigate from the Azure Portal to the **Form Recognizer** resource you created earlier. 
    2. Select **Keys and Endpoint** on the left hand panel. Copy **Key 1** and **Endpoint** into the configuration file. 
    
    <a id ="sig"></a>
    ### Create a Shared Access Signature
    
    Now you will obtain our storage blob container's URI by creating a Shared Access Signature.  

    1. Navigate from the Azure Portal to your resources. From the main menu of your Storage Account, navigate to **Storage Explorer**, select **BLOB CONTAINERS**, and right click on the container **sampleforms**. 

    ![Visual of how to get shared access signature.](../20-custom-form/shared_access_sig.jpg)
 
    2. Select **Get Shared Access Signature**. Then use the following configurations: 
   
    - Access Policy: (none)
    - Start time: *leave as is for this exercise* 
    - End time: *leave as is for this exercise* 
    - Time Zone: Local 
    - Permissions: _Select **Read** and **List**_ 

    3. Select **Create** and copy the **URI**. 
    
    ![Visual of how to copy Shared Access Signature URI.](../20-custom-form/sas_example.jpg)

    4. Paste it to your local configuration file's storage url value. 
  
4. Note that the **train-without-labels** folder contains a code file for the client application:

    - **C#**: Program.cs
    - **Python**: train-model-without-labels&period;py

    Open the code file and review the code it contains, noting the following details:
    - Namespaces from the package you installed are imported
    - The **Main** function retrieves the configuration settings, and uses the key and endpoint to create an authenticated **Client**.
    > **C#**: The code uses the the training client with the <mark>StartTrainingAsync</mark> function and <mark>useTrainingLabels: false</mark> parameter.

    > **Python**: The code uses the training client with the <mark>begin_training</mark> function and <mark>use_training_labels=False</mark> parameter.  

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
7. Review the model output and locate the Model ID in the terminal.  
8. Copy the Model ID from the terminal output. You will use it when analyzing new forms.  

Now you're ready use your trained model. Notice how you trained your model using files from a storage container URI. You could also have trained the model using local files. Similarly, you can test your model using forms from a URI or from local files. You will test the form model with a local file. 

## Test the model created without labels 
Now that you've got the model ID, you can use it from a client application. Once again, you can choose to use **C#** or **Python**.

1. Browse to the **20-custom-form** folder and in the folder for your preferred language (**C-Sharp** or **Python**), expand the **test-without-labels** folder.
2. Right-click the **test-without-labels** folder. Open the code file for your client application (*Program.cs* for C#, *test-model-without-labels&period;py* for Python) and review the code it contains, noting the following details:
    - Namespaces from the package you installed are imported
    - The **Main** function retrieves the configuration settings, and uses the key and endpoint to create an authenticated **Client**.
    >**C#**: Notice that the program uses the <mark>StartRecognizeCustomForms</mark> function. If we were to analyze files from a storage blob URI we would use the <mark>StartRecognizeCustomFormsFromUri</mark> function. 
    
    >**Python**: Notice the program uses the same <mark>begin_recognize_custom_forms</mark> function with different parameters depending on whether we are analyzing files from a storage blob URI or local file.   
    
5. Return the integrated terminal for the **test-without-labels** folder, and enter the following SDK-specific command to run the program:

    **C#**

    ```
    dotnet run
    ```

    **Python**

    ```
    python test-model-without-labels.py
    ```

6. View the output and notice the prediction confidence scores. Notice how the output provides field names field-1, field-2 etc. 

>**Check In**: Can you find either of these fields in the terminal output?   

>Field 'field-X' has label 'Vendor Name:' with value 'Dwight Schrute' and a confidence score of ..
 
>Field 'field-X' has label 'Company Name:' with value 'Dunder Mifflin Paper' and a confidence score of ..


Now let's train a model using labels. 

## Train a model **with** labels using the client library 

Suppose after you trained a model with the invoice forms, you wanted to see how a model trained on labeled data performs. If you have not done so, please return to the [top of the page](#blob) and follow instructions to upload all the sample form files to a Storage Blob. 

1. In Visual Studio Code open the **AI-102** project, and in the **Explorer** pane, browse to the **20-custom-form** folder and expand the **C-Sharp** or **Python** folder depending on your language preference.
 
2. Right-click the **train-with-labels** folder and open an integrated terminal. If you have not already done so, [see here for directions](#package) to install the Form Recognizer package by running the appropriate command for your language. 

3. When you trained a model without labels you only used the **.jpg** forms from your Azure blob container. Now you will train a model using the **.jpg** and **.json** files. 

4. View the contents of the **train-with-labels** folder, and note that it contains a file for configuration settings:
    - **C#**: appsettings.json
    - **Python**: .env

    Open the configuration file. Update the configuration values it contains to reflect the endpoint and key for your Form Recognizer resource, and container Shared Access Signature.  
    
    You can use the same Form Recognizer key and endpoint created earlier. If you have not created a Form Recognizer Resource, [follow the directions here](#getform). 
    
    ### Get the Form Recognizer keys and endpoint 
    
    1. Navigate to the Form Recognizer resource.
    2. Select **Keys and Endpoint** on the left hand panel. Copy the key and endpoint into the configuration file. 
    
    You can use the same Shared Access Signature as you did before to configure the storage URI setting. You can review the [get Container's Shared Access Signature](#sig) section if you have not created your container's Shared Access Signature. 

5. Note that the **train-with-labels** folder contains a code file for the client application:

    - **C#**: Program.cs
    - **Python**: train-model-with-labels&period;py

    Open the code file and review the code it contains, noting the following details:
    - Namespaces from the package you installed are imported
    - The **Main** function retrieves the configuration settings, and uses the key and endpoint to create an authenticated **Client**.
    > **C#**: The code uses the the training client with the <mark>StartTrainingAsync</mark> function and <mark>useTrainingLabels: true</mark> parameter.

    > **Python**: The code uses the training client with the <mark>begin_training</mark> function and <mark>use_training_labels=True</mark> parameter.
    
6. Return the integrated terminal for the **train-with-labels** folder, and enter the following command to run the program:

    **C#**

    ```
    dotnet run
    ```

    **Python**

    ```
    python train-model-with-labels.py
    ```

7. Wait for the program to end, then review the model output. 
8. Copy the Model ID in the terminal output. You will use your Model ID when analyzing new forms.  

## Test the model created with labels

Now that you've got the model ID, test out the model. Once again, you can choose to use **C#** or **Python**.

1. In Visual Studio Code, in the **AI-102** project, browse to the **20-custom-form** folder and in the folder for your preferred language (**C-Sharp** or **Python**), expand the **test-with-labels** folder.

2. Right-click the **test-with-labels** folder. Open the code file for your client application (*Program.cs* for C#, *test-model-with-labels&period;py* for Python) and review the code it contains, noting the following details:
    - Namespaces from the package you installed are imported
    - The **Main** function retrieves the configuration settings, and uses the key and endpoint to create an authenticated **Client**.
    >**C#**: Notice that the program uses the <mark>StartRecognizeCustomForms</mark> function. If we were to analyze files from a storage blob URI we would use the <mark>StartRecognizeCustomFormsFromUri</mark> function. 
    
    >**Python**: Notice the program uses the same <mark>begin_recognize_custom_forms</mark> function with different parameters depending on whether we are analyzing files from a storage blob URI or local file.
    
3. Return the integrated terminal for the **test-with-labels** folder, and enter the following SDK-specific command to run the program:

    **C#**

    ```
    dotnet run
    ```

    **Python**

    ```
    python test-model-with-labels.py
    ```

4. View the output and notice the prediction confidence scores. Observe how the output for the model trained **with** labels provides field names like "CompanyPhoneNumber" and "DatedAs" unlike the output from the model trained **without** labels, which produced an output of field-1, field-2 etc.   

>**Check in**: Now that you have trained a custom model using Form Recognizer _with_ and _without_ labels, what similarities and differences do you see in the processes? 

While the program code for training a model with labels may not differ greatly from the code for training without labels, choosing one versus another can greatly change your project timeline. For example, if you use labeled forms you will need to label your documents (something we did not cover in this exercise but you can explore [here with the sample labeling tool](https://docs.microsoft.com/en-us/azure/cognitive-services/form-recognizer/quickstarts/label-tool?tabs=v2-0)). The choice of model also affects the downstream processes based on what fields the model returns and how confident you are with the returned values.  

## More information

For more information about the Form Recognizer service, see the [Form Recognizer documentation](https://docs.microsoft.com/azure/cognitive-services/form-recognizer/).


