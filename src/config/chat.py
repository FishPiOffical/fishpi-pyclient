class ChatConfig(object):
    def __init__(self, blacklist: list[str] = [], kw_notification: list[str] = [], kw_blacklist: list[str] = ['你点的歌来了'], repeat_mode_switch=False, frequency=5, soliloquize_switch=False,
                 soliloquize_frequency=20, sentences: list[str] = [], answer_mode: bool = False, fish_ball: str = '凌 捞鱼丸',
                 chat_user_color: str | None = None, chat_content_color: str | None = None, output_mode: str = 'console', output_path: str = None):
        self.repeat_mode_switch = repeat_mode_switch
        self.frequency = frequency
        self.soliloquize_switch = soliloquize_switch
        self.soliloquize_frequency = soliloquize_frequency
        self.sentences = ['你们好！', '牵着我的手，闭着眼睛走你也不会迷路。',
                          '吃饭了没有?', '💗 爱你哟！'] + sentences
        self.blacklist = blacklist
        self.kw_blacklist = kw_blacklist
        self.kw_notification = kw_notification
        self.answer_mode = answer_mode
        self.fish_ball = fish_ball
        self.chat_user_color = chat_user_color
        self.chat_content_color = chat_content_color
        self.output_mode = output_mode
        self.output_path = output_path

    def to_config(self) -> dict:
        res = {
            'fishBall': str(self.fish_ball),
            'repeatMode': str(self.repeat_mode_switch),
            'answerMode': str(self.answer_mode),
            'repeatFrequency': str(self.frequency),
            'soliloquizeMode': str(self.soliloquize_switch),
            'soliloquizeFrequency': str(self.soliloquize_frequency),
            'sentences': '[' + ",".join('\"'+item+'\"' for item in self.sentences) + ']',
            'blacklist': '[' + ",".join('\"'+item+'\"' for item in self.blacklist) + ']',
            'kwBlacklist': '[' + ",".join('\"'+item+'\"' for item in self.kw_blacklist) + ']',
            'kwNotification': '[' + ",".join('\"'+item+'\"' for item in self.kw_notification) + ']',
            'chatUserColor': self.chat_user_color,
            'chatContentColor': self.chat_content_color,
            'outputMode': self.output_mode,
            'outputPath': self.output_path
        }

        if self.chat_user_color is None:
            res['chatUserColor'] = ''
        if self.chat_user_color is None:
            res['chatContentColor'] = ''
        return res
