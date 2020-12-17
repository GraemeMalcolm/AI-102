# Graeme is Working on this

## Create resources for Margie's Travel

The solution you will create for Margie's Travel requires the following resources in your Azure subscription:

- An Azure Storage account with a blob container in which the documents to be searched are stored.
- An Azure Cognitive Search resource, which will manage indexing and querying.
- An Azure Cognitive Services resource, which provides the AI services for skills in your enrichment pipeline

A script containing Azure command-line interface (CLI) commands to create these resources has been provided. Use the following steps to run it.

1. In the **km** project in Visual Studio Code, right-click (Ctrl+click if using a Mac) the **02-Create-an-enrichment-pipeline** folder and select **Open in Integrated Terminal**. This will open a new bash terminal pane.

    > [!TIP]
    > You're going to open multiple terminal sessions during this module, each associated with a folder. They'll all be available in the same **Terminal** pane, and you can switch between them using the drop-down list (which will currently include the *bash* terminal you just opened).

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

6. In a new browser tab, open the Azure portal at [https://portal.azure.com](https://portal.azure.com?azure-portal=true), signing in with the credentials associated with your Azure subscription if prompted.
7. In the Azure portal, find the resource group that was created by the setup script, and verify that it contains the Azure Storage account, Azure Cognitive Services resource, and Azure Cognitive Search resource.

## Create a data source

:::zone pivot="csharp"

Azure Cognitive Search provides a software development kit (SDK) for Microsoft .NET, which you can use to write C# code that works with your search resources.

1. In  Visual Studio Code, expand the **02-Create-an-enrichment-pipeline** folder and the **C-Sharp** folder it contains.
2. Expand the **create-enriched-index** folder and open the **appsettings.json** file. This file contains configuration values for your C# code.
3. Modify the following values in the **appsettings.json** file to reflect your Azure resources, and then save the updated file:
    - **SearchServiceName**: Your Azure Cognitive Search service name (<u>without</u> the .*search&#46;windows&#46;net* suffix)
    - **SearchServiceAdminApiKey**: Your Azure Cognitive Search ***admin*** key
    - **CognitiveServicesApiKey**: Your Azure Cognitive Services key
    - **AzureBlobConnectionString**: Your Azure Storage blob container connection string.

    *Ignore the **AzureFunctionUri** setting for now - you'll update this setting later!*

4. Open the **Program.cs** file, and view the code it contains. The **Main** function:
    - Gets the configuration settings from the **appsettings.json** file.
    - Creates a **SearchServiceClient** object for your Azure Cognitive Search service.
    - Prompts the user for input, calling the appropriate functions to create Azure Cognitive Search components.
5. View the **CreateOrUpdateDataSource** function, which creates a data source named **margies-docs-cs** that references the Azure Storage blob container where the PDF documents are stored.
6. Right-click (Ctrl+click if using a Mac) the **C-Sharp/create-enriched-index** folder and select **Open in Integrated Terminal**. This will open a new bash terminal in this folder.
7. In the terminal for the **create-enriched-index** folder, enter the following command:
    ```bash
    dotnet run
    ```
8. When prompted, press **1** to create a data source. Then wait while the program creates the data source.
9. When the prompt is redisplayed, press **q** to quit the program.
10. Open your search service in the [Azure portal](https://portal.azure.com?portal=true) and view its **Data sources** tab to confirm that the data source has been created.

:::zone-end

:::zone pivot="python"

There is no Python SDK for creating Azure Cognitive Search objects, but you can use Python to submit requests to the Azure Cognitive Search REST API. In the case of a data source, the body of the REST request takes the form of a JSON document defining the data source to be created.

1. In Visual Studio Code, expand the **02-Create-an-enrichment-pipeline** folder and the **Python** folder it contains.
2. Expand the **create-enriched-index** folder and open the **data_source.json** file. This contains the JSON definition for a data source that can be submitted to the Azure Cognitive Search REST interface.
3. Review the JSON code, which defines an Azure blob data source named **margies-docs-py** that references the **margies** container in an Azure Storage account. The connection string for the blob container is null - you will address this in your code later.
4. Open the **submit-rest&#46;py** code file and review the Python code it contains. This code is used to submit REST requests to your Azure Cognitive Search service.
5. Open the **.env** file, which contains environment variables for your Python code.
6. Modify the values in the **.env** file to reflect the Azure Cognitive Search endpoint, Azure Cognitive Search admin key, Azure Cognitive Services key, and Azure Storage blob container connection string for the Azure resources you created previously. Then save the updated file.
7. Right-click (Ctrl+click if using a Mac) the **Python/create-enriched-index** folder and select **Open in Integrated Terminal**. This will open a new bash terminal in this folder.
8. In the terminal for the **create-enriched-index** folder, enter the following command:
    ```bash
    python3 submit-rest.py 'POST' 'datasources' 'data_source.json'
    ```
9. Wait while Python runs the **submit-rest&#46;py** script to create the data store.
10. Review the JSON response that is returned from the REST interface, noting that the data source connection string is null to avoid returning sensitive data.
11. Open your search service in the [Azure portal](https://portal.azure.com?portal=true) and view its **Data sources** tab to confirm that the data source has been created.

:::zone-end

## Create a skillset

:::zone pivot="csharp"

1. In the **C-Sharp/create-enriched-index** folder, open the **Program.cs** file.
2. Review the code in the **CreateSkillset** function. There's a lot of code in this function, which defines a list of skills, and then creates a skillset that includes those skills. The skills defined by the code are:
    - A **language detection** skill that identifies the language in which a document is written (for example **en** for English, or **fr** for French.)
    - An **image analysis** skill that analyzes the images in the document and extracts insights from them. The image analysis skill can be used to return a wide range of information from images, including recognized objects in the image, locations and analysis of faces detected in the image, brand logos in the image, and other insights. In this case, the skill is used to extract a *description* of the image (which as you'll see later, consists of a set of suggested *tags* and a set of suggested *captions* for the image.)
    - An **OCR** skill that uses optical character recognition (OCR) to extract areas of text from the images in the document.
    - A **merge** skill that combines the OCR text extracted from images with the original text content in the document.
    - A **sentiment** skill that calculates a sentiment score for the text in the document. Values close to 0 indicate a negative sentiment, while values close to 1 indicate a positive sentiment.
    - An **entity recognition** skill that identifies and extracts entities in the document contents. In this case, the skill specifically extracts locations and URLs that are mentioned in the documents.
    - A **key phrase extraction** skill that extracts a list of key phrases in each document based on an analysis of the text.
3. Observe that for each skill, the code defines the required input and output parameters, and in some cases some additional configuration parameters to specify the data values to be extracted. Each skill runs in a specified *context*, which defines a location within an enriched document structure. The skills take their inputs from locations within the document, and write their outputs as new document fields within their context. In this way, the outputs from one skill are available within the document as inputs for subsequent skills. For example, the **languageCode** output from the language detection skill is used as an input for the sentiment, entity recognition, and key phrase extraction skills later in the pipeline.
4. Observe that after the list of skills has been created, the code creates a skillset, which includes a reference to your Cognitive Services account. Azure Cognitive Search uses Cognitive Services to implement the skills. The key for your Cognitive Services account will be retrieved from the **appsettings.json** file you updated previously.
5. In the **Terminal** pane, select the bash terminal for the **create-enriched-index** folder. If you have closed this terminal, right-click (Ctrl+click if using a Mac) the **C-Sharp/create-enriched-index** folder and select **Open in Integrated Terminal**.
6. In the terminal for the **create-enriched-index** folder, enter the following command:
    ```bash
    dotnet run
    ```
7. When prompted, press **2** to create a skillset. Then wait while the program creates the skillset.
8. When the prompt is redisplayed, press **q** to quit the program.
9. Open your search service in the [Azure portal](https://portal.azure.com?portal=true) and view its **Skillsets** tab to confirm that the skillset has been created.

:::zone-end

:::zone pivot="python"

1. In the **Python/create-enriched-index** folder, open the **skillset.json** file. This contains the JSON definition of a skillset.
2. Review the skillset definition. It includes the following skills:
    - A **language detection** skill that identifies the language in which a document is written (for example **en** for English, or **fr** for French.)
    - An **image analysis** skill that analyzes the images in the document and extracts insights from them. The image analysis skill can be used to return a wide range of information from images, including recognized objects in the image, locations and analysis of faces detected in the image, brand logos in the image, and other insights. In this case, the skill is used to extract a *description* of the image (which as you'll see later, consists of a set of suggested *tags* and a set of suggested *captions* for the image.)
    - An **OCR** skill that uses optical character recognition (OCR) to extract areas of text from the images in the document.
    - A **merge** skill that combines the OCR text extracted from images with the original text content in the document.
    - A **sentiment** skill that calculates a sentiment score for the text in the document. Values close to 0 indicate a negative sentiment, while values close to 1 indicate a positive sentiment.
    - An **entity recognition** skill that identifies and extracts entities in the document contents. In this case, the skill specifically extracts locations and URLs that are mentioned in the documents.
    - A **key phrase extraction** skill that extracts a list of key phrases in each document based on an analysis of the text.
3. Observe that each skill runs in a specified *context*, which defines a location within an enriched document structure. The skills take their inputs from locations within the document, and write their outputs as new document fields within their context. In this way, the outputs from one skill are available within the document as inputs for subsequent skills. For example, the **languageCode** output from the language detection skill is used as an input for the sentiment, entity recognition, and key phrase extraction skills later in the pipeline.
4. Observe that the skillset also includes a reference to your Cognitive Services account. Azure Cognitive Search uses Cognitive Services to implement the skills. The key for your Cognitive Services account will be inserted into the JSON from the environment variable you defined previously.
5. In the **Terminal** pane, select the bash terminal for the **create-enriched-index** folder. If you have closed this terminal, right-click (Ctrl+click if using a Mac) the **Python/create-enriched-index** folder and select **Open in Integrated Terminal**.
6. In the terminal for the **create-enriched-index** folder, enter the following command:
    ```bash
    python3 submit-rest.py 'PUT' 'skillsets/margies-skillset-py' 'skillset.json'
    ```
7. Wait while Python runs the **submit-rest&#46;py** script to create the skillset.
8. Review the JSON response that is returned from the REST interface.
9. Open your search service in the [Azure portal](https://portal.azure.com?portal=true) and view its **Skillsets** tab to confirm that the skillset has been created.

:::zone-end

> [!NOTE]
> For more information about the full set of available built-in skills, see the [Built-in cognitive skills for text and image processing during indexing (Azure Cognitive Search)](https://docs.microsoft.com/azure/search/cognitive-search-predefined-skills) in the Azure Cognitive Search documentation.

## Create an index for Margie's Travel

The index for the Margie's Travel solution must contain fields that can be used to search for information in brochures and customer reviews. Choose your preferred language at the top of this page, and then follow the steps below to create an index for the Margie's Travel search solution.

:::zone pivot="csharp"

To create an index using C#, you must implement a class that represents the index, including all of its fields.

1. In the **C-Sharp/create-enriched-index** folder, open the **MargiesIndex.cs** code file and view the code it contains. This code defines the following types:
    - **Caption**: A struct containing **text** and **confidence** properties.
    - **ImageDescription**: A struct containing a **captions** property (which is) collection of **Captions**) and a **tags** property, which is a collection of strings.
    - **MargiesIndex**: A class that defines the structure of the index for the search solution, which includes a complex field based on the **ImageDescription** struct. 
2. Review the definition of the **MargiesIndex** class, which includes the following fields:
   - **id**: A unique identifier for each indexed document.
    - **url**: The URL link for the indexed document.
    - **file_name**: The file name of the document.
    - **author**: The author of the document.
    - **size**: The size (in bytes) of the document file.
    - **last_modified**: The date and time the document was last updated.
    - **language**: The language in which the document is written.
    - **sentiment**: A numeric value between 0 and 1 indicating how positive or negative the sentiment of the document is.
    - **key_phrases**: A list of key phrases in the document, which can be useful for identifying its main points.
    - **locations**: A list of geographical locations mentioned in the document.
    - **links**: A list of URLs mentioned in the document.
    - **image_descriptions**: A complex structure containing AI-generated descriptions of images in the document. The description consists of two elements:
        - **tags**: A list of *tag* words that denote some descriptive attribute of the image.
        - **captions**: A list of suggested textual descriptions of the image, each caption consisting of a **text** value and a **confidence** score.
    - **image_captions**: A list of caption text values (*this is the same data as the **image_descriptions/captions/text** value above - we've duplicated it here to demonstrate multiple ways to deal with complex index field values*).
    - **image_text**: A list of text extracted from images in the document.
    - **content**: The original document text merged with text extracted from images in the document.
3. Observe that each field in the index has several *attributes* that control its usage. These attributes include:
    - **key**: Fields that define a unique key for index records.
    - **searchable**: Fields that can be queried using full-text search.
    - **filterable**: Fields that can be included in filter expressions to return only documents that match specified constraints.
    - **sortable**: Fields that can be used to order the results.
    - **facetable**: Fields that can be used to determine values for *facets* (user interface elements used to filter the results based on a list of known field values).
    - **retrievable**: Fields that can be included in search results (*by default, all fields are retrievable, so even though this attribute is omitted in the JSON, all of the index fields will be implicitly retrievable*.).
4. Open the **Program.cs** code file and review the code in the **CreateIndex** function, which creates an index named **margies-index-cs** based on the **MargiesIndex** class.
5. In the **Terminal** pane, select the bash terminal for the **create-enriched-index** folder. If you have closed this terminal, right-click (Ctrl+click if using a Mac) the **C-Sharp/create-enriched-index** folder and select **Open in Integrated Terminal**.
6. In the terminal for the **create-enriched-index** folder, enter the following command:
    ```bash
    dotnet run
    ```
7. When prompted, press **3** to create an index. Then wait while the program creates the index.
8. When the prompt is redisplayed, press **q** to quit the program.
9. Open your search service in the [Azure portal](https://portal.azure.com?portal=true) and view its **Indexes** tab to confirm that the index has been created.

:::zone-end

:::zone pivot="python"

To create an index using Python, you must use the **indexes** REST endpoint. You can submit an HTTP *PUT* request to create or update an index based on a JSON document that defines the index schema.

1. In the **Python/create-enriched-index** folder, open the **index.json** file. This file contains the JSON definition of an index.
2. Review the index definition. It includes the following fields:
    - **id**: A unique identifier for each indexed document.
    - **url**: The URL link for the indexed document.
    - **file_name**: The file name of the document.
    - **author**: The author of the document.
    - **size**: The size (in bytes) of the document file.
    - **last_modified**: The date and time the document was last updated.
    - **language**: The language in which the document is written.
    - **sentiment**: A numeric value between 0 and 1 indicating how positive or negative the sentiment of the document is.
    - **key_phrases**: A list of key phrases in the document, which can be useful for identifying its main points.
    - **locations**: A list of geographical locations mentioned in the document.
    - **links**: A list of URLs mentioned in the document.
    - **image_descriptions**: A complex structure containing AI-generated descriptions of images in the document. The description consists of two elements:
        - **tags**: A list of *tag* words that denote some descriptive attribute of the image.
        - **captions**: A list of suggested textual descriptions of the image, each caption consisting of a **text** value and a **confidence** score.
    - **image_captions**: A list of caption text values (*this is the same data as the **image_descriptions/captions/text** value above - we've duplicated it here to demonstrate multiple ways to deal with complex index field values*).
    - **image_text**: A list of text extracted from images in the document.
    - **content**: The original document text merged with text extracted from images in the document.
3. Observe that each field in the index has several *attributes* that control its usage. These attributes include:
    - **key**: Fields that define a unique key for index records.
    - **searchable**: Fields that can be queried using full-text search.
    - **filterable**: Fields that can be included in filter expressions to return only documents that match specified constraints.
    - **sortable**: Fields that can be used to order the results.
    - **facetable**: Fields that can be used to determine values for *facets* (user interface elements used to filter the results based on a list of known field values).
    - **retrievable**: Fields that can be included in search results (*by default, all fields are retrievable, so even though this attribute is omitted in the JSON, all of the index fields will be implicitly retrievable*.)
4. In the **Terminal** pane, select the bash terminal for the **create-enriched-index** folder. If you have closed this terminal, right-click (Ctrl+click if using a Mac) the **Python/create-enriched-index** folder and select **Open in Integrated Terminal**.
5. In the terminal for the **create-enriched-index** folder, enter the following command:
    ```bash
    python3 submit-rest.py 'PUT' 'indexes/margies-index-py' 'index.json'
    ```
6. Wait while Python runs the **submit-rest&#46;py** script, causing it to submit an HTTP PUT request to the *indexes* REST endpoint, adding an index named *margies-index-py* based on the JSON body defined in the *index.json* file. The use of a PUT request ensures that if the index already exists, it is updated based on the JSON; otherwise it is created.
7. Review the JSON response that is returned from the REST interface.
8. Open your search service in the [Azure portal](https://portal.azure.com?portal=true) and view its **Indexes** tab to confirm that the index has been created.

:::zone-end

## Create and run an indexer for Margie's Travel

Select your preferred language at the top of this page, and then follow the steps below to create and run an indexer for the Margie's Travel search solution.

:::zone pivot="csharp"

To create an indexer, you can use the **Create** method of the **SearchServiceClient**'s **Indexers** member. When you initially create an indexer, it runs to populate the index. To check the status of an indexer, you use the **GetStatus** method of the **SearchServiceClient**'s **Indexers** member.

1. In the **C-Sharp/create-enriched-index** folder, open the **Program.cs** file and review the code in the **CreateIndexer** function, observing that:
    - The indexer configuration includes an **imageAction** setting with the value **generateNormalizedImages** - this causes the indexer to extract images from the source data and put the extracted image data in a **normalized_images** collection field in the **document**.
    - The **fieldMappings** list maps file metadata extracted directly from the data source to index fields. This represents the initial state of the document that will be processed by the pipeline.
    - The **outputMappings** list maps the enriched data values generated by the skillset to index fields after the pipeline has finished.
    - The **imageDescription** output from the image analysis skill is mapped to the **image_descriptions** index field. Recall that this field is a complex object consisting of a collection of tags and a collection of captions for each image in the document.
    - The **text** values for the captions in the description are mapped directly to the **image_captions** index field. This demonstrates that you can choose to map an entire complex object generated by a skill to a field, or map subelements of the object to individual fields.
    - The **mergedText** value, which combines the original text content and the text extracted from images, is mapped to the **content** image field.
2. Review the code in the **CheckIndexerOverallStatus** function, which retrieves the indexer status.
3. In the **Terminal** pane, select the bash terminal for the **create-enriched-index** folder. If you have closed this terminal, right-click (Ctrl+click if using a Mac) the **C-Sharp/create-enriched-index** folder and select **Open in Integrated Terminal**.
4. In the terminal for the **create-enriched-index** folder, enter the following command:
    ```bash
    dotnet run
    ```
5. When prompted, press **4** to create and run an indexer. Then wait while the program creates the indexer and then retrieves it status.
6. When the prompt is redisplayed, press **q** to quit the program.
7. Open your search service in the [Azure portal](https://portal.azure.com?portal=true) and view its **Indexers** tab to confirm that the indexer has been created and has processed 72 documents.

    > [!NOTE]
    > There may be some warnings indicating that some documents were too large for the sentiment skill to analyze fully, and only the first 1000 characters of these documents were processed. You can ignore these warnings.

:::zone-end

:::zone pivot="python"

To create an indexer with Python, you need to submit a request to the **indexers** REST endpoint with the name of the indexer. The body of the request must be a JSON document that defines the indexer.

1. In the **Python/create-enriched-index** folder, open the **indexer.json** file. This file contains the JSON definition of an indexer.
2. Review the indexer definition and observe the following:
    - The indexer maps fields from the **margies-docs-py** data source to the **margies-index-py** index, and uses the **margies-skillset-py** skillset to generate enriched fields.
    - The **parameters** configuration includes an imageAction setting with the value **generateNormalizedImages** - this causes the indexer to extract images from the source data and put the extracted image data in a **normalized_images** collection field in the **document**.
    - The **fieldMappings** list maps file metadata extracted directly from the data source to index fields. This represents the initial state of the document that will be processed by the pipeline.
    - The **outputMappings** list maps the enriched data values generated by the skillset to index fields after the pipeline has finished.
    - The **imageDescription** output from the image analysis skill is mapped to the **image_description** index field. Recall that this field is a complex object consisting of a collection of tags and a collection of captions.
    - The **text** values for the captions in the description are mapped directly to the **image_caption** index field. This demonstrates that you can choose to map an entire complex object generated by a skill to a field, or map subelements of the object to individual fields.
    - The **mergedText** value, which combines the original text content and the text extracted from images, is mapped to the **content** image field.
3. In the **Terminal** pane, select the bash terminal for the **Python/create-enriched-index** folder. If you have closed this terminal, right-click (CTRL+click if using a Mac) the **create-enriched-index** folder and select **Open in Integrated Terminal**.
4. In the terminal for the **create-enriched-index** folder, enter the following command:
    ```bash
    python3 submit-rest.py 'PUT' 'indexers/margies-indexer-py' 'indexer.json'
    ```
5. Wait while Python runs the **submit-rest&#46;py** script, causing it to submit an HTTP PUT request to the *indexers* REST endpoint, adding an indexer named *margies-indexer-py* based on the JSON body defined in the *indexer.json* file. The use of a PUT request ensures that if the indexer already exists, it is updated based on the JSON; otherwise it is created.
6. Review the JSON response that is returned from the REST interface. The indexer is created and automatically run to initialize the index.
7. In the terminal for the **create-enriched-index** folder, enter the following command:
    ```bash
    python3 submit-rest.py 'GET' 'indexers/margies-indexer-py/status' 'null'
    ```
8. Review the JSON response that is returned from the REST interface, which shows the status of the indexer. In particular, check the **status** value in the **lastResult** section of the response. If this is shown as **inProgress**, the indexer is still being applied to the index. You can rerun the previous command to retrieve the status until the last result status is **success**.
9. Open your search service in the [Azure portal](https://portal.azure.com?portal=true) and view its **Indexers** tab to confirm that the indexer has been created and has processed 72 documents.

    > [!NOTE]
    > There may be some warnings indicating that some documents were too large for the sentiment skill to analyze fully, and only the first 1000 characters of these documents were processed. You can ignore these warnings.

:::zone-end

## Search the Margie's Travel index

To search the Margie's Travel index, you will use a web application that includes a form in which users can submit search expressions. Select your preferred language at the top of this page, and then follow the steps below to query the Margie's Travel search solution.

:::zone pivot="csharp"

1. In the **02-Create-an-enrichment-pipeline/Python/C-Sharp** folder, expand the **enriched-search-client** folder. This folder contains a simple ASP&#46;NET Core web application for the Margie's Travel web site.
2. Open the **appsettings.json** file. This file contains configuration values for the web application.
3. Modify the values in the **appsettings.json** file to reflect the service name (<u>without</u> the .*search&#46;windows&#46;net* suffix) and query key for your Azure Cognitive Search service (be sure to specify the *query* key, and not the *admin* key!). Then save the updated file.
4. In the **Pages** folder for the web application, open the **Index.cshtml** code file. This file defines the main page of the web application. The page contains a form in which users can submit search terms, and code to render the search results.
5. Open the **Index.cshtml.cs** code file, which contains C# code to support the web page. Review the **OnGet** function, which is called when the page is requested. It extracts parameters passed in the request, and then uses a **SearchServiceClient** object to submit a query to Azure Cognitive Search. The query includes the following parameters:
    - **Select**: The index fields to be included in the query results.
    - **SearchMode**: This value determines how the search query is applied. A value of **All** means that all of the specified search terms must be present for the document to be included in the results. A value of **Any** means that only one or more of the terms must be present.
    - **HighlightFields**: Fields that can be used to display a snippet of the document data with the search term highlighted. In this case, the results include extracts from the **content** field with up to three instances of the search term shown in context.
    - **Facets**: Fields that can be used to provide filters in the user interface, enabling users to "drill-down" into the results. In this case, the **author** field is specified, so the results can include navigation elements that enable users to further refine the query by selecting individual author values.
6. In the **Models** folder, open the **SearchResults.cs** code file. This defines a class for the search results - the query returns a list of these objects.
7. Right-click (Ctrl+click if using a Mac) the **C-Sharp/enriched-search-client** folder and select **Open in Integrated Terminal** to open a new bash terminal in this folder.
8. In the terminal for the **enriched-search-client** folder, enter the following command:
    ```bash
    dotnet run
    ```
9. When the following message is displayed, follow the `https://localhost:5000/` link to open the web application in a new browser tab:
    ```text
    info: Microsoft.Hosting.Lifetime[0]
    Now listening on: http://localhost:5000
    info: Microsoft.Hosting.Lifetime[0]
    Application started. Press Ctrl+C to shut down.
    info: Microsoft.Hosting.Lifetime[0]
    Hosting environment: Development
    info: Microsoft.Hosting.Lifetime[0]
    Content root path: /root/workspace/km/01-Create-a-search-solution/C-Sharp/search-client
   ```
10. Wait for the web site to open (the web site is being run in the development container, and port forwarding is used to make it available as a locally hosted site in your browser session - you may need to allow access through your firewall).
11. In the Margie's Travel website, enter **"Statue of Liberty"** (including the quotation marks to search for the whole phrase) into the search box and click **Search**.
12. Review the search results. They include the file name (with a hyperlink to the file URL), author, size, last modified date, and an extract of the file content with the search term (*Statue of Liberty*) emphasized.
13. Examine the extract of the file content with *Statue of Liberty* emphasized, and observe that the term was found as text in images and in the AI-generated caption of one of the images.
14. Try another search by entering the search term **skyscraper** in the search box at the top of the page and clicking **Search**.
15. Examine the results, observing that the term *skyscraper* is not used anywhere in the document contents, but is one of the suggested image tags for each of the results.
16. Try another search by entering the search term **"Tower of London"** (including the quotation marks) in the search box at the top of the page and clicking **Search**.
17. Examine the results, observing that the term *Tower of London* not only appears in the resulting documents, but is also identified as a key phrase and a location.
18. Try another search by entering the search term **quiet hotel in London** in the search box at the top of the page and clicking **Search**.
19. When the results are returned, change the **Sort by** option to **Positive to negative** and refine the results to list them in descending order of sentiment.
20. Close the browser tab containing the Margie's Travel web site and return to Visual Studio Code. Then in the terminal for the **enriched-search-client** folder (where the dotnet process is running), enter Ctrl+C to stop the app.

:::zone-end

:::zone pivot="python"

1. In the **02-Create-an-enrichment-pipeline/Python** folder, expand the **enriched-search-client** folder. This folder contains a simple Flask-based web application for the Margie's Travel web site.
2. Open the **.env** file. This file contains environment variables for the web application.
3. Modify the values in the **.env** file to reflect the endpoint and query key for your Azure Cognitive Search resources (be sure to specify the *query* key, and not the *admin* key!). Then save the updated file.
4. Open the **app&#46;py** code file. This contains the code for the Flask web application. The code:
    - Loads the required Azure Cognitive Search credentials from environment variables.
    - Defines a function named **azsearch_query** that submits a query as a REST request to an Azure Cognitive Search endpoint.
    - Defines a route for the web site's home page (*/*) that displays a web page based on the **default.html** template. This template includes a basic search form.
    - Defines a route for the search results page (*/search*) that retrieves the query text from the search form, constructs parameters for the REST request, submits the query, and renders the results in the **search.html** template.
    - Defines a route for a more advanced search page (*/filter*) that includes filtering and sorting.
5. Right-click (Ctrl+click if using a Mac) the **Python/enriched-search-client** folder and select **Open in Integrated Terminal** to open a new bash terminal in this folder.
6. In the terminal for the **enriched-search-client** folder, enter the following command:
    ```bash
    flask run
    ```
7. When the following message is displayed, follow the `https://127.0.0.1:5000/` link to open the web application in a new browser tab:
    ```text
    * Environment: production
      WARNING: This is a development server. Do not use it in a production deployment.
      Use a production WSGI server instead.
   * Debug mode: off
   * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
   ```
8. Wait for the web site to open (the web site is being run in the development container, and port forwarding is used to make it available as a locally hosted site in your browser session - you may need to allow access through your firewall)
9. In the Margie's Travel website, enter **"Statue of Liberty"** (including the quotation marks to search for the whole phrase) into the search box and click **Search**.
10. Review the search results. They include the file name (with a hyperlink to the file URL), author, size, last modified date, and an extract of the file content with the search term (*Statue of Liberty*) emphasized.
11. Examine the extract of the file content with *Statue of Liberty* emphasized, and observe that the term was found as text in images and in the AI-generated caption of one of the images.
12. Try another search by entering the search term **skyscraper** in the search box at the top of the page and clicking **Search**.
13. Examine the results, observing that the term *skyscraper* is not used anywhere in the document contents, but is one of the suggested image tags for each of the results.
14. Try another search by entering the search term **"Tower of London"** (including the quotation marks) in the search box at the top of the page and clicking **Search**.
15. Examine the results, observing that the term *Tower of London* not only appears in the resulting documents, but is also identified as a key phrase and a location.
16. Try another search by entering the search term **quiet hotel in London** in the search box at the top of the page and clicking **Search**.
17. When the results are returned, change the **Sort by** option to **Positive to negative** and refine the results to list them in descending order of sentiment.
18. Close the browser tab containing the Margie's Travel web site and return to Visual Studio Code. Then in the Python terminal for the **enriched-search-client** folder (where the flask application is running), enter CTRL+C to stop the app.

:::zone-end

## Create an Azure Function

To implement your custom skill, you'll create an Azure Function in your preferred language.

:::zone pivot="csharp"

1. In Visual Studio Code, view the Azure Extensions tab (**&boxplus;**), and verify that the **Azure Functions** extension is installed. This extension enables you to create and deploy Azure Functions from Visual Studio Code.
2. On Azure tab (**&Delta;**), in the **Azure Functions** pane, create new Azure Function project (&#128194;) with the following settings:
    - **Folder**: Browse to the **02-Create an enrichment pipeline/C-Sharp/custom-skill** folder
    - **Language**: C#
    - **Template**: HTTP trigger
    - **Function name**: wordcount
    - **Namespace**: margies.search
    - **Authorization level**: Function

    *If you are prompted to overwrite **launch.json**, do so!*

3. Switch back to the **Explorer** (**&#128461;**) tab and verify that the **02-Create an enrichment pipeline/C-Sharp/custom-skill** folder now contains the code files for your Azure Function.
4. Open the **wordcount.cs** file if it is not already open, and replace its entire contents with the following code:

    ```C#
    using System.IO;
    using Microsoft.AspNetCore.Mvc;
    using Microsoft.Azure.WebJobs;
    using Microsoft.Azure.WebJobs.Extensions.Http;
    using Microsoft.AspNetCore.Http;
    using Newtonsoft.Json;
    using System.Collections.Generic;
    using Microsoft.Extensions.Logging;
    using System.Text.RegularExpressions;
    using System.Linq;

    namespace margies.search
    {
        public static class wordcount
        {

            //define classes for responses
            private class WebApiResponseError
            {
                public string message { get; set; }
            }

            private class WebApiResponseWarning
            {
                public string message { get; set; }
            }

            private class WebApiResponseRecord
            {
                public string recordId { get; set; }
                public Dictionary<string, object> data { get; set; }
                public List<WebApiResponseError> errors { get; set; }
                public List<WebApiResponseWarning> warnings { get; set; }
            }

            private class WebApiEnricherResponse
            {
                public List<WebApiResponseRecord> values { get; set; }
            }

            //function for custom skill
            [FunctionName("wordcount")]
            public static IActionResult Run(
                [HttpTrigger(AuthorizationLevel.Function, "post", Route = null)]HttpRequest req, ILogger log)
            {
                log.LogInformation("Function initiated.");

                string recordId = null;
                string originalText = null;

                string requestBody = new StreamReader(req.Body).ReadToEnd();
                dynamic data = JsonConvert.DeserializeObject(requestBody);

                // Validation
                if (data?.values == null)
                {
                    return new BadRequestObjectResult(" Could not find values array");
                }
                if (data?.values.HasValues == false || data?.values.First.HasValues == false)
                {
                    return new BadRequestObjectResult("Could not find valid records in values array");
                }

                WebApiEnricherResponse response = new WebApiEnricherResponse();
                response.values = new List<WebApiResponseRecord>();
                foreach (var record in data?.values)
                {
                    recordId = record.recordId?.Value as string;
                    originalText = record.data?.text?.Value as string;

                    if (recordId == null)
                    {
                        return new BadRequestObjectResult("recordId cannot be null");
                    }

                    // Put together response.
                    WebApiResponseRecord responseRecord = new WebApiResponseRecord();
                    responseRecord.data = new Dictionary<string, object>();
                    responseRecord.recordId = recordId;
                    responseRecord.data.Add("text", Count(originalText));

                    response.values.Add(responseRecord);
                }

                return (ActionResult)new OkObjectResult(response); 
            }


                public static string RemoveHtmlTags(string html)
            {
                string htmlRemoved = Regex.Replace(html, @"<script[^>]*>[\s\S]*?</script>|<[^>]+>| ", " ").Trim();
                string normalised = Regex.Replace(htmlRemoved, @"\s{2,}", " ");
                return normalised;
            }

            public static List<string> Count(string text)
            {
                
                //remove html elements
                text=text.ToLowerInvariant();
                string html = RemoveHtmlTags(text);
                
                //split into list of words
                List<string> list = html.Split(" ").ToList();
                
                //remove any non alphabet characters
                var onlyAlphabetRegEx = new Regex(@"^[A-z]+$");
                list = list.Where(f => onlyAlphabetRegEx.IsMatch(f)).ToList();

                //remove stop words
                string[] stopwords = { "", "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", 
                        "you're", "you've", "you'll", "you'd", "your", "yours", "yourself", 
                        "yourselves", "he", "him", "his", "himself", "she", "she's", "her", 
                        "hers", "herself", "it", "it's", "its", "itself", "they", "them", 
                        "their", "theirs", "themselves", "what", "which", "who", "whom", 
                        "this", "that", "that'll", "these", "those", "am", "is", "are", "was",
                        "were", "be", "been", "being", "have", "has", "had", "having", "do", 
                        "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", 
                        "because", "as", "until", "while", "of", "at", "by", "for", "with", 
                        "about", "against", "between", "into", "through", "during", "before", 
                        "after", "above", "below", "to", "from", "up", "down", "in", "out", 
                        "on", "off", "over", "under", "again", "further", "then", "once", "here", 
                        "there", "when", "where", "why", "how", "all", "any", "both", "each", 
                        "few", "more", "most", "other", "some", "such", "no", "nor", "not", 
                        "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", 
                        "will", "just", "don", "don't", "should", "should've", "now", "d", "ll",
                        "m", "o", "re", "ve", "y", "ain", "aren", "aren't", "couldn", "couldn't", 
                        "didn", "didn't", "doesn", "doesn't", "hadn", "hadn't", "hasn", "hasn't", 
                        "haven", "haven't", "isn", "isn't", "ma", "mightn", "mightn't", "mustn", 
                        "mustn't", "needn", "needn't", "shan", "shan't", "shouldn", "shouldn't", "wasn", 
                        "wasn't", "weren", "weren't", "won", "won't", "wouldn", "wouldn't"}; 
                list = list.Where(x => x.Length > 2).Where(x => !stopwords.Contains(x)).ToList();
                
                //get distict words by key and count, and then order by count.
                var keywords = list.GroupBy(x => x).OrderByDescending(x => x.Count());
                var klist = keywords.ToList();

                // return the top 10 words
                var numofWords = 10;
                if(klist.Count<10)
                    numofWords=klist.Count;
                List<string> resList = new List<string>();
                for (int i = 0; i < numofWords; i++)
                {
                    resList.Add(klist[i].Key);
                }
                return resList;
            }
        }
    }
    ```

5. Right-click (Ctrl+click on a Mac) the **custom-skill** folder and select **Deploy to Function App**. Then deploy the function with the following settings:
    - **Subscription** (if prompted): Select your Azure subscription.
    - **Function**: Create a new Function App in Azure (Advanced)
    - **Function App Name**: Enter a globally unique name.
    - **Runtime**: .NET Core 3.1
    - **OS**: Linux
    - **Hosting plane**: Consumption
    - **Resource group**: Select the existing resource group containing your Cognitive Search, Storage, and Cognitive Services resources (its name will be similar to *rg1234abcd5678efgh*).
    - **Storage account**: Select your existing storage account (its name will be similar to *store1234abcd5678efgh*).
    - **Application Insights**: Skip for now

    *Visual Studio Code will deploy the compiled version of the function (in the **bin** subfolder) based on the configuration settings in the **.vscode** folder that were saved when you created the function project.*

6. Wait for your function app to be created. You can view the **Output Window** to monitor its status.
7. Open the [Azure portal](https://portal.azure.com), and browse to the resource group where you created the function app. Then open the app service for your function app.
8. In the blade for your app service, on the **Functions** page, open the **wordcount** function.
9. On the **wordcount** function blade, view the **Code + Test** page and open the **Test/Run** pane.
10. In the **Test/Run** pane, replace the existing **Body** with the following JSON, which reflects the schema expected by an Azure Cognitive Search skill in which records containing data for one or more documents are submitted for processing:

    ```json
    {
        "values": [
            {
                "recordId": "a1",
                "data":
                {
                "text":  "Tiger, tiger burning bright in the darkness of the night.",
                "language": "en"
                }
            },
            {
                "recordId": "a2",
                "data":
                {
                "text":  "The rain in spain stays mainly in the plains! That's where you'll find the rain!",
                "language": "en"
                }
            }
        ]
    }
    ```

11. Click **Run** and view the HTTP response content that is returned by your function. This reflects the schema expected by Azure Cognitive Search when consuming a skill, in which a response for each document is returned. In this case, the response consists of up to 10 terms in each document in descending order of how frequently they appear:

    ```text
    {
    "values": [
        {
        "recordId": "a1",
        "data": {
            "text": [
            "tiger",
            "burning",
            "bright",
            "darkness",
            "night"
            ]
        },
        "errors": null,
        "warnings": null
        },
        {
        "recordId": "a2",
        "data": {
            "text": [
            "rain",
            "spain",
            "stays",
            "mainly",
            "plains",
            "thats",
            "youll",
            "find"
            ]
        },
        "errors": null,
        "warnings": null
        }
    ]
    }
    ```
12. Close the **Test/Run** pane and in the **wordcount** function blade, click **Get function URL**. Then copy the URL for the default key to the clipboard. You'll need this in the next unit.

:::zone-end

:::zone pivot="python"

1. In Visual Studio Code, view the Azure Extensions tab (**&boxplus;**), and verify that the **Azure Functions** extension is installed. This extension enables you to create and deploy Azure Functions from Visual Studio Code.
2. On Azure tab (**&Delta;**), in the **Azure Functions** pane, create new Azure Function project (&#128194;) with the following settings:
    - **Folder**: Browse to the **02-Create an enrichment pipeline/Python/custom-skill** folder
    - **Language**: Python
    - **Virtual environment**: Skip virtual environment
    - **Template**: HTTP trigger
    - **Function name**: wordcount
    - **Authorization level**: Function

    *If you are prompted to overwrite **launch.json**, do so!*

3. Switch back to the **Explorer** (**&#128461;**) tab and verify that the **02-Create an enrichment pipeline/Python/custom-skill** folder now contains the code files for your Azure Function.
4. Open the **\_\_init\_\_&#46;py** file if it is not already open, and replace its entire contents with the following code:

    ```Python
    import logging
    import os
    import sys
    import json
    from string import punctuation
    from collections import Counter
    import azure.functions as func


    def main(req: func.HttpRequest) -> func.HttpResponse:
        logging.info('Wordcount function initiated.')

        # The result will be a "values" bag
        result = {
            "values": []
        }
        statuscode = 200

        # We're going to exclude words from this list in the word counts
        stopwords = ['', 'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 
                    "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 
                    'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 
                    'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 
                    'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 
                    'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was',
                    'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 
                    'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 
                    'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 
                    'about', 'against', 'between', 'into', 'through', 'during', 'before', 
                    'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 
                    'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 
                    'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 
                    'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 
                    'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 
                    'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll',
                    'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 
                    'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 
                    'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', 
                    "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', 
                    "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

        try:
            values = req.get_json().get('values')
            logging.info(values)

            for rec in values:
                # Construct the basic JSON response for this record
                val = {
                        "recordId": rec['recordId'],
                        "data": {
                            "text":None
                        },
                        "errors": None,
                        "warnings": None
                    }
                try:
                    # get the text to be processed from the input record
                    txt = rec['data']['text']
                    # remove numeric digits
                    txt = ''.join(c for c in txt if not c.isdigit())
                    # remove punctuation and make lower case
                    txt = ''.join(c for c in txt if c not in punctuation).lower()
                    # remove stopwords
                    txt = ' '.join(w for w in txt.split() if w not in stopwords)
                    # Count the words and get the most common 10
                    wordcount = Counter(txt.split()).most_common(10)
                    words = [w[0] for w in wordcount]
                    # Add the top 10 words to the output for this text record
                    val["data"]["text"] = words
                except:
                    # An error occured for this text record, so add lists of errors and warning
                    val["errors"] =[{"message": "An error occurred processing the text."}]
                    val["warnings"] = [{"message": "One or more inputs failed to process."}]
                finally:
                    # Add the value for this record to the response
                    result["values"].append(val)
        except Exception as ex:
            statuscode = 500
            # A global error occurred, so return an error response
            val = {
                    "recordId": None,
                    "data": {
                        "text":None
                    },
                    "errors": [{"message": ex.args}],
                    "warnings": [{"message": "The request failed to process."}]
                }
            result["values"].append(val)
        finally:
            # Return the response
            return func.HttpResponse(body=json.dumps(result), mimetype="application/json", status_code=statuscode)
    ```

5. After the page has refreshed, right-click (Ctrl+click on a Mac) the **custom-skill** folder and select **Deploy to Function App**. Then deploy the function with the following settings:
    - **Subscription** (if prompted): Select your Azure subscription.
    - **Function**: Create a new Function App in Azure (Advanced)
    - **Function App Name**: Enter a globally unique name.
    - **Runtime**: Python 3.7
    - **Hosting plane**: Consumption
    - **Resource group**: Select the existing resource group containing your Cognitive Search, Storage, and Cognitive Services resources (its name will be similar to *rg1234abcd5678efgh*).
    - **Storage account**: Select your existing storage account (its name will be similar to *store1234abcd5678efgh*).
    - **Application Insights**: Skip for now
6. Wait for your function app to be created. You can view the **Output Window** to monitor its status.
7. Open the [Azure portal](https://portal.azure.com), and browse to the resource group where you created the function app. Then open the app service for your function app.
8. In the blade for your app service, on the **Functions** page, open the **wordcount** function.
9. On the **wordcount** function blade, view the **Code + Test** page and open the **Test/Run** pane.
10. In the **Test/Run** pane, replace the existing **Body** with the following JSON, which reflects the schema expected by an Azure Cognitive Search skill in which records containing data for one or more documents are submitted for processing:

    ```json
    {
        "values": [
            {
                "recordId": "a1",
                "data":
                {
                "text":  "Tiger, tiger burning bright in the darkness of the night.",
                "language": "en"
                }
            },
            {
                "recordId": "a2",
                "data":
                {
                "text":  "The rain in spain stays mainly in the plains! That's where you'll find the rain!",
                "language": "en"
                }
            }
        ]
    }
    ```

11. Click **Run** and view the HTTP response content that is returned by your function. This reflects the schema expected by Azure Cognitive Search when consuming a skill, in which a response for each document is returned. In this case, the response consists of up to 10 terms in each document in descending order of how frequently they appear:

    ```text
    {
    "values": [
        {
        "recordId": "a1",
        "data": {
            "text": [
            "tiger",
            "burning",
            "bright",
            "darkness",
            "night"
            ]
        },
        "errors": null,
        "warnings": null
        },
        {
        "recordId": "a2",
        "data": {
            "text": [
            "rain",
            "spain",
            "stays",
            "mainly",
            "plains",
            "thats",
            "youll",
            "find"
            ]
        },
        "errors": null,
        "warnings": null
        }
    ]
    }
    ```
12. Close the **Test/Run** pane and in the **wordcount** function blade, click **Get function URL**. Then copy the URL for the default key to the clipboard. You'll need this in the next unit.

:::zone-end

> [!NOTE]
> To learn more about implementing custom skills for an Azure Cognitive Search enrichment pipeline, see [How to add a custom skill to an Azure Cognitive Search enrichment pipeline](https://docs.microsoft.com/azure/search/cognitive-search-custom-skill-interface) in the Azure Cognitive Search documentation.

:::zone pivot="csharp"

## Add the function URL to the app configuration

The URL for your function is how the skillset will connect to it, so you need to add it to your app configuration.

1. In the **C-Sharp/create-enriched-index** folder, open the **appsettings.json** file, which contains the configuration settings for your app.
2. Update the **AzureFunctionUri** setting with the URL for your Azure function (which you copied to the clipboard in the previous procedure), replacing ***YOUR-FUNCTION-APP-URL***.

## Modify the skillset definition

Now you need to add your custom skill to the skillset.

1. In the **C-Sharp/create-enriched-index** folder, open **Program.cs** and review the **CreateCustomSkill** function. This function creates a **WebApiSkill** that includes a **uri** property referencing your Azure function.
2. In the **CreateSkillset** function, after all of the built-in skills have been defined, find the comment `//Uncomment below to add custom skill` and uncomment the code beneath it to add the custom skill to the list of skills for the skillset:

    ```C#
    skills.Add(CreateCustomSkill());
    ```

## Modify the index definition

The custom skill returns a list of the top 10 words found in each document, which you can add as a field in your index.

1. In the **C-Sharp/create-enriched-index** folder, open **MargiesIndex.cs** and review the **MargiesIndex** class definition.
2. At the bottom of the class definition, find the comment `// Uncomment below to add custom skill field`, and uncomment the two lines beneath it to define a searchable and filterable field named **top_words**:

    ```C#
    [IsSearchable, IsFilterable]
    public string[] top_words { get; set; }
    ```

## Modify the indexer definition

Now that you've defined a skill to extract the list of top 10 words, and a corresponding field in the index, you must modify the indexer to map the skill output to the index field.

1. In the **C-Sharp/create-enriched-index** folder, open **Program.cs** and review the **CreateIndexer** function.
2. At the bottom of the function, find the comment `// Uncomment below to add custom skill field`, and uncomment the code beneath it to map the custom skill output to the **top_words** index field:

    ```C#
    outputMappings.Add(new FieldMapping(
        sourceFieldName: "/document/topWords",
        targetFieldName: "top_words"
    ));
    ```
3. Review the **ResetIndexer** function. which resets and reruns the indexer. After you update the existing indexer, you'll need to explicitly reset and rerun it to repopulate the index.

## Run the code

Now you're ready to run the modified code and update the index with the output from your custom skill.

1. In the **Terminal** pane, select the bash terminal for the **create-enriched-index** folder. If you have closed this terminal, right-click (Ctrl+click if using a Mac) the **C-Sharp/create-enriched-index** folder and select **Open in Integrated Terminal**.
2. In the terminal for the **create-enriched-index** folder, enter the following command:
    ```bash
    dotnet run
    ```
3. When prompted, press **2** to recreate the skillset.
4. When the prompt is redisplayed, press **3** to recreate the index.
5. When the prompt is redisplayed, press **4** to recreate the indexer.
6. When the prompt is redisplayed, press **5** to reset and rerun the index.
7. When the prompt is redisplayed, press **q** to quit the program.
8. Open your search service in the [Azure portal](https://portal.azure.com?portal=true) and view its **Indexers** tab to confirm that the indexer has run successfully (if it is still in-progress, wait for it to complete - it may initially fail and then rerun).

:::zone-end

:::zone pivot="python"

## Update the skillset and index

First, you need to update the skillset and index to reflect the enriched field you want to add.

1. In the **Python/create-enriched-index** folder, open the **updated_skillset.json** file. This contains the JSON definition of a skillset.
2. Review the skillset definition. It includes the same skills as before, as well as a new **WebApiSkill** skill named **get-top-words**.
3. Edit the **get-top-words** skill definition to set the **uri** value to the URL for your Azure function (which you copied to the clipboard in the previous procedure), replacing ***YOUR-FUNCTION-APP-URL***.
4. In the **Terminal** pane, select the bash terminal for the **create-enriched-index** folder. If you have closed this terminal, right-click (Ctrl+click if using a Mac) the **Python/create-enriched-index** folder and select **Open in Terminal**.
5. In the terminal for the **create-enriched-index** folder, enter the following command:
    ```bash
    python3 submit-rest.py 'PUT' 'skillsets/margies-skillset-py' 'updated_skillset.json'
    ```
6. Wait while Python runs the **submit-rest&#46;py** script to update your skillset.
7. In the **create-enriched-index** folder, open the **updated_index.json** file. This contains the JSON definition of an index.
8. Review the index definition. It includes the same fields as before, as well as a new field named **top_words**, which consists of a list of string values.
9. In the **Terminal** pane, select the bash terminal for the **create-enriched-index** folder. If you have closed this terminal, right-click (CTRL+click if using a Mac) the **create-enriched-index** folder and select **Open in Terminal**.
10. In the terminal for the **create-enriched-index** folder, enter the following command:
    ```bash
    python3 submit-rest.py 'PUT' 'indexes/margies-index-py' 'updated_index.json'
    ```
11. Wait while Python runs the **submit-rest&#46;py** script to update your index.

## Update and rerun the indexer

To map the data extracted by your custom skill to the corresponding field in the index, you need to modify and rerun the indexer.

1. In the **create-enriched-index** folder, open the **updated_indexer.json** file. This contains the JSON definition of an indexer.
2. Review the indexer definition, noting that it includes a mapping between the **/document/topWords** value extracted by your custom skill and the **top_words** field in the index.
3. In the **Terminal** pane, select the bash terminal for the **create-enriched-index** folder. If you have closed this terminal, right-click (Ctrl+click if using a Mac) the **create-enriched-index** folder and select **Open in Terminal**.
4. In the terminal for the **create-enriched-index** folder, enter the following command:
    ```bash
    python3 submit-rest.py 'PUT' 'indexers/margies-indexer-py' 'updated_indexer.json'
    ```
5. Wait while Python runs the **submit-rest&#46;py** script to update the indexer definition.
6. In the terminal for the **create-enriched--index** folder, enter the following command to reset the indexer (so that all documents will be reindexed the next time it runs):
    ```bash
    python3 submit-rest.py 'POST' 'indexers/margies-indexer-py/reset' 'null'
    ```
7. In the terminal for the **create-enriched--index** folder, enter the following command to run the indexer:
    ```bash
    python3 submit-rest.py 'POST' 'indexers/margies-indexer-py/run' 'null'
    ```
8. In the terminal for the **create-enriched--index** folder, enter the following command:
    ```bash
    python3 submit-rest.py 'GET' 'indexers/margies-indexer-py/status' 'null'
    ```
9. Review the JSON response that is returned from the REST interface, which shows the status of the indexer. In particular, check the **status** value in the **lastResult** section of the response. If this is shown as **inProgress**, the indexer is still being applied to the index. You can rerun the previous command to retrieve the status until the last result status is **success**.

:::zone-end

## Search the updated index

::zone pivot="csharp"

1. In the **Terminal** pane, select the bash terminal for the **enriched-search-client** folder. If you have closed this terminal, right-click (Ctrl+click if using a Mac) the **C-Sharp/enriched-search-client** folder and select **Open in Integrated Terminal**.
2. In the terminal for the **enriched-search-client** folder, enter the following command:

    ```bash
    dotnet run
    ```

3. Follow the link for the `https://localhost:5000/` address to open the web site in a new browser tab. Then in the Margie's Travel website, enter **Las Vegas volcano** into the search box and click **Search**.
4. When the results are displayed, observe that they include a list of the top words found in each document.
5. Close the browser tab containing the Margie's Travel web site and return to Visual Studio Code. Then in the terminal for the **search-client** folder (where the dotnet process is running), enter Ctrl+C to stop the app.

:::zone-end

:::zone pivot="python"

1. In the **Terminal** pane, select the bash terminal for the **enriched-search-client** folder. If you have closed this terminal, right-click (Ctrl+click if using a Mac) the **Python/enriched-search-client** folder and select **Open in Integrated Terminal**.
2. In the terminal for the **enriched-search-client** folder, enter the following command:

    ```bash
    flask run
    ```

3. Follow the link for the `https://127.0.0.1:5000/` address to open the web site in a new browser tab. Then in the Margie's Travel website, enter **Las Vegas volcano** into the search box and click **Search**.
4. When the results are displayed, observe that they include a list of the top words found in each document.
5. Close the browser tab containing the Margie's Travel web site and return to Visual Studio Code. Then in the Python terminal for the **enriched-search-client** folder (where the flask application is running), enter Ctrl+C to stop the app.

:::zone-end

## Clean up resources

Now that you have finished the exercises, you can delete the Azure resources.

1. Right-click (Ctrl+click if using a Mac) the **02-Create-an-enriched-pipeline** folder and select **Open in Integrated Terminal**. This will open a new bash terminal pane.
2. In the terminal pane, enter the following command to delete the resources used in this module:

    ```bash
    bash reset.sh
    ```

3. When prompted, follow the link, enter the provided code, and sign into your Azure subscription. Then wait for the script to complete and confirm that the resource group has been deleted.
