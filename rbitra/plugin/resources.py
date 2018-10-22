from rbitra import db
from rbitra.plugin.model import Plugin
from rbitra.plugin.schema import PluginSchema
from flask_rest_jsonapi import ResourceList, ResourceDetail, ResourceRelationship


class PluginList(ResourceList):
    schema = PluginSchema
    data_layer = {'session': db.session,
                  'model': Plugin}


class PluginDetail(ResourceDetail):
    schema = PluginSchema
    data_layer = {'session': db.session,
                  'model': Plugin}


class PluginRelationship(ResourceRelationship):
    schema = PluginSchema
    data_layer = {'session': db.session,
                  'model': Plugin}
