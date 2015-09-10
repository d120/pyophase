def check_permissions(user, permissions):
    """
    Check if the user has enough permissions to perform this action

    :param user: django.user user object, representing the currently logged in user
    :param permissions: list of permissions
    :return: True if user has at least one of the permissions required in list or if the list is empty, otherwise False
    """

    #...without special permissions...
    if len(permissions) == 0:
        return True
    #...or those with at least one matching permission
    else:
        for permission in permissions:
            if user.has_perm(permission):
                return True
    return False
