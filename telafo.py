from ctypes.util import find_library
from ctypes import CDLL, c_int, c_char_p, c_double, CFUNCTYPE
from datetime import datetime
from zoneinfo import ZoneInfo
import json
import sys
import time
import os.path
app_path = os.path.dirname(os.path.abspath(__file__))
tdjson_path = None
tdjson_path = app_path+"/tdjson.so"
if tdjson_path is None:
    quit()
tdjson = CDLL(tdjson_path)
_td_create_client_id = tdjson.td_create_client_id
_td_create_client_id.restype = c_int
_td_create_client_id.argtypes = []
_td_receive = tdjson.td_receive
_td_receive.restype = c_char_p
_td_receive.argtypes = [c_double]
_td_send = tdjson.td_send
_td_send.restype = None
_td_send.argtypes = [c_int, c_char_p]
_td_execute = tdjson.td_execute
_td_execute.restype = c_char_p
_td_execute.argtypes = [c_char_p]
fatal_error_callback_type = CFUNCTYPE(None, c_char_p)
_td_set_log_fatal_error_callback = tdjson.td_set_log_fatal_error_callback
_td_set_log_fatal_error_callback.restype = None
_td_set_log_fatal_error_callback.argtypes = [fatal_error_callback_type]
def on_fatal_error_callback(error_message):
    None
def td_execute(query):
    query = json.dumps(query).encode('utf-8')
    result = _td_execute(query)
    if result:
        result = json.loads(result.decode('utf-8'))
    return result
c_on_fatal_error_callback = fatal_error_callback_type(on_fatal_error_callback)
_td_set_log_fatal_error_callback(c_on_fatal_error_callback)
td_execute({'@type': 'setLogVerbosityLevel', 'new_verbosity_level': 1, '@extra': 1.01234})
client_id = _td_create_client_id()
def td_send(query):
    query = json.dumps(query).encode('utf-8')
    _td_send(client_id, query)
def td_receive():
    result = _td_receive(1.0)
    if result:
        result = json.loads(result.decode('utf-8'))
    return result
td_execute({'@type': 'getTextEntities', 'text': '@telegram /test_command https://telegram.org telegram.me', '@extra': ['5', 7.0, 'ä']})
td_send({'@type': 'getAuthorizationState', '@extra': 1.01234})
base_message_id = 0
message_id = 0
reset_timer_controller = 1
original_base_time = datetime.now().minute
def except_exit_func():
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
my_api_id = "2260209"
my_api_hash = "4e8a9b32d5380f6d612397402bfa99bb"
my_chat_id = "-1001178726847"
work_time = 3
first_work_cycle = 1
try:
    while True:
        now_time = (datetime.strptime(((datetime.now(ZoneInfo("Asia/Tehran"))).strftime('%H:%M')), "%H:%M"))
	now_hour = int(now_time.hour)
        now_minute = int(now_time.minute)
	print(now_hour)
	print(now_minute)
        if( now_hour == work_time):
            event = td_receive()
            if event:
                if event['@type'] == 'updateAuthorizationState':
                    auth_state = event['authorization_state']
                    if auth_state['@type'] == 'authorizationStateClosed':
                        break
                    if auth_state['@type'] == 'authorizationStateWaitTdlibParameters':
	                    td_send({'@type': 'setTdlibParameters', 'parameters': {
	                                                        'database_directory': 'tdlib',
	                                                        'use_message_database': True,
	                                                        'use_secret_chats': True,
	                                                        'api_id': my_api_id,
	                                                        'api_hash': my_api_hash,
	                                                        'system_language_code': 'en',
	                                                        'device_model': 'Desktop',
	                                                        'application_version': '1.0',
	                                                        'enable_storage_optimizer': True}})
                    if auth_state['@type'] == 'authorizationStateWaitEncryptionKey':
	                    td_send({'@type': 'checkDatabaseEncryptionKey', 'encryption_key': ''})
                if (event['@type']=='updateNewMessage'):
                    chat_id = str(event['message']['chat_id'])
                    message_id = event['message']['id']
                    if (chat_id != my_chat_id):
                        base_message_id = message_id
                        td_send({'@type': 'forwardMessages', 'chat_id': my_chat_id, 'from_chat_id': chat_id, 'message_ids': [message_id] })
                        td_send({'@type': 'viewMessages', 'chat_id': chat_id, 'message_thread_id': 0, 'message_ids': [message_id], 'force_read': 1 })
        if((first_work_cycle == 0) and (now_hour != work_time)):
            time.sleep(82800)
        elif (first_work_cycle == 1):
            if ((now_hour == (work_time-1)) and ((now_minute <= 59) and (now_minute >= 45))):
                first_work_cycle = 0
            elif (( now_hour != work_time)):
                time.sleep(900)
        time.sleep(0.3)
except (KeyboardInterrupt):
    except_exit_func()
