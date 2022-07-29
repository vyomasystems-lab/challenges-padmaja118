# See LICENSE.vyoma for details

import cocotb
import sys
from cocotb.triggers import Timer

@cocotb.test()
async def test_mux(dut):
    """Test for mux2"""
    # Drive inputs 
    for i in range (31):
      dut.sel.value = i
      print(i)
      #await cocotb.triggers.Timer(10, "ns")
      for j in range (4):
           sig = "dut.inp"+str(i)+".value"
           #print(sig)
           exec(sig+" = j")
           #eval("dut.inp"+str(i)+".value") = j
           await cocotb.triggers.Timer(10, "ns")
         
           tmp_val = eval("dut.inp"+str(i)+".value")  
          # print(tmp_val)
           assert(tmp_val == dut.out.value)
             
      
            
       
  #  cocotb.log.info('##### CTB: Develop your test here ########')
