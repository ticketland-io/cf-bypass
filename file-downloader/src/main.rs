use eyre::Result;
use file_downloader::{
  grpc_client::GrpcClient, image::resize_gif,
};

#[tokio::main]
async fn main() -> Result<()> {
  let uri = "https://nft.blocto.app/aptos-blocto-lfb/blocto.png".to_string();
  let mut client = GrpcClient::new("http://[::1]:50051").await?;
  let file_response = client.download_file(uri).await?;

  if file_response.data.len() == 0 {
    println!("Invalid html page");
  } else {
    resize_gif(file_response.data).await?;
  }

  
  Ok(())
}
