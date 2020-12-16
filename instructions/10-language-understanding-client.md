# Creating a Language Understanding Client Application

The Language Understanding service enables you to define an app that encapsulates a language model that applications can use to interpret natural language input from users,  predict the users *intent* (what they want to achieve), and identify any *entities* to which the intent should be applied. You can create client applications that consume Language Understanding apps directly through REST interfaces, or by using language -specific software development kits (SDKs).

## Clone the repository for this course

If you have not already done so, you must clone the code repository for this course:

1. Start Visual Studio Code.
2. Open the palette (SHIFT+CTRL+P) and run a `Git: Clone` command to clone the `https://github/com/GraemeMalcolm/AI-102` repository to a local folder.
3. When the repository has been cloned, open the folder in Visual Studio Code.

## Create Language Understanding resources

To use the Language Understanding service, you need two kinds of resource:

- An *authoring* resource: used to define, train, and test the language understanding app. This must be a **Language Understanding - Authoring** resource in your Azure subscription.
- A *prediction* resource: used to publish your language understanding app and handle requests from client applications that use it. This can be either a **Language Understanding** or **Cognitive Services** resource in your Azure subscription.

> **Note**: If you already have Language Understanding authoring and prediction resources in your Azure subscription, you can use them in this exercise. Otherwise, follow these instructions to create them.

1. Open the Azure portal at [https://portal.azure.com](https://portal.azure.com), and sign in using the Microsoft account associated with your Azure subscription.
2. Select the **&#65291;Create a resource** button, search for *language understanding*, and create a **Language Understanding** resource with the following settings:
    - **Create option**: Both
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Choose or create a resource group (if you are using a hosted lab environment, you may not have permission to create a new resource group - use the one provided)*
    - **Name**: *Enter a unique name*
    - **Authoring location**: *Select your preferred location*
    - **Authoring pricing tier**: F0
    - **Prediction location**: *Choose the <u>same location</u> as your authoring location*
    - **Prediction pricing tier**: F0\*

    \**If F0 is not available, choose S0*

3. Wait for the resources to be created, and note that two Language Understanding resources are provisioned; one for authoring, and another for prediction. You can view both of these by navigating to the resource group where you created them.

## Import, train, and publish a Language Understanding app

In this exercise, you'll use an app that contains a language model for clock-related intents. For example, the user input *what is the time?* predicts an intent named **GetTime**.

> **Note**: If you already have a **Clock** app from a previous exercise, you can use it in this exercise. Otherwise, follow these instructions to create it.

1. In a new browser tab, open the Language Understanding portal for the location where you created your authoring resource:
    - US: [https://www.luis.ai](https://www.luis.ai)
    - Europe: [https://eu.luis.ai](https://eu.luis.ai)
    - Australia: [https://au.luis.ai](https://au.luis.ai)
 2. Sign in using the Microsoft account associated with your Azure subscription. If this is the first time you have signed into the Language Understanding portal, you may need to grant the app some permissions to access your account details. Then complete the *Welcome* steps by selecting your Azure subscription and the authoring resource you just created.
3. Open the **Conversation Apps** page, next to **&#65291;New app**, view the drop-down list and select **Import As LU**.
Browse to the **10-luis-client** subfolder in the project folder containing the lab files for this exercise, and select **Clock&period;lu**. Then specify a unique name for the clock app.
4. If a panel with tips for creating an effective Language Understanding app is displayed, close it.
5. At the top of the Language Understanding portal, select **Train** to train the app.
6. At the top right of the Language Understanding portal, select **Publish** and publish the app to the **Production slot**.
7. After publishing is complete, at the top of the Language Understanding portal, select **Manage**.
8. On the **Settings** page, note the **App ID**. Client applications need this to use your app.
9. On the **Azure Resources** page, under **Prediction resources**, if no prediction resource is listed, add the prediction resource in your Azure subscription.
10. Note the **Primary Key**, **Secondary Key**, and **Endpoint URL** for the prediction resource. Client applications need the endpoint and one of the keys to connect to the prediction resource and be authenticated.

## Prepare to use the Language Understanding SDK

In this exercise, you'll complete a partially implemented client application that uses the clock Language Understanding app to predict intents from user input and respond appropriately.

> **Note**: You can choose to use the SDK for either **C#** or **Python**. In the steps below, perform the actions appropriate for your preferred language.

1. In Visual Studio Code open the **AI-102** project, and in the **Explorer** pane, browse to the **10-luis-client** folder and expand the **C-Sharp** or **Python** folder depending on your language preference.
2. Right-click the **speaking-clock** folder and open an integrated terminal. Then install the Language Understanding SDK package by running the appropriate command for your language preference:

   **C#**

    ```
    dotnet add package Microsoft.Azure.CognitiveServices.Language.LUIS.Runtime --version 3.0.0
    ```

   **Python**

   ```
   pip install azure-cognitiveservices-language-luis==0.7.0
   ```

3. View the contents of the **speaking-clock** folder, and note that it contains a file for configuration settings:
    - **C#**: appsettings.json
    - **Python**: .env

