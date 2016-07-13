from __future__ import absolute_import
from __future__ import print_function
import veriloggen
import types_bram_read_dataflow

expected_verilog = """
module test;

  reg CLK;
  reg RST;

  main
  uut
  (
    .CLK(CLK),
    .RST(RST)
  );


  initial begin
    $dumpfile("uut.vcd");
    $dumpvars(0, uut, CLK, RST);
  end


  initial begin
    CLK = 0;
    forever begin
      #5 CLK = !CLK;
    end
  end


  initial begin
    RST = 0;
    #100;
    RST = 1;
    #100;
    RST = 0;
    #100000;
    $finish;
  end


endmodule



module main
(
  input CLK,
  input RST
);

  reg [14-1:0] mybram_0_addr;
  wire [32-1:0] mybram_0_rdata;
  reg [32-1:0] mybram_0_wdata;
  reg mybram_0_wenable;
  reg [14-1:0] mybram_1_addr;
  wire [32-1:0] mybram_1_rdata;
  reg [32-1:0] mybram_1_wdata;
  reg mybram_1_wenable;

  mybram
  inst_mybram
  (
    .CLK(CLK),
    .mybram_0_addr(mybram_0_addr),
    .mybram_0_rdata(mybram_0_rdata),
    .mybram_0_wdata(mybram_0_wdata),
    .mybram_0_wenable(mybram_0_wenable),
    .mybram_1_addr(mybram_1_addr),
    .mybram_1_rdata(mybram_1_rdata),
    .mybram_1_wdata(mybram_1_wdata),
    .mybram_1_wenable(mybram_1_wenable)
  );

  reg [32-1:0] fsm;
  localparam fsm_init = 0;
  reg [8-1:0] _tmp_0;
  reg _tmp_1;
  wire [32-1:0] _tmp_data_2;
  wire _tmp_valid_2;
  wire _tmp_ready_2;
  assign _tmp_ready_2 = (fsm == 0) && !_tmp_1;
  reg _mybram_cond_0_1;
  reg _tmp_3;
  reg _tmp_4;
  wire _tmp_5;
  wire _tmp_6;
  assign _tmp_5 = 1 && _tmp_ready_15;
  assign _tmp_6 = 1 && _tmp_ready_16;
  localparam _tmp_7 = 1;
  wire [_tmp_7-1:0] _tmp_8;
  assign _tmp_8 = (_tmp_5 || !_tmp_3) && (_tmp_6 || !_tmp_4);
  reg [_tmp_7-1:0] __tmp_8_1;
  wire [32-1:0] _tmp_9;
  reg [32-1:0] __tmp_9_1;
  assign _tmp_9 = (__tmp_8_1)? mybram_1_rdata : __tmp_9_1;
  reg [7-1:0] _tmp_10;
  reg _tmp_11;
  reg _tmp_12;
  reg _tmp_13;
  reg _tmp_14;
  wire [32-1:0] _tmp_data_15;
  wire _tmp_valid_15;
  wire _tmp_ready_15;
  assign _tmp_ready_15 = 1;
  wire [1-1:0] _tmp_data_16;
  wire _tmp_valid_16;
  wire _tmp_ready_16;
  assign _tmp_ready_16 = 1;
  reg [32-1:0] sum;
  reg _seq_cond_0_1;

  always @(posedge CLK) begin
    if(RST) begin
      mybram_1_wdata <= 0;
      mybram_1_wenable <= 0;
      mybram_0_addr <= 0;
      mybram_0_wdata <= 0;
      mybram_0_wenable <= 0;
      _tmp_0 <= 0;
      _tmp_1 <= 0;
      _mybram_cond_0_1 <= 0;
      __tmp_8_1 <= 0;
      __tmp_9_1 <= 0;
      _tmp_14 <= 0;
      _tmp_3 <= 0;
      _tmp_4 <= 0;
      _tmp_12 <= 0;
      _tmp_13 <= 0;
      _tmp_11 <= 0;
      mybram_1_addr <= 0;
      _tmp_10 <= 0;
    end else begin
      if(_mybram_cond_0_1) begin
        mybram_0_wenable <= 0;
        _tmp_1 <= 0;
      end 
      mybram_1_wdata <= 0;
      mybram_1_wenable <= 0;
      if(_tmp_valid_2 && ((fsm == 0) && !_tmp_1) && (_tmp_0 == 0)) begin
        mybram_0_addr <= 0;
        mybram_0_wdata <= _tmp_data_2;
        mybram_0_wenable <= 1;
        _tmp_0 <= 63;
      end 
      if(_tmp_valid_2 && ((fsm == 0) && !_tmp_1) && (_tmp_0 > 0)) begin
        mybram_0_addr <= mybram_0_addr + 1;
        mybram_0_wdata <= _tmp_data_2;
        mybram_0_wenable <= 1;
        _tmp_0 <= _tmp_0 - 1;
      end 
      if(_tmp_valid_2 && ((fsm == 0) && !_tmp_1) && (_tmp_0 == 1)) begin
        _tmp_1 <= 1;
      end 
      _mybram_cond_0_1 <= 1;
      __tmp_8_1 <= _tmp_8;
      __tmp_9_1 <= _tmp_9;
      if((_tmp_5 || !_tmp_3) && (_tmp_6 || !_tmp_4) && _tmp_12) begin
        _tmp_14 <= 0;
        _tmp_3 <= 0;
        _tmp_4 <= 0;
        _tmp_12 <= 0;
      end 
      if((_tmp_5 || !_tmp_3) && (_tmp_6 || !_tmp_4) && _tmp_11) begin
        _tmp_3 <= 1;
        _tmp_4 <= 1;
        _tmp_14 <= _tmp_13;
        _tmp_13 <= 0;
        _tmp_11 <= 0;
        _tmp_12 <= 1;
      end 
      if((_tmp_5 || !_tmp_3) && (_tmp_6 || !_tmp_4) && (fsm == 2) && (_tmp_10 == 0) && !_tmp_13 && !_tmp_14) begin
        mybram_1_addr <= 0;
        _tmp_10 <= 31;
        _tmp_11 <= 1;
      end 
      if((_tmp_5 || !_tmp_3) && (_tmp_6 || !_tmp_4) && (_tmp_10 > 0)) begin
        mybram_1_addr <= mybram_1_addr + 1;
        _tmp_10 <= _tmp_10 - 1;
        _tmp_11 <= 1;
        _tmp_13 <= 0;
      end 
      if((_tmp_5 || !_tmp_3) && (_tmp_6 || !_tmp_4) && (_tmp_10 == 1)) begin
        _tmp_13 <= 1;
      end 
    end
  end

  assign _tmp_data_15 = _tmp_9;
  assign _tmp_valid_15 = _tmp_3;
  assign _tmp_data_16 = _tmp_14;
  assign _tmp_valid_16 = _tmp_4;
  reg [32-1:0] _tmp_data_17;
  reg _tmp_valid_17;
  wire _tmp_ready_17;
  assign _tmp_ready_17 = (_tmp_ready_18 || !_tmp_valid_18) && _tmp_valid_17;
  reg [32-1:0] _tmp_data_18;
  reg _tmp_valid_18;
  wire _tmp_ready_18;
  assign _tmp_data_2 = _tmp_data_18;
  assign _tmp_valid_2 = _tmp_valid_18;
  assign _tmp_ready_18 = _tmp_ready_2;

  always @(posedge CLK) begin
    if(RST) begin
      _tmp_data_17 <= 1'd0;
      _tmp_valid_17 <= 0;
      _tmp_data_18 <= 0;
      _tmp_valid_18 <= 0;
    end else begin
      if((_tmp_ready_17 || !_tmp_valid_17) && 1 && 1) begin
        _tmp_data_17 <= _tmp_data_17 + 2'd1;
      end 
      if(_tmp_valid_17 && _tmp_ready_17) begin
        _tmp_valid_17 <= 0;
      end 
      if((_tmp_ready_17 || !_tmp_valid_17) && 1) begin
        _tmp_valid_17 <= 1;
      end 
      if((_tmp_ready_18 || !_tmp_valid_18) && _tmp_ready_17 && _tmp_valid_17) begin
        _tmp_data_18 <= _tmp_data_17 - 2'd1;
      end 
      if(_tmp_valid_18 && _tmp_ready_18) begin
        _tmp_valid_18 <= 0;
      end 
      if((_tmp_ready_18 || !_tmp_valid_18) && _tmp_ready_17) begin
        _tmp_valid_18 <= _tmp_valid_17;
      end 
    end
  end

  localparam fsm_1 = 1;
  localparam fsm_2 = 2;
  localparam fsm_3 = 3;

  always @(posedge CLK) begin
    if(RST) begin
      fsm <= fsm_init;
    end else begin
      case(fsm)
        fsm_init: begin
          if(_tmp_1) begin
            fsm <= fsm_1;
          end 
        end
        fsm_1: begin
          fsm <= fsm_2;
        end
        fsm_2: begin
          if(_tmp_14) begin
            fsm <= fsm_3;
          end 
        end
      endcase
    end
  end


  always @(posedge CLK) begin
    if(RST) begin
      sum <= 0;
      _seq_cond_0_1 <= 0;
    end else begin
      if(_seq_cond_0_1) begin
        $display("sum=%d expected_sum=%d", sum, 496);
      end 
      if(_tmp_valid_15) begin
        sum <= sum + _tmp_data_15;
      end 
      _seq_cond_0_1 <= _tmp_valid_15 && (_tmp_data_16 == 1);
    end
  end


endmodule



module mybram
(
  input CLK,
  input [14-1:0] mybram_0_addr,
  output [32-1:0] mybram_0_rdata,
  input [32-1:0] mybram_0_wdata,
  input mybram_0_wenable,
  input [14-1:0] mybram_1_addr,
  output [32-1:0] mybram_1_rdata,
  input [32-1:0] mybram_1_wdata,
  input mybram_1_wenable
);

  reg [14-1:0] mybram_0_daddr;
  reg [14-1:0] mybram_1_daddr;
  reg [32-1:0] mem [0:16384-1];

  always @(posedge CLK) begin
    if(mybram_0_wenable) begin
      mem[mybram_0_addr] <= mybram_0_wdata;
    end 
    mybram_0_daddr <= mybram_0_addr;
  end

  assign mybram_0_rdata = mem[mybram_0_daddr];

  always @(posedge CLK) begin
    if(mybram_1_wenable) begin
      mem[mybram_1_addr] <= mybram_1_wdata;
    end 
    mybram_1_daddr <= mybram_1_addr;
  end

  assign mybram_1_rdata = mem[mybram_1_daddr];

endmodule
"""


def test():
    veriloggen.reset()
    test_module = types_bram_read_dataflow.mkTest()
    code = test_module.to_verilog()

    from pyverilog.vparser.parser import VerilogParser
    from pyverilog.ast_code_generator.codegen import ASTCodeGenerator
    parser = VerilogParser()
    expected_ast = parser.parse(expected_verilog)
    codegen = ASTCodeGenerator()
    expected_code = codegen.visit(expected_ast)

    assert(expected_code == code)
