from __future__ import annotations

from typing import List, Optional, Sequence, Tuple, Union, Mapping, Callable, Awaitable

import stem.control
from stem.descriptor.router_status_entry import RouterStatusEntryV3
from stem.response.events import CircuitEvent, StreamEvent

# temp
from stem.response.events import Event
from stem.control import EventType

from .models import Circuit, Hop, Relay, Stream


class Control():

    @staticmethod
    def from_port(address: str = '127.0.0.1', port: Union[int, str] = 'default') -> Control:
        return Control(stem.control.Controller.from_port(address, port))

    def __init__(self, controller: stem.control.Controller = None):
        self._controller = controller

    def authenticate(self, password=None, chroot_path=None, protocolinfo_response=None):
        self._controller.authenticate(
            password, chroot_path, protocolinfo_response)

    def close(self):
        self._controller.close()

    def get_circuits(self) -> List[Circuit]:
        circuit_events: List[CircuitEvent] = self._controller.get_circuits()
        circuits = self._to_circuits(circuit_events)
        return circuits

    def get_circuit(self, circuit_id: int) -> Optional[Circuit]:
        circuits = self.get_circuits()
        for circuit in circuits:
            if circuit.id == circuit_id:
                return circuit
        return None

    def new_circuit(self, path: Union[None, str, Sequence[str]] = None, purpose: str = 'general', await_build: bool = False, timeout: Optional[float] = None) -> str:
        return self.extend_circuit('0', path, purpose, await_build, timeout)

    def extend_circuit(self, circuit_id: str = '0', path: Union[None, str, Sequence[str]] = None, purpose: str = 'general', await_build: bool = False, timeout: Optional[float] = None) -> str:
        return self._controller.extend_circuit(circuit_id, path, purpose, await_build, timeout)

    def close_circuit(self, circuit_id: str, flag: str = '') -> None:
        return self._controller.close_circuit(circuit_id, flag)

    def get_network_status(self, relay: Optional[str] = None) -> Relay:
        router_status: RouterStatusEntryV3 = self._controller.get_network_status(
            relay)
        return self._to_relay(router_status)

    def get_network_statuses(self, relays: Optional[Sequence[str]] = None) -> List[Relay]:
        router_statuses: List[RouterStatusEntryV3] = self._controller.get_network_statuses(
            relays)
        return self._to_relays(router_statuses)

    def get_streams(self) -> List[Stream]:
        stream_events: List[StreamEvent] = self._controller.get_streams()
        streams = self._to_streams(stream_events)
        return streams

    def get_stream(self, stream_id: int) -> Optional[Stream]:
        streams = self.get_streams()
        for stream in streams:
            if stream.id == stream_id:
                return stream
        return None

    def attach_stream(self, stream_id, circuit_id, exiting_hop=None):
        self._controller.attach_stream(stream_id, circuit_id, exiting_hop)

    # type: ignore
    def add_event_listener(self, listener: Callable[[Event], Union[None, Awaitable[None]]], *events: EventType) -> None:
        self._controller.add_event_listener(listener, *events)

    def remove_event_listener(self, listener: Callable[[Event], Union[None, Awaitable[None]]]) -> None:
        self._controller.remove_event_listener(listener)

    def set_conf(self, param: str, value: Union[str, Sequence[str]]) -> None:
        self.set_options({param: value}, False)

    def reset_conf(self, params: str):
        self.set_options(Mapping([(entry, None) for entry in params]), True)

    def set_options(self, params: Union[Mapping[str, Union[str, Sequence[str]]], Sequence[Tuple[str, Union[str, Sequence[str]]]]], reset: bool = False) -> None:
        self._controller.set_options(params, reset)

    def get_info(self, params: Union[str, Sequence[str]]) -> Union[str, Mapping[str]]:
        return self._controller.get_info(params)

    def _to_circuits(self, circuit_events: List[CircuitEvent]) -> List[Circuit]:
        return [self._to_circuit(circuit_event) for circuit_event in circuit_events]

    def _to_circuit(self, circuit_event: CircuitEvent) -> Circuit:
        return Circuit(
            id=circuit_event.id,
            path=[self._to_hop(hop) for hop in circuit_event.path],
            created=circuit_event.created,
        )

    def _to_hop(self, hop: Tuple[str, str]) -> Hop:
        return Hop(
            fingerprint=hop[0],
            nickname=hop[1],
        )

    def _to_relays(self, router_statuses: List[RouterStatusEntryV3]) -> List[Relay]:
        return [self._to_relay(router_status) for router_status in router_statuses]

    def _to_relay(self, router_status: RouterStatusEntryV3) -> Relay:
        return Relay(
            fingerprint=router_status.fingerprint,
            nickname=router_status.nickname,
            address=router_status.address,
            or_port=router_status.or_port,
            flags=router_status.flags,
            bandwidth=router_status.bandwidth,
        )

    def _to_streams(self, stream_events: List[StreamEvent]) -> List[Stream]:
        return [self._to_stream(stream_event) for stream_event in stream_events]

    def _to_stream(self, stream_event: StreamEvent) -> Stream:
        return Stream(
            id=stream_event.id,
            target=stream_event.target,
        )

    # useful methods

    def get_country(self, address: str) -> str:
        return self.get_info(f'ip-to-country/{address}')

    def disable_stream_attachment(self):
        self.set_conf('__LeaveStreamsUnattached', '1')

    def enable_stream_attachment(self):
        self.reset_conf('__LeaveStreamsUnattached')

    def get_exit_relays(self) -> List[Relay]:
        relays = self.get_network_statuses()
        return [relay for relay in relays if 'Exit' in relay.flags]

    def get_exit_relays_by_country(self, _country: str) -> List[Relay]:
        exit_relays = self.get_exit_relays()
        return [relay for relay in exit_relays if self.get_country(relay.address) == _country]
