import tarantool
import mmh3


connection = tarantool.Connection('localhost', 3302)


def get_dialog_id(user1, user2):
	user1_hash = mmh3.hash(user1, signed=False)
	user2_hash = mmh3.hash(user2, signed=False)

	if user1_hash < user2_hash:
		dialog_id = user1 + user2
	else:
		dialog_id = user2 + user1

	return dialog_id

#SEND DIALOG
def send_dialog(from_user_id, to_user_id, text):

	dialog_id = get_dialog_id(from_user_id, to_user_id)

	try:
		response = connection.call('new_dialog', (dialog_id, from_user_id, to_user_id, text))
		new_dialog_uuid = response.data[0]
	except connection.Error as err:
		
		print(err)
		return None

	return new_dialog_uuid

#GET LIST of DIALOGS
def list_dialog(from_user_id, to_user_id):

	dialog_id = get_dialog_id(from_user_id, to_user_id)

	try:
		response = connection.call('get_dialog', (dialog_id))
		dialogs = response.data
	except connection.Error as err:
		
		print(err)
		return None

	return dialogs


 
