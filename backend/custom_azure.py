from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    account_name = 'tarkovblob' # Must be replaced by your <storage_account_name>
    account_key = '/bclC+eBREHsnNL/lhXC3+p68/GoBHdHL/WBpcFTbGxCfjTQiz3nqNV3h1MgXY8oxckyRQ+Ym1AntDum8k3TSg==' # Must be replaced by your <storage_account_key>
    azure_container = 'media'
    expiration_secs = None

class AzureStaticStorage(AzureStorage):
    account_name = 'tarkovblob' # Must be replaced by your storage_account_name
    account_key = '/bclC+eBREHsnNL/lhXC3+p68/GoBHdHL/WBpcFTbGxCfjTQiz3nqNV3h1MgXY8oxckyRQ+Ym1AntDum8k3TSg==' # Must be replaced by your <storage_account_key>
    azure_container = 'static'
    expiration_secs = None