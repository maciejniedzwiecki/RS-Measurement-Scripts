from RsInstrument import *
from time import sleep

analyzer = RsInstrument('TCPIP::192.168.1.30::5025::SOCKET ', reset=True, id_query=True, options="SelectVisa='socket'")
recdur = 10  # Time in seconds to find max hold peaks
filename = 'TraceFile.CSV'


def com_prep():
    """Preparation of the communication (termination, timeout, etc...)"""

    print(f'VISA Manufacturer: {analyzer.visa_manufacturer}')  # Confirm VISA package to be chosen
    analyzer.visa_timeout = 5000  # Timeout in ms for VISA Read Operations
    analyzer.opc_timeout = 3000  # Timeout in ms for opc-synchronised operations
    analyzer.instrument_status_checking = True  # Error check after each command
    analyzer.clear_status()  # Clear status register


def close():
    """Close the VISA session"""
    analyzer.close()


def com_check():
    """Check communication with the device by requesting it's ID"""
    idn_response = analyzer.query_str('*IDN?')
    print('Hello, I am ' + idn_response)


def meas_prep(freq: int, span: int, mode: str, revlevel: int, rbw: str):
    analyzer.write_str_with_opc(f'FREQuency:CENTer {freq}')
    analyzer.write_str_with_opc(f'FREQuency:SPAN {span}')
    analyzer.write_str_with_opc(f'BAND {rbw}')
    analyzer.write_str_with_opc(f'DISPlay:TRACe1:MODE {mode}')  # Trace to Max Hold
    analyzer.write_str_with_opc(f'DISPlay:WINDow:TRACe:Y:SCALe:RLEVel {revlevel}')


def trace_get():

    total_amp = 0
    for i in range(0, 5):
        """Initialize continuous measurement, stop it after the desired time, query trace data"""
        analyzer.write_str_with_opc('INITiate:CONTinuous ON')  # Continuous measurement on trace 1 ON
        print('Please wait for maxima to be found...')
        sleep(int(recdur))  # Wait for preset record time
        analyzer.write('DISPlay:TRACe1:MODE AVERage')  # Set trace to view mode / stop collecting data
        analyzer.query_opc()
        sleep(0.5)

        # Get y data (amplitude for each point)
        trace_data = analyzer.query('Trace:DATA? TRACe1')  # Read y data of trace 1
        csv_trace_data = trace_data.split(",")  # Slice the amplitude list
        trace_len = len(csv_trace_data)  # Get number of elements of this list

        # Reconstruct x data (frequency for each point) as it can not be directly read from the analyzer
        start_freq = analyzer.query_float('FREQuency:STARt?')
        span = analyzer.query_float('FREQuency:SPAN?')
        step_size = span / (trace_len - 1)

        # Now write values into file
        file = open(filename, 'a+')  # Open file for writing
        max_amp = -150
        x = 0  # Set counter to 0 as list starts with 0
        while x < int(trace_len):  # Perform loop until all sweep points are covered
            amp = float(csv_trace_data[x])
            if amp > max_amp:
                max_amp = amp
                max_x = x

            x = x + 1

        total_amp = total_amp + max_amp
        avg_amp = total_amp / 5
    file.write(f'{(start_freq + max_x * step_size):.1f}')  # Write adequate frequency information
    file.write(";")
    file.write(f'{avg_amp:.2f}')  # Write adequate amplitude information
    file.write("\n")

    print(start_freq, f'{avg_amp:.2f}')
    file.close()  # CLose the file
