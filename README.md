# ESPHome Audio Stream Component

An ESPHome component for streaming audio data over WebSocket from I2S microphones.

## Features
- I2S microphone support
- WebSocket streaming
- Configurable buffer size
- Debug mode
- Integration with ESPHome's I2S audio component

## Installation

Add this external component to your ESPHome configuration:

```yaml
external_components:
  - source: github://cusnir/esphome-audio-stream@main
    components: [ audio_stream ]
```

## Configuration

Example configuration:

```yaml
i2s_audio:
  id: i2s_audio_id
  i2s_lrclk_pin: 11
  i2s_bclk_pin: 12
  i2s_din_pin: 10
  sample_rate: 16000

audio_stream:
  i2s_audio_id: i2s_audio_id
  websocket_server: "ws://your_server:3000"
  buffer_size: 512
  debug_mode: true
```

## Configuration variables

- **i2s_audio_id** (*Required*, ID): The ID of the I2S audio component
- **websocket_server** (*Required*, string): WebSocket server URL
- **buffer_size** (*Optional*, int): Size of the audio buffer. Default: 512
- **debug_mode** (*Optional*, bool): Enable debug logging. Default: false

## Dependencies
- ESPHome 2023.12.0 or newer
- ESP32 board with I2S support

## Example Projects
- Audio streaming server
- Sound level monitoring
- Voice recording

## License
GNU General Public License v3.0
