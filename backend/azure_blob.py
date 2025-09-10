from azure.storage.blob import BlobServiceClient, ContentSettings
from config import Config
import uuid

_blob_service = None


def get_blob_service():
    global _blob_service
    if _blob_service is None:
        conn_str = f"DefaultEndpointsProtocol=https;AccountName={Config.AZURE_ACCOUNT_NAME};AccountKey={Config.AZURE_ACCOUNT_KEY};EndpointSuffix=core.windows.net"
        _blob_service = BlobServiceClient.from_connection_string(conn_str)
    return _blob_service


def upload_file_stream(file_stream, filename, content_type=None):
    service = get_blob_service()
    container = Config.AZURE_CONTAINER
    blob_name = f"attachments/{uuid.uuid4().hex}_{filename}"
    blob_client = service.get_blob_client(container=container, blob=blob_name)
    content_settings = None
    if content_type:
        content_settings = ContentSettings(content_type=content_type)
    blob_client.upload_blob(
        file_stream, overwrite=True, content_settings=content_settings
    )
    url = blob_client.url
    return url
