# See LICENSE.vyoma for details

# SPDX-License-Identifier: CC0-1.0

import os
import random
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge

def check(*args):
    num =0
    for x in args:
      num = num*10+int(x)
    if(num == 1011):
      return 1
    else: 
      return 0  
      


@cocotb.test()
async def test_seq_bug1(dut):
    """Test for seq detection """

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    # reset
    dut.reset.value = 1
    await FallingEdge(dut.clk)  
    dut.reset.value = 0
    await FallingEdge(dut.clk)
    bs = []
    cocotb.log.info('#### CTB: Develop your test here! ######')
    for i in range (200):
       bs.append(random.randint(0,1))
       dut.inp_bit.value = bs[i]
       print(bs[i])
       await RisingEdge(dut.clk)
       if(i>3):
          assert(check(bs[i-4], bs[i-3], bs[i-2], bs[i-1]) 
          == dut.seq_seen.value), f"FSM output incorrect: {dut.seq_seen.value} != {check(bs[i-3], bs[i-2], bs[i-1], bs[i])}"


