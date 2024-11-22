"""AudioStream component for ESPHome."""

import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import i2s_audio
from esphome.const import CONF_ID
from esphome.components.sound_level_meter import (
    CONF_WS_PIN,
    CONF_BCK_PIN,
    CONF_DIN_PIN,
    CONF_SAMPLE_RATE,
    CONF_BITS_PER_SAMPLE,
    CONF_DMA_BUF_COUNT,
    CONF_DMA_BUF_LEN,
    CONF_USE_APLL,
    CONF_CHANNEL
)

DEPENDENCIES = ['i2s_audio']
AUTO_LOAD = ['i2s_audio']
MULTI_CONF = True

CONF_I2S_AUDIO_ID = 'i2s_audio_id'
CONF_WEBSOCKET_SERVER = 'websocket_server'
CONF_BUFFER_SIZE = 'buffer_size'
CONF_DEBUG_MODE = 'debug_mode'

audio_stream_ns = cg.esphome_ns.namespace('audio_stream')
AudioStream = audio_stream_ns.class_('AudioStream', cg.Component)

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(AudioStream),
    cv.Optional(CONF_I2S_AUDIO_ID): cv.use_id(i2s_audio.I2SAudio),
    cv.Required(CONF_WEBSOCKET_SERVER): cv.string,
    cv.Optional(CONF_BUFFER_SIZE, default=1024): cv.positive_int,
    cv.Optional(CONF_DEBUG_MODE, default=False): cv.boolean,
    cv.Optional(CONF_WS_PIN): cv.int_,
    cv.Optional(CONF_BCK_PIN): cv.int_,
    cv.Optional(CONF_DIN_PIN): cv.int_,
    cv.Optional(CONF_SAMPLE_RATE, default=16000): cv.positive_int,
    cv.Optional(CONF_BITS_PER_SAMPLE, default=32): cv.one_of(16, 24, 32, int=True),
    cv.Optional(CONF_CHANNEL, default="left"): cv.one_of("left", "right", "stereo", lower=True),
    cv.Optional(CONF_DMA_BUF_COUNT, default=8): cv.positive_int,
    cv.Optional(CONF_DMA_BUF_LEN, default=1024): cv.positive_int,
    cv.Optional(CONF_USE_APLL, default=False): cv.boolean,
}).extend(cv.COMPONENT_SCHEMA)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)

    if CONF_I2S_AUDIO_ID in config:
        i2s = await cg.get_variable(config[CONF_I2S_AUDIO_ID])
        cg.add(var.set_i2s_audio(i2s))
    else:
        # If no I2S audio ID provided, create new I2S configuration
        i2s_config = {
            CONF_WS_PIN: config[CONF_WS_PIN],
            CONF_BCK_PIN: config[CONF_BCK_PIN],
            CONF_DIN_PIN: config[CONF_DIN_PIN],
            CONF_SAMPLE_RATE: config[CONF_SAMPLE_RATE],
            CONF_BITS_PER_SAMPLE: config[CONF_BITS_PER_SAMPLE],
            CONF_CHANNEL: config[CONF_CHANNEL],
            CONF_DMA_BUF_COUNT: config[CONF_DMA_BUF_COUNT],
            CONF_DMA_BUF_LEN: config[CONF_DMA_BUF_LEN],
            CONF_USE_APLL: config[CONF_USE_APLL],
        }
        cg.add(var.init_i2s(i2s_config))

    cg.add(var.set_websocket_server(config[CONF_WEBSOCKET_SERVER]))
    cg.add(var.set_buffer_size(config[CONF_BUFFER_SIZE]))
    cg.add(var.set_debug_mode(config[CONF_DEBUG_MODE]))
