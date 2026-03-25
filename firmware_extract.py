#!/usr/bin/env python3
import sys, os

class FirmwarePart:
    def __init__(self, name, offset, size):
        self.name = name
        self.offset = offset
        self.size = size

firmware_parts = [
    FirmwarePart("XXXX", 0x000000, 0x040000),
    FirmwarePart("XXXX", 0x038000, 0x008000),
    FirmwarePart("XXXX", 0x040000, 0x008000),
    FirmwarePart("XXXX", 0x040000, 0x008000), # modify here the offsets and the names of the partitions according to the data found in boot logs for mtdparts
    FirmwarePart("XXXX",   0x048000, 0x1A0000),
    FirmwarePart("XXXX",  0x1E8000, 0x100000),
    FirmwarePart("XXXX", 0x2E8000, 0x040000),
    FirmwarePart("XXXX", 0x328000, 0x4D8000),
]

if len(sys.argv) < 3:
    print("Usage:\n  unpack: python3 fw_tool.py unpack firmware.bin\n  pack: python3 fw_tool.py pack output.bin")
    sys.exit(1)

mode = sys.argv[1]
filename = sys.argv[2]

if mode == "unpack":
    with open(filename, "rb") as f:
        for part in firmware_parts:
            f.seek(part.offset)
            data = f.read(part.size)
            with open(part.name + ".bin", "wb") as out:
                out.write(data)
            print(f"[+] Wrote {part.name}.bin ({len(data):#x} bytes)")
elif mode == "pack":
    with open(filename, "wb") as out:
        for part in firmware_parts:
            name = part.name + ".bin"
            if not os.path.exists(name):
                print(f"[-] Missing {name}, skipping")
                out.write(b"\xff" * part.size)
                continue
            with open(name, "rb") as f:
                data = f.read()
            out.write(data)
            if len(data) < part.size:
                out.write(b"\xff" * (part.size - len(data)))
            print(f"[+] Added {name} ({len(data):#x} bytes)")
    print("[+] Repacked image complete")

