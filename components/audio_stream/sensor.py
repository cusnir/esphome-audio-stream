import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import i2s_audio
from esphome.const import CONF_ID

DEPENDENCIES = ['i2s_audio']
AUTO_LOAD = ['i2s_audio']

audio_stream_ns = cg.esphome_ns.namespace('audio_stream')
AudioStream = audio_stream_ns.class_('AudioStream', cg.Component)

CONF_I2S_AUDIO_ID = 'i2s_audio_id'
CONF_WEBSOCKET_SERVER = 'websocket_server'
CONF_BUFFER_SIZE = 'buffer_size'
CONF_DEBUG_MODE = 'debug_mode'

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(AudioStream),
    cv.Required(CONF_I2S_AUDIO_ID): cv.use_id(i2s_audio.I2SAudio),
    cv.Required(CONF_WEBSOCKET_SERVER): cv.string,
    cv.Optional(CONF_BUFFER_SIZE, default=512): cv.positive_int,
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
