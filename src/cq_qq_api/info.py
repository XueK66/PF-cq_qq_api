#=====================================================================#
import re
import json

from mcdreforged.api.event import LiteralEvent
#=====================================================================#
class QQInfo:
    PROCESS_POST_TYPE = [
        "message",
        "request", 
        "notice"
    ]

    def __init__(self, message, server, bot):
        message = message if isinstance(message, dict) else json.loads(message) 
        self.message_data = message
        self.server = server
        self.bot = bot

        # common info for all post
        self.time = message.get("time")
        self.self_id = message.get("self_id")
        self.post_type = message.get("post_type")
        
        if self.post_type not in self.PROCESS_POST_TYPE:
            return
        
        if self.post_type == "message":
            self.__process_message(message)
        elif self.post_type == "request":
            self.__process_request(message)
        elif self.post_type == "notice":
            self.__process_notice(message)
#=====================================================================#
    def __process_content(self):
        content = self.raw_message
        content = re.sub(r'\[CQ:file(?:,.*?)*\]', '[文件]', content)
        content = re.sub(r'\[CQ:image,file=.*?]', '[图片]', content)
        content = re.sub(r'\[CQ:share,file=.*?]', '[链接]', content)
        content = re.sub(r'\[CQ:face,id=.*?]', '[表情]', content)
        content = re.sub(r'\[CQ:record,file=.*?]', '[语音]', content)
        content = re.sub(r'\[CQ:video,file=.*?]', '[视频]', content)
        content = re.sub(r'\[CQ:music,type=.*?]', '[音乐]', content)
        content = re.sub(r'\[CQ:redbag,title=.*?]', '[红包]', content)
        content = re.sub(r'\[CQ:forward,id=.*?]', '[转发消息]', content)
        content = content.replace('CQ:at,qq=', '@')
        self.content = content

    def __process_message(self, message):
        self.message_type = message.get("message_type")
        self.sub_type     = message.get("sub_type")
        self.message_id   = message.get("message_id")
        self.user_id      = message.get("user_id")
        self.message      = message.get("message")
        self.raw_message  = message.get("raw_message")
        self.font         = message.get("font")
        self.sender       = message.get("sender")
        if isinstance(self.sender, dict):
            self.sender_id        = self.sender.get("user_id")
            self.sender_nickname  = self.sender.get("nickname")
            self.sender_card      = self.sender.get("card")

        self.__process_content()

        if self.message_type == 'private':
            self.source_id = self.user_id
        elif self.message_type == 'group':
            self.source_id = message.get("group_id")

        self.server.dispatch_event(
            LiteralEvent("cq_qq_api.on_qq_command"),
            (self, self.bot)
        )

        self.server.dispatch_event(
            LiteralEvent("cq_qq_api.on_qq_message"),
            (self, self.bot)
        )

    def __process_request(self, message):
        self.request_type = message.get("request_type")
        self.user_id = message.get("user_id")              # 发送请求的 QQ 号
        self.flag = message.get("flag")

        if self.request_type == "friend":                  # 加好友请求
            self.comment = message.get("comment")          # 验证信息
        elif self.request_type == "group":                 # 加群请求
            self.sub_type = message.get("sub_type")        # add、invite
            self.group_id = message.get("group_id")         
            self.comment = message.get("comment")          # 验证信息

        self.server.dispatch_event(
            LiteralEvent("cq_qq_api.on_qq_request"),
            (self, self.bot)
        )

    def __process_notice(self, message):
        self.notice_type = message.get("notice_type")
        
        if self.notice_type == "friend_recall":            # 私聊消息撤回
            self.user_id = message.get("user_id")
            self.message_id = message.get("message_id")
        
        elif self.notice_type == "friend_recall":          # 群消息撤回
            self.group_id = message.get("group_id")
            self.user_id = message.get("user_id")
            self.operator_id = message.get("operator_id")
            self.message_id = message.get("message_id")

        elif self.notice_type in ["group_increase", "group_decrease"]:         # 群成员增加/减少
            self.sub_type = message.get("sub_type")        # approve、invite/leave、kick、kick_me
            self.group_id = message.get("group_id")
            self.operator_id = message.get("operator_id")  # 操作者 QQ 号
            self.user_id  = message.get("user_id")         # 加入/离开者 QQ 号

        elif self.notice_type == "group_admin":            # 群管理员变动
            self.sub_type = message.get("sub_type")        # set、unset
            self.group_id = message.get("group_id")
            self.user_id  = message.get("user_id")         # 管理员 QQ 号

        
        elif self.notice_type == "group_upload":           # 群文件上传
            self.group_id = message.get("group_id")
            self.user_id  = message.get("user_id")         # 发送者 QQ 号
            self.file     = message.get("file")            # {id, name, size}

        elif self.notice_type == "group_admin":            # 群禁言
            self.sub_type = message.get("sub_type")        # ban、lift_ban
            self.group_id = message.get("group_id")
            self.operator_id = message.get("operator_id")  # 操作者 QQ 号
            self.user_id  = message.get("user_id")         # 被禁言 QQ 号 (为全员禁言时为0)
            self.duration = message.get("duration")        # 禁言时长, 单位秒 (为全员禁言时为-1)

        elif self.notice_type == "friend_add":             # 好友添加
            self.user_id  = message.get("user_id") 

        elif self.notice_type == "notify":                 
            self.sub_type = message.get("sub_type")        
            if self.sub_type == "poke":                    # 戳一戳
                self.user_id = message.get("user_id")      # 发送者 QQ 号
                self.target_id = message.get("target_id")  # 被戳者 QQ 号
                self.group_id  = message.get("group_id")   # 群号（如在群里发生）
            
            elif self.sub_type == "lucky_king":            # 红包运气王
                self.user_id = message.get("user_id")      # 发送者 QQ 号
                self.target_id = message.get("target_id")  # 运气王 QQ 号
                self.group_id  = message.get("group_id")   # 群号

            elif self.sub_type == "honor":                 # 群成员荣誉变更提示
                self.user_id = message.get("user_id")      # QQ 号
                self.group_id  = message.get("group_id")   # 群号
                self.honor_type = message.get("honor_type")# talkative:龙王 performer:群聊之火 emotion:快乐源泉

            elif self.sub_type == "title":                 # 群成员头衔变更
                self.user_id = message.get("user_id")      # QQ 号
                self.group_id  = message.get("group_id")   # 群号
                self.title   = message.get("title")        # 新头衔

        elif self.notice_type == "group_card":             # 群成员名片更新
            self.user_id = message.get("user_id")          # QQ 号
            self.group_id  = message.get("group_id")       # 群号
            self.card_new = message.get("card_new")        # 新名片 # 当名片为空时 card_xx 字段为空字符串, 并不是昵称
            self.card_old = message.get("card_old")        # 旧名片 # 当名片为空时 card_xx 字段为空字符串, 并不是昵称

        elif self.notice_type == "offline_file":           # 接收到离线文件
            self.user_id = message.get("user_id")
            self.file    = message.get("file")             # {name, size, url}

        elif self.notice_type == "essence":                # 精华消息变更
            self.sub_type = message.get("sub_type")        # add, delete
            self.group_id  = message.get("group_id")
            self.sender_id = message.get("sender_id")      # 消息发送者ID
            self.operator_id = message.get("operator_id")  # 操作者ID
            self.message_id = message.get("message_id")    # 消息ID

        self.server.dispatch_event(
            LiteralEvent("cq_qq_api.on_qq_notice"),
            (self, self.bot)
        )
        
#=====================================================================#