use std::{
  thread, io::{Cursor}, num::NonZeroU32, time::Instant,
};
use eyre::{Result, Report, ContextCompat};
use gifski::{Settings, Repeat, progress::NoProgress};
use crate::{
  gif_decoder::{GifDecoder, Fps, Source},
};
use webp::Encoder as WebPEncoder;
use usvg::{fontdb, TreeParsing, TreeTextToPath};
use image::{
  io::{Reader as ImageReader}, ColorType, ImageEncoder,
  codecs::{
    png::PngEncoder, jpeg::JpegEncoder, bmp::BmpEncoder,
  }
};

use fast_image_resize as fr;

fn can_resize(mime_type: &str) -> bool {
  mime_type == "image/png" ||
  mime_type == "image/jpeg" ||
  mime_type == "image/bpm" ||
  mime_type == "image/webp" ||
  mime_type == "image/gif" ||
  mime_type == "image/svg+xml"
}

pub fn resize_img(original_img: Vec<u8>, mime_type: &str) -> Result<Vec<u8>> {
  // If it's not an image type we can just return the original file
  if !can_resize(mime_type) {
    return Ok(original_img)
  };

  if mime_type == "image/gif" {
    return resize_gif(original_img)
  }

  let start = Instant::now();
  let img = ImageReader::new(Cursor::new(original_img)).with_guessed_format()?.decode()?;
  let width = NonZeroU32::new(img.width()).context("width read")?;
  let height = NonZeroU32::new(img.height()).context("height read")?;
  let src_image = fr::Image::from_vec_u8(
    width,
    height,
    img.to_rgba8().into_raw(),
    fr::PixelType::U8x4,
  )?;

  // Create container for data of destination image
  let dst_width = NonZeroU32::new(512).unwrap();
  let dst_height = NonZeroU32::new(512).unwrap();
  let mut dst_image = fr::Image::new(
    dst_width,
    dst_height,
    src_image.pixel_type(),
  );

  // Get mutable view of destination image data
  let mut dst_view = dst_image.view_mut();

  // Create Resizer instance and resize source image into buffer of destination image
  let mut resizer = fr::Resizer::new(fr::ResizeAlg::Convolution(fr::FilterType::Box));
  resizer.resize(&src_image.view(), &mut dst_view).unwrap();

  let mut resized_img = Vec::new();
  
  match mime_type {
    "image/png" => {
      PngEncoder::new(&mut resized_img)
      .write_image(
        dst_image.buffer(),
        dst_width.get(),
        dst_height.get(),
        ColorType::Rgba8,
      )?;
    },
    "image/jpeg" => {
      JpegEncoder::new(&mut resized_img)
      .write_image(
        dst_image.buffer(),
        dst_width.get(),
        dst_height.get(),
        ColorType::Rgba8,
      )?;
    },
    "image/webp" => {
      resized_img = WebPEncoder::from_rgba(
        dst_image.buffer(),
        dst_width.get(),
        dst_height.get(),
      )
      .encode_lossless()
      .to_vec();
    },
    "image/bmp" => {
      BmpEncoder::new(&mut resized_img)
      .write_image(
        dst_image.buffer(),
        dst_width.get(),
        dst_height.get(),
        ColorType::Rgba8,
      )?;
    },
    // This should never happen because we check the mime types in the beginning of the function
    _ => panic!("Unsupported image type"),
  };
  
  let duration = start.elapsed();
  println!("Img resize time: {:?}", duration);
  
  Ok(resized_img)
}

pub fn is_svg(buf: &[u8]) -> bool {
  buf.len() > 4 && buf[0] == b'<' && buf[1] == b's' && buf[2] == b'v' && buf[3] == b'g'
}

pub fn svg_to_png(svg_data: &[u8]) -> Result<Vec<u8>> {
  let start = Instant::now();
  let opt = usvg::Options::default();
  let mut fontdb = fontdb::Database::new();
  fontdb.load_system_fonts();
  
  let mut tree = usvg::Tree::from_data(&svg_data, &opt)?;
  tree.convert_text(&fontdb);

  let pixmap_size = tree.size.to_screen_size();
  let mut pixmap = tiny_skia::Pixmap::new(pixmap_size.width(), pixmap_size.height()).context("svg render error")?;
  
  resvg::render(
    &tree,
    resvg::FitTo::Original,
    tiny_skia::Transform::default(),
    pixmap.as_mut(),
  ).context("svg render error")?;

  let duration = start.elapsed();
  println!("svg-to-png time: {:?}", duration);

  Ok(pixmap.encode_png()?)
}

pub fn resize_gif(original_img: Vec<u8>) -> Result<Vec<u8>> {
  let start = Instant::now();
  let rate = Fps {fps: 10.0, speed: 1.0};
  let settings = Settings {
    width: Some(512),
    height: Some(512),
    quality: 50,
    fast: false,
    repeat: Repeat::Infinite,
  };
  let (mut collector, mut writer) = gifski::new(settings)?;

  #[allow(deprecated)]
  writer.set_motion_quality(50);
  #[allow(deprecated)]
  writer.set_lossy_quality(30);

  let decode_thread = thread::Builder::new().name("decode".into()).spawn(move || {
    let mut decoder = GifDecoder::new(&original_img, rate)?;
    decoder.collect(&mut collector)
  })?;

  let mut resized_img = Vec::new();
  let mut nopb = NoProgress {};

  writer.write(&mut resized_img, &mut nopb)?;
  decode_thread.join().map_err(|_| "thread died?").map_err(|error| Report::msg(format!("{:?}", error.to_string())))??;

  let duration = start.elapsed();
  println!("GIF resize time: {:?}", duration);

  Ok(resized_img)
}
