# By @Krishna_Singhal

import os

from userge import userge, Message, Config, logging
from userge.utils import get_import_path
from userge.plugins import ROOT

PLUGINS_CHAT_ID = int(os.environ.get("PLUGINS_CHAT_ID", 0))
_CHANNEL = userge.getCLogger(__name__)
_LOG = logging.getLogger(__name__)


@userge.on_cmd(
    'loadall', about={
        'header': "load all plugins from plugins Channel.",
        'usage': "{tr}loadall"
    }
)
async def loadall(msg: Message) -> None:
    if not PLUGINS_CHAT_ID:
        await msg.edit("Add `PLUGINS_CHAT_ID` var to Load Plugins from Plugins Channel")
        return
    await msg.edit("`Loading All Plugin(s)...`")
    success, total, p_error = await load_all_plugins()
    if success:
        if success == total:
            await msg.edit('`Loaded all Plugin(s)`')
        else:
            await msg.edit(
                f'`{success} Plugin(s) loaded from {total}`\n__see log channel for more info__')
            await _CHANNEL.log(p_error)
    else:
        await msg.edit(f'`0 Plugin(s) loaded from {total}`\n__see log channel for more info__')
        await _CHANNEL.log(p_error)


async def load_all_plugins():
    success = 0
    total = 0
    p_error = ''
    async for _file in userge.search_messages(
        PLUGINS_CHAT_ID, filter="document"
    ):
        total += 1
        file_ = _file.document
        if file_.file_name.endswith('.py') and file_.file_size < 2 ** 20:
            if not os.path.isdir(Config.TMP_PATH):
                os.makedirs(Config.TMP_PATH)
            t_path = os.path.join(Config.TMP_PATH, file_.file_name)
            if os.path.isfile(t_path):
                os.remove(t_path)
            await _file.download(file_name=t_path)
            plugin = get_import_path(ROOT, t_path)
            try:
                await userge.load_plugin(plugin, reload_plugin=True)
                await userge.finalize_load()
            except (ImportError, SyntaxError, NameError) as i_e:
                os.remove(t_path)
                p_error += f'\n\n**PLUGIN:** `{file_.file_name}`\n**ERROR:** `{i_e}`'
            else:
                success += 1
                _LOG.info(f"Loaded {plugin}")
    return (success, total, p_error)
