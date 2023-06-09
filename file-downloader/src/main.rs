use std::{fs::File, io::Write};
use eyre::Result;
use futures::future::join_all;
use file_downloader::{
  grpc_client::{GrpcClient, file_server::FileResponse},
  image::{resize_img, svg_to_png},
};

async fn run(id: usize) -> Result<()> {
  println!("Running task {id}");

  for _ in 0..10 {
    let uri = "https://nft.blocto.app/aptos-blocto-lfb/blocto.png".to_string();
    // let uri = "https://art-sandbox.sunflower.industries/token/0xd58434f33a20661f186ff67626ea6bdf41b80bca/955".to_string();
    // let uri = "https://cloudflare-ipfs.com/ipfs/QmVet4B2giUTyyJ9rAkU8oRR8TcL5XRkdjcm6TVDaKjSHy".to_string();
    // let uri = "https://gateway.pinata.cloud/ipfs/QmXiSJPXJ8mf9LHijv6xFH1AtGef4h8v5VPEKZgjR4nzvM".to_string();
    let mut client = GrpcClient::new("http://[::1]:50051").await?;
    let FileResponse {mime_type, data} = client.download_file(uri).await?;

    let mut image_data = Vec::new();

    if data.len() == 0 {
      println!("Invalid html page");
    } else if mime_type == "application/json" {
      println!("JSON: {:#?}", std::str::from_utf8(&data)?);
    } else if mime_type == "image/svg+xml" {
      image_data = resize_img(svg_to_png(&data)?, "image/png")?;
    } else {
      image_data = resize_img(data, &mime_type)?;
    }

    let mut file = File::create("image.png")?;
    file.write_all(&image_data)?;

    println!("Processed task {id}");
  }

  Ok(())
}

#[tokio::main]
async fn main() -> Result<()> {
  let mut tasks = Vec::with_capacity(10);

  for id in 0..1 {
    tasks.push(tokio::spawn(run(id)));
  }

  join_all(tasks).await;
  
  Ok(())
}
