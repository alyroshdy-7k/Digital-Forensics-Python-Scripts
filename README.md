This script reads the MBR of my disk image and helps me understand how the partitions are laid out.

What it basically does:

Opens my .dd disk image.
Reads the first 512 bytes (which is the MBR).
Goes through the four possible partition entries stored inside the MBR.
Uses Python’s struct library to actually decode the raw bytes and convert them into readable values like the start sector and the number of sectors.
(I’m not manually calculating it, the library handles that part)
For each real partition, it shows:

If it's bootable or not

Its partition type (like NTFS)

Where it starts (sector number)

Rough size in GB

