# Graeme is Working on this

## Create resources for Margie's Travel

The solution you will create for Margie's Travel requires the following resources in your Azure subscription:

- An Azure Storage account with a blob container in which the documents to be searched are stored.
- An Azure Cognitive Search resource, which will manage indexing and querying.

A script containing Azure command-line interface (CLI) commands to create these resources has been provided. Use the following steps to run it.

1. In Visual Studio Code, right-click (Ctrl+click if using a Mac) the **01-Create-a-search-solution** folder and select **Open in Integrated Terminal**. This will open a new bash terminal pane.

    > [!TIP]
    > You're going to open multiple terminal sessions during this module, each associated with a folder. They'll all be available in the same **Terminal** pane, and you can switch between them using the drop-down list (which will currently include the *bash* terminal you just opened for the **01-Create-a-search-solution** folder.).

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
    - Search service endpoint
    - Search service admin key
    - Search service query key

6. Open the Azure portal at [https://portal.azure.com](https://portal.azure.com?azure-portal=true), signing in with the credentials associated with your Azure subscription if prompted.
7. In the Azure portal, find the resource group that was created by the setup script, and verify that it contains the Azure Storage account and Azure Cognitive Search resource.

## Create a data source for Margie's Travel

In the Margie's Travel scenario, the data consists of unstructured documents in Azure Storage, so you must create a data source for the blob container where the documents are stored.

Choose the language you want to use at the top of this page, and follow the steps to create a data source.

> [!NOTE]
> The exercises in this module assume you will use the same language for each task to incrementally build a search solution. If you wish, you can repeat each task in both languages, but doing so will create two search solutions - you can't use a mix of language-specific instructions to create a single solution.

:::zone pivot="csharp"

Azure Cognitive Search provides a software development kit (SDK) for Microsoft .NET, which you can use to write C# code that works with your search resources.

1. In Visual Studio Code, expand the **01-Create-a-search-solution** folder and the **C-Sharp** folder it contains.
2. Expand the **create-index** folder and open the **appsettings.json** file. This file contains configuration values for your C# code. Using a configuration file like this enables you to specify variable parameters separately from the code that uses them, adding flexibility to your infrastructure-as-code solution. It also avoids hard-coding sensitive values, such as keys and passwords in your code - enabling you to manage code files in a shared source control repository without compromising secure data.
3. Modify the values in the **appsettings.json** file to reflect the Azure Cognitive Search service name (<u>without</u> the .*search&#46;windows&#46;net* suffix), Azure Cognitive Search admin key, and Azure Storage blob container connection string for the Azure resources you created previously. Then save the **appsettings.json** file.
4. Open the **Program.cs** file, and view the code it contains. The **Main** function:
    - Gets the configuration settings from the **appsettings.json** file.
    - Creates a **SearchServiceClient** object for your Azure Cognitive Search service.
    - Prompts the user for input, calling the appropriate functions to create Azure Cognitive Search components.
5. View the **CreateOrUpdateDataSource** function, which creates a data source named **margies-docs-cs** that references the Azure Storage blob container where the PDF documents are stored.
6. Right-click (Ctrl+click if using a Mac) the **create-index** folder and select **Open in Integrated Terminal**. This will open a new bash terminal in this folder.
7. In the terminal for the **create-index** folder, enter the following command:
    ```bash
    dotnet run
    ```
8. When prompted, press **1** to create a data source. Then wait while the program creates the data source.
9. When the prompt is redisplayed, press **q** to quit the program.
10. Open your search service in the [Azure portal](https://portal.azure.com?portal=true) and view its **Data sources** tab to confirm that the data source has been created.

:::zone-end

:::zone pivot="python"

There is no Python SDK for creating Azure Cognitive Search objects, but you can use Python to submit requests to the Azure Cognitive Search REST API. In the case of a data source, the body of the REST request takes the form of a JSON document defining the data source to be created.

1. In Visual Studio Code, expand the **01-Create-a-search-solution** folder and the **Python** folder it contains.
2. Expand the **create-index** folder and open the **data_source.json** file. This contains the JSON definition for a data source that can be submitted to the Azure Cognitive Search REST interface.
3. Review the JSON code, which defines an Azure blob data source named **margies-docs-py** that references the **margies** container in an Azure Storage account. The connection string for the blob container is null - you will address this in your code later.
4. Open the **submit-rest&#46;py** code file and review the Python code it contains. The code contains the following functions:
    - **azsearch_rest**: This function submits an HTTP request to the Azure Cognitive Search REST interface. The specific operation initiated by the request is determined by the endpoint that is called and the JSON body that is submitted.
    - **main**: This is the main entry-point function for the script. It loads environment variables for the secure credentials required to connect to your Azure Cognitive Search resource, and the JSON file specified in the parameters used to call the script. If the *data_source.json* file is specified, the Azure Storage blob container connection string is loaded from the environment variables and inserted into the JSON body. Then the JSON is submitted to the **az_search** function along with the specified HTTP operation and method endpoint. The response returned for the request is then displayed as JSON.
5. Open the **.env** file, which contains environment variables for your Python code. Using environment variables enables you to specify variable parameters separately from the code that uses them, adding flexibility to your infrastructure-as-code solution. It also avoids hard-coding sensitive values, such as keys and passwords in your code - enabling you to manage code files in a shared source control repository without compromising secure data.
6. Modify the values in the **.env** file to reflect the Azure Cognitive Search endpoint, Azure Cognitive Search admin key, and Azure Storage blob container connection string for the Azure resources you created previously. **.env** file
7. Right-click (Ctrl+click if using a Mac) the **create-index** folder and select **Open in Integrated Terminal**. This will open a new bash terminal in this folder.
8. In the terminal for the **create-index** folder, enter the following command:
    ```bash
    python3 submit-rest.py 'POST' 'datasources' 'data_source.json'
    ```
9. Wait while Python runs the **submit-rest&#46;py** script, causing it to submit an HTTP POST request to the *datasources* REST endpoint with the JSON body defined in the *data_source.json* file.
10. Review the JSON response that is returned from the REST interface. It contains the full JSON definition of the data source (the data source connection string is null to avoid returning sensitive data).
11. Open your search service in the [Azure portal](https://portal.azure.com?portal=true) and view its **Data sources** tab to confirm that the data source has been created.

:::zone-end

## Create an index for Margie's Travel

The index for the Margie's Travel solution must contain fields that can be used to search for information in brochures and customer reviews. Choose your preferred language at the top of this page, and then follow the steps below to create an index for the Margie's Travel search solution.

:::zone pivot="csharp"

To create an index using C#, you must implement a class that represents the index, including all of its fields.

1. In the **C-Sharp/create-index** folder, open the **MargiesIndex.cs** code file and view the code it contains. This code defines a class for the index, including the following fields:
    - **id**: A unique identifier for each indexed document.
    - **url**: The URL link for the indexed document.
    - **file_name**: The file name of the document.
    - **author**: The author of the document.
    - **content**: The text content of the document.
    - **size**: The size (in bytes) of the document file.
    - **last_modified**: The date and time the document was last updated.
2. Observe that each field in the index has several *attributes* that control its usage. These attributes include:
    - **key**: Fields that define a unique key for index records.
    - **searchable**: Fields that can be queried using full-text search.
    - **filterable**: Fields that can be included in filter expressions to return only documents that match specified constraints.
    - **sortable**: Fields that can be used to order the results.
    - **facetable**: Fields that can be used to determine values for *facets* (user interface elements used to filter the results based on a list of known field values).
    - **retrievable**: Fields that can be included in search results (*by default, all fields are retrievable, so even though this attribute is omitted in the code, all of the index fields will be implicitly retrievable.*).
3. Open the **Program.cs** code file and review the code in the **CreateIndex** function, which creates an index named **margies-index-cs** based on the **MargiesIndex** class.
4. In the **Terminal** pane, select the bash terminal for the **create-index** folder. If you have closed this terminal, right-click (Ctrl+click if using a Mac) the **C-Sharp/create-index** folder and select **Open in Integrated Terminal**.
5. In the terminal for the **create-index** folder, enter the following command:
    ```bash
    dotnet run
    ```
6. When prompted, press **2** to create an index. Then wait while the program creates the index.
7. When the prompt is redisplayed, press **q** to quit the program.
8. Open your search service in the [Azure portal](https://portal.azure.com?portal=true) and view its **Indexes** tab to confirm that the index has been created.

:::zone-end

:::zone pivot="python"

To create an index using Python, you must use the **indexes** REST endpoint. You can submit an HTTP *PUT* request to create or update an index based on a JSON document that defines the index schema.

1. In the **Python/create-index** folder, open the **index.json** file. This file contains the JSON definition of an index.
2. Review the index definition. It includes the following fields:
    - **id**: A unique identifier for each indexed document.
    - **url**: The URL link for the indexed document.
    - **file_name**: The file name of the document.
    - **author**: The author of the document.
    - **content**: The text content of the document.
    - **size**: The size (in bytes) of the document file.
    - **last_modified**: The date and time the document was last updated.
3. Observe that each field in the index has several *attributes* that control its usage. These attributes include:
    - **key**: Fields that define a unique key for index records.
    - **searchable**: Fields that can be queried using full-text search.
    - **filterable**: Fields that can be included in filter expressions to return only documents that match specified constraints.
    - **sortable**: Fields that can be used to order the results.
    - **facetable**: Fields that can be used to determine values for *facets* (user interface elements used to filter the results based on a list of known field values).
    - **retrievable**: Fields that can be included in search results (*by default, all fields are retrievable, so even though this attribute is omitted in the JSON, all of the index fields will be implicitly retrievable.*)
4. In the **Terminal** pane, select the bash terminal for the **create-index** folder. If you have closed this terminal, right-click (Ctrl+click if using a Mac) the **Python/create-index** folder and select **Open in Integrated Terminal**.
5. In the terminal for the **create-index** folder, enter the following command:
    ```bash
    python3 submit-rest.py 'PUT' 'indexes/margies-index-py' 'index.json'
    ```
6. Wait while Python runs the **submit-rest&#46;py** script, causing it to submit an HTTP PUT request to the *indexes* REST endpoint, adding an index named *margies-index-py* based on the JSON body defined in the *index.json* file. The use of a PUT request ensures that if the index already exists, it is updated based on the JSON; otherwise it is created.
7. Review the JSON response that is returned from the REST interface.
8. Open your search service in the [Azure portal](https://portal.azure.com?portal=true) and view its **Indexes** tab to confirm that the index has been created.

:::zone-end

## Create and run an indexer for Margie's Travel

The indexer for the Margie's Travel search solution must map the metadata fields and content from the documents in the data store to the fields in the index. Select your preferred language at the top of this page, and then follow the steps below to create and run an indexer for the Margie's Travel search solution.

:::zone pivot="csharp"

To create an indexer, you can use the **Create** method of the **SearchServiceClient**'s **Indexers** member. When you initially create an indexer, it runs to populate the index. Alternatively, you can include a **schedule** in the indexer definition that will cause the indexer to run periodically.

Indexing is an asynchronous operation. To check the status of an indexer, you use the **GetStatus** method of the **SearchServiceClient**'s **Indexers** member.

1. In the **C-Sharp/create-index** folder, open the **Program.cs** file and review the code in the **CreateIndexer** function, which creates an indexer that maps the metadata fields from the documents in the data source to the index fields.
2. Review the code in the **CheckIndexerOverallStatus** function, which retrieves the indexer status.
3. In the **Terminal** pane, select the bash terminal for the **create-index** folder. If you have closed this terminal, right-click (Ctrl+click if using a Mac) the **C-Sharp/create-index** folder and select **Open in Integrated Terminal**.
4. In the terminal for the **create-index** folder, enter the following command:
    ```bash
    dotnet run
    ```
5. When prompted, press **3** to create and run an indexer. Then wait while the program creates the indexer and then retrieves it status.
6. When the prompt is redisplayed, press **q** to quit the program.
7. Open your search service in the [Azure portal](https://portal.azure.com?portal=true) and view its **Indexers** tab to confirm that the indexer has been created and has processed 72 documents.

:::zone-end

:::zone pivot="python"

To create an indexer with Python, you need to submit a request to the **indexers** REST endpoint with the name of the indexer. The body of the request must be a JSON document that defines the indexer.

The first time you submit a *PUT* request with an indexer definition, the index is created and run automatically to initialize the index. Subsequent *PUT* requests will update the indexer without running it. You must explicitly submit a request to the indexer's **run** endpoint to rerun the indexer. Alternatively, you can include a **schedule** in the indexer definition that will cause the indexer to run periodically.

Indexing is an asynchronous operation. To check the status of an indexer, you can submit a *GET* request to the indexer's **status** endpoint.

1. In the **Python/create-index** folder, open the **indexer.json** file. This file contains the JSON definition of an indexer.
2. Review the indexer definition. It defines an indexer that maps fields from the *margies-docs-py* data source to the *margies-index-py* index. The source fields are standard fields that are extracted from blob data sources based on file metadata and the file contents after Azure Cognitive Search has performed the required document cracking to the PDF files to extract their content.
3. In the **Terminal** pane, select the bash terminal for the **create-index** folder. If you have closed this terminal, right-click (CTRL+click if using a Mac) the **Python/create-index** folder and select **Open in Integrated Terminal**.
4. In the terminal for the **create-index** folder, enter the following command:
    ```bash
    python3 submit-rest.py 'PUT' 'indexers/margies-indexer-py' 'indexer.json'
    ```
5. Wait while Python runs the **submit-rest&#46;py** script, causing it to submit an HTTP PUT request to the *indexers* REST endpoint, adding an indexer named *margies-indexer-py* based on the JSON body defined in the *indexer.json* file. The use of a PUT request ensures that if the indexer already exists, it is updated based on the JSON; otherwise it is created.
6. Review the JSON response that is returned from the REST interface. The indexer is created and automatically run to initialize the index.
7. In the terminal for the **create-index** folder, enter the following command:
    ```bash
    python3 submit-rest.py 'GET' 'indexers/margies-indexer-py/status' 'null'
    ```
8. Review the JSON response that is returned from the REST interface, which shows the status of the indexer. In particular, check the **status** value in the **lastResult** section of the response. If this is shown as **inProgress**, the indexer is still being applied to the index. You can rerun the previous command to retrieve the status until the last result status is **success**.
9. Open your search service in the [Azure portal](https://portal.azure.com?portal=true) and view its **Indexers** tab to confirm that the indexer has been created and has processed 72 documents.

:::zone-end

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


