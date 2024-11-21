#pragma once

#include "esphome/core/component.h"
#include "esphome/components/i2s_audio/i2s_audio.h"
#include <WebSocketsClient.h>

namespace esphome {
namespace audio_stream {

class AudioStream : public Component {
 public:
  void set_i2s_audio(i2s_audio::I2SAudio *i2s) { i2s_ = i2s; }
  void set_websocket_server(const std::string &url) { websocket_server_ = url; }
  void set_buffer_size(size_t size) { buffer_size_ = size; }
  void set_debug_mode(bool debug) { debug_mode_ = debug; }

  void setup() override;
  void loop() override;
  float get_setup_priority() const override { return setup_priority::AFTER_WIFI; }

 protected:
  i2s_audio::I2SAudio *i2s_{nullptr};
  std::string websocket_server_;
  size_t buffer_size_{512};
  bool debug_mode_{false};

  WebSocketsClient webSocket;
  std::vector<int32_t> buffer_;

  void handle_audio_data_();
  void websocket_event_(WStype_t type, uint8_t * payload, size_t length);
};

}  // namespace audio_stream
}  // namespace esphome
