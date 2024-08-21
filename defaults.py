class Default:
    freq = 433          # MHz
    freq_unit = 'MHz'
    bw = 125000         # Hz
    cr = 5
    sf = 7
    plen = 16

    tx_power = 20       # dBm
    lna_gain = 6        # ?
    ack_delay = 0.1     # [s]
    ack_wait = 1        # [s]
    rx_timeout = 0.5    # [s]

    node_addr = 186
    dest_addr = 171

    chksum = False

    host = ''
    port = ''
    usr = ''
    pw = ''

    rotport = 'localhost'
    rotport = '4535'
    rotmodel = '1901'
    rotdevice = '/dev/ttyUSB0'
    sspeed = 115200
    daemoncmd = 'rotctld'
