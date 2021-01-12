import os
from azure.core.exceptions import ResourceNotFoundError
from azure.ai.formrecognizer import FormRecognizerClient
from azure.ai.formrecognizer import FormTrainingClient
from azure.core.credentials import AzureKeyCredential

endpoint = "<paste-your-form-recognizer-endpoint-here>"
key = "<paste-your-form-recognizer-key-here>"

form_recognizer_client = FormRecognizerClient(endpoint, AzureKeyCredential(key))
form_training_client = FormTrainingClient(endpoint, AzureKeyCredential(key))

#### Change formUrl 
formUrl = "https://raw.githubusercontent.com/Azure/azure-sdk-for-python/master/sdk/formrecognizer/azure-ai-formrecognizer/tests/sample_forms/forms/Form_1.jpg"

poller = form_recognizer_client.begin_recognize_content_from_url(formUrl)
page = poller.result()

table = page[0].tables[0] # page 1, table 1
print("Table found on page {}:".format(table.page_number))
for cell in table.cells:
    print("Cell text: {}".format(cell.text))
    print("Location: {}".format(cell.bounding_box))
    print("Confidence score: {}\n".format(cell.confidence))

# Model ID from when you trained your model.
model_id = "<your custom model id>"

poller = form_recognizer_client.begin_recognize_custom_forms_from_url(
    model_id=model_id, form_url=formUrl)
result = poller.result()

for recognized_form in result:
    print("Form type: {}".format(recognized_form.form_type))
    for name, field in recognized_form.fields.items():
        print("Field '{}' has label '{}' with value '{}' and a confidence score of {}".format(
            name,
            field.label_data.text if field.label_data else name,
            field.value,
            field.confidence
        ))


## Uncomment to check the number of models in your Form Recognizer account
# account_properties = form_training_client.get_account_properties()
# print("Our account has {} custom models, and we can have at most {} custom models".format(
#     account_properties.custom_model_count, account_properties.custom_model_limit
# ))

## Uncomment to list the models currently stored in the resource account 
# # Next, we get a paged list of all of our custom models
# custom_models = form_training_client.list_custom_models()

# print("We have models with the following ids:")

# # Let's pull out the first model
# first_model = next(custom_models)
# print(first_model.model_id)
# for model in custom_models:
#     print(model.model_id)

## Uncomment to get a specific model using the model's ID 
# model_id = "<model_id from the Train a Model sample>"

# custom_model = form_training_client.get_custom_model(model_id=model_id)
# print("Model ID: {}".format(custom_model.model_id))
# print("Status: {}".format(custom_model.status))
# print("Training started on: {}".format(custom_model.training_started_on))
# print("Training completed on: {}".format(custom_model.training_completed_on))

## Uncomment to delete a model from the resource account 
# form_training_client.delete_model(model_id=custom_model.model_id)

# try:
#     form_training_client.get_custom_model(model_id=custom_model.model_id)
# except ResourceNotFoundError:
#     print("Successfully deleted model with id {}".format(custom_model.model_id))