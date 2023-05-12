use eyre::Result;
use file_downloader::{
  grpc_client::GrpcClient, image::resize_gif,
};

#[tokio::main]
async fn main() -> Result<()> {
  let uri = "https://gateway.pinata.cloud/ipfs/QmXiSJPXJ8mf9LHijv6xFH1AtGef4h8v5VPEKZgjR4nzvM".to_string();
  let mut client = GrpcClient::new("http://[::1]:50051").await?;
  let file_response = client.download_file(uri).await?;

  if file_response.data.len() == 0 {
    println!("Invalid html page");
  } else {
    resize_gif(file_response.data).await?;
  }

  
  Ok(())
}
