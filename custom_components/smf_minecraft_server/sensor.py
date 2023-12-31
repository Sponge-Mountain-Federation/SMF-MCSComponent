"""The Minecraft Server sensor platform."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import MinecraftServer, MinecraftServerEntity
from .const import (
    ATTR_PLAYERS_LIST,
    DOMAIN,
    ICON_LATENCY_TIME,
    ICON_MOTD,
    ICON_PLAYERS_MAX,
    ICON_PLAYERS_ONLINE,
    ICON_PROTOCOL_VERSION,
    ICON_VERSION,
    NAME_LATENCY_TIME,
    NAME_MOTD,
    NAME_PLAYERS_MAX,
    NAME_PLAYERS_ONLINE,
    NAME_PROTOCOL_VERSION,
    NAME_VERSION,
    UNIT_PLAYERS_MAX,
    UNIT_PLAYERS_ONLINE,
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Minecraft Server sensor platform."""
    server = hass.data[DOMAIN][config_entry.unique_id]

    # Create entities list.
    entities = [
        MinecraftServerVersionSensor(server),
        MinecraftServerProtocolVersionSensor(server),
        MinecraftServerLatencyTimeSensor(server),
        MinecraftServerPlayersOnlineSensor(server),
        MinecraftServerPlayersMaxSensor(server),
        MinecraftServerMOTDSensor(server),
    ]

    # Add sensor entities.
    async_add_entities(entities, True)


class MinecraftServerSensorEntity(MinecraftServerEntity, SensorEntity):
    """Representation of a Minecraft Server sensor base entity."""

    def __init__(
        self,
        server: MinecraftServer,
        type_name: str,
        icon: str,
        unit: str | None = None,
        device_class: str | None = None,
    ) -> None:
        """Initialize sensor base entity."""
        super().__init__(server, type_name, icon, device_class)
        self._attr_native_unit_of_measurement = unit

    @property
    def available(self) -> bool:
        """Return sensor availability."""
        return self._server.online


class MinecraftServerVersionSensor(MinecraftServerSensorEntity):
    """Representation of a Minecraft Server version sensor."""

    _attr_translation_key = "version"

    def __init__(self, server: MinecraftServer) -> None:
        """Initialize version sensor."""
        super().__init__(server=server, type_name=NAME_VERSION, icon=ICON_VERSION)

    async def async_update(self) -> None:
        """Update version."""
        self._attr_native_value = self._server.version


class MinecraftServerProtocolVersionSensor(MinecraftServerSensorEntity):
    """Representation of a Minecraft Server protocol version sensor."""

    _attr_translation_key = "protocol_version"

    def __init__(self, server: MinecraftServer) -> None:
        """Initialize protocol version sensor."""
        super().__init__(
            server=server,
            type_name=NAME_PROTOCOL_VERSION,
            icon=ICON_PROTOCOL_VERSION,
        )

    async def async_update(self) -> None:
        """Update protocol version."""
        self._attr_native_value = self._server.protocol_version


class MinecraftServerLatencyTimeSensor(MinecraftServerSensorEntity):
    """Representation of a Minecraft Server latency time sensor."""

    _attr_translation_key = "latency"

    def __init__(self, server: MinecraftServer) -> None:
        """Initialize latency time sensor."""
        super().__init__(
            server=server,
            type_name=NAME_LATENCY_TIME,
            icon=ICON_LATENCY_TIME,
            unit=UnitOfTime.MILLISECONDS,
        )

    async def async_update(self) -> None:
        """Update latency time."""
        self._attr_native_value = self._server.latency_time


class MinecraftServerPlayersOnlineSensor(MinecraftServerSensorEntity):
    """Representation of a Minecraft Server online players sensor."""

    _attr_translation_key = "players_online"

    def __init__(self, server: MinecraftServer) -> None:
        """Initialize online players sensor."""
        super().__init__(
            server=server,
            type_name=NAME_PLAYERS_ONLINE,
            icon=ICON_PLAYERS_ONLINE,
            unit=UNIT_PLAYERS_ONLINE,
        )

    async def async_update(self) -> None:
        """Update online players state and device state attributes."""
        self._attr_native_value = self._server.players_online

        extra_state_attributes = {}
        players_list = self._server.players_list

        if players_list is not None and len(players_list) != 0:
            extra_state_attributes[ATTR_PLAYERS_LIST] = self._server.players_list

        self._attr_extra_state_attributes = extra_state_attributes


class MinecraftServerPlayersMaxSensor(MinecraftServerSensorEntity):
    """Representation of a Minecraft Server maximum number of players sensor."""

    _attr_translation_key = "players_max"

    def __init__(self, server: MinecraftServer) -> None:
        """Initialize maximum number of players sensor."""
        super().__init__(
            server=server,
            type_name=NAME_PLAYERS_MAX,
            icon=ICON_PLAYERS_MAX,
            unit=UNIT_PLAYERS_MAX,
        )

    async def async_update(self) -> None:
        """Update maximum number of players."""
        self._attr_native_value = self._server.players_max


class MinecraftServerMOTDSensor(MinecraftServerSensorEntity):
    """Representation of a Minecraft Server MOTD sensor."""

    _attr_translation_key = "motd"

    def __init__(self, server: MinecraftServer) -> None:
        """Initialize MOTD sensor."""
        super().__init__(
            server=server,
            type_name=NAME_MOTD,
            icon=ICON_MOTD,
        )

    async def async_update(self) -> None:
        """Update MOTD."""
        self._attr_native_value = self._server.motd
