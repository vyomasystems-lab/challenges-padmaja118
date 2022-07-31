# Mux Design Verification

The verification environment is setup using [Vyoma's UpTickPro](https://vyomasystems.com) provided for the hackathon.

![image](https://user-images.githubusercontent.com/96460492/182003829-78a7512c-a8f4-4614-8972-42f715209bf8.png)


## Verification Environment

The [CoCoTb](https://www.cocotb.org/) based Python test is developed as explained. The test drives inputs to the Design Under Test (31x1 mux module here) which takes in 31 two bit wide inputs and 5 wide sel and gives two bit wide output *out*

The values are assigned to the input port using below code. As mux design takes 31 (0 to 30) inputs and each input is 2 bit wide, I have a for loop veriable i from 0 to 30 and assign i to the select line. 
Then for each select line, i have another loop from 0 to 3 to drive the inputs and check the output with the expected output.
```
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

```

The assert statement is used for comparing the adder's outut to the expected value.


## Test Scenario **(Important)**
- Checks all the select lines with all combinations of inputs 
- Expected Output: what we are driving to the corresponding input port. 
- Observed Output in the DUT dut.out == dut.inp<i>

 Output mismatches for the above inputs proving that there is a design bug

## Design Bug
Based on the above test input and analysing the design, I see the following bugs

```
      5'b01011: out = inp11;
      5'b01101: out = inp12;   ====> BUG1   this should be  5'b01100: out = inp12;
      5'b01101: out = inp13;

  
      5'b11100: out = inp28;
      5'b11101: out = inp29;
                             ====> BUG2   missing case30  5'b11110: out = inp30;
      default: out = 0;
```


## Design Fix
Updating the design and re-running the test makes the test pass.


The updated design is checked in as mux.v

## Verification Strategy
  Verify the all the possible combinations 

## Is the verification complete ?
  Yes, I covered all the possible input combinations.
