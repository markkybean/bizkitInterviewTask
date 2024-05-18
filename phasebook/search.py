from flask import Blueprint, request

from .data.search_data import USERS

bp = Blueprint("search", __name__, url_prefix="/search")

@bp.route("")
def search():
    return search_users(request.args.to_dict()), 200

def search_users(args):
    """Search users database based on provided query parameters and sort based on priority

    Parameters:
        args: a dictionary containing the following search parameters:
            id: string
            name: string
            age: string
            occupation: string

    Returns:
        a list of users that match the search parameters, sorted based on priority
    """
    filtered_users = []  # Initialize an empty list to store filtered users

    # If no search parameters are provided, return all users
    if not args:
        return USERS

    # Check if the id parameter is provided
    if 'id' in args:
        # Include user with the provided id in the filtered users
        user_with_id = next((user for user in USERS if user['id'] == args['id']), None)
        if user_with_id:
            filtered_users.append(user_with_id)

    # Check other search parameters
    for user in USERS:
        # Include user if name matches the search parameter
        if 'name' in args and args['name'].lower() in user['name'].lower() and user not in filtered_users:
            filtered_users.append(user)
        # Include user if age falls within the specified range
        if 'age' in args and 'age' in user and int(args['age']) in range(user['age'] - 1, user['age'] + 2) and user not in filtered_users:
            filtered_users.append(user)
        # Include user if occupation matches the search parameter
        if 'occupation' in args and args['occupation'].lower() in user['occupation'].lower() and user not in filtered_users:
            filtered_users.append(user)

    # Sort filtered users based on priority
    sorted_users = sorted(filtered_users, key=lambda user: (
        'id' in args and user['id'] == args['id'],   # Priority 1: Matched id
        'name' in args and args['name'].lower() in user['name'].lower(),  # Priority 2: Matched name
        'age' in args and int(args['age']) in range(user['age'] - 1, user['age'] + 2),  # Priority 3: Matched age
        'occupation' in args and args['occupation'].lower() in user['occupation'].lower()  # Priority 4: Matched occupation
    ), reverse=True)

    return sorted_users
