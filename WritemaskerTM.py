import re


write_protected_bits_PCIE = (
    "00000f00",  # 1
    "00000010",  # 2
    "ff7f0f00",  # 3
    "00000000",  # 4
    "cb0d00c0",  # 5
    "00000000",  # 6
    "0000ffff",  # 7
    "00000000",  # 8
    "00000000",  # 9
    "00000000",  # 10
    "ff7f0000",  # 11
    "00000000",  # 12
    "bfff2000",  # 13
)

write_protected_bits_PM = (
    "00000000",  # 1
    "00000000",  # 2
)

write_protected_bits_MSI_ENABLED_0 = (
    "0000f104",  # 1
)

write_protected_bits_MSI_64_bit_1 = (
    "0000f104",  # 1
    "03000000",  # 2
    "00000000",  # 3
    "ffff0000",  # 4
)

write_protected_bits_MSI_Multiple_Message_Capable_1 = (
    "0000f104",  # 1
    "03000000",  # 2
    "00000000",  # 3
    "ffff0000",  # 4
    "00000000",  # 5
    "01000000",  # 6
)

write_protected_bits_MSIX_3 = (
    "000000c0",  # 1
    "00000000",  # 2
    "00000000",  # 3
)

write_protected_bits_MSIX_4 = (
    "000000c0",  # 1
    "00000000",  # 2
    "00000000",  # 3
    "00000000",  # 4
)

write_protected_bits_MSIX_5 = (
    "000000c0",  # 1
    "00000000",  # 2
    "00000000",  # 3
    "00000000",  # 4
    "00000000",  # 5
)

write_protected_bits_MSIX_6 = (
    "000000c0",  # 1
    "00000000",  # 2
    "00000000",  # 3
    "00000000",  # 4
    "00000000",  # 5
    "00000000",  # 6
)

write_protected_bits_MSIX_7 = (
    "000000c0",  # 1
    "00000000",  # 2
    "00000000",  # 3
    "00000000",  # 4
    "00000000",  # 5
    "00000000",  # 6
    "00000000",  # 7
)

write_protected_bits_MSIX_8 = (
    "000000c0",  # 1
    "00000000",  # 2
    "00000000",  # 3
    "00000000",  # 4
    "00000000",  # 5
    "00000000",  # 6
    "00000000",  # 7
    "00000000",  # 8
)

write_protected_bits_VPD = (
    "0000ffff",  # 1
    "ffffffff",  # 2
)

write_protected_bits_VSC = (
    "000000ff",  # 1
    "ffffffff",  # 2
)

write_protected_bits_TPH = (
    "00000000",  # 1
    "00000000",  # 2
    "070c0000",  # 3
)

write_protected_bits_VSEC = (
    "00000000",  # 1
    "00000000",  # 2
    "ffffffff",  # 3
    "ffffffff",  # 4
)

write_protected_bits_AER = (
    "00000000",  # 1
    "31f0ff07",  # 2
    "31f0ff07",  # 3
    "31f0ff07",  # 4
    "c1f10000",  # 5
    "c1f10000",  # 6
    "40050000",  # 7
    "00000000",  # 8
    "00000000",  # 9
    "00000000",  # 10
    "00000000",  # 11
)

write_protected_bits_DSN = (
    "00000000",  # 1
    "00000000",  # 2
    "00000000",  # 3
)

write_protected_bits_LTR = (
    "00000000",  # 1
    "00000000",  # 2
)

write_protected_bits_L1PM = (
    "00000000",  # 1
    "00000000",  # 2
    "3f00ffe3",  # 3
    "fb000000",  # 4
)

write_protected_bits_PTM = (
    "00000000",  # 1
    "00000000",  # 2
    "00000000",  # 3
    "03ff0000",  # 4
)

CAPABILITY_NAMES = {
    0x01: "power management",
    0x02: "AGP",
    0x03: "VPD",
    0x04: "slot identification",
    0x05: "MSI",
    0x06: "compact PCI hot swap",
    0x07: "PCI-X",
    0x08: "hyper transport",
    0x09: "vendor specific",
    0x0A: "debug port",
    0x0B: "compact PCI central resource control",
    0x0C: "PCI hot plug",
    0x0D: "PCI bridge subsystem vendor ID",
    0x0E: "AGP 8x",
    0x0F: "secure device",
    0x10: "PCI express",
    0x11: "MSI-X",
    0x12: "SATA data/index configuration",
    0x13: "advanced features",
    0x14: "enhanced allocation",
    0x15: "flattening portal bridge",
}

EXTENDED_CAPABILITY_NAMES = {
    0x0001: "advanced error reporting",
    0x0002: "virtual channel",
    0x0003: "device serial number",
    0x0004: "power budgeting",
    0x0005: "root complex link declaration",
    0x0006: "root complex internal link control",
    0x0007: "root complex event collector endpoint association",
    0x0008: "multi-function virtual channel",
    0x0009: "virtual channel",
    0x000A: "root complex register block",
    0x000B: "vendor specific",
    0x000C: "configuration access correlation",
    0x000D: "access control services",
    0x000E: "alternative routing-ID interpretation",
    0x000F: "address translation services",
    0x0010: "single root IO virtualization",
    0x0011: "multi-root IO virtualization",
    0x0012: "multicast",
    0x0013: "page request interface",
    0x0014: "AMD reserved",
    0x0015: "resizable BAR",
    0x0016: "dynamic power allocation",
    0x0017: "TPH requester",
    0x0018: "latency tolerance reporting",
    0x0019: "secondary PCI express",
    0x001A: "protocol multiplexing",
    0x001B: "process address space ID",
    0x001C: "LN requester",
    0x001D: "downstream port containment",
    0x001E: "L1 PM substates",
    0x001F: "precision time measurement",
    0x0020: "M-PCIe",
    0x0021: "FRS queueing",
    0x0022: "Readyness time reporting",
    0x0023: "designated vendor specific",
    0x0024: "VF resizable BAR",
    0x0025: "data link feature",
    0x0026: "physical layer 16.0 GT/s",
    0x0027: "receiver lane margining",
    0x0028: "hierarchy ID",
    0x0029: "native PCIe enclosure management",
    0x002A: "physical layer 32.0 GT/s",
    0x002B: "alternate protocol",
    0x002C: "system firmware intermediary",
}

fixed_section = [
    "00000000", "470500f9", "00000000", "ffff0040",
    "f0ffffff", "ffffffff", "f0ffffff", "ffffffff",
    "f0ffffff", "f0ffffff", "00000000", "00000000",
    "01f8ffff", "00000000", "00000000", "ff000000",
]

writemask_dict = {
    "0x10": write_protected_bits_PCIE,
    "0x03": write_protected_bits_VPD,
    "0x01": write_protected_bits_PM,
    "0x05": write_protected_bits_MSI_ENABLED_0,
    "0x05": write_protected_bits_MSI_64_bit_1,
    "0x05": write_protected_bits_MSI_Multiple_Message_Capable_1,
    "0x11": write_protected_bits_MSIX_3,
    "0x11": write_protected_bits_MSIX_4,
    "0x11": write_protected_bits_MSIX_5,
    "0x11": write_protected_bits_MSIX_6,
    "0x11": write_protected_bits_MSIX_7,
    "0x11": write_protected_bits_MSIX_8,
    "0x09": write_protected_bits_VSC,
    "0x000A": write_protected_bits_VSEC,
    "0x0001": write_protected_bits_AER,
    "0x0003": write_protected_bits_DSN,
    "0x0018": write_protected_bits_LTR,
    "0x001E": write_protected_bits_L1PM,
    "0x000B": write_protected_bits_PTM,
    "0x0017": write_protected_bits_TPH,
}

def get_user_choice(cap_id):
    msi_choices = {
        '1': write_protected_bits_MSI_ENABLED_0,
        '2': write_protected_bits_MSI_64_bit_1,
        '3': write_protected_bits_MSI_Multiple_Message_Capable_1
    }
    
    msix_choices = {
        '1': write_protected_bits_MSIX_3,
        '2': write_protected_bits_MSIX_4,
        '3': write_protected_bits_MSIX_5,
        '4': write_protected_bits_MSIX_6,
        '5': write_protected_bits_MSIX_7,
        '6': write_protected_bits_MSIX_8
    }
    
    if cap_id == 0x05:
        print("\nChoose MSI writemask variation:")
        print("1. MSI length: 1")
        print("2. MSI length: 4")
        print("3. MSI length: 6")
        choice = input("\nEnter choice (1/2/3): ")
        return msi_choices.get(choice)
    
    if cap_id == 0x11:
        print("\nChoose MSIX writemask variation:")
        print("1. MSIX length: 3")
        print("2. MSIX length: 4")
        print("3. MSIX length: 5")
        print("4. MSIX length: 6")
        print("5. MSIX length: 7")
        print("6. MSIX length: 8")
        choice = input("\nEnter choice (1/2/3/4/5/6): ")
        return msix_choices.get(choice)
    
    return None

def read_cfg_space(file_path):
    dword_map = {}
    index = 0
    with open(file_path, 'r') as file:
        for line in file:
            dwords = re.findall(r'[0-9a-fA-F]{8}', line.strip())
            for dword in dwords:
                if dword and index < 1024:
                    dword_map[index] = int(dword, 16)
                    index += 1
    return dword_map


def locate_caps(dword_map):
    capabilities = {}
    start = dword_map[0x34 // 4] >> 24
    cap_location = start

    while cap_location != 0:
        cap_dword = dword_map[cap_location // 4]
        cap_id = (cap_dword >> 24) & 0xFF
        next_cap = (cap_dword >> 16) & 0xFF
        cap_name = CAPABILITY_NAMES.get(cap_id, "Capability Pointer")
        if cap_location == start:
            print("Found Capabilities:")
        print(f"{hex(cap_location):<3}: {cap_name}")
        if next_cap == 0:
            print("-" * 40)
        capabilities[f"0x{cap_id:02X}"] = cap_location
        cap_location = next_cap


    ext_cap_location = 0x100
    while ext_cap_location != 0:
        ext_cap_dword = dword_map[ext_cap_location // 4]

        ext_cap_dword_le = int.from_bytes(ext_cap_dword.to_bytes(4, byteorder='big'), byteorder='little')
        ext_cap_id = ext_cap_dword_le & 0xFFFF
        next_ext_cap = (ext_cap_dword_le >> 20) & 0xFFF
        ext_cap_name = EXTENDED_CAPABILITY_NAMES.get(ext_cap_id, "Unknown")
        if ext_cap_location == 0x100:
            print(f"Found Extended Capabilities:")
        else:
            print(f"{hex(ext_cap_location):<3}: {ext_cap_name}")
        capabilities[f"0x{ext_cap_id:04X}"] = ext_cap_location
        ext_cap_location = next_ext_cap

    return capabilities


def create_wrmask(dwords):
    return ['ffffffff' for _ in dwords]


def update_writemask(wr_mask, input, start_index):
    end_index = min(start_index + len(input), len(wr_mask))
    wr_mask[start_index:end_index] = input[:end_index - start_index]
    return wr_mask


def main(file_in, file_out):
    cfg_space = read_cfg_space(file_in)
    caps = locate_caps(cfg_space)

    wr_mask = create_wrmask(cfg_space)
    wr_mask = update_writemask(wr_mask, fixed_section, 0)

    for cap_id, cap_start in caps.items():
        section = writemask_dict.get(cap_id)
        if cap_id == "0x05" or cap_id == "0x11":
            section = get_user_choice(int(cap_id, 16))
        if section is None:
            continue
        cap_start_index = cap_start // 4
        wr_mask = update_writemask(wr_mask, section, cap_start_index)

    with open(file_out, 'w') as f:
        for i in range(0, len(wr_mask), 4):
            f.write(','.join(wr_mask[i:i + 4]) + ',\n')


if __name__ == "__main__":
    main('pcileech_cfgspace.coe', 'pcileech_cfgspace_writemask.coe')
