"""
reed_solomon_demo.py

Demonstration of Reed–Solomon encoding and decoding in Python,
showing both error correction (unknown error locations) and
erasure correction (known error locations).

Based on Bert Hubert's "Practical Reed–Solomon for Programmers".
"""

import sys
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

def demo_simple_message():
    # 1) Prepare a short message
    msg = b"I am a Fullstack developer at Alshadows Technology"
    print_section("REED-SOLOMON ERROR CORRECTION DEMO")
    print_subsection("Original Message")
    print(f"Message: {msg.decode()}")
    print(f"Length: {len(msg)} bytes")
    print(f"Hex: {hexify(msg)}")

    # 2) Choose number of parity bytes (nroots = 8 → can correct up to 4 unknown errors)
    nsym = 8
    rsc = RSCodec(nsym)
    print_subsection("Encoding Parameters")
    print(f"Number of parity bytes (nsym): {nsym}")
    print(f"Maximum correctable errors: {nsym//2}")

    # 3) Encode: this returns msg + parity
    codeword = rsc.encode(msg)
    data, parity = codeword[:-nsym], codeword[-nsym:]
    print_subsection("Encoded Message")
    print(f"Total codeword length: {len(codeword)} bytes")
    print(f"Data bytes ({len(data)}): {hexify(data)}")
    print(f"Parity bytes ({len(parity)}): {hexify(parity)}")

    # 4) Simulate random corruption of 4 bytes (positions unknown to decoder)
    corrupted = bytearray(codeword)
    error_positions = [10, 11, 12, 13]
    for pos in error_positions:
        corrupted[pos] ^= 0xFF  # flip all bits at these positions
    print_subsection("Error Simulation")
    print(f"Corrupted positions: {error_positions}")
    print(f"Corrupted codeword: {hexify(bytes(corrupted))}")

    # 5) Decode (error correction)
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

    # 6) Simulate heavier corruption: 8 bytes flipped, but we tell the decoder where
    corrupted2 = bytearray(codeword)
    erasure_positions = [0,1,2,3,10,11,12,13]
    for pos in erasure_positions:
        corrupted2[pos] ^= 0xFF
    print_subsection("Erasure Simulation")
    print(f"Erasure positions: {erasure_positions}")
    print(f"Corrupted codeword: {hexify(bytes(corrupted2))}")

    # 7) Decode with known erasures (up to 8 erasures can be corrected)
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
