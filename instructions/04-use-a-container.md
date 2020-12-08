# Use a Cognitive Services Container

Using cognitive services hosted in Azure enables application developers to focus on the infrastructure for their own code while benefiting from scalable services that are managed by Microsoft. However, in many scenarios, organizations require more control over their service infrastructure and the data that is passed between services.

Many of the cognitive services APIs can be packaged and deployed in a *container*, enabling organizations to host cognitive services in their own infrastructure; for example in local Docker servers, Azure Container Instances, or Azure Kubernetes Services clusters. Containerized cognitive services need to communicate with an Azure-based cognitive services account to support billing; but application data is not passed to the back-end service, and organizations have greater control over the deployment configuration of their containers, enabling custom solutions for authentication, scalability, and other considerations.

## Clone the repository for this course

If you have not already done so, you must clone the code repository for this course:

1. Start Visual Studio Code.
2. Open the palette (SHIFT+CTRL+P) and run a `Git: Clone` command to clone the `https://github/com/GraemeMalcolm/AI-102` repository to a local folder.
3. When the repository has been cloned, open the folder in Visual Studio Code.

## Provision a Cognitive Services resource

If you don't already have on in your subscription, you'll need to provision a **Cognitive Services** resource.

1. Open the Azure portal at [https://portal.azure.com](https://portal.azure.com), and sign in using the Microsoft account associated with your Azure subscription.
2. Select the **&#65291;Create a resource** button, search for *cognitive services*, and create a **Cognitive Services** resource with the following settings:
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Choose or create a resource group (if you are using a hosted lab environment, you may not have permission to create a new resource group - use the one provided)*
    - **Region**: *Choose any available region*
    - **Name**: *Enter a unique name*
    - **Pricing tier**: Standard S0
3. Select the required checkboxes and create the resource.
4. Wait for deployment to complete, and then view the deployment details.
5. When the resource has been deployed, go to it and view its **Keys and Endpoint** page. You will need the endpoint and one of the keys from this page in the next procedure.

## Deploy and run a Text Analytics container

Many of the most commonly used cognitive services APIs are available in container images. For a full list, check out the [cognitive services documentation](https://docs.microsoft.com/azure/cognitive-services/cognitive-services-container-support#container-availability-in-azure-cognitive-services). In this exercise, you'll use the container image for the Text Analytics *language detection* API; but the principles are the same for all of the available images.

1. Start Docker Deskop. It will take a minute or so to start, and when it does, close the window that opens. Docker Desktop is still running (you can verify this by looking for the icon in the system tray).
2. In Visual Studio Code, open a terminal window and enter the following command (on a single line) to deploy the language detection container to your local Docker instance, replacing *&lt;yourEndpoint&gt;* and *&lt;yourKey&gt;* with your endpoint URI and either of the keys for your cognitive services resource.

    ```bash
    docker run --rm -it -p 5000:5000 --memory 4g --cpus 1 mcr.microsoft.com/azure-cognitive-services/textanalytics/language Eula=accept Billing=<yourEndpoint> ApiKey=<yourKey>
    ```

    The command will look for the image on your local machine, and when it doesn't find it there it will pull it from the *mcr&period;microsoft&period;com* image registry and deploy it to your Docker instance. When deployment is complete, the container will start and listen for incoming requests on port 5000.

3. When prompted, allow access through the firewall. If you are using a hosted lab environment, enter the password you logged in with.
4. Note that the container will run until you press CTRL+C in the terminal window. Leave this terminal running for now.
5. In a new web browser tab, browse to http://localhost:5000 and verify that the container is running at this endpoint.
6. Browse to http://localhost:5000/swagger to view information about the REST functions you can call in the containerized service.
7. Return to Visual Studio Code and open a new terminal window. Then in the new terminal, enter the following command to call the language detection REST API on your local container. Note that you do not need to specify the cognitive services endpoint or key - the request is processed by the containerized service. The container in turn communicates periodically with the service in Azure to report usage for billing, but does not send request data.

    ```curl
    curl -X POST "http://localhost:5000/text/analytics/v3.0/languages?" -H "Content-Type: application/json" --data-ascii "{'documents':[{'id':1,'text':'hello'}]}"
    ```

    The command returns a JSON document containing information about the language detected in the input data (which should be English).

8. In Visual Studio Code, in the terminal pane, switch to the **docker** terminal where the container is running, and then press **CTRL+C** to stop the container.
9. In the system tray, right-click the Docker Desktop icon and quit Docker Desktop.
