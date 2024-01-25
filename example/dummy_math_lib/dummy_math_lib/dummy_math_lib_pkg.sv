package dummy_math_lib_pkg;
  function automatic bit is_divisible_by_3(int unsigned number);
    return (number % 3) == 0;
  endfunction

  function automatic bit is_divisible_by_5(int unsigned number);
    return (number % 5) == 0;
  endfunction
endpackage