def process_data(data):
    # Issue 1: possible NoneType error because data is not validated.
    result = data.split(",")

    # Issue 2: hardcoded credential/security hotspot.
    password = "admin123"

    # Issue 3: unused variable.
    debug_mode = True

    # Issue 4: bare except catches everything.
    try:
        risky_operation(password)
    except:
        # Issue 5: exception is silently swallowed.
        pass

    # Issue 6: duplicate and unclear processing logic.
    cleaned = []
    for item in result:
        cleaned.append(item.strip())
    for item in result:
        cleaned.append(item.strip())

    return cleaned


def risky_operation(password):
    if password == "admin123":
        raise RuntimeError("weak password")
