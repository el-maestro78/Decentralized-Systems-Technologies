def filter_table(rt_list):
    """Καθαρίζει το routing table από None τιμές.
    :param list rt_list: Η λίστα που θέλουμε να 'καθαρίσουμε' από None τιμές.
    :return: Η καθαρή λίστα.
    :rtype: list"""
    clean_list = []
    for i in rt_list:
        if rt_list is not None:
            clean_list.append(i)
    return clean_list
