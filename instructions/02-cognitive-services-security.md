# Manage Cognitive Services Security

Security is a critical consideration for any application, and as a developer you should ensure that access to resources such as cognitive services is restricted to only those who require it.

Access to cognitive services is typically controlled through authentication keys, which are generated when you initially create a cognitive services resource.

## Clone the repository for this course

If you have not already done so, you must clone the code repository for this course:

1. Start Visual Studio Code.
2. Open the palette (SHIFT+CTRL+P) and run a `Git: Clone` command to clone the `https://github.com/GraemeMalcolm/AI-102` repository to a local folder.
3. When the repository has been cloned, open the folder in Visual Studio Code.
4. Wait while additional files are installed to support the C# code projects in the repo.

## Provision a Cognitive Services resource

If you don't already have on in your subscription, you'll need to provision a **Cognitive Services** resource.

1. Open the Azure portal at [https://portal.azure.com](https://portal.azure.com), and sign in using the Microsoft account associated with your Azure subscription.
2. Select the **&#65291;Create a resource** button, search for *cognitive services*, and create a **Cognitive Services** resource with the following settings:
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Choose or create a resource group (if you are using a restricted subscription, you may not have permission to create a new resource group - use the one provided)*
    - **Region**: *Choose any available region*
    - **Name**: *Enter a unique name*
    - **Pricing tier**: Standard S0
3. Select the required checkboxes and create the resource.
4. Wait for deployment to complete, and then view the deployment details.

## Manage authentication keys

When you created your cognitive services resource, two authentication keys were generated. You can manage these in the Azure portal or by using the Azure command line interface (CLI).

1. In the Azure portal, go to your cognitive services resource and view its **Keys and Endpoint** page. This page contains the information that you will need to connect to your resource and use it from applications you develop. Specifically:
    - An HTTP *endpoint* to which client applications can send requests.
    - Two *keys* that can be used for authentication (client applications can use either of the keys. A common practice is to use one for development, and another for production. You can easily regenerate the development key after developers have finished their work to prevent continued access).
    - The *location* where the resource is hosted. This is required for requests to some (but not all) APIs.
2. In Visual Studio Code, open a terminal and enter the following command to sign into your Azure subscription by using the Azure CLI.

    ```azurecli
    az login
    ```

    If you are not already signed in, a web browser will open and prompt you to sign into Azure. Do so, and then close the browser and return to Visual Studio Code.

    > **Tip**: If you have multiple subscriptions, you'll need to ensure that you are working in the one that contains your cognitive services resource.  Use this command to determine your current subscription.
    >
    > ```azurecli
    > az account show
    > ```
    >
    > If you need to change the subscription, run this command, changing *&lt;subscriptionName&gt;* to the correct subscription name.
    >
    > ```azurecli
    > az account set --subscription <subscriptionName>
    > ```

3. Now you can use the following command to get the list of cognitive services keys, replacing *&lt;resourceName&gt;* with the name of your cognitive services resource, and *&lt;resourceGroup&gt;* with the name of the resource group in which you created it.

    ```azurecli
    az cognitiveservices account keys list --name <resourceName> --resource-group <resourceGroup>
    ```

    The command returns a list of the keys for your cognitive services resource - there are two keys, named **key1** and **key2**.

4. To test your cognitive service, you can use *curl* - a command line tool for HTTP requests. Enter the following command (on a single line), replacing *&lt;yourEndpoint&gt;* and *&lt;yourKey&gt;* with your endpoint URI and **Key1** key to use the Text Analytics API in your cognitive services resource.

    ```curl
    curl -X POST "<yourEndpoint>/text/analytics/v3.0/languages?" -H "Content-Type: application/json" -H "Ocp-Apim-Subscription-Key: <yourKey>" --data-ascii "{'documents':[{'id':1,'text':'hello'}]}"
    ```

    The command returns a JSON document containing information about the language detected in the input data (which should be English).

5. If a key becomes compromised, or the developers who have it no longer require access, you can regenerate it in the portal or by using the Azure CLI. Run the following command to regenerate your **key1** key (replacing *&lt;resourceName&gt;* and *&lt;resourceGroup&gt;* for your resource).

    ```azurecli
    az cognitiveservices account keys regenerate --name <resourceName> --resource-group <resourceGroup> --key-name key1
    ```

    The list of keys for your cognitive services resource is returned - note that **key1** has changed since you last retrieved them.

6. Re-run the *curl* command with the old key (you can use the **^** key to cycle through previous commands), and verify that it now fails.
7. Re-run the *curl* command, replacing the key with the new **key1** value and verify that it succeeds.

> **Tip**: In this exercise, you used the full names of Azure CLI parameters, such as ``` --resource-group ```.  You can also use shorter alternatives, such as ``` -g ```, to make your commands less verbose (but a little harder to understand).  The [Cognitive Services CLI command reference](https://docs.microsoft.com/cli/azure/cognitiveservices?view=azure-cli-latest) lists the parameter options for each cognitive services CLI command.

## Secure key access with Azure Key Vault

You can develop applications that consume cognitive services by using a key for authentication. However, this means that the application code must be able to obtain the key. One option is to store the key in an environment variable or a configuration file where the application is deployed, but this approach leaves the key vulnerable to unauthorized access. A better approach when developing applications on Azure is to store the key securely in Azure Key Vault, and provide access to the key through a *managed identity* (in other words, a user account used by the application itself).

### Create a key vault and add a secret

First, you need to create a key vault and add a *secret* for the cognitive services key.

1. Make a note of the **key1** value for your cognitive services resource (or copy it to the clipboard).
2. In the Azure portal, select the **&#65291;Create a resource** button, search for *Key Vault*, and create a **Key Vault** resource with the following settings:
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *The same resource group as your cognitive service resource*
    - **Key vault name**: *Enter a unique name*
    - **Region**: *The same region as your cognitive service resource*
    - **Pricing tier**: Standard
3. Wait for deployment to complete and then go to your key vault resource.
4. In the left navigation pane, select **Secrets** (in the Settings section).
5. Select **+ Generate/Import** and add a new secret with the following settings :
    - **Upload options**: Manual
    - **Name**: Cognitive-Services-Key *(it's important to match this exactly, because later you'll run code that retrieves the secret based on this name)*
    - **Value**: *Your **key1** cognitive services key*

### Create a service principal

To access the secret in the key vault, your application must use a service principal that has access to the secret.

1. To create a service principal with owner role on the resource group, run the following Azure CLI command, replacing *&lt;spName&gt;* with a suitable name for an application identity (for example, *ai-app*). Also replace *&lt;subscriptionId&gt;* and *&lt;resourceGroup&gt;* with the correct values for your subscription ID and the resource group containing your cognitive services and key vault resources:

    > **Tip**: If you are unsure of your subscription ID, use the `az account show` command to retrieve your subscription information - the subscription ID is the **id** attribute in the output.

    ```azurecli
    az ad sp create-for-rbac -n "https://<spName>" --role owner --scopes subscriptions/<subscriptionId>/resourceGroups/<resourceGroup>
    ```

    The output of this command includes information about your new service principal. It should look similar to this:

    ```azurecli
    {
      "appId": "abcd12345efghi67890jklmn",
      "displayName": "ai-app",
      "name": "https://ai-app",
      "password": "1a2b3c4d5e6f7g8h9i0j",
      "tenant": "1234abcd5678fghi90jklm"
    }
    ```
    Make a note of the **appId**, **password**, and **tenant** values - you will need them later (if you close this terminal, you won't be able to retrieve the password; so it's important to note the values now!)

2. To assign permission for your new service principal to access secrets in your Key Vault, run the following Azure CLI command, replacing *&lt;keyVaultName&gt;* with the name of your Azure Key Vault resource and *&lt;spName&gt;* with the same value you provided when creating the service principal.

    ```azurecli
    az keyvault set-policy -n <keyVaultName> --spn "https://<spName>" --secret-permissions get list
    ```

### Use the service principal in an application

Now you're ready to use the service principal identity in an application, so it can access the secret congitive services key in your key vault and use it to connect to your cognitive services resource.

> **Note**: In this exercise, we'll store the service principal credentials in environment variables and use them to authenticate the **DefaultAzureCredential** identity in your application code. This is fine for development and testing, but in a real production application, an administrator would assign a *managed identity* to the application so that it uses the service principal identity to access resources, without caching or storing the password.

1. In Visual Studio Code, in the **AI-102** project, browse to the **02-cognitive-security** folder and expand the **C-Sharp** or **Python** folder depending on your language preference.
2. Right-click the **keyvault-client** folder and open an integrated terminal. Then install the packages you will need to use Azure Key Vault and the Text Analytics API in your cognitive services resource by running the appropriate command for your language preference:

   **C#**

    ```
    dotnet add package Azure.AI.TextAnalytics --version 5.0.0
    dotnet add package Azure.Identity --version 1.3.0
    dotnet add package Azure.Security.KeyVaults.Secrets --version 4.1.0
    ```

   **Python**

   ```
   pip install azure-ai-textanalytics==5.0.0
   pip install azure-identity==1.5.0
   pip install azure-keyvault-secrets==4.2.0
   ```

3. View the contents of the **keyvault-client** folder, and note that it contains a file for configuration settings:
    - **C#**: appsettings.json
    - **Python**: .env

    Open the configuration file and update the configuration value it contains to reflect the **endpoint** for your Cognitive Services resource and the name of the Azure Key Vault resource. Save your changes.
4. Note that the **keyvault-client** folder contains a code file for the client application:

    - **C#**: Program.cs
    - **Python**: keyvault-client&period;py

    Open the code file and review the code it contains, noting the following details:
    - The namespace for the SDK you installed is imported
    - Code in the **Main** function retrieves the cognitive services endpoint and name of your key vault resource, and then it uses the default Azure credentials to get the cognitive services key from the key vault.
    - The **GetLanguage** function uses the SDK to create a client for the service, and then uses the client to detect the language of the text that was entered.
5. Return to the integrated terminal for the **keyvault-client** folder, and run the following commands to set environment variables, replacing *&lt;appId&gt;*, *&lt;tenant&gt;*, and, *&lt;password&gt;* with the corresponding values from the output when you created the service principal. These are used for the default Azure credentials, and will cause your application to use the service principal identity.

    ```azurecli
    setx AZURE_CLIENT_ID <appId>
    setx AZURE_TENANT_ID <tenant>
    setx AZURE_CLIENT_SECRET <password>
    ```
6. Enter the following command to run the program:

    **C#**

    ```
    dotnet run
    ```

    **Python**

    ```
    python keyvault-client.py
    ```

6. When prompted, enter some text and review the language that is detected by the service. For example, try entering "Hello", "Bonjour", and "Hola".
7. When you have finished testing the application, enter "quit" to stop the program.

### Reset the security context

1. In the Terminal window, enter the command `az logout` to log out of your Azure subscription.
2. In the Windows Search box, enter **Edit the system environment variables**. Then in the **System Properties** dialog box, select **Environment variables**.
3. Delete the following system environment variables:
    - AZURE_CLIENT_ID
    - AZURE_TENANT_ID
    - AZURE_CLIENT_SECRET

## More information

For more information about securing cognitive services, see the [Cognitive Services security documentation](https://docs.microsoft.com/azure/cognitive-services/cognitive-services-security).