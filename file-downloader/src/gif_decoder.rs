//! This is for reading GIFs as an input for re-encoding as another GIF

use gif::Decoder;
use eyre::Result;
use gifski::{Collector};

pub trait Source: Send {
  fn total_frames(&self) -> Option<u64>;
  fn collect(&mut self, dest: &mut Collector) -> Result<()>;
}

#[derive(Debug, Copy, Clone)]
pub struct Fps {
  /// output rate
  pub fps: f32,
  /// skip frames
  pub speed: f32,
}
pub struct GifDecoder<'a> {
  speed: f32,
  decoder: Decoder<&'a [u8]>,
  screen: gif_dispose::Screen,
}

impl <'a> GifDecoder <'a> {
  pub fn new(file: &'a [u8], fps: Fps) -> Result<Self> {
    let mut gif_opts = gif::DecodeOptions::new();
    gif_opts.set_color_output(gif::ColorOutput::Indexed);

    let decoder = gif_opts.read_info(file)?;
    let screen = gif_dispose::Screen::new_decoder(&decoder);

    Ok(Self {
      speed: fps.speed,
      decoder,
      screen,
    })
  }
}

impl <'a> Source for GifDecoder<'a> {
  fn total_frames(&self) -> Option<u64> { None }

  fn collect(&mut self, c: &mut Collector) -> Result<()> {
    let mut idx = 0;
    let mut delay_ts = 0;

    while let Some(frame) = self.decoder.read_next_frame()? {
      self.screen.blit_frame(frame)?;
      let pixels = self.screen.pixels.clone();
      let presentation_timestamp = f64::from(delay_ts) * (self.speed as f64 / 100.);

      c.add_frame_rgba(idx, pixels, presentation_timestamp).unwrap();
      
      idx += 1;
      delay_ts += frame.delay as u32;
    }
    Ok(())
  }
}
