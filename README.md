# Reed-Solomon Error Correction Demo

## Overview

This project demonstrates the implementation of Reed-Solomon error correction codes using Python. Reed-Solomon codes are a type of error-correcting code that can detect and correct multiple symbol errors in data transmission or storage.

## What are Reed-Solomon Codes?

Reed-Solomon codes are a type of forward error correction (FEC) code that:
- Can detect and correct multiple symbol errors
- Are widely used in digital communications and storage
- Are particularly effective against burst errors
- Are used in applications like:
  - QR codes
  - CDs and DVDs
  - Satellite communications
  - Digital television
  - Deep space communications

### Key Concepts

1. **Symbols**: The basic units of data (in this demo, bytes)
2. **Parity Bytes**: Extra bytes added to the message for error correction
3. **Error Correction Capacity**: 
   - Can correct up to t errors where t = (n-k)/2
   - n = total codeword length
   - k = message length
4. **Erasures**: Known error locations (can correct twice as many erasures as errors)

## Requirements

- Python 3.x
- reedsolo package (`pip install reedsolo`)

## Usage

Run the demo script:
```bash
python reed-solomon.py
```

### Interactive Features

The demo script provides an interactive experience where you can:

1. **Enter Your Message**
   - Type any message you want to encode
   - Default message provided if none entered

2. **Set Parity Bytes**
   - Choose the number of parity bytes (must be even)
   - More parity bytes = more error correction capability
   - Default: 8 parity bytes (can correct up to 4 errors)

3. **Simulate Errors**
   - Choose how many random errors to introduce
   - Errors are randomly placed in the codeword
   - Maximum errors = parity_bytes/2

4. **Simulate Erasures**
   - Choose how many erasures to simulate
   - Erasures are known error locations
   - Can correct up to parity_bytes erasures

### Output Format

The script provides detailed output in the following sections:

1. **Original Message**
   - Shows the input message
   - Displays message length and hex representation

2. **Encoding Parameters**
   - Shows number of parity bytes
   - Displays maximum correctable errors

3. **Encoded Message**
   - Shows total codeword length
   - Displays data and parity bytes in hex

4. **Error Simulation**
   - Shows corrupted positions
   - Displays corrupted codeword

5. **Error Correction**
   - Shows number of errors corrected
   - Displays error positions
   - Shows recovered message

6. **Erasure Simulation**
   - Shows erasure positions
   - Displays corrupted codeword

7. **Erasure Correction**
   - Shows number of errors corrected
   - Displays error positions
   - Shows recovered message

## Example

```
============================================================
                REED-SOLOMON ERROR CORRECTION DEMO
============================================================

Enter your message [This is a test of the reed-solomon code]: Hello World!
Enter number of parity bytes (must be even) [8]: 8

----------------------------------------
Original Message
----------------------------------------
Message: Hello World!
Length: 12 bytes
Hex: 48656c6c6f20576f726c6421

----------------------------------------
Encoding Parameters
----------------------------------------
Number of parity bytes (nsym): 8
Maximum correctable errors: 4

[... more output ...]
```

## Technical Details

The implementation uses the `reedsolo` Python package which provides:
- Reed-Solomon encoding and decoding
- Error correction
- Erasure correction
- Support for various field sizes

## References

- [Reed-Solomon Error Correction](https://en.wikipedia.org/wiki/Reed%E2%80%93Solomon_error_correction)
- [reedsolo Python Package](https://github.com/tomerfiliba/reedsolomon)
- [Practical Reed-Solomon for Programmers](https://berthub.eu/articles/posts/reed-solomon-for-programmers/)

## License

This project is open source and available under the MIT License. 