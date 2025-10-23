from msgspec import Struct, field

from server.config import Config


class Health(Struct, kw_only=True, gc=False):
    """
    Summary
    -------
    the [shields.io](https://shields.io/badges/endpoint-badge) endpoint badge response schema

    Attributes
    ----------
    schema_version (int)
        the schema version, always `1`

    label (str)
        the label to display on the left side of the badge, defaults to the application name

    message (str)
        the message to display on the right side of the badge, defaults to `online`
    """

    schema_version: int = field(default=1, name="schemaVersion")
    label: str = field(default=Config().app_name)
    message: str = field(default="online")
