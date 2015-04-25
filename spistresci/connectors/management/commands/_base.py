from spistresci.connectors import Tools
from spistresci.connectors.generic.GenericConnector import GenericConnector
from spistresci.connectors.utils.ConfigReader import ConfigReader


class ConnectorsCommandBase(object):

    def get_list_of_connectors_to_run(self):

        GenericConnector.config_object = ConfigReader.read_config(
            GenericConnector.config_file
        )

        config_connector_classnames_list = Tools.get_classnames(
            GenericConnector.config_object
        ).items()

        connector_classnames_list = config_connector_classnames_list

        filtered_list = self.filter_varargs(
            Tools.filter_disabled,
            config_connector_classnames_list,
            False,
            GenericConnector.config_object,
            self.logger,
        )

        partial = connector_classnames_list > filtered_list

        connectors = [
            Tools.load_connector(
                connectorname=connector[1],
                config=GenericConnector.config_object
            )(
                name=connector[0],
                limit_books=0   # args.limit_books
            )
            for connector in connector_classnames_list
        ]

        return connectors, partial

    @staticmethod
    def filter_varargs(fun, iterable, expected, *args, **kwargs):
        return [
            item for item in iterable
            if fun(item, *args, **kwargs) == expected
        ]
