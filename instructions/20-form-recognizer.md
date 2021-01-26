# Build custom models with the Form Recognizer service 

**Form Recognizer** is a cognitive service that lets you build automated data processing software by extracting text, and key/value pairs from form documents using optical character recognition (OCR). Form Recognizer has pre-built models for recognizing invoices, receipts, and business cards. The service also gives you the capability to create custom models, trained to your industry-specific forms. In this exercise, you will focus on building custom models.

## Clone the repository for this course

If you have not already done so, you must clone the code repository for this course:

1. Start Visual Studio Code.
2. Open the palette (SHIFT+CTRL+P) and run a `Git: Clone` command to clone the `https://github/com/MicrosoftLearning/AI-102-AIEngineer` repository to a local folder.
3. When the repository has been cloned, open the folder in Visual Studio Code.

<a id="getform"></a>
## Create a Form Recognizer resource 

1. Navigate to the Microsoft account associated with your Azure subscription at [https://portal.azure.com](https://portal.azure.com).
2. Select the **&#65291;Create a resource** button, search for *Form Recognizer*, and create a **Form Recognizer** resource with the following settings:
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Choose or create a resource group (if you are using a restricted subscription, you may not have permission to create a new resource group - use the one provided)*
    - **Region**: *Choose any available region*
    - **Name**: *Enter a unique name*
    - **Pricing tier**: F0

> **Note**: If you already have an F0 custom vision service in your subscription, select **S0** for this one.

3. When the resource has been deployed, go to it and view its **Keys and Endpoint** page. You will need the endpoint and one of the keys from this page to manage access from your code later on.

## Custom Form Case: Hero Limited

Suppose the company Hero Limited asks you to automate the their data entry process. Currently an employee at Hero Limited manually reads each invoice and enters its data it into a database. You want to build a model that will use a machine learning model to read an invoice and produce structured data that can be used to automatically update a database.   

You will use Form Recognizer to train and test custom form recognition models. First you'll train a model **without** labeled sample forms, then train a model **with** labeled sample forms.  

Overview of next steps: 
- Gather and upload training documents to an Azure Storage Blob
- Create a Form Recognizer resource, taking note of its keys and endpoint
- Configure our environment variables
- Run a program to train a model without labels 
- Run a program to test the model trained without labels
- Repeat process to train and test a model with labels  

## Gather documents for training

![An image of a Hero Limited invoice.](../20-custom-form/sample-forms/train/Form_1.jpg)

 You need to provide a minimum of **five** filled-in forms or an empty form (you must include the word "empty" in the file name) with two filled-in forms.Their format must be JPG, PNG, PDF (text or scanned), or TIFF. The full custom model input requirements can be found [here](https://docs.microsoft.com/azure/cognitive-services/form-recognizer/build-training-data-set#custom-model-input-requirements) and are discussed in depth in the Learn module (no link yet).    

You'll use the sample forms in the **20-custom-form/sample-forms/train** folder in this repo, which contain all the files you'll need to train a model with labels and without labels. 

Take a look at the files in the folder. In Visual Studio Code open the **AI-102** project, and in the **Explorer** pane, browse to the **20-custom-form** folder and expand the **sample-forms/train** folder. Notice there are files ending in **.json** and **.jpg**. You will upload all the files to our Azure Storage Blob.   

You will first use the **.jpg** files to train our first model _without_ labels.  

Later you will use the files ending in **.json** and **.jpg** to train our second model _with_ labels. The **.json** files contain special label information. To train with labels, you need to have special label information files (<mark>&lt;filename&gt;.jpg.labels.json</mark>) in your blob storage container alongside the forms.

 Next, create an Azure blob container to store the training form documents.

<a id="blob"></a>
## Store training data in an Azure blob storage container 

1. Open the Azure portal at [https://portal.azure.com](https://portal.azure.com), and sign in using the Microsoft account associated with your Azure subscription.
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

14. In the Azure portal, refresh the resource group and verify that it contains the Azure Storage account and a blob file with the forms from the local **20-custom-form/sample-forms/train** folder. 

## Train a model **without labels** using the client library

You will use the Form Recognizer SDK to train and test a custom model.  

> **Note**: In this exercise, you can choose to use the API from either the **C#** or **Python** SDK. In the steps below, perform the actions appropriate for your preferred language.

1. In Visual Studio Code open the **AI-102** project, and in the **Explorer** pane, browse to the **20-custom-form** folder and expand the **C-Sharp** or **Python** folder depending on your language preference.
 
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

    Open the configuration file. You will need our Form Recognizer's key and endpoint, and the URI of our blob container for our configuration file.
    
    ### Get the Form Recognizer keys and endpoint 
    
    1. Navigate to the Form Recognizer resource. 
    2. Select **Keys and Endpoint** on the left hand panel. Copy the key and endpoint into the configuration file. 
    
    Now you will obtain our storage blob container's URI by creating a Shared Access Signature.  
    
    <a id ="sig"></a>
    ### Create a Shared Access Signature

    Navigate to the [Azure portal](https://portal.azure.com/) and select your recently created Storage Account. From the main menu of your Storage Account, navigate to **Storage Explorer**, select **BLOB CONTAINERS**, and right click on the container **sampleforms**. 

    ![Visual of how to get shared access signature.](../20-custom-form/shared_access_sig.jpg)
 
     Select **Get Shared Access Signature**. Then use the following configurations: 
   
    - Access Policy: (none)
    - Start time: *leave as is for this exercise* 
    - End time: *leave as is for this exercise* 
    - Time Zone: Local 
    - Permissions: _Select **Read** and **List**_ 

    Select **Create** and copy the **URI**. Paste it to your local configuration file's **STORAGE_URL** value.

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
7. Review the model output in the terminal. Locate the Model ID.  
8. Copy the Model ID from the terminal output. You will use it when analyzing new forms.  

Now you're ready use your trained model. Notice how you trained your model using files from a storage container URI. You could also have trained our model using local files. Similarly, you can test your model using forms from a URI or from local files. You will test our form model with a local file using the **StartRecognizeCustomForms** method. However, you can also analyze new forms from a URI using the **StartRecognizeCustomFormsFromUri** method. 

## Test the model created without labels 
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

6. View the output and notice the prediction confidence scores. Notice how the output provides field names field-1, field-2. 

### Check In 

Can you find either of these identified fields in the terminal output?   
```
Field 'field-X' has label 'Vendor Name:' with value 'Dwight Schrute' and a confidence score of .. 
Field 'field-X' has label 'Company Name:' with value 'Dunder Mifflin Paper' and a confidence score of ..
```

Now let's train a model using labels. 

## Train a model **with** labels using the client library 

Suppose after you trained a model with the invoice forms, you wanted to see how a model trained on labeled data would perform. You will use labeled forms this time. If you have not done so, please return to the [top of the page](#blob) and follow instructions to upload all the sample form files to a Storage Blob. 

> **Note**: In this exercise, you can choose to use the API from either the **C#** or **Python** SDK. In the steps below, perform the actions appropriate for your preferred language.

1. In Visual Studio Code open the **AI-102** project, and in the **Explorer** pane, browse to the **20-custom-form** folder and expand the **C-Sharp** or **Python** folder depending on your language preference.
 
2. Right-click the **train-with-labels** folder and open an integrated terminal. If you have not already done so, [see here for directions](#package) to install the Form Recognizer package by running the appropriate command for your language. 

3. If you have not created an Azure blob yet for the Form Recognizer lab, please [see here for directions](#blob). Otherwise your blob should already contain images of our sample forms and labeled **.json** files. When you trained a model without labels the <mark>begin_training</mark> function only used the **.jpg** forms. Now you will train a model using the **.jpg** and **.json** files from this Azure blob.  

4. View the contents of the **train-with-labels** folder, and note that it contains a file for configuration settings:
    - **C#**: appsettings.json
    - **Python**: .env

    Open the configuration file. Update the configuration values it contains to reflect the endpoint and key for your Form Recognizer resource, and container Shared Access Signature.  
    
    You can use the same Form Recognizer key and endpoint created earlier. If you have not created a Form Recognizer Resource, [follow the directions here](#getform). 
    
    ### Get the Form Recognizer keys and endpoint 
    
    1. Navigate to the Form Recognizer resource.
    2. Select **Keys and Endpoint** on the left hand panel. Copy the key and endpoint into the configuration file. 
    
    Since you stored all your sample documents in one Azure Blob, you will use the same Shared Access Signature as you did before to configure the storage URI setting. You can review the [get Container's Shared Access Signature](#sig) section if you have not created your container's Shared Access Signature. 

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

## Test the model created with labels

Now that you've got the model ID, test out the model. Once again, you can choose to use **C#** or **Python**.

1. In Visual Studio Code, in the **AI-102** project, browse to the **20-custom-form** folder and in the folder for your preferred language (**C-Sharp** or **Python**), expand the **test-with-labels** folder.

2. Right-click the **test-with-labels** folder. Open the code file for your client application (*Program.cs* for C#, *test-model-with-labels&period;py* for Python) and review the code it contains, noting the following details:
    - Namespaces from the package you installed are imported
    - The **Main** function retrieves the configuration settings, and uses the key and endpoint to create an authenticated **Client**.
    
3. Return the integrated terminal for the **test-with-labels** folder, and enter the following SDK-specific command to run the program:

    **C#**

    ```
    dotnet run
    ```

    **Python**

    ```
    python test-model-with-labels.py
    ```

4. View the output and notice the prediction confidence scores. Notice how the output provides field names like "CompanyPhoneNumber" and "DatedAs" unlike the output from the model trained without labels, which produced an output of field-1, field-2 etc.   

### Check in
Now that you have trained a custom model using Form Recognizer without and with labels, what similarities and differences do you see in the processes? You can 

## More information

For more information about the Form Recognizer service, see the [Form Recognizer documentation](https://docs.microsoft.com/azure/cognitive-services/form-recognizer/).
