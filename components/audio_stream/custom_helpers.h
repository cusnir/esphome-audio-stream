#pragma once

#include "esphome/core/component.h"

namespace esphome {
namespace audio_stream {

// Audio processing helpers
class AudioHelpers {
public:
    static float calculate_rms(float* samples, size_t count) {
        float sum = 0.0f;
        for (size_t i = 0; i < count; i++) {
            sum += samples[i] * samples[i];
        }
        return sqrt(sum / count);
    }

    static float apply_calibration(float db_value, float calibration_offset) {
        return db_value + calibration_offset;
    }

    // Add more audio processing helpers as needed
    static float calculate_peak(float* samples, size_t count) {
        float peak = 0.0f;
        for (size_t i = 0; i < count; i++) {
            peak = std::max(peak, std::abs(samples[i]));
        }
        return peak;
    }

    static float db_to_amplitude(float db) {
        return pow(10, db / 20.0);
    }

    static float amplitude_to_db(float amplitude) {
        return 20 * log10(amplitude);
    }
};

}  // namespace audio_stream
}  // namespace esphome
