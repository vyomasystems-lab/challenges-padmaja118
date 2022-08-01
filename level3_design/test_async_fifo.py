

import random
import sys
import cocotb
from cocotb.decorators import coroutine
from cocotb.triggers import Timer, RisingEdge
from cocotb.result import TestFailure
from cocotb.clock import Clock

# Clock Generation
@cocotb.coroutine
def clock_gen(signal,period=100):
    while True:
        signal.value <= 0
        yield Timer(period/2) 
        signal.value <= 1
        yield Timer(period/2) 
           
def drive_txn(data, rw):        
        if rw: #read
            yield RisingEdge(dut.rclk)
            #even if fifo empty, try to access in order to reach underflow status
            if (dut.rempty):
                success = False
            else:
                data = int(dut.rdata)
            dut.rinc <= 1
            yield RisingEdge(dut.rclk)
            dut.rinc <= 0
        elif not rw:
            yield RisingEdge(dut.wclk)
            dut.wdata <= data
            dut.winc <= 1
            yield RisingEdge(dut.clk)
            dut.winc <= 0
            #if FIFO full, data was not written (overflow status)
            if status.wfull:
                success = False
        return data, success       
        
# Sample Test
@cocotb.test()
def run_test(dut):

    # clock
    cocotb.fork(clock_gen(dut.wclk,period=60))
    cocotb.fork(clock_gen(dut.rclk,period=50))

    # reset
    dut.wrst_n.value <= 0
    yield Timer(10) 
    dut.wrst_n.value <= 1
    cocotb.log.info('wrst_n deasserted')  
    
    dut.rrst_n.value <= 0
    yield Timer(10) 
    dut.rrst_n.value <= 1
    cocotb.log.info('rrst_n deasserted')  
    
    for i in range(3): 
        rw = random.choice([True, False])
        data = random.randint(0,255) if not rw else None
      
        data, success = yield drive_txn(data, rw)
    
    
