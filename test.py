from pysimplesoap.client import SoapClient
from datetime import datetime

def main():
	client = SoapClient(wsdl="https://merchant.w1.ru/checkout/service.asmx?wsdl",trace=True)
	utcnow = datetime.utcnow()
	response = client.GetBalance(MerchantId = 129400107178, RequestDate = datetime.utcnow())
	print response	

if __name__ == '__main__':
	main()