# Create a Language Understanding Application

The Language Understanding service enables you to define a language model that applications can use to interpret natural language input from users,  predict the users *intent* (what they want to achieve), and identify any *entities* to which the intent should be applied.

For example, a language model for a clock application might be expected to process input such as:

*What is the time in London?*

This kind of input is an example of an *utterance* (something a user might say or type), for which the desired *intent* is to get the time in a specific location (an *entity*); in this case, London.

> **Note**: The task of the language model is to predict the user's intent, and identify any entities to which the intent applies. It is <u>not</u> the job of the language model to actually perform the actions required to satisfy the intent. For example, the clock application can use a language model to discern that the user wants to know the time in London; but the application itself must then implement the logic to determine the correct time and present it to the user.

## Clone the repository for this course

If you have not already done so, you must clone the code repository for this course:

1. Start Visual Studio Code.
2. Open the palette (SHIFT+CTRL+P) and run a `Git: Clone` command to clone the `https://github/com/GraemeMalcolm/AI-102` repository to a local folder.
3. When the repository has been cloned, open the folder in Visual Studio Code.

## Create Language Understanding resources

To use the Language Understanding service, you need two kinds of resource:

- An *authoring* resource: used to define, train, and test the language model. This must be a **Language Understanding - Authoring** resource in your Azure subscription.
- A *prediction* resource: used to publish model and handle requests from client applications that use it. This can be either a **Language Understanding** or **Cognitive Services** resource in your Azure subscription.

     > **Important**: Authoring resources must be created in one of three *regions* (Europe, Australia, or US). Models created in European or Australian authoring resources can only be deployed to prediction resources in Europe or Australia respectively; models created in US authoring resources can be deployed to prediction resources in any Azure location other than Europe and Australia. See the [authoring and publishing regions documentation](https://docs.microsoft.com/azure/cognitive-services/luis/luis-reference-regions) for details about matching authoring and prediction locations.

1. Open the Azure portal at [https://portal.azure.com](https://portal.azure.com), and sign in using the Microsoft account associated with your Azure subscription.
2. Select the **&#65291;Create a resource** button, search for *language understanding*, and create a **Language Understanding** resource with the following settings:
    - **Create option**: Both
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Choose or create a resource group (if you are using a hosted lab environment, you may not have permission to create a new resource group - use the one provided)*
    - **Name**: *Enter a unique name*
    - **Authoring location**: *Select your preferred location*
    - **Authoring pricing tier**: F0
    - **Prediction location**: *Choose a location in the same region as your authoring location*
    - **Prediction pricing tier**: F0
3. Wait for the resources to be created, and note that two Language Understanding resources are provisioned; one for authoring, and another for prediction. You can view both of these by navigating to the resource group where you created them.

## Create a Language Understanding App

Now that you have created an authoring resource, you can use it to create a Language Understanding app.

1. In a new browser tab, open the Language Understanding portal for the authoring region where you created your authoring resource:
    - US: [https://www.luis.ai](https://www.luis.ai)
    - Europe: [https://eu.luis.ai](https://eu.luis.ai)
    - Australia: [https://au.luis.ai](https://au.luis.ai)
 2. Sign in using the Microsoft account associated with your Azure subscription. If this is the first time you have signed into the Language Understanding portal, you may need to grant the app some permissions to access your account details. Then complete the *Welcome* steps by selecting your Azure subscription and the authoring resource you just created.
3. Open the **Conversation Apps** page, and select your subscription and Language Understanding authoring resource. Then create a new app for conversation with the following settings:
    - **Name**: Clock
    - **Culture**: English (*if this option is not available, leave it blank*)
    - **Description**: Natural language clock
    - **Prediction resource**: *Your Language Understanding prediction resource*
4. If a panel with tips for creating an effective Language Understanding app is displayed, close it.

## Create intents

The first thing well do in the new app is to define some intents.

1. On the **Intents** page, select **&#65291; Create** to create a new intent named **GetTime**.
2. In the **GetTime** intent, add the following utterances as example user input:

    *what is the time?*

    *what time is it?*

3. After you've added these utterances, go back to the **Intents** page and add another new intent named **GetDay** with the following utterances:

    *what is the day today?*

    *what day is it?*

4. After you've added these utterances, go back to the **Intents** page and select the **None** intent. This is provided as a fallback for input that doesn't map to any of the intents you have defined in your language model.
5. Add the following utterances to the **None** intent:

    *hello*

    *goodbye*

## Train and test the app

Now that you've added some intents, let's train the app model and see if it can correctly predict them from user input.

1. At the top right of the portal, select **Train** to train the app.
2. When the app is trained, select **Test** to display the Test pane, and then enter the following test utterance:

    *what's the time now?*

    Review the result that is returned, noting that it includes the predicted intent (which should be **GetTime**) and a confidence score that indicates the probability the model calculated for the predicted intent.

3. Try the following test utterance:

    *tell me the time*

    Again, review the predicted intent and confidence score.

4. Try the following test utterance:

    *what's today?*

    Hopefully the model predicts the **GetDay** intent.

5. Finally, try this test utterance:

    *hi*

    This should return the **None** intent.

6. Close the Test pane.

## Add an entity

So far you've defined some simple utterances that map to intents. Most real applications include more complex utterances from which specific data entities must be extracted to get more context for the intent.

1. On the **Entities** page, select **&#65291; Create** to create a new entity.
2. In the **Create an entity** dialog box, create a **Machine learned** entity named **Location**.
3. After the **Location** entity has been created, return to the **Intents** page and select the **GetTime** intent.
4. Enter the following new example utterance:

    *what time is it in London?*

5. When the utterance has been added, select the word ***london***, and in the drop-down list that appears, select **Location** to indicate that "london" is an example of a location.
6. Add another example utterance:

    *what is the current time in New York?*

7. When the utterance has been added, select the words ***new york***, and map them to the **Location** entity.

8. At the top right of the portal, select **Train** to retrain the app.
9. When the app is trained, select **Test** to display the Test pane, and then enter the following test utterance:

    *what's the time in Edinburgh?*

10. Review the result that is returned, which should hopefully predict the **GetTime** intent. Then select **Inspect** and in the additional inspection pane that is displayed, examine the **ML entities** section. The model should have predicted that "edinburgh" is an instance of a **Location** entity.

3. Close the inspection pane.

## Perform batch testing
