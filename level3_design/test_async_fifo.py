

import random
import sys
import cocotb
from cocotb.decorators import coroutine
from cocotb.triggers import Timer, RisingEdge, FallingEdge
from cocotb.result import TestFailure
from cocotb.clock import Clock

       
# Sample Test
@cocotb.test()
async def run_test(dut):

    # clock
    clock = Clock(dut.wclk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock
    clock = Clock(dut.rclk, 12, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock
    
    # reset
    await RisingEdge(dut.wclk)
    dut.wrst_n.value = 0
    await RisingEdge(dut.wclk)
    await RisingEdge(dut.wclk)
    await FallingEdge(dut.wclk)
    dut.wrst_n.value = 1
    await RisingEdge(dut.wclk)

    await RisingEdge(dut.rclk)    
    dut.rrst_n.value = 0
    await RisingEdge(dut.rclk)
    await RisingEdge(dut.rclk)
    await FallingEdge(dut.rclk) 
    dut.rrst_n.value = 1
    await RisingEdge(dut.rclk)
   
    async def drive_txn(rw,data):  
        success = True      
        if rw: #read
            await RisingEdge(dut.rclk)
            if (dut.rempty.value):
                success = False
                print("FIFO rempty")
            else:
                dut.rinc.value = 1
                await FallingEdge(dut.rclk)
                data = (dut.rdata.value)
                await RisingEdge(dut.rclk)
                dut.rinc.value = 0   
        elif not rw:
            await RisingEdge(dut.wclk)
            dut.winc.value = 1
            dut.wdata.value = data
            await RisingEdge(dut.wclk)
            dut.winc.value = 0
            #if FIFO full, data was not written (overflow status)
            if dut.wfull.value:
                print("FIFO full")
                success = False
        return data, success         
    
    for i in range(3): 
       # rw = random.choice([True, False])
       # data = random.randint(0,255) 
       # print("rw=", rw , "data =", data )
        data, success = await drive_txn( False, 0x5A) # Write 0x5A
        print("data=",data,"success=", success)
        data, success = await drive_txn( False, 0x5B) # Write 0x5B
        print("data=",data,"success=", success)
        data, success = await drive_txn( False, 0x5C) # Write 0x5C
        print("data=",data,"success=", success)
        data, success = await drive_txn(True, 0x0) # Read
        print("data=",data,"success=", success)


    
    
