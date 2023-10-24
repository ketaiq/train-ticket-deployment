import requests
import logging
from json import JSONDecodeError


def user_login(username: str, password: str, host: str):
    """
    Login a user with the valid combination of a username and a password.
    """
    response = requests.post(
        url="{host}/api/v1/users/login".format(host=host),
        headers={"Accept": "application/json", "Content-Type": "application/json"},
        json={"username": username, "password": password},
    )

    data = response.json()["data"]
    return data["userId"], "Bearer " + data["token"]


def get_all_users(admin_bearer: str, host: str):
    """
    Get all users in the system.
    """
    logging.info(f'Try to get all users using admin bearer "{admin_bearer}".')
    response = requests.get(
        url="{host}/api/v1/adminuserservice/users".format(host=host),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": admin_bearer,
        },
    )
    try:
        if response.ok:
            response_json = response.json()
            msg = response_json["msg"]
            users = response_json["data"]
            num_users = len(users)
            logging.info(f'Get {num_users} users with the message "{msg}".')
            return users
        else:
            logging.error(f"Get HTTP error {response.status_code}!")
    except JSONDecodeError:
        logging.error(f"Response {response.text} could not be decoded as JSON!")
    except KeyError:
        logging.error(f"Response JSON {response_json} did not contain expected key!")


# def contact_get_list_user(user_id: str, bearer: str):
#     """

#     :param user_id:
#     :param bearer:
#     :return: list of contacts assigned to the account of the user
#     """
#     response = requests.get(
#         url="{host}/api/v1/contactservice/contacts/account/{user_id}".format(
#             host=tt_host, user_id=user_id
#         ),
#         headers={
#             "Accept": "application/json",
#             "Content-Type": "application/json",
#             "Authorization": bearer,
#         },
#     )

#     data = response.json()["data"]
#     return data


# def contact_get_list_all(admin_bearer: str):
#     """

#     :param admin_bearer
#     :return: list of contacts available in the system
#     """
#     response = requests.get(
#         url="{host}/api/v1/contactservice/contacts".format(host=tt_host),
#         headers={
#             "Accept": "application/json",
#             "Content-Type": "application/json",
#             "Authorization": admin_bearer,
#         },
#     )

#     contacts_list = response.json()["data"]
#     if contacts_list is None:
#         contacts_list = []

#     return contacts_list


# def contact_delete(contact_id: str, bearer: str):
#     response = requests.delete(
#         url="{host}/api/v1/contactservice/contacts/{contact_id}".format(
#             host=tt_host, contact_id=contact_id
#         ),
#         headers={
#             "Accept": "application/json",
#             "Content-Type": "application/json",
#             "Authorization": bearer,
#         },
#     )

#     status = response.json()["status"]
#     return status


# def orders_get_list_all(bearer: str):
#     response = requests.get(
#         url="{host}/api/v1/adminorderservice/adminorder".format(host=tt_host),
#         headers={
#             "Accept": "application/json",
#             "Content-Type": "application/json",
#             "Authorization": bearer,
#         },
#     )

#     orders_list = response.json()["data"]
#     return orders_list


# def orders_get_list_user(bearer: str, account_id: str):
#     return list(
#         filter(
#             lambda item: item["accountId"] == account_id, orders_get_list_all(bearer)
#         )
#     )


# def orders_delete(bearer: str, order_id, train_number):
#     response = requests.delete(
#         url="{host}/api/v1/adminorderservice/adminorder/{order_id}/{train_number}".format(
#             host=tt_host, order_id=order_id, train_number=train_number
#         ),
#         headers={
#             "Accept": "application/json",
#             "Content-Type": "application/json",
#             "Authorization": bearer,
#         },
#     )

#     # 1 - deleted, 0 - Order Not Exist
#     status = response.json()["status"]
#     return status
