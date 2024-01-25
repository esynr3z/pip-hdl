module tb;
  import fizzbuzz_agent_pkg::fizzbuzz_agent;

  initial begin
    fizzbuzz_agent agent = new();

    void'(agent.run_sequence(100));
    $finish();
  end
endmodule
