# See LICENSE.iitm for details
# See LICENSE.vyoma for details

import random
import sys
import cocotb
from cocotb.decorators import coroutine
from cocotb.triggers import Timer, RisingEdge
from cocotb.result import TestFailure
from cocotb.clock import Clock

from model_mkbitmanip import *

# Clock Generation
@cocotb.coroutine
def clock_gen(signal):
    while True:
        signal.value <= 0
        yield Timer(1) 
        signal.value <= 1
        yield Timer(1) 

# Sample Test
@cocotb.test()
def run_test(dut):

    # clock
    cocotb.fork(clock_gen(dut.CLK))

    # reset
    dut.RST_N.value <= 0
    yield Timer(10) 
    dut.RST_N.value <= 1
    cocotb.log.info('RST_N deasserted') 
    ######### CTB : Modify the test to expose the bug #############
    for i in range (2):
    # input transaction
       cocotb.log.info(f'Driving transactions i = {i}')   
       mav_putvalue_src1 = random.randint(0x55555555,0xAAAAAAAA ) #0x5
       mav_putvalue_src2 = 0xa5a55a5a
       mav_putvalue_src3 = 0xa5a55a5a
       mav_putvalue_instr = 0x40007033 # 0x101010B3

       # expected output from the model
       expected_mav_putvalue = bitmanip(mav_putvalue_instr, mav_putvalue_src1, mav_putvalue_src2, mav_putvalue_src3)

       # driving the input transaction
       dut.mav_putvalue_src1.value = mav_putvalue_src1
       dut.mav_putvalue_src2.value = mav_putvalue_src2
       dut.mav_putvalue_src3.value = mav_putvalue_src3
       dut.EN_mav_putvalue.value = 1
       dut.mav_putvalue_instr.value = mav_putvalue_instr
  
       yield Timer(4) # wait one clock cycle
       #await (dut.mav_putvalue[0].value == 1)
       # obtaining the output
       dut_output = dut.mav_putvalue.value

       cocotb.log.info(f'DUT OUTPUT={hex(dut_output)}')
       cocotb.log.info(f'EXPECTED OUTPUT={hex(expected_mav_putvalue)}')
    
       # comparison
       if(dut.mav_putvalue[0].value):
          error_message = f'Value mismatch DUT = {hex(dut_output)} does not match MODEL = {hex(expected_mav_putvalue)}'
          assert dut_output == expected_mav_putvalue, error_message
