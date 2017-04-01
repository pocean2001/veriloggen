from __future__ import absolute_import
from __future__ import print_function
import sys
import os

# the next line can be removed after installation
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))

from veriloggen import *
import veriloggen.thread as vthread
import veriloggen.types.axi as axi

import veriloggen.types.ipcore as ipcore


def mkLed():
    m = Module('blinkled')
    clk = m.Input('CLK')
    rst = m.Input('RST')

    datawidth = 32
    addrwidth = 10
    myaxi = vthread.AXIM(m, 'myaxi', clk, rst, datawidth)
    myram = vthread.RAM(m, 'myram', clk, rst, datawidth, addrwidth)

    saxi = vthread.AXISLite(m, 'saxi', clk, rst, datawidth)
    saxi.make_register()

    all_ok = m.TmpReg(initval=0)

    def blink(size):
        # done
        saxi.write_register(1, 0)
        # result
        saxi.write_register(2, 0)
        # start
        saxi.wait_register(0, value=1)
        all_ok.value = True

        for i in range(4):
            print('# iter %d start' % i)
            offset = i * 1024 * 16
            body(size, offset)
            print('# iter %d end' % i)

        if all_ok:
            print('ALL OK')
        else:
            print('NOT ALL OK')

        # result
        saxi.write_register(2, all_ok)
        # done
        saxi.write_register(1, 1)

    def body(size, offset):
        # write
        for i in range(size):
            wdata = i + 100
            myram.write(i, wdata)

        laddr = 0
        gaddr = offset
        myaxi.dma_write(myram, laddr, gaddr, size)
        print('dma_write: [%d] -> [%d]' % (laddr, gaddr))

        # write
        for i in range(size):
            wdata = i + 1000
            myram.write(i, wdata)

        laddr = 0
        gaddr = (size + size) * 4 + offset
        myaxi.dma_write(myram, laddr, gaddr, size)
        print('dma_write: [%d] -> [%d]' % (laddr, gaddr))

        # read
        laddr = 0
        gaddr = offset
        myaxi.dma_read(myram, laddr, gaddr, size)
        print('dma_read:  [%d] <- [%d]' % (laddr, gaddr))

        for i in range(size):
            rdata = myram.read(i)
            if rdata != i + 100:
                print('rdata[%d] = %d' % (i, rdata))
                all_ok.value = False

        # read
        laddr = 0
        gaddr = (size + size) * 4 + offset
        myaxi.dma_read(myram, laddr, gaddr, size)
        print('dma_read:  [%d] <- [%d]' % (laddr, gaddr))

        for i in range(size):
            rdata = myram.read(i)
            if rdata != i + 1000:
                print('rdata[%d] = %d' % (i, rdata))
                all_ok.value = False

    th = vthread.Thread(m, 'th_blink', clk, rst, blink)
    fsm = th.start(16)

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

    # slave controller
    _saxi = axi.AxiLiteMaster(m, '_saxi', clk, rst, noio=True)
    _saxi.connect(ports, 'saxi')
    fsm = FSM(m, 'saxi_fsm', clk, rst)

    wdata = m.Reg('wdata', 32, initval=0)

    for _ in range(8):
        awaddr = 0
        ack = _saxi.write_request(awaddr, cond=fsm)
        fsm(
            wdata(0)  # not start
        )
        fsm.If(ack).goto_next()

        ack = _saxi.write_data(wdata, cond=fsm)
        fsm.If(ack).goto_next()

    awaddr = 0
    ack = _saxi.write_request(awaddr, cond=fsm)
    fsm(
        wdata(1)  # start
    )
    fsm.If(ack).goto_next()

    ack = _saxi.write_data(wdata, cond=fsm)
    fsm.If(ack).goto_next()

    # wait done
    wait_state = fsm.current

    araddr = 4 * 1
    ack = _saxi.read_request(araddr, cond=fsm)
    fsm.If(ack).goto_next()

    rdata, rvalid = _saxi.read_data(cond=fsm)
    fsm.If(rvalid, rdata == 0).goto(wait_state)
    fsm.If(rvalid, rdata != 0).goto_next()

    # check
    araddr = 4 * 2
    ack = _saxi.read_request(araddr, cond=fsm)
    fsm.If(ack).goto_next()

    rdata, rvalid = _saxi.read_data(cond=fsm)
    fsm.If(rvalid, rdata)(
        Display('SLAVE: ALL OK')
    )
    fsm.If(rvalid, Not(rdata))(
        Display('SLAVE: NOT ALL OK')
    )
    fsm.If(rvalid).goto_next()

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

    simcode = """
reg [31:0] _addr;
reg [31:0] _data;
initial begin
  #1000;
  _addr = 0;
  _data = 1;
  slave_write_ipgen_slave_lite_memory_saxi_1(_data, _addr);

  _addr = 4;
  _data = 0;
  while(_data == 0) begin
    slave_read_ipgen_slave_lite_memory_saxi_1(_data, _addr);
    nclk();
  end

  _addr = 8;
  slave_read_ipgen_slave_lite_memory_saxi_1(_data, _addr);
  if(_data) begin
    $display("SLAVE: ALL OK");
  end else begin
    $display("SLAVE: NOT ALL OK");
  end

  #10000;
  $finish;
end
"""

    m = mkLed()
    ipcore.to_ipcore(m, 'myipcore', simcode=simcode, iftype='axi')