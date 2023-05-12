use eyre::Result;
use tonic::{transport::{Channel}};
use file_server::file_downloader_client::FileDownloaderClient;
use file_server::{Request, FileResponse};

pub mod file_server {
  tonic::include_proto!("file_server");
}

#[derive(Clone, Debug)]
pub struct GrpcClient {
  client: FileDownloaderClient<Channel>,
}

impl GrpcClient {
  pub async fn new<S: AsRef<str>>(uri: S) -> Result<Self> {
    let uri = uri
    .as_ref()
    .parse::<String>()
    .expect("the url should have been validated by now, so it is a valid Uri");

    let client = FileDownloaderClient::connect(uri).await?;

    Ok(Self {client})
  }

  pub async fn download_file(&mut self, uri: String) -> Result<FileResponse> {
    let request = tonic::Request::new(Request {uri});
    let response = self.client.download_file(request).await?;

    Ok(response.into_inner())
  }
}
