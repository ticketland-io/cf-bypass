use eyre::Result;
use file_downloader::grpc_client::GrpcClient;

#[tokio::main]
async fn main() -> Result<()> {
  let mut client = GrpcClient::new("http://[::1]:50051").await?;
  let file_response = client.download_file("file_name".to_string()).await?;
  println!("{:?}", file_response);
  
  Ok(())
}
