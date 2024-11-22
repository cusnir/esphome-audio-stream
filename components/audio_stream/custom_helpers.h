#pragma once

#include "esphome/core/component.h"

namespace esphome {
namespace audio_stream {

class AudioHelpers {
public:
    static float calculate_rms(float* samples, size_t count) {
        if (count == 0) return 0.0f;
        float sum = 0.0f;
        for (size_t i = 0; i < count; i++) {
            sum += samples[i] * samples[i];
        }
        return sqrt(sum / count);
    }

    static float apply_calibration(float db_value, float calibration_offset) {
        return db_value + calibration_offset;
    }

    static float calculate_peak(float* samples, size_t count) {
        if (count == 0) return 0.0f;
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
        return 20 * log10(std::max(amplitude, 1e-9f));
    }

    // Add noise reduction
    static void apply_noise_reduction(float* samples, size_t count, float threshold) {
        for (size_t i = 0; i < count; i++) {
            if (std::abs(samples[i]) < threshold) {
                samples[i] = 0.0f;
            }
        }
    }

    // Add DC offset removal
    static void remove_dc_offset(float* samples, size_t count) {
        if (count == 0) return;
        float sum = 0.0f;
        for (size_t i = 0; i < count; i++) {
            sum += samples[i];
        }
        float dc_offset = sum / count;
        for (size_t i = 0; i < count; i++) {
            samples[i] -= dc_offset;
        }
    }
};

}  // namespace audio_stream
}  // namespace esphome
