class Action:
	Read = "read"
	Update = "update"
	Delete = "delete"
	New = "new"
	Password = "password"
	Role = "role"
	AccessList = "access_list"

resources = {
"logout" : [Action.Read],
"index" : [Action.Read], 
"users" : [Action.New, Action.Password, Action.Role, Action.AccessList, Action.Read, Action.Update]
}

roles = {
	"projectAdmin": {}
}