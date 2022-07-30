# See LICENSE.vyoma for details

TOPLEVEL_LANG ?= verilog

PWD=$(shell pwd)

VERILOG_SOURCES = $(PWD)/design/async_fifo.v               # provide your design path
VERILOG_SOURCES +=$(PWD)/design/fifo_2mem.v
VERILOG_SOURCES +=$(PWD)/design/rptr_empty.v
VERILOG_SOURCES +=$(PWD)/design/sync_r2w.v
VERILOG_SOURCES +=$(PWD)/design/sync_w2r.v
VERILOG_SOURCES +=$(PWD)/design/wptr_full.v

TOPLEVEL :=  async_fifo         # design file
MODULE   :=  test_async_fifo    # test file

include $(shell cocotb-config --makefiles)/Makefile.sim

clean_all: clean
	rm -rf *.xml sim_build __pycache__ 
