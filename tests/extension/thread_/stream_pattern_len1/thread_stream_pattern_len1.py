from __future__ import absolute_import
from __future__ import print_function
import sys
import os
import functools

# the next line can be removed after installation
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))

from veriloggen import *
import veriloggen.thread as vthread
import veriloggen.types.axi as axi


def mkLed():
    m = Module('blinkled')
    clk = m.Input('CLK')
    rst = m.Input('RST')

    datawidth = 32
    addrwidth = 10
    myaxi = vthread.AXIM(m, 'myaxi', clk, rst, datawidth)
    ram_a = vthread.RAM(m, 'ram_a', clk, rst, datawidth, addrwidth)
    ram_b = vthread.RAM(m, 'ram_b', clk, rst, datawidth, addrwidth)
    ram_c = vthread.RAM(m, 'ram_c', clk, rst, datawidth, addrwidth)

    shape = [1, 1, 1]
    size = functools.reduce(lambda x, y: x * y, shape, 1)
    order = [1, 2, 0]

    def to_pattern(shape, order):
        pattern = []
        for p in order:
            size = shape[p]
            stride = functools.reduce(lambda x, y: x * y,
                                      shape[p + 1:], 1)
            pattern.append((size, stride))
        return pattern

    pattern_a = to_pattern(shape, order)
    pattern_b = to_pattern(shape, order)
    pattern_c = to_pattern(shape, order)

    strm = vthread.Stream(m, 'mystream', clk, rst)
    a = strm.source('a')
    b = strm.source('b')
    c = a + b
    strm.sink(c, 'c')

    def comp_stream(offset):
        strm.set_source_pattern('a', ram_a, offset, pattern_a)
        strm.set_source_pattern('b', ram_b, offset, pattern_b)
        strm.set_sink_pattern('c', ram_c, offset, pattern_c)
        strm.run()
        strm.join()

    def comp_sequential(offset):
        sum = 0
        for i in range(size):
            a = ram_a.read(i + offset)
            b = ram_b.read(i + offset)
            sum = a + b
            ram_c.write(i + offset, sum)

    def check(offset_stream, offset_seq):
        all_ok = True
        st = ram_c.read(offset_stream)
        sq = ram_c.read(offset_seq)
        if vthread.verilog.NotEql(st, sq):
            all_ok = False

        if all_ok:
            print('OK')
        else:
            print('NG')

    def comp():
        offset = 0
        myaxi.dma_read(ram_a, offset, 0, size)
        myaxi.dma_read(ram_b, offset, 0, size)
        comp_stream(offset)
        myaxi.dma_write(ram_c, offset, 1024 * 4, 1)

        offset = size
        myaxi.dma_read(ram_a, offset, 0, size)
        myaxi.dma_read(ram_b, offset, 0, size)
        comp_sequential(offset)
        myaxi.dma_write(ram_c, offset, 1024 * 8, 1)

        check(0, offset)

    th = vthread.Thread(m, 'th_comp', clk, rst, comp)
    fsm = th.start()

    return m


def mkTest():
    m = Module('test')

    # target instance
    led = mkLed()

    # copy paras and ports
    params = m.copy_params(led)
    ports = m.copy_sim_ports(led)

    clk = ports['CLK']
    rst = ports['RST']

    memory = axi.AxiMemoryModel(m, 'memory', clk, rst)
    memory.connect(ports, 'myaxi')

    uut = m.Instance(led, 'uut',
                     params=m.connect_params(led),
                     ports=m.connect_ports(led))

    simulation.setup_waveform(m, uut)
    simulation.setup_clock(m, clk, hperiod=5)
    init = simulation.setup_reset(m, rst, m.make_reset(), period=100)

    init.add(
        Delay(100000),
        Systask('finish'),
    )

    return m


if __name__ == '__main__':
    test = mkTest()
    verilog = test.to_verilog('tmp.v')
    print(verilog)

    sim = simulation.Simulator(test)
    rslt = sim.run()
    print(rslt)
