class Action:
	Read = "read"
	Update = "update"
	Delete = "delete"
	New = "new"
	Password = "password"
	Role = "role"
	AccessList = "access_list"
	Key = "key"

class Resource:
	Logout = "logout"
	Index = "index"
	Users = "users"
	Merchants = "merchants"
	InvoiceInfo = "invoice_info"
	TransferInfo = "transfer_info"
	MyMerchant = "my_merchant"

resources = {
	Resource.Logout: [Action.Read],
	Resource.Index: [Action.Read], 
	Resource.Users: [Action.New, Action.Password, Action.Role, Action.AccessList, Action.Read, Action.Update],
	Resource.Merchants: [Action.New, Action.Read, Action.Update],
	Resource.InvoiceInfo: [Action.Read],
	Resource.TransferInfo: [Action.Read],
	Resource.MyMerchant: [Action.Read, Action.Update, Action.Key]
}

roles = {
	"projectAdmin": {
		Resource.Logout: [Action.Read],
		Resource.Index: [Action.Read],
		Resource.Merchants: [Action.New, Action.Read, Action.Update],
		Resource.Users: [Action.New, Action.Password, Action.Role, Action.AccessList, Action.Read, Action.Update],
	},
	
	"operator": {
		Resource.Logout: [Action.Read],
		Resource.Index: [Action.Read],
		Resource.InvoiceInfo: [Action.Read],
		Resource.TransferInfo: [Action.Read],
	},
	
	"admin": {
		Resource.Logout: [Action.Read],
		Resource.Index: [Action.Read],
		Resource.MyMerchant: [Action.Read, Action.Update, Action.Key],
		Resource.Users: [Action.New, Action.Password, Action.Read, Action.Update],
		Resource.InvoiceInfo: [Action.Read],
		Resource.TransferInfo: [Action.Read],
	}
}