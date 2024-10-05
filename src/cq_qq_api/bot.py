#=====================================================================#
import uuid
import time
#=====================================================================#
class bot:
    # Websocket 请求格式
    # {
    #     "action": "终结点名称, 例如 'send_group_msg'",
    #     "params": {
    #         "参数名": "参数值",
    #         "参数名2": "参数值"
    #     },
    #     "echo": "'回声', 如果指定了 echo 字段, 那么响应包也会同时包含一个 echo 字段, 它们会有相同的值"
    # }

    def __init__(self, send_message, max_wait_time:int=10) -> None:
        self.send_message = send_message
        self.max_wait_time = max_wait_time

        self.function_return = {}

    @staticmethod
    def format_request(action:str, params:dict={}):
        return {
            "action": action,
            "params": params,
            "echo": params.get("echo", "")
        }
    
    def wait_and_return_function_result(self, function_return_id):
        start_time = time.time()
        while True:
            if function_return_id in self.function_return:
                result = self.function_return[function_return_id]
                del self.function_return[function_return_id]
                return result
                
            time.sleep(0.2)

            # exceed max_wait_time -> return None
            if time.time() - start_time >= self.max_wait_time:
                break
#=====================================================================#
# Account
    # 获取登录号信息
    def get_login_info(self):
        function_return_id = str(uuid.uuid4())
        params = {"echo": function_return_id}
        command_request = self.format_request("get_login_info", params)
        self.send_message(command_request)

        return self.wait_and_return_function_result(function_return_id)

    # 设置登录号资料
    def set_qq_profile(self, **kargs):
        if kargs:                                                      # 不为空才发送
            command_request = self.format_request("set_qq_profile", kargs)
        self.send_message(command_request)
    
#=====================================================================#
# friend information
    # 获取陌生人信息
    def get_stranger_info(self, user_id):
        function_return_id = str(uuid.uuid4())
        params = {"user_id": int(user_id),
                  "echo": function_return_id}
        command_request = self.format_request("get_stranger_info", params)
        self.send_message(command_request)

        return self.wait_and_return_function_result(function_return_id)

    # 获取好友列表
    def get_friend_list(self):
        function_return_id = str(uuid.uuid4())
        params = {"echo": function_return_id}
        command_request = self.format_request("get_friend_list", params)
        self.send_message(command_request)

        return self.wait_and_return_function_result(function_return_id)

    # 获取单向好友列表
    def get_unidirectional_friend_list(self):
        function_return_id = str(uuid.uuid4())
        params = {"echo": function_return_id}
        command_request = self.format_request("get_unidirectional_friend_list", params)
        self.send_message(command_request)

        return self.wait_and_return_function_result(function_return_id)

#=====================================================================#
# friend operation
    # 删除好友
    def delete_friend(self, user_id):
        params = {"user_id": int(user_id)}
        command_request = self.format_request("delete_friend", params)
        self.send_message(command_request)

    # 删除单向好友
    def delete_unidirectional_friend(self, user_id):
        params = {"user_id": int(user_id)}
        command_request = self.format_request("delete_unidirectional_friend", params)
        self.send_message(command_request)

#=====================================================================#
# message
    # reply
    def reply(self, info, message):
        if info.message_type == 'private':
            self.send_private_msg(info.source_id, message)
        elif info.message_type == 'group':
            self.send_group_msg(info.source_id, message)

    # 发送私聊消息
    def send_private_msg(self, user_id, message, group_id=None):
        params = {
            "user_id": int(user_id),
            "message": message,
        }
        if group_id is not None:
            params["group_id"] = int(group_id)
        command_request = self.format_request("send_private_msg", params)
        self.send_message(command_request)

    # 发送群聊消息
    def send_group_msg(self, group_id, message):
        params = {
            "group_id": int(group_id),
            "message_type": "group",
            "message": message
        }
        command_request = self.format_request("send_group_msg", params)
        self.send_message(command_request)
    
    # 发送消息
    def send_msg(self, message, user_id=None, group_id=None, message_type=None):
        params = {
            "message": message,
        }
        if (message_type=="private" and user_id) or user_id:
            params["user_id"] = int(user_id)
        else:
            params["group_id"] = int(group_id)
        command_request = self.format_request("send_msg", params)
        self.send_message(command_request)

    # 获取消息
    def get_msg(self, message_id):
        function_return_id = str(uuid.uuid4())
        params = {"echo": function_return_id,
                  "message_id": message_id}
        command_request = self.format_request("get_msg", params)
        self.send_message(command_request)

        return self.wait_and_return_function_result(function_return_id)

    # 撤回消息
    def delete_msg(self, message_id):
        params = {"message_id": message_id}
        command_request = self.format_request("delete_msg", params)
        self.send_message(command_request)

    # 获取合并转发内容
    def get_forward_msg(self, message_id):
        function_return_id = str(uuid.uuid4())
        params = {"echo": function_return_id,
                  "message_id": message_id}
        command_request = self.format_request("get_forward_msg", params)
        self.send_message(command_request)

        return self.wait_and_return_function_result(function_return_id)

    # 发送合并转发 ( 群聊 )
    def send_group_forward_msg(self, group_id, message):
        params = {
            "group_id": int(group_id),
            "message": message
        }
        command_request = self.format_request("send_group_forward_msg", params)
        self.send_message(command_request)

    # 发送合并转发 ( 好友 )
    def send_private_forward_msg(self, user_id, message):
        params = {
            "group_id": int(user_id),
            "message": message
        }
        command_request = self.format_request("send_private_forward_msg", params)
        self.send_message(command_request)

    # 获取群消息历史记录
    def get_group_msg_history(self, message_seq, group_id):
        function_return_id = str(uuid.uuid4())
        params = {
            "message_seq": message_seq,
            "group_id": int(group_id),
            "echo": function_return_id
        }
        command_request = self.format_request("get_group_msg_history", params)
        self.send_message(command_request)

        return self.wait_and_return_function_result(function_return_id)

#=====================================================================#
# image
    # 获取图片信息
    def get_image(self, file):
        function_return_id = str(uuid.uuid4())
        params = {
            "file": file,
            "echo": function_return_id
        }
        command_request = self.format_request("get_image", params)
        self.send_message(command_request)

        return self.wait_and_return_function_result(function_return_id)

    # 检查是否可以发送图片
    def can_send_image(self):
        function_return_id = str(uuid.uuid4())
        params = {
            "echo": function_return_id
        }
        command_request = self.format_request("can_send_image", params)
        self.send_message(command_request)

        return self.wait_and_return_function_result(function_return_id)

#=====================================================================#
# audio
    # 获取语音
    def get_record(self, file, out_format):
        function_return_id = str(uuid.uuid4())
        params = {
            "file": file,
            "out_format": out_format,
            "echo": function_return_id
        }
        command_request = self.format_request("get_record", params)
        self.send_message(command_request)

        return self.wait_and_return_function_result(function_return_id)

    # 检查是否可以发送语音
    def can_send_record(self):
        function_return_id = str(uuid.uuid4())
        params = {
            "echo": function_return_id
        }
        command_request = self.format_request("can_send_record", params)
        self.send_message(command_request)

        return self.wait_and_return_function_result(function_return_id)
#=====================================================================#
# process
    # 处理加好友请求
    def set_friend_add_request(self, flag, approve, remark=""):
        params = {
            "flag": flag,
            "approve": approve,
        }
        if remark:
            params["remark"] = remark
        command_request = self.format_request("set_friend_add_request", params)
        self.send_message(command_request)

    # 处理加群请求／邀请
    def set_friend_add_request(self, flag, sub_type, approve=True, reason=""):
        params = {
            "flag": flag,
            "approve": approve,
            "sub_type": sub_type
        }
        if not approve:
            params["reason"] = reason
        command_request = self.format_request("set_friend_add_request", params)
        self.send_message(command_request)

    # 获取群信息
    def get_group_info(self, group_id):
        function_return_id = str(uuid.uuid4())
        params = {
            "group_id": int(group_id),
            "echo": function_return_id
        }
        command_request = self.format_request("get_group_info", params)
        self.send_message(command_request)

        return self.wait_and_return_function_result(function_return_id)

    # 获取群列表
    def get_group_list(self):
        function_return_id = str(uuid.uuid4())
        params = {
            "echo": function_return_id
        }
        command_request = self.format_request("get_group_list", params)
        self.send_message(command_request)

        return self.wait_and_return_function_result(function_return_id)

    # 获取群成员信息
    def get_group_member_info(self, group_id, user_id):
        function_return_id = str(uuid.uuid4())
        params = {
            "group_id": int(group_id),
            "user_id": int(user_id),
            "echo": function_return_id
        }
        command_request = self.format_request("get_group_member_info", params)
        self.send_message(command_request)

        return self.wait_and_return_function_result(function_return_id)

    # 获取群成员列表
    def get_group_member_list(self, group_id):
        function_return_id = str(uuid.uuid4())
        params = {
            "group_id": int(group_id),
            "echo": function_return_id
        }
        command_request = self.format_request("get_group_member_list", params)
        self.send_message(command_request)

        return self.wait_and_return_function_result(function_return_id)

    # 获取群荣誉信息
    def get_group_honor_info(self, group_id):
        function_return_id = str(uuid.uuid4())
        params = {
            "group_id": int(group_id),
            "echo": function_return_id
        }
        command_request = self.format_request("get_group_honor_info", params)
        self.send_message(command_request)

        return self.wait_and_return_function_result(function_return_id)

    # 获取群系统消息
    def get_group_system_msg(self):
        function_return_id = str(uuid.uuid4())
        params = {
            "echo": function_return_id
        }
        command_request = self.format_request("get_group_system_msg", params)
        self.send_message(command_request)

        return self.wait_and_return_function_result(function_return_id)
    
    # 获取精华消息列表
    def get_essence_msg_list(self, group_id):
        function_return_id = str(uuid.uuid4())
        params = {
            "group_id": int(group_id),
            "echo": function_return_id
        }
        command_request = self.format_request("get_essence_msg_list", params)
        self.send_message(command_request)

        return self.wait_and_return_function_result(function_return_id)
    
    # 获取群 @全体成员 剩余次数
    def get_group_at_all_remain(self, group_id):
        function_return_id = str(uuid.uuid4())
        params = {
            "group_id": int(group_id),
            "echo": function_return_id
        }
        command_request = self.format_request("get_group_at_all_remain", params)
        self.send_message(command_request)

        return self.wait_and_return_function_result(function_return_id)
#=====================================================================#
# group setting
    # 设置群名
    def set_group_name(self, group_id, group_name):
        params = {
            "group_id": int(group_id),
            "group_name": group_name
        }
        command_request = self.format_request("set_group_name", params)
        self.send_message(command_request)

    # 设置群头像
    def set_group_portrait(self, group_id, user_id, enable):
        params = {
            "group_id": int(group_id),
            "user_id": int(user_id),
            "enable": enable
        }
        command_request = self.format_request("set_group_portrait", params)
        self.send_message(command_request)

    # 设置群管理员
    def set_group_admin(self, group_id, user_id, special_title=""):
        params = {
            "group_id": int(group_id),
            "user_id": int(user_id),
            "special_title": special_title
        }
        command_request = self.format_request("set_group_admin", params)
        self.send_message(command_request)

    # 设置群名片 ( 群备注 )
    def set_group_card(self, group_id, user_id, card):
        params = {
            "group_id": int(group_id),
            "user_id": int(user_id),
            "card": card
        }
        command_request = self.format_request("set_group_card", params)
        self.send_message(command_request)

    # 设置群组专属头衔
    def set_group_special_title(self, group_id, user_id, special_title):
        params = {
            "group_id": int(group_id),
            "user_id": int(user_id),
            "special_title": special_title
        }
        command_request = self.format_request("set_group_special_title", params)
        self.send_message(command_request)
#=====================================================================#
# group operation
    # 群单人禁言
    def set_group_ban(self, group_id, user_id, duration=0):
        params = {
            "group_id": int(group_id),
            "user_id": int(user_id),
            "duration": duration
        }
        command_request = self.format_request("set_group_ban", params)
        self.send_message(command_request)

    # 群全员禁言
    def set_group_whole_ban(self, group_id, enable):
        params = {
            "group_id": int(group_id),
            "enable": enable
        }
        command_request = self.format_request("set_group_whole_ban", params)
        self.send_message(command_request)

    # 群匿名用户禁言
    def set_group_anonymous_ban(self, group_id, flag, duration, anonymous=None):
        params = {
            "group_id": int(group_id),
            "duration": duration,
            "flag": flag
        }
        if anonymous:
            params["anonymous"] = anonymous
        command_request = self.format_request("set_group_anonymous_ban", params)
        self.send_message(command_request)

    # 设置精华消息
    def set_essence_msg(self, message_id):
        params = {
            "message_id": message_id,
        }
        command_request = self.format_request("set_essence_msg", params)
        self.send_message(command_request)

    # 移出精华消息
    def delete_essence_msg(self, message_id):
        params = {
            "message_id": message_id
        }
        command_request = self.format_request("delete_essence_msg", params)
        self.send_message(command_request)

    # 群打卡
    def send_group_sign(self, group_id):
        params = {
            "group_id": int(group_id)
        }
        command_request = self.format_request("send_group_sign", params)
        self.send_message(command_request)

    # 群设置匿名
    def set_group_anonymous(self, group_id, enable):
        params = {
            "group_id": int(group_id),
            "enable": enable
        }
        command_request = self.format_request("set_group_anonymous", params)
        self.send_message(command_request)

    # 发送群公告
    def _send_group_notice(self, group_id, content, image=None):
        params = {
            "group_id": int(group_id),
            "content": content
        }
        if image:
            params["image"] = image
        command_request = self.format_request("_send_group_notice", params)
        self.send_message(command_request)

    # 获取群公告
    def _get_group_notice(self, group_id):
        function_return_id = str(uuid.uuid4())
        params = {
            "group_id": int(group_id),
            "echo": function_return_id
        }
        command_request = self.format_request("_get_group_notice", params)
        self.send_message(command_request)

        return self.wait_and_return_function_result(function_return_id)

    # 群组踢人
    def set_group_kick(self, group_id, user_id, reject_add_request=False):
        params = {
            "group_id": int(group_id),
            "user_id": int(user_id),
            "reject_add_request": reject_add_request
        }
        command_request = self.format_request("set_group_kick", params)
        self.send_message(command_request)

    # 退出群组
    def set_group_leave(self, group_id, is_dismiss=False):
        params = {
            "group_id": int(group_id),
            "is_dismiss": is_dismiss
        }
        command_request = self.format_request("set_group_leave", params)
        self.send_message(command_request)
#=====================================================================#
# group operation
    # 上传群文件
    def upload_group_file(self, group_id, file, name, folder):
        params = {
            "group_id": int(group_id),
            "file": file,
            "name": name,
            "folder": folder
        }
        command_request = self.format_request("upload_group_file", params)
        self.send_message(command_request)

    # 删除群文件
    def delete_group_file(self, group_id, file_id, busid):
        params = {
            "group_id": int(group_id),
            "file_id": file_id,
            "busid": busid
        }
        command_request = self.format_request("delete_group_file", params)
        self.send_message(command_request)

    # 创建群文件文件夹
    def create_group_file_folder(self, group_id, name, parent_id):
        params = {
            "group_id": int(group_id),
            "name": name,
            "parent_id": parent_id
        }
        command_request = self.format_request("create_group_file_folder", params)
        self.send_message(command_request)

    # 删除群文件文件夹
    def delete_group_folder(self, group_id, folder_id):
        params = {
            "group_id": int(group_id),
            "folder_id": folder_id
        }
        command_request = self.format_request("delete_group_folder", params)
        self.send_message(command_request)


    # 获取群文件系统信息
    def get_group_file_system_info(self, group_id):
        function_return_id = str(uuid.uuid4())
        params = {
            "group_id": int(group_id),
            "echo": function_return_id
        }
        command_request = self.format_request("get_group_file_system_info", params)
        self.send_message(command_request)

        return self.wait_and_return_function_result(function_return_id)

    # 获取群根目录文件列表
    def get_group_root_files(self, group_id):
        function_return_id = str(uuid.uuid4())
        params = {
            "group_id": int(group_id),
            "echo": function_return_id
        }
        command_request = self.format_request("get_group_root_files", params)
        self.send_message(command_request)

        return self.wait_and_return_function_result(function_return_id)

    # 获取群子目录文件列表
    def get_group_files_by_folder(self, group_id, folder_id):
        function_return_id = str(uuid.uuid4())
        params = {
            "group_id": int(group_id),
            "folder_id": folder_id,
            "echo": function_return_id
        }
        command_request = self.format_request("get_group_files_by_folder", params)
        self.send_message(command_request)

        return self.wait_and_return_function_result(function_return_id)

    # 获取群文件资源链接
    def get_group_file_url(self, group_id, file_id, busid):
        function_return_id = str(uuid.uuid4())
        params = {
            "group_id": int(group_id),
            "file_id": file_id,
            "busid": busid,
            "echo": function_return_id
        }
        command_request = self.format_request("get_group_file_url", params)
        self.send_message(command_request)

        return self.wait_and_return_function_result(function_return_id)

    # 上传私聊文件
    def upload_private_file(self, user_id, file, name):
        params = {
            "user_id": int(user_id),
            "file": file,
            "name": name
        }
        command_request = self.format_request("upload_private_file", params)
        self.send_message(command_request)

#=====================================================================#