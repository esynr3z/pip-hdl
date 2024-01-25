.PHONY: all clean build sim

BIN   := Vtop
NPROC := 4

# Export all variables needed for filelists
$(foreach var, $(shell pip-hdl inspect requirements.txt all_sources_vars), $(eval export $(var)))

BUILD_OPTS = \
	--timescale 1ns/1ps \
	--cc \
	--binary \
	--timing \
	-O3 \
	-j $(NPROC) \
	-o $(BIN)

SOURCES = \
	$(shell pip-hdl inspect requirements.txt all_filelists_as_args) \
	tb.sv

all: clean build sim

clean:
	rm -rf obj_dir

build:
	# This export is an alternative to a global foreach loop export above
	#export $(shell pip-hdl inspect requirements.txt all_sources_vars);\
	verilator $(BUILD_OPTS) $(SOURCES)

sim:
	./obj_dir/$(BIN)
