from flask_restful import HTTPException


class DefaultServerUnconfigured(HTTPException):
    """
    Errors arising from a lack of a server specified in the current_config record of the Configuration table.
    """
    code = 501
    description = "Default server is unconfigured."

