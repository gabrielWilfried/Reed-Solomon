"""
reed_solomon_demo.py

Demonstration of Reed–Solomon encoding and decoding in Python,
showing both error correction (unknown error locations) and
erasure correction (known error locations).

Based on Bert Hubert's "Practical Reed–Solomon for Programmers".
"""

import sys
import random
from reedsolo import RSCodec, ReedSolomonError

def hexify(b: bytes) -> str:
    """Return a hex string, grouping two hex digits per byte."""
    return b.hex()

def print_section(title: str, width: int = 60):
    """Print a formatted section header."""
    print("\n" + "=" * width)
    print(f"{title:^{width}}")
    print("=" * width)

def print_subsection(title: str):
    """Print a formatted subsection header."""
    print(f"\n{'-' * 40}")
    print(f"{title}")
    print(f"{'-' * 40}")

def get_user_input(prompt: str, default: str = None) -> str:
    """Get user input with a default value."""
    if default:
        user_input = input(f"{prompt} [{default}]: ").strip()
        return user_input if user_input else default
    return input(f"{prompt}: ").strip()

def demo_simple_message():
    print_section("REED-SOLOMON ERROR CORRECTION DEMO")
    
    # 1) Get user input for message
    default_msg = "This is a test of the reed-solomon code"
    msg = get_user_input("Enter your message", default_msg).encode()
    
    # 2) Get user input for number of parity bytes
    default_nsym = 8
    while True:
        try:
            nsym = int(get_user_input("Enter number of parity bytes (must be even)", str(default_nsym)))
            if nsym % 2 != 0:
                print("Error: Number of parity bytes must be even")
                continue
            break
        except ValueError:
            print("Error: Please enter a valid number")
    
    rsc = RSCodec(nsym)
    print_subsection("Original Message")
    print(f"Message: {msg.decode()}")
    print(f"Length: {len(msg)} bytes")
    print(f"Hex: {hexify(msg)}")
    
    print_subsection("Encoding Parameters")
    print(f"Number of parity bytes (nsym): {nsym}")
    print(f"Maximum correctable errors: {nsym//2}")

    # 3) Encode the message
    codeword = rsc.encode(msg)
    data, parity = codeword[:-nsym], codeword[-nsym:]
    print_subsection("Encoded Message")
    print(f"Total codeword length: {len(codeword)} bytes")
    print(f"Data bytes ({len(data)}): {hexify(data)}")
    print(f"Parity bytes ({len(parity)}): {hexify(parity)}")

    # 4) Simulate errors
    max_errors = nsym // 2
    while True:
        try:
            num_errors = int(get_user_input(f"Enter number of errors to simulate (1-{max_errors})", str(max_errors//2)))
            if num_errors < 1 or num_errors > max_errors:
                print(f"Error: Number of errors must be between 1 and {max_errors}")
                continue
            break
        except ValueError:
            print("Error: Please enter a valid number")

    # Generate random error positions
    error_positions = sorted(random.sample(range(len(codeword)), num_errors))
    corrupted = bytearray(codeword)
    for pos in error_positions:
        corrupted[pos] ^= 0xFF  # flip all bits at these positions
    
    print_subsection("Error Simulation")
    print(f"Corrupted positions: {error_positions}")
    print(f"Corrupted codeword: {hexify(bytes(corrupted))}")

    # 5) Decode with error correction
    print_subsection("Error Correction")
    try:
        decoded_msg, num_errors, err_pos = rsc.decode(bytes(corrupted))
        print("✓ Decoding successful!")
        print(f"Number of errors corrected: {num_errors}")
        print(f"Error positions: {err_pos}")
        print(f"Recovered message: {decoded_msg.decode()}")
        print(f"Recovered hex: {hexify(decoded_msg)}")
    except ReedSolomonError as e:
        print("✗ Decoding failed!")
        print(f"Error: {e}")

    # 6) Simulate erasures
    while True:
        try:
            num_erasures = int(get_user_input(f"Enter number of erasures to simulate (1-{nsym})", str(nsym//2)))
            if num_erasures < 1 or num_erasures > nsym:
                print(f"Error: Number of erasures must be between 1 and {nsym}")
                continue
            break
        except ValueError:
            print("Error: Please enter a valid number")

    # Generate random erasure positions
    erasure_positions = sorted(random.sample(range(len(codeword)), num_erasures))
    corrupted2 = bytearray(codeword)
    for pos in erasure_positions:
        corrupted2[pos] ^= 0xFF
    
    print_subsection("Erasure Simulation")
    print(f"Erasure positions: {erasure_positions}")
    print(f"Corrupted codeword: {hexify(bytes(corrupted2))}")

    # 7) Decode with erasure correction
    print_subsection("Erasure Correction")
    try:
        decoded_msg2, num_errors2, err_pos2 = rsc.decode(bytes(corrupted2), erase_pos=erasure_positions)
        print("✓ Decoding with erasures successful!")
        print(f"Number of errors corrected: {num_errors2}")
        print(f"Error positions: {err_pos2}")
        print(f"Recovered message: {decoded_msg2.decode()}")
        print(f"Recovered hex: {hexify(decoded_msg2)}")
    except ReedSolomonError as e:
        print("✗ Decoding with erasures failed!")
        print(f"Error: {e}")

if __name__ == "__main__":
    demo_simple_message()
