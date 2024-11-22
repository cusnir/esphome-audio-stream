"""AudioStream component for ESPHome."""

import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.const import CONF_ID

DEPENDENCIES = ['i2s_audio']
AUTO_LOAD = ['i2s_audio']

CONF_AUDIO_STREAM_ID = 'audio_stream_id'
