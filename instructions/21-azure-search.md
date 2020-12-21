# Create an Azure Cognitive Search solution

All organizations rely on information to make decisions, answer questions, and function efficiently. The problem for most organizations is not a lack of information, but the challenge of finding and  extracting the information from the massive set of documents, databases, and other sources in which the information is stored.

For example, suppose *Margie's Travel* is a travel agency that specializes in organizing trips to cities around the world. Over time, the company has amassed a huge amount of information in documents such as brochures, as well as reviews of hotels submitted by customers. This data is a valuable source of insights for travel agents and customers as they plan trips, but the sheer volume of data can make it difficult to find relevant information to answer a specific customer question.

To address this challenge, Margie's Travel can use Azure Cognitive Search to implement a solution in which the documents are indexed and made easy to search.

## Clone the repository for this course

If you have not already done so, you must clone the code repository for this course:

1. Start Visual Studio Code.
2. Open the palette (SHIFT+CTRL+P) and run a `Git: Clone` command to clone the `https://github/com/GraemeMalcolm/AI-102` repository to a local folder.
3. When the repository has been cloned, open the folder in Visual Studio Code.

## Create Azure resources

The solution you will create for Margie's Travel requires the following resources in your Azure subscription:

- An Azure Storage account with a blob container in which the documents to be searched are stored.
- - An Azure Cognitive Services resource, which provides AI services for skills that your search solution can use to enrich the data in the data source with AI-generated insights.
- An Azure Cognitive Search resource, which will manage indexing and querying.

### Create a storage account and upload files

1. Open the Azure portal at [https://portal.azure.com](https://portal.azure.com), and sign in using the Microsoft account associated with your Azure subscription.
2. Select the **&#65291;Create a resource** button, search for *storage*, and create a **Storage account** resource with the following settings:
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Choose or create a resource group (if you are using a restricted subscription, you may not have permission to create a new resource group - use the one provided)*
    - **Storage account name**: *Enter a unique name*
    - **Location**: *Choose any available location*
    - **Performance**: Standard
    - **Account kind**: Storage V2
    - **Replication**: Locally-redundant storage (LRS)
3. Wait for deployment to complete, and then go to the deployed resource.
4. In the blade for your storage account, in the pane on the left, select **Storage Explorer**.
5. In Storage Explorer, right-click **BLOB CONTAINERS** and create a blob container named **margies** with **Blob** level public access (the container will host documents that Margie's Travel makes publicly available in their web site).
6. Expand **BLOB CONTAINERS** and select your new **margies** container.
7. In the **margies** container, use the **&#65291;New Folder** button to create a new folder named **collateral**.
8. In the **margies > collateral** folder, select **Upload**, and in the **Upload blob** pane, select *all* of the files in the local **21-create-a-search-solution/data/collateral** folder (in the folder where you cloned the repo) and upload them.
9. Use the **&#8593;** button to navigate back up to the root of the **margies** container. Then create a new folder named **reviews**, alongside the existing **collateral** folder.
10. In the **margies > reviews** folder, select **Upload**, and in the **Upload blob** pane, select *all* of the files in the local **ai-102-ai-engineer/21-create-a-search-solution/data/reviews** folder and upload them.

    You should end up with a blob container structure like this:
    
    - **margies** (container)
        - **collateral** (folder)
            - 6 brochures (PDF files)
        - **reviews** (folder)
            - 66 hotel reviews (PDF files)

### Create a Cognitive Services resource

If you don't already have on in your subscription, you'll need to provision a **Cognitive Services** resource. Your search solution will use this to enrich the data in the datastore with AI-generated insights.

1. Return to the home page of the Azure portal, and then select the **&#65291;Create a resource** button, search for *cognitive services*, and create a **Cognitive Services** resource with the following settings:
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *The same resource group as your storage account*
    - **Region**: *Choose any available region*
    - **Name**: *Enter a unique name*
    - **Pricing tier**: Standard S0
2. Select the required checkboxes and create the resource.
3. Wait for deployment to complete, and then view the deployment details.

### Create an Azure Cognitive Search resource

1. Return to the home page of the Azure portal, and then select the **&#65291;Create a resource** button, search for *search*, and create a **Azure Cognitive Search** resource with the following settings:
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *The same resource group as your storage account and cognitive services resource*
    - **URL**: *Enter a unique name*
    - **Location**: *The same location as your storage account*
    - **Pricing tier**: Free\*

    \* *You can only have one free-tier resource per subscription. If you already have a free-tier resource that you can't use for this exercise, create a **Basic** tier resource.*

2. Wait for deployment to complete, and then go to the deployed resource.
3. Review the **Overview** page on the blade for your Azure Cognitive Search resource in the Azure portal. Here, you can use a visual interface to create, test, manage, and monitor the various components of a search solution; including data sources, indexes, indexers, and skillsets.

## Index the documents

Now that you have the necessary Azure resources in place, you can create a search solution by indexing the documents.

1. On the **Overview** page for your Azure Cognitive Search resource, select **import data**.
2. On the **Connect to your data** page, in the **Data Source** list, select **Azure Blob Storage**. Then complete the data store details with the following values:
    - **Data Source**: Azure Blob Storage
    - **Data source name**: margies-data
    - **Data to extract**: Content and metadata
    - **Parsing mode**: Default
    - **Connection string**: *Select **Choose an existing connection**. Then select your storage account, and finally select the **margies** container you created previously.*
    - **Authenticate using managed identity**: Unselected
    - **Blob folder**: *Leave this blank*
    - **Description**: Brochures and reviews in Margie's Travel web site.
3. Proceed to the next step (*Add cognitive skills*).
4. in the **Attach Cognitive Services** section, select your cognitive services resource.
5. In the **Add enrichments** section:
    - Change the **Skillset name** to **margies-skillset**.
    - Select the option **Enable OCR and merge all text into merged_content field**.
    - Set the **Source data field** to **merged_content**.
    - Leave the **Enrichment granularity level** as **Source field**, which is set the enture ciontents of the document being indexed; but note that you can change this to extract information at more granular levels, like pages or sentences.
    - Select the following enriched fields:

        | Cognitive Skill | Parameter | Field name |
        | --------------- | ---------- | ---------- |
        | Extract location names | | locations |
        | Extract key phrases | | keyphrases |
        | Detect language | | language |
        | Generate tags from images | | imageTags |
        | Generate captions from images | | imageCaptions |

6. Proceed to the next step (*Customize target index*).
7. Change the **Index name** to **margies-index**.
8. Set the **Key** set to **metadata_storage_path** and the **Suggester name** and **Search mode** blank.
9. Make the following changes to the index fields, leaving all other fields with their default settings:
    | Field name | Retrievable | Filterable | Sortable | Facetable | Searchable |
    | ---------- | ----------- | ---------- | -------- | --------- | ---------- |
    | metadata_storage_size | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&#10004; | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&#10004; | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&#10004; | | |
    | metadata_storage_last_modified | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&#10004; | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&#10004; | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&#10004; | | |
    | metadata_storage_name | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&#10004; | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&#10004; | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&#10004; | | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&#10004; |
    | metadata_author | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&#10004; | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&#10004; | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&#10004; | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&#10004; | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&#10004; |
    | locations | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&#10004; | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&#10004; | | | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&#10004; |
    | language | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&#10004; | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&#10004; | | | |

11. Proceed to the next step (*Create an indexer*).
12. Change the **Indexer name** to **margies-indexer**.
13. Leave the **Schedule** set to **Once**.
14. Expand the **Advanced** options, and ensure that the **Base-64 encode keys** option is selected (generally encoding keys make the index more efficient).
15. Select **Submit** to create the data source, skillset, index, and indexer. The indexer is run automatically and runs the indexing pipeline, which:
    1. Extracts the document metadata fields and content from the data source
    2. Runs the skillset of cognitive skills to generate additional enriched fields
    3. Maps the extracted fields to the index.
16. View the **Indexers** tab of the blade for your Azure Cognitive Search resource, which should show the newly created **margies-indexer**. Wait a few minutes, and click **&orarr; Refresh** until the **Status** indicates success.

## Search the index

Now that you have an index, you can search it.

1. At the top of the blade for your Azure Cognitive Search resource, select **Search explorer**.
2. In Search explorer, in the **Query string** box, enter `*` (a single asterisk), and then select **Search**.

    This query retrieves all documents in the index in JSON format. Examine the results and note the fields for each document, which contain document content, metadata, and enriched data extracted by the cognitive skills you selected.

3. Modify the query string to `search=*&$count=true` and submit the search.

    This time, the results include a **@odata.count** field at the top of the results that indicates the number of documents returned by the search.

4. Try the following query string:

    ```
    search=*&$count=true&$select=metadata_storage_name,metadata_author,locations
    ```

    This time the results include only the file name, author, and any locations mentioned in the document content. The file name and author are in the **metadata_content_name** and **metadata_author** fields, which were extracted from the source document. The **locations** field was generated by a cognitive skill.

5. Now try the following query string:

    ```
    search="New York"&$count=true&$select=metadata_storage_name,keyphrases
    ```

    This search finds documents that mention "New York" in any of the searchable fields, and returns the file name and key phrases in the document.

6. Let's try one more query string:

    ```
    search="New York"&$count=true&$select=metadata_storage_name&$filter=author eq 'Reviewer'
    ```

    This query returns the filename of any documents authored by *Reviewer* that mention "New York".

## Explore and modify definitions of search components

The components of the search solution are based on JSON definitions, which you can view and edit in the Azure portal.

### Review the data source

1. In the Azure portal, return to the **Overview** page on the blade for your Azure Cognitive Search resource, and select the **Data sources** tab. The **margies-data** data source should be listed.
2. Select the **margies-data** data source to view its settings. Then select the **Data Source Definition (JSON)** tab to view the JSON definition of the data source. This includes the information it uses to connect to the blob container in your storage account.
3. Close the **margies-data** page to return to the blade for your Azure Cognitive Search resource.

### Review and modify the skillset

1. On the blade for your Azure Cognitive Search resource, select the **Skillsets** tab, where **margies-skillset** should be listed.
2. Select **margies-skillset** and view the **Skillset Definition (JSON)** page. This shows a JSON definition that includes the six skills you specified in the user interface previously.
3. On the right side of the page, note that there are templates for additional skills you might want to add to the skillset. For example, it would be good to identify the *sentiment* of the documents being indexed - particularly the hotel reviews, so we can easily find reviews that are positive or negative.
4. In the **Skills** list, select **Sentiment Skill** to show a JSON template for this skill.
5. Copy the template to the clipboard, and then on the left side, in the JSON for your skillset definition, paste the copied skill in a newly inserted line immediately after the following line (which should be line 6) - be careful not to overwrite the **{** marking the beginning of the first existing skill:

    ```json
    "skills": [
    ```

6. Add a comma immediately after the newly inserted skill, and reformat the JSON indentation to make it more readable. It should look like this:

    ```json
    {
    "@odata.context": "https://....",
    "@odata.etag": "\"....\"",
    "name": "margies-skillset",
    "description": "Skillset created from the portal....",
    "skills": [
        /* New skill inserted here */
        {
            "@odata.type": "#Microsoft.Skills.Text.SentimentSkill",
            "defaultLanguageCode": "",
            "name": "",
            "description": "",
            "context": "",
            "inputs": [
                {
                    "name": "text",
                    "source": ""
                },
                {
                    "name": "languageCode",
                    "source": ""
                }
            ],
            "outputs": [
                {
                    "name": "score",
                    "targetName": "score"
                }
            ]
        },
        /* Add a comma after the new skill, before the first existing skill */
        {
            "@odata.type": "#Microsoft.Skills.Text.EntityRecognitionSkill",
            "name": "#1",
            ...
    }
    ```
7. Update the new skill definition like this:

    ```json
		{
			"@odata.type": "#Microsoft.Skills.Text.SentimentSkill",
			"defaultLanguageCode": "en",
			"name": "get-sentiment",
			"description": "Evaluate sentiment",
			"context": "/document",
			"inputs": [
				{
					"name": "text",
					"source": "/document/merged_content"
				},
				{
					"name": "languageCode",
					"source": "/document/language"
				}
			],
			"outputs": [
				{
					"name": "score",
					"targetName": "sentimentScore"
				}
			]
		},
    ```

    The new skill is named **get-sentiment**, and will evaluate the text found in the **merged_content** field of the document being indexed (which includes the source content as well as any text extracted from images in the content). It uses the extracted **language** of the document (with a default of English), and evaluates a score for the sentiment of the content. This score is then  output as a new field named **sentimentScore** at the **document** level of the object that represents the indexed document.

8. Select **Save** to save the skillset with the new skill.
9. Close the **margies-skillset** page to return to the blade for your Azure Cognitive Search resource.

### Review and modify the index

1. On the blade for your Azure Cognitive Search resource, select the **Indexes** tab (<u>not</u> Indexe**r**s), where **margies-index** should be listed.
2. Select **margies-index** and view the **Index Definition (JSON)** page. This shows a JSON definition for your index, including definitions for each field. Some fields are based on metadata and content in the source document, and others are the results of skills in the skillset.
3. You added a skill to the skillset to extract a sentiment score for the document. Now you must add a corresponding field in the index to which this value can be mapped. At the bottom of the **fields** list (before the closing **]**, which is followed by index properties such as **suggesters**), add the following field (being sure to include the comma at the beginning, after the previous field):

    ```json
    ,
    {
      "name": "sentiment",
      "type": "Edm.Double",
      "facetable": false,
      "filterable": true,
      "key": false,
      "retrievable": true,
      "searchable": false,
      "sortable": true,
      "analyzer": null,
      "indexAnalyzer": null,
      "searchAnalyzer": null,
      "synonymMaps": [],
      "fields": []
    }
    ```

4. The index includes the **metadata_storage_path** field (the URL of the document), which is currently used as the index key. The key is Base-64 encoded, making it efficient as a key but requiring de-encoding to be useful to client applications as a field. We'll resolve this by adding another field that will be mapped to the unencoded value. Add the following field definition immediately after the **sentiment** field you just added:

    ```json
    ,
    {
      "name": "url",
      "type": "Edm.String",
      "facetable": false,
      "filterable": true,
      "key": false,
      "retrievable": true,
      "searchable": false,
      "sortable": false,
      "analyzer": null,
      "indexAnalyzer": null,
      "searchAnalyzer": null,
      "synonymMaps": [],
      "fields": []
    }
    ```

5. Select **Save** to save the index with the new fields.
6. Close the **margies-index** page to return to the blade for your Azure Cognitive Search resource.

### Review and modify the indexer

1. On the blade for your Azure Cognitive Search resource, select the **Indexers** tab (<u>not</u> Indexes), where **margies-indexer** should be listed.
2. Select **margies-indexer** and view the **Indexer Definition (JSON)** page. This shows a JSON definition for your indexer, which maps fields extracted from document content and metadata (in the **fieldMappings** section), and values extracted by skills in the skillset (in the **outputFieldMappings** section), to fields in the index.
3. In the **fieldMappings** section, after the existing mapping for the **metadata_storage_path** value to the base-54 encoded key field, add another mapping to map the same value to the **url** field, so that the entire **fieldMappings** section looks like this (be sure to include the comma between the existing mapping and the new one):

    ```json
    "fieldMappings": [
        {
        "sourceFieldName": "metadata_storage_path",
        "targetFieldName": "metadata_storage_path",
        "mappingFunction": {
            "name": "base64Encode",
            "parameters": null
            }
        },
        {
            "sourceFieldName" : "metadata_storage_path",
            "targetFieldName" : "url"
        }
    ],
    ```

    All of the other metadata and content field in the source document are implicitly mapped to fields of the same name in the index.

4. At the end of the **ouputFieldMappings** section, add the following mapping to map the **sentimentScore** value extracted by your sentiment skill to the **sentiment** field you added to the index:

    ```json
    ,
    {
      "sourceFieldName": "/document/sentimentScore",
      "targetFieldName": "sentiment"
    }
    ```

5. Select **Save** to save the indexer with the new mappings.
6. Select **Reset** to reset the index, and confirm that you want to do this when prompted. You've added new fields to an already-populated index, so you'll need to reset and reindex to update the existing index records with the new field values.
7. Select **Run** to run the updated indexer, confirming that you want to run it now when prompted.

    *Note that in a free-tier resource, you can only run the indexer once every three minutes; so if you have already run the indexer recently, you may need to wait before running it again.*

8. Select **Refresh** to track the progress of the indexing operation. It may take a minute or so to complete.
9. When indexing has completed successfully, close the **margies-indexer** page to return to the blade for your Azure Cognitive Search resource.

    *There may be some warnings for a few documents that are too large to evaluate sentiment. Often sentiment analysis is performed at the page or sentence level rather than the full document; but in this case scenario, most of the documents - particularly the hotel reviews, are short enough for useful document-level sentiment scores to be evaluated.*

### Query the modified index

1. At the top of the blade for your Azure Cognitive Search resource, select **Search explorer**.
2. In Search explorer, in the **Query string** box, enter the following query string, and then select **Search**.

    ```
    search=London&$select=url,sentiment,keyphrases&$filter=metadata_author eq 'Reviewer' and sentiment gt 0.5
    ```

    This query retrieves the **url**, **sentiment**, and **keyphrases** for all documents that mention *London* authored by *Reviewer* that have a **sentiment** score greater than *0.5* (in other words, positive reviews that mention London)

## Create a search client application

Now that you have a useful index, you can use it from a client application. You can do this by consuming the REST interface, submitting requests and receiving responses in JSON format over HTTP; or you can use the software development kit (SDK) for your preferred programming language. In this exercise, we'll use the SDK.

> **Note**: You can choose to use the SDK for either **C#** or **Python**. In the steps below, perform the actions appropriate for your preferred language.

### Get the endpoint and keys for your search resource

1. In the Azure portal, return to the blade for your Azure Cognitive Search resource and on the **Overview** page, note the **Url** value, which should be similar to **https://*your_resource_name*.search.windows.net**. This is the endpoint for your search resource.
2. On the **Keys** page, note that there are two **admin** keys, and a single **query** key. An *admin* key is used to create and manage search resources; a *query* key is used by client applications that only need to perform search queries.

    *You will need the endpoint and query key for your client application.*

### Prepare to use the Azure Cognitive Search SDK

1. In Visual Studio Code open the **AI-102** project, and in the **Explorer** pane, browse to the **create-a-search-solution** folder and expand the **C-Sharp** or **Python** folder depending on your language preference.
2. Right-click the **margies-travel** folder and open an integrated terminal. Then install the Azure Cognitive Search SDK package by running the appropriate command for your language preference:

   **C#**

    ```
    dotnet add package Azure.Search.Documents --version 11.1.1
    ```

   **Python**

   ```
   pip install azure-search-documents==11.0.0
   ```
3. View the contents of the **margies-travel** folder, and note that it contains a file for configuration settings:
    - **C#**: appsettings.json
    - **Python**: .env

    Open the configuration file and update the configuration values it contains to reflect the **endpoint** and **query key** for your Azure Cognitive Search resource. Save your changes.

### Add code to search an index

The **margies-travel** folder contains code files for a web application (a Microsoft C# *ASP&period;NET Razor* web application or a Python *Flask* application), which you will update to include search functionality.

1. Open the following code file in the web application, depending on your choice of programming language:
    - **C#**:Pages/Index.cshtml.cs
    - **Python**: app&period;py
2. Near the top of the code file, find the comment **Import namespaces**, and add the following code below this comment:

    **C#**

    ```C#
    // Import namespaces
    using Azure;
    using Azure.Search.Documents;
    using Azure.Search.Documents.Models;
    ```

    **Python**

    ```Python
    # Import namespaces
    from azure.core.credentials import AzureKeyCredential
    from azure.search.documents import SearchClient
    ```

3. In the **search_query** function, find the comment **Create a search client**, and add the following code:

    **C#**

    ```C#
    // Create a search client
    AzureKeyCredential credential = new AzureKeyCredential(QueryKey);
    SearchClient searchClient = new SearchClient(SearchEndpoint, IndexName, credential);
    ```

    **Python**

    ```Python
    # Create a search client
    azure_credential = AzureKeyCredential(search_key)
    search_client = SearchClient(search_endpoint, search_index, azure_credential)
    ```

4. In the **search_query** function, find the comment **Submit search query**, and add the following code to submit a search for the specified text with the following options:
    - A *search mode* that requires **all** of the individual words in the search text are found.
    - The total number of documents found by the search is included in the results.
    - The results are filtered to include only documents that match the provided filter expression.
    - The results are sorted into the specified sort order.
    - Each discrete value of the **metadata_author** field is returned as a *facet* that can be used to display pre-defined values for filtering.
    - Up to three extracts of the **merged_content** and **imageCaption** fields with the search terms highlighted are included in the results.
    - The results include only the fields specified.

    **C#**

    ```C#
    // Submit search query
    var options = new SearchOptions{
        IncludeTotalCount = true,
        SearchMode = SearchMode.All,
        Filter = FilterExpression,
        OrderBy = {SortOrder},
        Facets = {"metadata_author"},
        HighlightFields = {"merged_content-3","imageCaption-3"} 
    };
    options.Select.Add("url");
    options.Select.Add("metadata_storage_name");
    options.Select.Add("metadata_author");
    options.Select.Add("metadata_storage_size");
    options.Select.Add("metadata_storage_last_modified");
    options.Select.Add("language");
    options.Select.Add("sentiment");
    options.Select.Add("merged_content");
    options.Select.Add("keyphrases");
    options.Select.Add("locations");
    options.Select.Add("imageTags");
    options.Select.Add("imageCaption");
    SearchResults<SearchResult> results = searchClient.Search<SearchResult>(SearchTerms, options);
    return results;
    ```

    **Python**

    ```Python
    # Submit search query
    results =  search_client.search(search_text,
                                    search_mode="all",
                                    include_total_count=True,
                                    filter=filter_by,
                                    order_by=sort_order,
                                    facets=['metadata_author'],
                                    highlight_fields='merged_content-3,imageCaption-3',
                                    # select fields on a single line
                                    select = "url,metadata_storage_name,metadata_author,metadata_storage_last_modified,language,sentiment,merged_content,keyphrases,locations,imageTags,imageCaption")
    return results
    ```

5. Save your changes.

### Explore code to render search results

The web app already includes code to process and render the search results.

1. 


### Run the web app

 1. return to the integrated terminal for the **margies-travel** folder, and enter the following command to run the program:

    **C#**

    ```
    dotnet run
    ```

    **Python**

    ```
    flask run
    ```
    In the message that is displayed when the app starts successfully, follow the link to the running web application (`https://localhost:5000/` or `https://127.0.0.1:5000/`) to open the Margies Travel site in a web browser:

2. In the Margie's Travel website, enter **London hotel** into the search box and click **Search**.
3. Review the search results. They include the file name (with a hyperlink to the file URL), an extract of the file content with the search terms (*London* and *hotel*) emphasized, and other attributes of the file from the index fields.
4. Observe that the results page includes some user interface elements that enable you to refine the results. These include:
    - A *filter* based on the *facetable* **metadata_author** field. You can use facetable fields to return a list of *facets* - fields with a small set of discrete values that can displayed as potential filter values in the user interface.
    - The ability to *order* the results based on a specified field and sort direction (ascending or descending). The default order is based on *relevancy*, which is calculated as a **search.score()** value based on a *scoring profile* that evaluates the frequency and importance of search terms in the index fields.

5. Select the **Reviewer** filter and the **Positive to negative** sort option, and click **Refine Results**.
6. Observe that the results are filtered to include only reviews, and sorted into descending order of sentiment.
7. Close the browser tab containing the Margie's Travel web site and return to Visual Studio Code. Then in the Python terminal for the **margies-travel** folder (where the flask application is running), enter Ctrl+C to stop the app.



## Search the Margie's Travel index

To search the Margie's Travel index, you will use a web application that includes a form in which users can submit search expressions. Select your preferred language at the top of this page, and then follow the steps below to query the Margie's Travel search solution.

:::zone pivot="csharp"

1. In the **01-Create-a-search-solution/C-Sharp** folder, expand the **search-client** folder. This folder contains a simple ASP&#46;NET Core web application for the Margie's Travel web site.
2. Open the **appsettings.json** file in the **search-client** folder. This file contains configuration values for the web application.
3. Modify the values in the **appsettings.json** file to reflect the service name (<u>without</u> the .*search&#46;windows&#46;net* suffix) and query key for your Azure Cognitive Search service) and the (be sure to specify the *query* key, and not the *admin* key!). Then save the **appsettings.json** file.
4. In the **Pages** folder for the web application, open the **Index.cshtml** code file. This file defines the main page of the web application. The page contains a form in which users can submit search terms, and code to render the search results.
5. Open the **Index.cshtml.cs** code file, which contains C# code to support the web page. Review the **OnGet** function, which is called when the page is requested. It extracts parameters passed in the request, and then uses a **SearchServiceClient** object to submit a query to Azure Cognitive Search. The query includes the following parameters:
    - **Select**: The index fields to be included in the query results.
    - **SearchMode**: This value determines how the search query is applied. A value of **All** means that all of the specified search terms must be present for the document to be included in the results. A value of **Any** means that only one or more of the terms must be present.
    - **HighlightFields**: Fields that can be used to display a snippet of the document data with the search term highlighted. In this case, the results include extracts from the **content** field with up to three instances of the search term shown in context.
    - **Facets**: Fields that can be used to provide filters in the user interface, enabling users to "drill-down" into the results. In this case, the **author** field is specified, so the results can include navigation elements that enable users to further refine the query by selecting individual author values.
6. In the **Models** folder, open the **SearchResults.cs** code file. This defines a class for the search results - the query returns a list of these.
7. Right-click (Ctrl+click if using a Mac) the **C-Sharp/search-client** folder and select **Open in Integrated Terminal** to open a new bash terminal in this folder.
8. In the terminal for the **search-client** folder, enter the following command:
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
11. In the Margie's Travel website, enter **London hotel** into the search box and click **Search**.
12. Review the search results. They include the file name (with a hyperlink to the file URL), author, size, last modified date, and an extract of the file content with the search terms (*London* and *hotel*) emphasized.
13. Observe that the **author** facets have been used to create user interface elements for filtering based on the author (the documents in the Margie's Travel data source have two possible author values: **Margies Travel** and **Reviewer**). You'll explore this feature in a later exercise.
14. Try another search by entering **"New York"** (including the quotation marks) in the search box at the top of the page and clicking **Search**. This time the results reflect a search for the complete phrase "New York".
15. Try another search by entering new search terms (for example **Luxury hotel in Las Vegas**) in the search box at the top of the page and clicking **Search**.
16. Close the browser tab containing the Margie's Travel web site and return to Visual Studio Code. Then in the terminal for the **search-client** folder (where the dotnet process is running), enter Ctrl+C to stop the app.

:::zone-end

:::zone pivot="python"

1. In the **01-Create-a-search-solution/Python** folder, expand the **search-client** folder. This folder contains a simple Flask-based web application for the Margie's Travel web site.
2. Open the **.env** file in the **search-client** folder. This file contains environment variables for the web application.
3. Modify the values in the **.env** file to reflect the endpoint and query key for your Azure Cognitive Search resources (be sure to specify the *query* key, and not the *admin* key!). Then save the **.env** file.
4. Open the **app&#46;py** code file. This file contains the code for the Flask web application. The code:
    - Loads the required Azure Cognitive Search credentials from environment variables.
    - Defines a function named **azsearch_query** that submits a query as a REST request to an Azure Cognitive Search endpoint.
    - Defines a route for the web site's home page (*/*) that displays a web page based on the **default.html** template. This template includes a basic search form.
    - Defines a route for the search results page (*/search*) that retrieves the query text from the search form, constructs parameters for the REST request, submits the query, and renders the results in the **search.html** template.
    - Defines a route for a more advanced search page (*/filter*) that includes filtering and sorting.
5. Examine the code in the **search** function (for the **/search** route), and review the **searchParams** definition. This configures the search query performed by Azure Cognitive Search, and includes the following parameters:
    - **search**: The text to be searched for. In this case, the search terms are passed to the function from the search form on the web page.
    - **searchMode**: This value determines how the search query is applied. A value of **All** means that all of the specified search terms must be present for the document to be included in the results. A value of **Any** means that only one or more of the terms must be present.
    - **$count**: Determines whether a value indicating the number of matching results (sometimes known as "search hits") is included in the results.
    - **queryType**: Indicates the query parser to be used. Azure Cognitive Search supports two query types: **simple**, which is optimized for basic full-text search queries; and **full**, which uses the Lucene query syntax to apply complex filters and other query expressions.
    - **$select**: The index fields to be included in the query results.
    - **facet**: Fields that can be used to provide filters in the user interface, enabling users to "drill-down" into the results. In this case, the **author** field is specified, so the results can include navigation elements that enable users to further refine the query by selecting individual author values.
    - **highlight**: Fields that can be used to display a snippet of the document data with the search term highlighted. In this case, the results include extracts from the **content** field with up to three instances of the search term shown in context.
    - **api-version**: The version of the Azure Cognitive Search REST API to be used.
6. Observe that the **search** function goes on to submit the query, extract the following data from the JSON response that is returned, and render it in the **search.html** template page:
    - **@odata.count**: The number of results, as returned by the **$count** parameter.
    - The **author** fields in the **@search.facets** collection, which is a list of the discrete **author** vales in the results returned by the **facet** parameter.
    - **value**: The collection of search results returned by the query.
7. Right-click (Ctrl+click if using a Mac) the **Python/search-client** folder and select **Open in Integrated Terminal** to open a new bash terminal in this folder.
8. In the terminal for the **search-client** folder, enter the following command:
    ```bash
    flask run
    ```
9. When the following message is displayed, follow the `https://127.0.0.1:5000/` link to open the web application in a new browser tab:
    ```text
    * Environment: production
      WARNING: This is a development server. Do not use it in a production deployment.
      Use a production WSGI server instead.
   * Debug mode: off
   * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
   ```
10. Wait for the web site to open (the web site is being run in the development container, and port forwarding is used to make it available as a locally hosted site in your browser session - you may need to allow access through your firewall).
11. In the Margie's Travel website, enter **London hotel** into the search box and click **Search**.
12. Review the search results. They include the file name (with a hyperlink to the file URL), author, size, last modified date, and an extract of the file content with the search terms (*London* and *hotel*) emphasized.
13. Observe that the **author** facets have been used to create user interface elements for filtering based on the author (the documents in the Margie's Travel data source have two possible author values: **Margies Travel** and **Reviewer**). You'll explore this feature in a later exercise.
14. Try another search by entering **"New York"** (including the quotation marks) in the search box at the top of the page and clicking **Search**. This time the results reflect a search for the complete phrase "New York".
15. Try another search by entering new search terms (for example **Luxury hotel in Las Vegas**) in the search box at the top of the page and clicking **Search**.
16. Close the browser tab containing the Margie's Travel web site and return to Visual Studio Code. Then in the Python terminal for the **search-client** folder (where the flask application is running), enter Ctrl+C to stop the app.

:::zone-end

> [!NOTE]
> For more information about querying an index, and details about **simple** and **full** syntax, see [Query types and composition in Azure Cognitive Search](https://docs.microsoft.com/azure/search/search-query-overview) in the Azure Cognitive Search documentation.

## Filter and sort Margie's Travel results

You can apply filtering and sorting to the Margie's Travel search results by submitting a new query that includes a filter and sort order. Select your preferred language at the top of this page, and then follow the steps below to filter and sort results.

:::zone pivot="csharp"

1. In the **C-Sharp/search-client/Pages** folder, open the **Index.cshtml.cs** code file containing the code for the web application's main page.
2. Examine the code in the **OnGet** function, noting that the parameters that can be submitted to the page include **sort** and **facet**. 
    - The **sort** parameter defines a sort order that is applied to the query results in the **OrderBy** search parameter. The default sort order is based on a built in field named **@search.score**, which uses a *scoring profile* to calculate a relevance score for each result based on factors like the frequency of search term occurrence, the presence of search terms in the document name, and so on  (you can create custom scoring profiles as alternatives to the default one). You can specify the scoring profile sort order explicitly by using the built-in **search.score()** function, or you can specify an alternative sort order based on user selection. In this case, the user can choose to sort the results into ascending order by file name, descending order by size, or descending order by last modified date.
    - The **facet** parameter contains the value of the faceted **author** field that the user has selected from the original results. Its value is used to specify a filtering expression in the **Filter** search parameter. In this case, the filter is based on the **author** facet value selected by the user in the user interface, but you could specify any filtering expression that applies comparative logic to any filterable field.
3. In the **Terminal** pane, select the bash terminal for the **search-client** folder. If you have closed this terminal, right-click (Ctrl+click if using a Mac) the **C-Sharp/search-client** folder and select **Open in Integrated Terminal**.
4. In the terminal for the **search-client** folder, enter the following command:
    ```bash
    dotnet run
    ```
5. Follow the link for the `https://localhost:5000/` address to open the web site in a new browser tab. Then in the Margie's Travel website, enter **"San Francisco"** into the search box and click **Search**.
6. When the results are displayed, select the **Reviewer** filter and the **Largest file size** sort option, and click **Refine Results**.
7. Observe that the results are filtered to include only reviews, and sorted into descending order of file size.
8. Close the browser tab containing the Margie's Travel web site and return to Visual Studio Code. Then in the terminal for the **search-client** folder (where the dotnet process is running), enter Ctrl+C to stop the app.

:::zone-end

:::zone pivot="python"

1. In the **Python/search-client** folder, open the **app&#46;py** code file containing the code for the Flask web application.
2. Examine the code in the **filter** function (for the **/filter** route), and review the **searchParams** definition. This includes some of the same parameters as the basic search function you examined previously, with the following differences:
    - **queryType**: This parameter has been changed to **Full**, indicating that Lucene syntax for filtering expressions will be used.
    - **$filter**: This parameter has been used to specify a filtering expression. In this case, the filter is based on the **author** facet value selected by the user in the user interface, but you could specify any filtering expression that applies comparative logic to any filterable field.
    - **$orderBy**: This parameter specifies a sort order for the results. The default sort order is based on a built-in field named **@search.score**, which uses a *scoring profile* to calculate a relevance score for each result based on factors like the frequency of search term occurrence, the presence of search terms in the document name, and so on  (you can create custom scoring profiles as alternatives to the default one). You can specify the scoring profile sort order explicitly by using the built-in **search.score()** function, or you can specify an alternative sort order based on user selection. In this case, the user can choose to sort the results into ascending order by file name, descending order by size, or descending order by last modified date.
3. In the **Terminal** pane, select the bash terminal for the **search-client** folder. If you have closed this terminal, right-click (Ctrl+click if using a Mac) the **Python/search-client** folder and select **Open in Integrated Terminal**.
4. In the terminal for the **search-client** folder, enter the following command:
    ```bash
    flask run
    ```
5. Follow the link for the `https://127.0.0.1:5000/` address to open the web site in a new browser tab. Then in the Margie's Travel website, enter **"San Francisco"** into the search box and click **Search**.
6. When the results are displayed, select the **Reviewer** filter and the **Largest file size** sort option, and click **Refine Results**.
7. Observe that the results are filtered to include only reviews, and sorted into descending order of file size.
8. Close the browser tab containing the Margie's Travel web site and return to Visual Studio Code. Then in the Python terminal for the **search-client** folder (where the flask application is running), enter Ctrl+C to stop the app.

:::zone-end

> [!NOTE]
> For more information about using filters, see [Filters in Azure Cognitive Search](https://docs.microsoft.com/azure/search/search-filters). For information about working with results, including sorting and hit highlighting, see [How to work with search results in Azure Cognitive Search](https://docs.microsoft.com/azure/search/search-pagination-page-layout).

## Enhancing the Margie's Travel index

Let's enhance the Margie's Travel index by adding synonyms for common geographic entities.

Select your preferred language at the top of this page, and then follow the steps below to enhance your search solution.

:::zone pivot="csharp"

1. In the **Terminal** pane, select the bash terminal for the **C-Sharp/search-client** folder. If you have closed this terminal, right-click (CTRL+click if using a Mac) the **search-client** folder and select **Open in Terminal**.
2. In the terminal for the **search-client** folder, enter the following command:
    ```bash
    dotnet run
    ```
3. Follow the link for the `https://localhost:5000/` address to open the web site in a new browser tab. Then in the Margie's Travel website, enter **"United Kingdom"** into the search box and click **Search**. Then review the results.
4. Enter **UK** into the search box and click **Search** and review the results. The results are different, even though a user might commonly use *UK* as an alternative term for *United Kingdom*. To address this issue, you will add a synonym map to your index.
5. Leaving the Margie's Travel website running, switch back to Visual Studio Code and in the **C-Sharp/create-index** folder, open the **Program.cs** file and review the code in the **AddSynonyms** function, which creates a synonym map and applies it to the **content** field of the index.
6. In the **Terminal** pane, select the bash terminal for the **C-Sharp/create-index** folder. If you have closed this terminal, right-click (Ctrl+click if using a Mac) the **C-Sharp/create-index** folder and select **Open in Integrated Terminal**.
7. In the terminal for the **create-index** folder, enter the following command:
    ```bash
    dotnet run
    ```
8. When prompted, press **4** to add a synonym map. Then wait while the program creates the synonym map and updates the index.
9. When the prompt is redisplayed, press **q** to quit the program.
10. After the index has been updated, switch back to the Margie's Travel website tab and search for **UK**. The results this time should include documents in which the term *United Kingdom* is highlighted.
11. Close the browser tab containing the Margie's Travel web site and return to Visual Studio Code. Then in the *dotnet* terminal for the **search-client** folder (where the web application is running), enter CTRL+C to stop the app.

:::zone-end

:::zone pivot="python"

1. In the **Terminal** pane, select the bash terminal for the **Python/search-client** folder. If you have closed this terminal, right-click (CTRL+click if using a Mac) the **search-client** folder and select **Open in Terminal**.
2. In the terminal for the **search-client** folder, enter the following command:
    ```bash
    flask run
    ```
3. Follow the link for the `https://127.0.0.1:5000/` address to open the web site in a new browser tab. Then in the Margie's Travel website, enter **"United Kingdom"** into the search box and click **Search**. Then review the results.
4. Enter **UK** into the search box and click **Search** and review the results. The results are different, even though a user might commonly use *UK* as an alternative term for *United Kingdom*. To address this issue, you will add a synonym map to your index.
5. Leaving the Margie's Travel website running, switch back to Visual Studio Code and in the **create-index** folder, open the **synonyms.json** file. This file contains a JSON definition for a synonym map that includes alternative terms for the United States, United Kingdom, and United Arab Emirates.
6. in the **create-index** folder, open the **updated_index.json** file. This file contains a JSON definition for the index in which the synonym map has been added to the **content** field.
7. In the **Terminal** pane, select the bash terminal for the **Python/create-index** folder. If you have closed this terminal, right-click (CTRL+click if using a Mac) the **Python/create-index** folder and select **Open in Integrated Terminal**.
8. In the terminal for the **create-index** folder, enter the following command to create the synonym map:
    ```bash
    python3 submit-rest.py 'PUT' 'synonymmaps/margies-synonyms-py' 'synonyms.json'
    ```
9. After the synonym map has been created, enter the following command to update the index:
    ```bash
    python3 submit-rest.py 'PUT' 'indexes/margies-index-py' 'updated_index.json'
    ```
10. After the index has been updated, switch back to the Margie's Travel website tab and search for **UK**. The results this time should include documents in which the term *United Kingdom* is highlighted.
11. Close the browser tab containing the Margie's Travel web site and return to Visual Studio Code. Then in the *Python3* terminal for the **search-client** folder (where the flask web application is running), enter CTRL+C to stop the app.

:::zone-end

You've now completed all of the exercises in this module. If you want to remove the Azure resources you created, in the *bash* terminal for the **01-Create-a-search-solution** folder, enter the following command to run the reset script that was created when you provisioned your Azure resources, signing in when prompted:

```bash
bash reset.sh
```


