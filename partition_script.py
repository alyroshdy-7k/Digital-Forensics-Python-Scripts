import struct
import os

#Path to your disk image
IMAGE_PATH = r"C:\Users\Aly\Desktop\CW Disk Image\CW Image.dd"
SECTOR_SIZE = 512  # size of one sector in bytes

def read_mbr(image_path):
    #Open the disk image and read the first 512 bytes (MBR)
    with open(image_path, "rb") as f:
        mbr = f.read(SECTOR_SIZE)
    return mbr

def find_partitions(mbr_data):
    #Go through the 4 possible partition entries in the MBR
    for i in range(4):
        offset = 446 + i * 16      # ach entry is 16 bytes
        entry = mbr_data[offset:offset + 16]

        status = entry[0]          #boot flag: 0x80 = bootable, 0x00 = not
        part_type = entry[4]       #partition type (e.g. 0x07 = NTFS)
        start_sector = struct.unpack("<I", entry[8:12])[0]
        total_sectors = struct.unpack("<I", entry[12:16])[0]

        #Skipping empty / unused entries
        if part_type == 0x00 or total_sectors == 0:
            continue

        #Work out size roughly in GB
        size_bytes = total_sectors * SECTOR_SIZE
        size_gb = size_bytes / (1024 ** 3)

        #Print info for this partition
        print(f"Partition {i + 1}:")
        print(f"  Bootable:   {status == 0x80}")
        print(f"  Type:       0x{part_type:02X}")
        print(f"  Start Sector:  {start_sector}")
        print(f"  Size:       {size_gb:.2f} GB\n")

def main():
    if not os.path.exists(IMAGE_PATH):
        print(f"Image not found: {IMAGE_PATH}")
        return

    print(f"Analyzing partition table for: {IMAGE_PATH}\n")

    mbr = read_mbr(IMAGE_PATH)
    find_partitions(mbr)

if __name__ == "__main__":
    main()
