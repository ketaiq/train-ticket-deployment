import requests
import configparser

configParser = configparser.RawConfigParser()
configFilePath = "experiments.ini"
configParser.read(configFilePath)

tt_host = configParser["DEFAULT"]["tt_host"]
admin_username = configParser["DEFAULT"]["admin_username"]
admin_password = configParser["DEFAULT"]["admin_password"]


def user_login(username=admin_username, password=admin_password):
	"""
	:param username:
	:param password:
	:return: [user_id, user_token]
	"""

	response = requests.post(
		url="{host}/api/v1/users/login".format(host=tt_host),
		headers={"Accept": "application/json", "Content-Type": "application/json"},
		json={"username": username, "password": password}
	)

	data = response.json()["data"]
	return data["userId"], "Bearer " + data["token"]


def contact_get_list_user(user_id: str, bearer: str):
	"""

	:param user_id:
	:param bearer:
	:return: list of contacts assigned to the account of the user
	"""
	response = requests.get(
		url="{host}/api/v1/contactservice/contacts/account/{user_id}".format(host=tt_host, user_id=user_id),
		headers={
			"Accept": "application/json",
			"Content-Type": "application/json",
			"Authorization": bearer
		}
	)

	data = response.json()["data"]
	return data


def contact_get_list_all(admin_bearer: str):
	"""

	:param admin_bearer
	:return: list of contacts available in the system
	"""
	response = requests.get(
		url="{host}/api/v1/contactservice/contacts".format(host=tt_host),
		headers={
			"Accept": "application/json",
			"Content-Type": "application/json",
			"Authorization": admin_bearer
		}
	)

	contacts_list = response.json()["data"]
	if contacts_list is None:
		contacts_list = []

	return contacts_list


def contact_delete(contact_id: str, bearer: str):
	response = requests.delete(
		url="{host}/api/v1/contactservice/contacts/{contact_id}".format(host=tt_host, contact_id=contact_id),
		headers={
			"Accept": "application/json",
			"Content-Type": "application/json",
			"Authorization": bearer,
		}
	)

	status = response.json()["status"]
	return status


def orders_get_list_all(bearer: str):
	response = requests.get(
		url="{host}/api/v1/adminorderservice/adminorder".format(host=tt_host),
		headers={
			"Accept": "application/json",
			"Content-Type": "application/json",
			"Authorization": bearer
		}
	)

	orders_list = response.json()["data"]
	return orders_list


def orders_get_list_user(bearer: str, account_id: str):
	return list(filter(lambda item: item['accountId'] == account_id, orders_get_list_all(bearer)))


def orders_delete(bearer: str, order_id, train_number):
	response = requests.delete(
		url="{host}/api/v1/adminorderservice/adminorder/{order_id}/{train_number}".format(host=tt_host,
																						  order_id=order_id,
																						  train_number=train_number),
		headers={
			"Accept": "application/json",
			"Content-Type": "application/json",
			"Authorization": bearer
		}
	)

	# 1 - deleted, 0 - Order Not Exist
	status = response.json()["status"]
	return status
