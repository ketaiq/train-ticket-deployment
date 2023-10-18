from __future__ import division
import datetime
import garbage_cleaning_utils as gcu
import configparser
import logging

configParser = configparser.RawConfigParser()
configFilePath = "experiments.ini"
configParser.read(configFilePath)


def setup_logger(name, log_file, level=logging.INFO):

	formatter = logging.Formatter('%(asctime)s %(message)s')

	handler = logging.FileHandler(log_file)
	handler.setFormatter(formatter)

	logger = logging.getLogger(name)
	logger.setLevel(level)
	logger.addHandler(handler)

	return logger


order_min_age = int(configParser["DEFAULT"]["order_min_age"])


def garbage_cleaning(data, context):

	# logger_tasks = setup_logger('logger_1', 'orders_cleaning.log')

	admin_user_id, admin_user_token = gcu.user_login()

	orders = gcu.orders_get_list_all(admin_user_token)
	contacts = gcu.contact_get_list_all(admin_user_token)

	order_account_id_list = []

	# logger_tasks.info("Total: " + str(len(orders)) + " | " + str(len(contacts)))
	print("Totals: " + str(len(orders)) + " | " + str(len(contacts)))

	orders_deleted = 0

	for idx, order in enumerate(orders):

		order_id = order["id"]
		order_train_number = order["trainNumber"]
		order_bought_time = order["boughtDate"]
		order_status = order["status"]
		order_account_id_list.append(order["accountId"])

		bought_time = datetime.datetime.fromtimestamp(round(order_bought_time / 1000))
		# current_time_utc = datetime.datetime.utcnow()
		current_time = datetime.datetime.now()
		seconds_passed = int((current_time - bought_time).total_seconds())
		# print(bought_time, current_time, seconds_passed)

		if order_status == 6 or seconds_passed > order_min_age:

			order_del_op_status = gcu.orders_delete(admin_user_token, order_id, order_train_number)

			if order_del_op_status == 1:
				orders_deleted += 1

	contacts_deleted = 0

	for idx, contact in enumerate(contacts):
		if contact["accountId"] not in order_account_id_list:
			order_del_op_status = gcu.contact_delete(contact["id"], admin_user_token)

			if order_del_op_status == 1:
				contacts_deleted += 1

	# logger_tasks.info("Deleted: " + str(orders_deleted) + " | " + str(contacts_deleted))
	print("Deleted: " + str(orders_deleted) + " | " + str(contacts_deleted))