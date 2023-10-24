from __future__ import division
import utils
from config import admin_username, admin_password, host, entity_min_age


def garbage_cleaning(data, context):
    admin_user_id, admin_bearer = utils.user_login(admin_username, admin_password, host)
    users = utils.get_all_users(admin_bearer, host)
    print()


def main():
    garbage_cleaning(None, None)


if __name__ == "__main__":
    main()
