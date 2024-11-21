#include "audio_stream.h"
#include "esphome/core/log.h"

namespace esphome {
namespace audio_stream {

static const char *TAG = "audio_stream";

void AudioStream::setup() {
  if (!i2s_) {
    ESP_LOGE(TAG, "I2S Audio component not set!");
    this->mark_failed();
    return;
  }

  buffer_.resize(buffer_size_);

  // Parse WebSocket URL
  std::string host = websocket_server_.substr(5); // Remove "ws://"
  int port = 3000; // Default port

  size_t colon_pos = host.find(':');
  if (colon_pos != std::string::npos) {
    port = std::stoi(host.substr(colon_pos + 1));
    host = host.substr(0, colon_pos);
  }

  // Connect to WebSocket server
  webSocket.begin(host.c_str(), port, "/");
  webSocket.onEvent([this](WStype_t type, uint8_t * payload, size_t length) {
    this->websocket_event_(type, payload, length);
  });
  webSocket.setReconnectInterval(5000);

  ESP_LOGI(TAG, "Audio stream initialized");
}

void AudioStream::loop() {
  webSocket.loop();
  handle_audio_data_();
}

void AudioStream::handle_audio_data_() {
  size_t bytes_read = 0;
  esp_err_t err = i2s_->read_bytes(buffer_.data(), buffer_size_ * sizeof(int32_t), &bytes_read, 10);

  if (err == ESP_OK && bytes_read > 0 && webSocket.isConnected()) {
    if (debug_mode_) {
      ESP_LOGD(TAG, "Sending %d bytes", bytes_read);
    }
    webSocket.sendBIN(reinterpret_cast<uint8_t*>(buffer_.data()), bytes_read);
  }
}

void AudioStream::websocket_event_(WStype_t type, uint8_t * payload, size_t length) {
  switch(type) {
    case WStype_DISCONNECTED:
      ESP_LOGW(TAG, "WebSocket disconnected");
      break;
    case WStype_CONNECTED:
      ESP_LOGI(TAG, "WebSocket connected");
      break;
    case WStype_ERROR:
      ESP_LOGE(TAG, "WebSocket error");
      break;
    default:
      break;
  }
}

}  // namespace audio_stream
}  // namespace esphome
