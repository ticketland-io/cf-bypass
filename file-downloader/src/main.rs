use eyre::Result;
use file_downloader::grpc_client::GrpcClient;

#[tokio::main]
async fn main() -> Result<()> {
  let uri = "https://gateway.pinata.cloud/ipfs/QmXiSJPXJ8mf9LHijv6xFH1AtGef4h8v5VPEKZgjR4nzvM".to_string();
  let mut client = GrpcClient::new("http://[::1]:50051").await?;
  let file_response = client.download_file(uri).await?;
  
  println!("{:?}", file_response);
  
  Ok(())
}
