use std::{
  fs::{File}, io::{Write}, thread
};
use eyre::Result;
use gifski::{Settings, Repeat, progress::NoProgress};
use crate::{
  gif_decoder::{GifDecoder, Fps, Source},
};

pub async fn resize_gif(image: Vec<u8>) -> Result<()> {
  let rate = Fps {fps: 10.0, speed: 1.0};
  let settings = Settings {
    width: Some(512),
    height: Some(512),
    quality: 50,
    fast: false,
    repeat: Repeat::Infinite,
  };

  let (mut collector, mut writer) = gifski::new(settings)?;

  writer.set_motion_quality(50);
  writer.set_lossy_quality(30);

  let decode_thread = thread::Builder::new().name("decode".into()).spawn(move || {
    let mut decoder = GifDecoder::new(&image, rate)?;
    decoder.collect(&mut collector)
  })?;

  let mut result_buf = Vec::new();
  let mut nopb = NoProgress {};
  
  writer.write(&mut result_buf, &mut nopb)?;
  decode_thread.join().map_err(|_| "thread died?").unwrap()?;

  let mut file = File::create("nft_resized.gif")?;
  file.write_all(&result_buf)?;

  Ok(())
}
