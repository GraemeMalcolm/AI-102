@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

rem Set values for your subscription and resource group
set subscription_id=YOUR_SUBSCRIPTION_ID
set resource_group=YOUR_RESOURCE_GROUP
set location=YOUR_LOCATION_NAME

rem Get random numbers to create unique resource names
set unique_id=!random!!random!

echo Creating storage...
call az storage account create --name ai102form!unique_id! --subscription !subscription_id! --resource-group !resource_group! --location !location! --sku Standard_LRS --encryption-services blob --default-action Allow --output none

echo Uploading files...
rem Hack to get storage key
for /f "tokens=*" %%a in ( 
'az storage account keys list --subscription !subscription_id! --resource-group !resource_group! --account-name ai102form!unique_id! --query "[?keyName=='key1']"' 
) do ( 
set key_json=!key_json!%%a 
) 
set key_string=!key_json:[ { "keyName": "key1", "permissions": "Full", "value": "=!
set AZURE_STORAGE_KEY=!key_string:" } ]=!
call az storage container create --account-name ai102form!unique_id! --name sampleforms --public-access blob --auth-mode key --account-key %AZURE_STORAGE_KEY% --output none
call az storage blob upload-batch -d sampleforms -s ./sample-forms/train --account-name ai102form!unique_id! --auth-mode key --account-key %AZURE_STORAGE_KEY%  --output none

echo -------------------------------------
echo Storage account: ai102form!unique_id!

