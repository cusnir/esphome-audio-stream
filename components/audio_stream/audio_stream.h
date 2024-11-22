#pragma once

#include "esphome/core/component.h"
#include "esphome/components/i2s_audio/i2s_audio.h"
#include <WebSocketsClient.h>
#include "custom_helpers.h"

namespace esphome {
namespace audio_stream {

class AudioStream : public Component {
 public:
  void set_i2s_audio(i2s_audio::I2SAudio *i2s) { i2s_ = i2s; }
  void set_websocket_server(const std::string &url) { websocket_server_ = url; }
  void set_buffer_size(size_t size) { buffer_size_ = size; }
  void set_debug_mode(bool debug) { debug_mode_ = debug; }

  void init_i2s(std::map<std::string, int> config) {
    i2s_config_ = config;
    needs_i2s_init_ = true;
  }

  void calibrate(float reference_db) {
    calibration_offset_ = reference_db - AudioHelpers::calculate_rms(buffer_.data(), buffer_.size());
  }

  void setup() override;
  void loop() override;
  float get_setup_priority() const override { return setup_priority::HARDWARE; }
  bool is_connected() const { return websocket_connected_; }

  // Recording control methods
  void start_recording() { is_recording_ = true; }
  void stop_recording() { is_recording_ = false; }
  bool is_recording() const { return is_recording_; }

 protected:
  i2s_audio::I2SAudio *i2s_{nullptr};
  std::string websocket_server_;
  size_t buffer_size_{1024};
  bool debug_mode_{false};
  bool needs_i2s_init_{false};
  bool websocket_connected_{false};
  bool is_recording_{false};
  float calibration_offset_{0.0f};
  std::map<std::string, int> i2s_config_;

  WebSocketsClient webSocket;
  std::vector<int32_t> buffer_;

  void setup_i2s_();
  void handle_audio_data_();
  void websocket_event_(WStype_t type, uint8_t * payload, size_t length);

  // Audio processing methods
  float calculate_audio_level_() {
    return AudioHelpers::calculate_rms(buffer_.data(), buffer_.size());
  }

  float get_calibrated_level_(float raw_level) {
    return AudioHelpers::apply_calibration(raw_level, calibration_offset_);
  }

  float calculate_peak_() {
    return AudioHelpers::calculate_peak(buffer_.data(), buffer_.size());
  }
};

}  // namespace audio_stream
}  // namespace esphome
