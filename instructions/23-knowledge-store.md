# Graeme is Working on this

The solution you will create for Margie's Travel requires the following resources in your Azure subscription:

- An Azure Storage account with a blob container in which the documents to be searched are stored, and in which you will create the knowledge store.
- An Azure Cognitive Search resource, which will manage the indexing process.
- An Azure Cognitive Services resource, which provides the AI services for skills in the enrichment pipeline.

A script containing Azure command-line interface (CLI) commands to create these resources has been provided. Use the following steps to run it.

1. In Visual Studio Code, in the **km** project, right-click (Ctrl+click if using a Mac) the **03-Create-a-knowledge-store** folder and select **Open in Integrated Terminal**. This will open a new bash terminal pane.

    > [!TIP]
    > You're going to open multiple terminal sessions during this module, each associated with a folder. They'll all be available in the same **Terminal** pane, and you can switch between them using the drop-down list (which will currently include a *bash* terminal for the session you just created).

2. In the terminal pane, enter the following command to establish an authenticated connection to your Azure subscription.

    ```bash
    az login --output none
    ```

3. When prompted, open `https://microsoft.com/devicelogin`, enter the provided code, and sign into your Azure subscription. Then return to Visual Studio Code and wait for the sign-in process to complete.
4. In the terminal pane, enter the following command to create the resources in the East US region. If you want to use a different region, change `eastus` to the region name of your choice - for example, `westus` or `northeurope` (for a full list of available regions, use the `az account list-locations -o table` command):

    ```bash
    bash setup.sh eastus
    ```

5. When the script completes, review the output it displays and note the following information about your Azure resources (you will need these values later):
    - Resource group name
    - Storage account name
    - Storage connection string
    - Cognitive Services account
    - Cognitive Services key
    - Search service endpoint
    - Search service admin key
    - Search service query key

6. Open the Azure portal at [https://portal.azure.com](https://portal.azure.com?azure-portal=true), signing in with the credentials associated with your Azure subscription if prompted.
7. In the Azure portal, find the resource group that was created by the setup script, and verify that it contains the Azure Storage account, Azure Cognitive Services resource, and Azure Cognitive Search resource.

## Create a data source

:::zone pivot="csharp"

Azure Cognitive Search provides a software development kit (SDK) for Microsoft .NET, which you can use to write C# code that works with your search resources.

1. In Visual Studio Code, expand the **03-Create-a-knowledge-store** folder and the **C-Sharp** folder it contains.
2. Expand the **create-knowledge-store** folder and open the **appsettings.json** file. This file contains configuration values for your C# code.
3. Modify the following values in the **appsettings.json** file to reflect your Azure resources, and then save the updated file:
    - **SearchServiceName**: Your Azure Cognitive Search service name (<u>without</u> the .*search&#46;windows&#46;net* suffix)
    - **SearchServiceAdminApiKey**: Your Azure Cognitive Search ***admin*** key
    - **CognitiveServicesApiKey**: Your Azure Cognitive Services key
    - **AzureBlobConnectionString**: Your Azure Storage blob container connection string.

4. Open the **Program.cs** file, and view the code it contains. The **Main** function:
    - Gets the configuration settings from the **appsettings.json** file.
    - Creates a **SearchServiceClient** object for your Azure Cognitive Search service.
    - Prompts the user for input, calling the appropriate functions to create Azure Cognitive Search components.
5. View the **CreateOrUpdateDataSource** function, which creates a data source named **margies-docs-cs** that references the Azure Storage blob container where the PDF documents are stored.
6. Right-click (Ctrl+click if using a Mac) the **C-Sharp/create-knowledge-store** folder and select **Open in Integrated Terminal**. This will open a new bash terminal in this folder.
7. In the terminal for the **create-knowledge-store** folder, enter the following command:
    ```bash
    dotnet run
    ```
8. When prompted, press **1** to create a data source. Then wait while the program creates the data source.
9. When the prompt is redisplayed, press **q** to quit the program.
10. Open your search service in the [Azure portal](https://portal.azure.com?portal=true) and view its **Data sources** tab to confirm that the data source has been created.

:::zone-end

:::zone pivot="python"

There is no Python SDK for creating Azure Cognitive Search objects, but you can use Python to submit requests to the Azure Cognitive Search REST API. In the case of a data source, the body of the REST request takes the form of a JSON document defining the data source to be created.

1. In Visual Studio Code, expand the **03-Create-a-knowledge-store** folder and the **Python** folder it contains.
2. Expand the **create-knowledge-store** folder and open the **data_source.json** file. This file contains the JSON definition for a data source that can be submitted to the Azure Cognitive Search REST interface.
3. Review the JSON code, which defines an Azure blob data source named **margies-docs-py** that references the **margies** container in an Azure Storage account. The connection string for the blob container is null - you will address this in your code later.
4. Open the **submit-rest&#46;py** code file and review the Python code it contains. This code is used to submit REST requests to your Azure Cognitive Search service.
5. Open the **.env** file, which contains environment variables for your Python code.
6. Modify the values in the **.env** file to reflect the Azure Cognitive Search endpoint, Azure Cognitive Search ***admin*** key, Azure Cognitive Services key, and Azure Storage blob container connection string for the Azure resources you created previously. Then save the updated file.
7. Right-click (Ctrl+click if using a Mac) the **Python/create-knowledge-store** folder and select **Open in Integrated Terminal**. This will open a new bash terminal in this folder.
8. In the terminal for the **create-knowledge-store** folder, enter the following command:
    ```bash
    python3 submit-rest.py 'POST' 'datasources' 'data_source.json'
    ```
9. Wait while Python runs the **submit-rest&#46;py** script to create the data store.
10. Review the JSON response that is returned from the REST interface, noting that the data source connection string is null to avoid returning sensitive data.
11. Open your search service in the [Azure portal](https://portal.azure.com?portal=true) and view its **Data sources** tab to confirm that the data source has been created.

:::zone-end

## Create a skillset

:::zone pivot="csharp"

At the time of writing, the .NET SDK for Azure Cognitive Search does not support creating skillsets that include a knowledge store definition. However, you can create a skillset by submitting its JSON definition to the Azure Cognitive Search REST interface. In this task, you'll use C# to create an HTTP request to the REST interface.

1. In the **C-Sharp/create-knowledge-store** folder, open the **skillset.json** file. This file contains the JSON definition of a skillset.
2. Review the skillset definition. It includes the following skills:
    - A **language detection** skill that identifies the language in which a document is written.
    - An **image analysis** skill that analyzes the images in the document and extracts insights from them.
    - An **OCR** skill that uses optical character recognition (OCR) to extract areas of text from the images in the document.
    - A **merge** skill that combines the OCR text extracted from images with the original text content in the document.
    - A **sentiment** skill that calculates a sentiment score for the text in the document.
    - An **entity recognition** skill that identifies and extracts locations and URLs that are mentioned in the documents.
    - A **key phrase extraction** skill that extracts a list of key phrases in each document based on an analysis of the text.
    - A **shaper** skill that defines a JSON structure for the enriched data. This object definition will be used for the *projections* that the pipeline will persist on the knowledge store for each document processed by the indexer.
3. Observe that the skillset also includes a **knowledgeStore** definition, which includes a connection string for the Azure Storage account where the knowledge store is to be created, and a collection of **projections**. This skillset includes three *projection groups*:
    - A group containing an *object* projection based on the **knowledge_projection** output of the shaper skill in the skillset.
    - A group containing a *file* projection based on the **normalized_images** collection of image data extracted from the documents.
    - A group containing the following *table* projections:
        - **KeyPhrases**: Contains an automatically generated key column and a **keyPhrase** column mapped to the **knowledge_projection/key_phrases/** collection output of the shaper skill.
        - **Locations**: Contains an automatically generated key column and a **location** column mapped to the **knowledge_projection/key_phrases/** collection output of the shaper skill.
        - **ImageTags**: Contains an automatically generated key column and a **tag** column mapped to the **knowledge_projection/image_tags/** collection output of the shaper skill.
        - **Docs**: Contains an automatically generated key column and all of the **knowledge_projection** output values from the shaper skill that are not already assigned to a table.
4. In the **C-Sharp/create-knowledge-store** folder, open the **Program.cs** file and review the **CreateSkillset** function. This function:
    - Reads the JSON skillset definition.
    - Updates the skillset definition with your cognitive services key and blob store connection string.
    - Submits an HTTP PUT request to the REST service that creates a skillset named **margies-skillset-cs**.
5. In the **Terminal** pane, select the bash terminal for the **create-knowledge-store** folder. If you have closed this terminal, right-click (Ctrl+click if using a Mac) the **C-Sharp/create-knowledge-store** folder and select **Open in Integrated Terminal**.
6. In the terminal for the **create-knowledge-store** folder, enter the following command:
    ```bash
    dotnet run
    ```
7. When prompted, press **2** to create a skillset. Then wait while the program creates the skillset.
8. When the prompt is redisplayed, press **q** to quit the program.
9. Open your search service in the [Azure portal](https://portal.azure.com?portal=true) and view its **Skillsets** tab to confirm that the skillset has been created.

:::zone-end

:::zone pivot="python"

1. In the **Python/create-knowledge-store** folder, open the **skillset.json** file. This file contains the JSON definition of a skillset.
2. Review the skillset definition. It includes the following skills:
    - A **language detection** skill that identifies the language in which a document is written.
    - An **image analysis** skill that analyzes the images in the document and extracts insights from them.
    - An **OCR** skill that uses optical character recognition (OCR) to extract areas of text from the images in the document.
    - A **merge** skill that combines the OCR text extracted from images with the original text content in the document.
    - A **sentiment** skill that calculates a sentiment score for the text in the document.
    - An **entity recognition** skill that identifies and extracts locations and URLs that are mentioned in the documents.
    - A **key phrase extraction** skill that extracts a list of key phrases in each document based on an analysis of the text.
    - A **shaper** skill that defines a JSON structure for the enriched data. This object definition will be used for the *projections* that the pipeline will persist on the knowledge store for each document processed by the indexer.
3. Observe that the skillset also includes a **knowledgeStore** definition, which includes a connection string for the Azure Storage account where the knowledge store is to be created, and a collection of **projections**. This skillset includes three *projection groups*:
    - A group containing an *object* projection based on the **knowledge_projection** output of the shaper skill in the skillset.
    - A group containing a *file* projection based on the **normalized_images** collection of image data extracted from the documents.
    - A group containing the following *table* projections:
        - **KeyPhrases**: Contains an automatically generated key column and a **keyPhrase** column mapped to the **knowledge_projection/key_phrases/** collection output of the shaper skill.
        - **Locations**: Contains an automatically generated key column and a **location** column mapped to the **knowledge_projection/key_phrases/** collection output of the shaper skill.
        - **ImageTags**: Contains an automatically generated key column and a **tag** column mapped to the **knowledge_projection/image_tags/** collection output of the shaper skill.
        - **Docs**: Contains an automatically generated key column and all of the **knowledge_projection** output values from the shaper skill that are not already assigned to a table.
4. In the **Terminal** pane, select the bash terminal for the **create-knowledge-store** folder. If you have closed this terminal, right-click (Ctrl+click if using a Mac) the **Python/create-knowledge-store** folder and select **Open in Integrated Terminal**.
5. In the terminal for the **create-knowledge-store** folder, enter the following command:
    ```bash
    python3 submit-rest.py 'PUT' 'skillsets/margies-skillset-py' 'skillset.json'
    ```
6. Wait while Python runs the **submit-rest&#46;py** script to create the skillset.
7. Review the JSON response that is returned from the REST interface.
8. Open your search service in the [Azure portal](https://portal.azure.com?portal=true) and view its **Skillsets** tab to confirm that the skillset has been created.

:::zone-end

> [!NOTE]
> To learn more about the **shaper** skill, see [Shaper cognitive skill](https://docs.microsoft.com/azure/search/cognitive-search-skill-shaper) in the Azure Cognitive Search documentation.
>
> To learn more about knowledge stores and projections, see [Knowledge store in Azure Cognitive Search](https://docs.microsoft.com/azure/search/knowledge-store-concept-intro) and [Knowledge store "projections" in Azure Cognitive Search](https://docs.microsoft.com/azure/search/knowledge-store-projection-overview).

## Create an index

:::zone pivot="csharp"

To create an index using C#, you must implement a class that represents the index, including all of its fields.

1. In the **C-Sharp/create-knowledge-store** folder, open the **MargiesIndex.cs** code file and view the code it contains. This code defines the index and the complex types it contains. 
2. Review the definition of the **MargiesIndex** class, which includes a mix of fields extracted directly from the data source and enriched fields generated by the skillset.
3. Open the **Program.cs** code file and review the code in the **CreateIndex** function, which creates an index named **margies-index-cs** based on the **MargiesIndex** class.
4. In the **Terminal** pane, select the bash terminal for the **create-knowledge-store** folder. If you have closed this terminal, right-click (Ctrl+click if using a Mac) the **C-Sharp/create-knowledge-store** folder and select **Open in Integrated Terminal**.
6. In the terminal for the **create-knowledge-store** folder, enter the following command:
    ```bash
    dotnet run
    ```
7. When prompted, press **3** to create an index. Then wait while the program creates the index.
8. When the prompt is redisplayed, press **q** to quit the program.
9. Open your search service in the [Azure portal](https://portal.azure.com?portal=true) and view its **Indexes** tab to confirm that the index has been created.

:::zone-end

:::zone pivot="python"

To create an index using Python, you must use the **indexes** REST endpoint. You can submit an HTTP *PUT* request to create or update an index based on a JSON document that defines the index schema.

1. In the **Python/create-knowledge-store** folder, open the **index.json** file. This file contains the JSON definition of an index.
2. Review the index definition. It includes a mix of fields extracted directly from the data source and enriched fields generated by the skillset.
3. In the **Terminal** pane, select the bash terminal for the **create-knowledge-store** folder. If you have closed this terminal, right-click (Ctrl+click if using a Mac) the **Python/create-knowledge-store** folder and select **Open in Integrated Terminal**.
4. In the terminal for the **create-knowledge-store** folder, enter the following command:
    ```bash
    python3 submit-rest.py 'PUT' 'indexes/margies-index-py' 'index.json'
    ```
5. Wait while Python runs the **submit-rest&#46;py** script, causing it to submit an HTTP PUT request to the *indexes* REST endpoint, adding an index named *margies-index-py* based on the JSON body defined in the *index.json* file. The use of a PUT request ensures that if the index already exists, it is updated based on the JSON; otherwise it is created.
6. Review the JSON response that is returned from the REST interface.
7. Open your search service in the [Azure portal](https://portal.azure.com?portal=true) and view its **Indexes** tab to confirm that the index has been created.

:::zone-end

## Run the indexer

:::zone pivot="csharp"

1. In the **C-Sharp/create-knowledge-store** folder, open the **Program.cs** file and review the code in the **CreateIndexer** function, which creates an indexer. The When a new indexer is initially created, it is run automatically.
2. Review the code in the **CheckIndexerOverallStatus** function, which retrieves the indexer status.
3. In the **Terminal** pane, select the bash terminal for the **create-knowledge-store** folder. If you have closed this terminal, right-click (Ctrl+click if using a Mac) the **C-Sharp/create-knowledge-store** folder and select **Open in Integrated Terminal**.
4. In the terminal for the **create-knowledge-store** folder, enter the following command:
    ```bash
    dotnet run
    ```
5. When prompted, press **4** to create and run an indexer. Then wait while the program creates the indexer and then retrieves it status.
6. When the prompt is redisplayed, press **q** to quit the program.
7. In another browser tab, open your search service in the [Azure portal](https://portal.azure.com?portal=true) and view its **Indexers** tab to confirm that the indexer has been created and has processed 72 documents (if it is still in-progress, wait for it to complete).

    > [!NOTE]
    > There may be some warnings indicating that some documents were too large for the sentiment skill to analyze fully, and only the first 1000 characters of these documents were processed. You can ignore these warnings.

:::zone-end

:::zone pivot="python"

1. In the **Python/create-knowledge-store** folder, open the **indexer.json** file. This file contains the JSON definition of an indexer.
2. Review the indexer definition and observe that it maps fields from the **margies-docs-py** data source to the **margies-index-py** index, and uses the **margies-skillset-py** skillset to generate enriched fields.
3. In the **Terminal** pane, select the bash terminal for the **create-knowledge-store** folder. If you have closed this terminal, right-click (CTRL+click if using a Mac) the **Python/create-knowledge-store** folder and select **Open in Integrated Terminal**.
4. In the terminal for the **create-knowledge-store** folder, enter the following command:
    ```bash
    python3 submit-rest.py 'PUT' 'indexers/margies-indexer-py' 'indexer.json'
    ```
5. Wait while Python runs the **submit-rest&#46;py** script, causing it to submit an HTTP PUT request to the *indexers* REST endpoint, adding an indexer named *margies-indexer-py* based on the JSON body defined in the *indexer.json* file. The use of a PUT request ensures that if the indexer already exists, it is updated based on the JSON; otherwise it is created.
6. Review the JSON response that is returned from the REST interface. The indexer is created and automatically run to initialize the index.
7. In the terminal for the **create-knowledge-store** folder, enter the following command:
    ```bash
    python3 submit-rest.py 'GET' 'indexers/margies-indexer-py/status' 'null'
    ```
8. Review the JSON response that is returned from the REST interface, which shows the status of the indexer. In particular, check the **status** value in the **lastResult** section of the response. If the status is shown as **inProgress**, the indexer is still being applied to the index. You can rerun the previous command to retrieve the status until the last result status is **success**.
9. In another browser tab, open your search service in the [Azure portal](https://portal.azure.com?portal=true) and view its **Indexers** tab to confirm that the indexer has been created and has processed 72 documents.

    > [!NOTE]
    > There may be some warnings indicating that some documents were too large for the sentiment skill to analyze fully, and only the first 1000 characters of these documents were processed. You can ignore these warnings.

:::zone-end

## View object projections

The *object* projections defined in the Margie's Travel skillset consist of a JSON file for each indexed document. These files are stored in a blob container in the Azure Storage account specified in the skillset definition.

1. Open the [Azure portal](https://portal.azure.com?portal=true) and view the Azure Storage account you created at the beginning of this module (its name is similar to *store1234abcd5678efgh*).
2. Select the **Storage explorer** tab (in the pane on the left) to view the storage account in the storage explorer interface in the Azure portal.
2. Expand **BLOB CONTAINERS** to view the containers in the storage account. In addition to the **margies** container where the source data is stored, there should be two new containers: **margies-images** and **margies-knowledge**. These were created by the indexing process.
3. Select the **margies-knowledge** container. It should contain a folder for each indexed document.
4. Open any of the folders, and then open the **knowledge-projection.json** file it contains. Each JSON file contains a representation of an indexed document, including the enriched data extracted by the skillset as shown here.

    ```json
    {
        "file_id":"abcd1234....",
        "file_name":"Margies Travel Company Info.pdf",
        "url":"https://store....blob.core.windows.net/margies/...pdf",
        "language":"en",
        "sentiment":0.83164644241333008,
        "key_phrases":[
            "Margie’s Travel",
            "Margie's Travel",
            "best travel experts",
            "world-leading travel agency",
            "international reach"
            ],
        "locations":[
            "Dubai",
            "Las Vegas",
            "London",
            "New York",
            "San Francisco"
            ],
        "image_tags":[
            "outdoor",
            "tree",
            "plant",
            "palm"
            ]
    }
    ```

The ability to create *object* projections like this enables you to generate enriched data objects that can be incorporated into an enterprise data analysis solution - for example by ingesting the JSON files into an Azure Data Factory pipeline for further processing or loading into a data warehouse.

## View file projections

The *file* projections defined in the skillset create JPEG files for each image that was extracted from the documents during the indexing process.

1. In the storage explorer interface in the Azure portal, select the **margies-images** blob container. This container contains a folder for each document that contained images.
2. Open any of the folders and view its contents - each folder contains at least one \*.jpg file.
3. Open any of the image files to verify that they contain images extracted from the documents.

The ability to generate *file* projections like this makes indexing an efficient way to extract embedded images from a large volume of documents.

## View table projections

The *table* projections defined in the skillset form a relational schema of enriched data.

1. In the storage explorer interface in the Azure portal, expand **TABLES**.
2. Select the **Docs** table to view its columns. The columns include some standard Azure Storage table columns - to hide these, modify the **Column Options** to select only the following columns:
    - **document_id** (the key column automatically generated by the indexing process)
    - **file_id** (the encoded file URL)
    - **file_name** (the file name extracted from the document metadata)
    - **language** (the language in which the document is written)
    - **sentiment** the sentiment score calculated for the document.
    - **url** the URL for the document blob in Azure storage.
3. View the other tables that were created by the indexing process:
    - **ImageTags** (contains a row for each individual image tag with the **document_id** for the document in which the tag appears).
    - **KeyPhrases** (contains a row for each individual key phrase with the **document_id** for the document in which the phrase appears).
    - **Locations** (contains a row for each individual location with the **document_id** for the document in which the location appears).

The ability to create *table* projections enables you to build analytical and reporting solutions that query the relational schema. The automatically generated key columns can be used to join the tables in queries - for example to return all of the locations mentioned in a specific document.

With the enriched document data persisted in the relational tables, you can use tools like Microsoft Power BI to analyze and visualize it, gaining rich new insights:

![A Power BI dashboard based on table projections in a knowledge store.](../media/power-bi.png)

## Clean up resources

Now that you have finished the exercises, you can delete the Azure resources.

1. Right-click (Ctrl+click if using a Mac) the **03-Create-a-knowledge-store** folder and select **Open in Integrated Terminal**. This will open a new bash terminal pane.
2. In the terminal pane, enter the following command to delete the resources used in this module:

    ```bash
    bash reset.sh
    ```
3. When prompted, follow the link, enter the provided code, and sign into your Azure subscription. Then wait for the script to complete and confirm that the resource group has been deleted.

When your resources have been deleted, continue to the next unit to check your learning.
