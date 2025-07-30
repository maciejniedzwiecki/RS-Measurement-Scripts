from RsSmw import *


generator = RsSmw('TCPIP::192.168.1.30::5025::SOCKET ', reset=True, id_query=True, options="SelectVisa='socket'")


def com_check():
    # Driver's instrument status checking ( SYST:ERR? ) after each command (default value is True):
    generator.utilities.instrument_status_checking = True
    # The generator object uses the global HW instance one - RF out A
    generator.repcap_hwInstance_set(repcap.HwInstance.InstA)
    # Direct SCPI interface:
    response = generator.utilities.query_str('*IDN?')
    print(f'Direct SCPI response on *IDN?: {response}')


def meas_prep(set: True, mode, amplitude: int, freq: int):
    generator.output.state.set_value(set)
    generator.source.frequency.set_mode(mode)
    generator.source.power.level.immediate.set_amplitude(amplitude)
    generator.source.frequency.fixed.set_value(freq)
    print(f'Channel 1 PEP level: {generator.source.power.get_pep()} dBm')
