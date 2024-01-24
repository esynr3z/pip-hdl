package hdlp_fizzbuzz_agent_pkg;
    import dummy_math_lib_pkg::is_divisible_by_3;
    import dummy_math_lib_pkg::is_divisible_by_5;

    class fizzbuzz_agent;
        function run_sequence(int unsigned limit);
            for (int i = 0; i < limit; i++) begin
                string msg;

                if (dummy_math_lib_pkg::is_divisible_by_5(i) && dummy_math_lib_pkg::is_divisible_by_3(i)) begin
                    msg = "FizzBuzz";
                end else if (dummy_math_lib_pkg::is_divisible_by_3(i)) begin
                    msg = "Fizz";
                end else if (dummy_math_lib_pkg::is_divisible_by_5(i)) begin
                    msg = "Buzz";
                end else begin
                    msg = $sformatf("%0d", i);
                end

                $display(msg);
            end
        endfunction : run_sequence
    endclass : fizzbuzz_agent
endpackage