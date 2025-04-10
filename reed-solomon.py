
"""
reed_solomon_demo.py

Demonstration of Reed–Solomon encoding and decoding in Python,
showing both error correction (unknown error locations) and
erasure correction (known error locations).

Based on Bert Hubert’s “Practical Reed–Solomon for Programmers” :contentReference[oaicite:0]{index=0}.
"""

import sys
from reedsolo import RSCodec, ReedSolomonError

def hexify(b: bytes) -> str:
    """Return a hex string, grouping two hex digits per byte."""
    return b.hex()

def demo_simple_message():
    # 1) Prepare a short message
    msg = b"I am a Fullstack developer at Alshadows Technology"
    print(f"Original message: {msg!r}")

    # 2) Choose number of parity bytes (nroots = 8 → can correct up to 4 unknown errors)
    nsym = 8
    rsc = RSCodec(nsym)

    # 3) Encode: this returns msg + parity
    codeword = rsc.encode(msg)
    data, parity = codeword[:-nsym], codeword[-nsym:]
    print(f"Encoded codeword (len={len(codeword)}):")
    print(f"  Data  bytes: {hexify(data)}")
    print(f"  Parity bytes: {hexify(parity)}\n")

    # 4) Simulate random corruption of 4 bytes (positions unknown to decoder)
    corrupted = bytearray(codeword)
    error_positions = [10, 11, 12, 13]
    for pos in error_positions:
        corrupted[pos] ^= 0xFF  # flip all bits at these positions
    print(f"Corrupted   bytes at positions {error_positions}: {hexify(bytes(corrupted))}")

    # 5) Decode (error correction)
    try:
        recovered = rsc.decode(bytes(corrupted))
        print(f"Recovered message (errors corrected): {recovered!r}\n")
    except ReedSolomonError as e:
        print(f"Decoding failed (too many errors?): {e}\n")

    # 6) Simulate heavier corruption: 8 bytes flipped, but we tell the decoder where
    corrupted2 = bytearray(codeword)
    erasure_positions = [0,1,2,3,10,11,12,13]
    for pos in erasure_positions:
        corrupted2[pos] ^= 0xFF
    print(f"Corrupted   bytes at positions {erasure_positions}: {hexify(bytes(corrupted2))}")

    # 7) Decode with known erasures (up to 8 erasures can be corrected)
    try:
        recovered2 = rsc.decode(bytes(corrupted2), erase_pos=erasure_positions)
        print(f"Recovered message (erasures corrected): {recovered2!r}")
    except ReedSolomonError as e:
        print(f"Decoding with erasures failed: {e}")

if __name__ == "__main__":
    demo_simple_message()
