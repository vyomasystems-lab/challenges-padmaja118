# Sequence detector Design Verification

The verification environment is setup using [Vyoma's UpTickPro](https://vyomasystems.com) provided for the hackathon.

*Make sure to include the Gitpod id in the screenshot*
![image](https://user-images.githubusercontent.com/96460492/182003928-61281939-5461-404d-9036-431325e770c8.png)


## Verification Environment

The [CoCoTb](https://www.cocotb.org/) based Python test is developed as explained. The test drives inputs to the Design Under Test (Sequence detector module here) which takes in 1 bit for each clock and if input bit sequence matches with 1011, next cycle it gives high output for one cycle. 

The values are assigned to the input port using below code. As design takes 1 bit for each cycle, test sends random values to the dut and the model and checks with the expected output. 

```
  for i in range (200):
       bs.append(random.randint(0,1))
       dut.inp_bit.value = bs[i]
       print(bs[i])
       await RisingEdge(dut.clk)
       if(i>3):
          assert(check(bs[i-4], bs[i-3], bs[i-2], bs[i-1]) 
          == dut.seq_seen.value), f"FSM output incorrect: {dut.seq_seen.value} != {check(bs[i-3], bs[i-2], bs[i-1], bs[i])}"

```

The assert statement is used for comparing the dut output to the expected value.

The following error is seen:
```
assert dut.sum.value == A+B, "Adder result is incorrect: {A} + {B} != {SUM}, expected value={EXP}".format(
                     AssertionError: Adder result is incorrect: 7 + 5 != 2, expected value=12
```
## Test Scenario **(Important)**
- Checks all the select lines with all combinations of inputs 
- Expected Output: what we are driving to the corresponding input port. 
- Observed Output in the DUT dut.out == dut.inp<i>

 Output mismatches for the above inputs proving that there is a design bug

## Design Bug
Based on the above test input and analysing the design, I see the following bugs

```
  // Original Bug1
        SEQ_1:
      begin
        if(inp_bit == 1)
          next_state = IDLE;
        else
          next_state = SEQ_10;
        end
      SEQ_10:
  
  // After fixing Bug1
      SEQ_1:
      begin
        if(inp_bit == 0)
          next_state = SEQ_10;
        else
          next_state = SEQ_1;
        end
      SEQ_10:
  
  
        if(inp_bit == 1)
          next_state = SEQ_1011;
        else
          next_state = IDLE;    ====> BUG2        next_state = SEQ_10;
      end
      SEQ_1011:
  
  // BUG3
   SEQ_1011:
    begin
        next_state = IDLE;
     end
  
 // BUG3 fix 
     SEQ_1011:
      begin
        next_state = IDLE;
        if(inp_bit ==1)
          next_state = SEQ_1;
        else
          next_state = SEQ_10;  
      end    
```


## Design Fix
Updating the design and re-running the test makes the test pass.


The updated design is checked in as mux.v

## Verification Strategy
  Verify the all the possible combinations 

## Is the verification complete ?
  Not sure, need to check coverage 
