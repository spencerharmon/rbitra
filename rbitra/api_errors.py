from flask_restful import HTTPException


class ServerUnconfigured(HTTPException):
    """
    Errors arising from a missing or incomplete current_config record of the Configuration table.
    """
    code = 501
    description = "Server is unconfigured."


class PluginError(HTTPException):
    '''
    class of exceptions related to plugin operations
    '''
    code = 541
    description = "General Plugin Error"


class PluginMethodUndefined(PluginError):
    """
    Raised when a plugin fails to define a method.
    """
    def __init__(self, method):
        self.desription = "Method '{}' not defined.".format(method)


class PluginContentsError(PluginError):
    def __init__(self, file_name, plugin_name):
        self.description = "File '{}' contents incompatible with plugin '{}'".format(file_name, plugin_name)


class RepoCouldNotBeLoaded(PluginError):
    """
    Errors related to loading a repository for a decision
    """
    def __init__(self, repo_path):
        self.description = "The decision repository '{}' could not be loaded. Ensure that the object exists".format(repo_path)


class DecisionError(HTTPException):
    """
    Parent class for decision-related exceptions.
    """
    code = 442
    description = "General decision error."


class FailedToCreateDecision(DecisionError):
    """
    Raised when decision creation fails.
    """
    def __init__(self, data):
        self.description = "Could not create decision: {}".format(data)
        super().__init__(self.description)


class DataLoadError(DecisionError):
    """
    Raised when data does not load properly from the decision repository.
    """
    def __init__(self, data):
        self.description = "Could not load: {}".format(data)
        super().__init__(self.description)


class PermissionsError(DecisionError):
    """
    Raised when the author of a decision doesn't have the required role to create it.
    """
    def __init__(self, msg):
        self.code = 401
        self.description = "Insufficient permissions: {}".format(msg)
        super().__init__(self.description)