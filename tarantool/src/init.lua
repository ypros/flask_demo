box.cfg{listen = 3302}

box.schema.user.passwd('pass')

box.once('init', function()
	dialogs = box.schema.create_space('dialogs', { if_not_exists = true })
	dialogs:format({{ name = 'id', type = 'uuid', is_nullable = false},{ name = 'dialog_id', type = 'string', is_nullable = false}, { name = 'user_from_id', type = 'uuid', is_nullable = false}, { name = 'user_to_id', type = 'uuid', is_nullable = false}, { name = 'text', type = 'string', is_nullable = false}, { name = 'created_at', type = 'datetime', is_nullable = false}})

	dialogs:create_index('pk', { parts = {{ field = 'id', type = 'uuid'}}})
	dialogs:create_index('dialog_id_k', { parts = {{ field = 'dialog_id', type = 'string'}}, unique = false}) end)

uuid = require('uuid')
datetime = require('datetime')

lua_code = [[function(dialog_id, user_from, user_to, text)
    uuid = require('uuid')
    datetime = require('datetime')
	new_uuid = uuid.new()
	box.space.dialogs:insert{new_uuid, dialog_id, uuid.fromstr(user_from), uuid.fromstr(user_to), text, datetime.now()}
	return new_uuid:str() end]]

box.schema.func.create('new_dialog', {body = lua_code})

lua_code = [[function(dialog_id)
	return box.space.dialogs.index.dialog_id_k:select({dialog_id})
	end]]

box.schema.func.create('get_dialog', {body = lua_code})


box.schema.user.grant('guest', 'execute', 'function', 'new_dialog')
box.schema.user.grant('guest', 'execute', 'function', 'get_dialog')
box.schema.user.grant('guest', 'read,write,execute', 'universe')