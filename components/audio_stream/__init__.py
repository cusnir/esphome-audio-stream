"""AudioStream component for ESPHome."""

import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import i2s_audio
from esphome.const import CONF_ID

DEPENDENCIES = ['i2s_audio']
AUTO_LOAD = ['i2s_audio']
MULTI_CONF = True

CONF_I2S_AUDIO_ID = 'i2s_audio_id'
CONF_WEBSOCKET_SERVER = 'websocket_server'
CONF_BUFFER_SIZE = 'buffer_size'
CONF_DEBUG_MODE = 'debug_mode'

# Define our own I2S configuration constants
CONF_WS_PIN = "ws_pin"
CONF_BCK_PIN = "bck_pin"
CONF_DIN_PIN = "din_pin"
CONF_SAMPLE_RATE = "sample_rate"
CONF_BITS_PER_SAMPLE = "bits_per_sample"
CONF_DMA_BUF_COUNT = "dma_buf_count"
CONF_DMA_BUF_LEN = "dma_buf_len"
CONF_USE_APLL = "use_apll"
CONF_CHANNEL = "channel"

audio_stream_ns = cg.esphome_ns.namespace('audio_stream')
AudioStream = audio_stream_ns.class_('AudioStream', cg.Component)

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(AudioStream),
    cv.Required(CONF_I2S_AUDIO_ID): cv.use_id(i2s_audio.I2SAudio),
    cv.Required(CONF_WEBSOCKET_SERVER): cv.string,
    cv.Optional(CONF_BUFFER_SIZE, default=1024): cv.positive_int,
    cv.Optional(CONF_DEBUG_MODE, default=False): cv.boolean,
}).extend(cv.COMPONENT_SCHEMA)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)

    i2s = await cg.get_variable(config[CONF_I2S_AUDIO_ID])
    cg.add(var.set_i2s_audio(i2s))
    cg.add(var.set_websocket_server(config[CONF_WEBSOCKET_SERVER]))
    cg.add(var.set_buffer_size(config[CONF_BUFFER_SIZE]))
    cg.add(var.set_debug_mode(config[CONF_DEBUG_MODE]))
