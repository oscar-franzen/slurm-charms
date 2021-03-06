#! /usr/bin/env python3
"""SlurmdbdProvidesRelation."""
import logging
import socket


from ops.framework import (
    EventBase,
    EventSource,
    Object,
    ObjectEvents,
    StoredState,
)


logger = logging.getLogger()


class SlurmctldAvailableEvent(EventBase):
    """Emitted when slurmctld is available."""


class SlurmctldUnAvailableEvent(EventBase):
    """Emitted when slurmctld is unavailable."""


class MungeKeyAvailableEvent(EventBase):
    """Emitted when the munge key becomes available."""


class SlurmdbdProvidesRelationEvents(ObjectEvents):
    """SlurmdbdProvidesRelationEvents."""

    munge_key_available = EventSource(MungeKeyAvailableEvent)
    slurmctld_available = EventSource(SlurmctldAvailableEvent)
    slurmctld_unavailable = EventSource(SlurmctldUnAvailableEvent)


class SlurmdbdProvidesRelation(Object):
    """SlurmdbdProvidesRelation."""

    on = SlurmdbdProvidesRelationEvents()

    _stored = StoredState()

    def __init__(self, charm, relation_name):
        """Set the provides initial data."""
        super().__init__(charm, relation_name)

        self._charm = charm
        self._relation_name = relation_name

        self._stored.set_default(munge_key=str())

        self.framework.observe(
            self._charm.on[self._relation_name].relation_created,
            self._on_relation_created
        )

        self.framework.observe(
            self._charm.on[self._relation_name].relation_changed,
            self._on_relation_changed
        )

        self.framework.observe(
            self._charm.on[self._relation_name].relation_broken,
            self._on_relation_broken
        )

    def set_slurmdbd_available_on_unit_relation_data(self):
        """Set slurmdbd_available."""
        slurmdbd_relations = self.framework.model.relations['slurmdbd']
        # Iterate over each of the relations setting the relation data.
        for relation in slurmdbd_relations:
            relation.data[self.model.unit]['slurmdbd_available'] = "true"

    def _on_relation_created(self, event):
        unit_relation_data = event.relation.data[self.model.unit]
        unit_relation_data['slurmdbd_available'] = "false"
        unit_relation_data['hostname'] = socket.gethostname().split(".")[0]
        unit_relation_data['port'] = "6819"

    def _on_relation_changed(self, event):
        app_relation_data = event.relation.data.get(event.app)
        # Check for the existence of the app in the relation data
        # defer if not exists.
        if not app_relation_data:
            event.defer()
            return

        munge_key = app_relation_data.get('munge_key')
        # Check for the existence of the munge key in the relation data
        # defer if not exists.
        if not munge_key:
            event.defer()
            return

        self._charm.set_munge_key(munge_key)
        self.on.munge_key_available.emit()

    def _on_relation_broken(self, event):
        """Emit the slurmctld_unavailable event when the relation is broken."""
        self.on.slurmctld_unavailable.emit()
