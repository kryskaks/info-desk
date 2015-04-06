from pysimplesoap.client import SoapClient
from datetime import datetime

test_merchant_id = 129400107178

def main():
	client = SoapClient(wsdl = "https://merchant.w1.ru/checkout/service.asmx?wsdl", trace = True)
	utcnow = datetime.utcnow()
	
	response = client.GetBalance(MerchantId = test_merchant_id, RequestDate = datetime.utcnow())
	print response	

if __name__ == '__main__':
	main()