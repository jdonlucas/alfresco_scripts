from utils import find_node_info, find_site_info, change_type


def change_type_of_file(session, site_name, node_name, new_type):
    """
    Change the type to files and adds properties to improve
    the metadata associated with the file.

    Params:
        session (Session):      A session object to make requests
                                to alfresco.
        site_name (string):     The name of the site where the
                                files are stored.
        node_name (string):     The name of a node.
        new_type (string):      The name of the aspect to add to
                                the files.

    Returns:
        (string):   Info string with the amount of updated files.
    """
    site_info = find_site_info(session, site_name)

    image = find_node_info(session, site_info["entry"]["id"], node_name)

    updated = change_type(session, image, new_type)

    return "Updated %d files" % len(updated)
