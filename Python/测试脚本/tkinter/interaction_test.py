from __future__ import print_function
from __future__ import unicode_literals

import logging

from prompt_toolkit import *
from prompt_toolkit.history import FileHistory  # 保存历史命令
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory  # 从历史记录中自动提示命令
from prompt_toolkit.contrib.completers import *


BaseCompleter = SystemCompleter()  # 系统指令自动补全


def main_task():
    """
    主程序启动，监听用户输入
    :return:
    """
    while True:
        session = PromptSession()

        text1 = session.prompt(u'>> ', auto_suggest=AutoSuggestFromHistory(), completer=BaseCompleter)
        text2 = session.prompt(u'>> ', auto_suggest=AutoSuggestFromHistory(), completer=BaseCompleter)
        user_input = prompt(u'>> ', history=FileHistory("../mqtt/remote_debug/test/history.txt"),
                            auto_suggest=AutoSuggestFromHistory(), completer=BaseCompleter)
        user_input1 = prompt(u'>> ', history=FileHistory("../mqtt/remote_debug/test/history.txt"),
                             auto_suggest=AutoSuggestFromHistory(), completer=BaseCompleter)
        print(user_input)
        print(user_input1)
        print(text1)
        print(text2)

        if text1.strip().lower() == "exit" or text2.strip().lower() == "exit":
            break


        #
        # # 如果输入 exit， 则退出
        # if user_input.strip().lower() == "exit":
        #     break


if __name__ == "__main__":
    main_task()
