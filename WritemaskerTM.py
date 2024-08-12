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

write_protected_bits_MSI = (
    "0000f104",  # 1
    "03000000",  # 2
    "00000000",  # 3
    "00000000",  # 4
    "00000000",  # 5
    "00000000",  # 6
    "00000000",  # 7
    "ffff0000",  # 8
)

write_protected_bits_MSIX = (
    "000000c0",  # 1
    "00000000",  # 2
    "00000000",  # 3
)

write_protected_bits_VSC = (
    "000000ff",  # 1
    "ffffffff",  # 2
    "00000000",  # 3
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

fixed_mask_section = {
    0x10: write_protected_bits_PCIE,
    0x01: write_protected_bits_PM,
    0x05: write_protected_bits_MSI,
    0x11: write_protected_bits_MSIX,
    0x09: write_protected_bits_VSC,
    0x0A: write_protected_bits_VSEC,
    0x0D: write_protected_bits_AER,
    0x03: write_protected_bits_DSN,
    0x0C: write_protected_bits_LTR,
    0x07: write_protected_bits_L1PM,
    0x0B: write_protected_bits_PTM,
}


def parse_pci_config_space(file_path):
    config_space_map = {}
    extended_config_space_map = {}
    index = 0
    with open(file_path, 'r') as file:
        for line in file:
            dwords = re.findall(r'[0-9a-fA-F]{8}', line.strip())
            for dword in dwords:
                if dword and index < 1024:
                    config_space_map[index] = int(dword, 16)
                    extended_config_space_map[index] = int(dword, 16)
                    index += 1
    return config_space_map, extended_config_space_map

def find_standard_capabilities(config_space_map):
    standard_capabilities = {}

    capability_start = get_capability_start_offset(config_space_map)
    current_capability_offset = capability_start

    while current_capability_offset != 0:
        capability_dword = config_space_map[current_capability_offset // 4]
        capability_id = (capability_dword >> 24) & 0xFF
        next_capability_offset = (capability_dword >> 16) & 0xFF

        standard_capabilities[capability_id] = current_capability_offset
        current_capability_offset = next_capability_offset

    return standard_capabilities

def find_extended_capabilities(extended_config_space_map):
    extended_capabilities = {}

    extended_capability_start = get_extended_capability_start_offset(extended_config_space_map)
    current_extended_capability_offset = extended_capability_start

    while current_extended_capability_offset != 0:
        extended_capability_dword = extended_config_space_map[current_extended_capability_offset // 4]
        extended_capability_id = (extended_capability_dword >> 8) & 0xFF and (extended_capability_dword >> 3) & 0xF
        extended_capability_id = extended_capability_id << 8 | extended_capability_id << 3
        next_extended_capability_offset = (extended_capability_dword >> 16) & 0xFF
        extended_capabilities[extended_capability_id] = current_extended_capability_offset
        current_extended_capability_offset = next_extended_capability_offset

    return extended_capabilities

def get_capability_start_offset(config_space_map):
    return config_space_map[0x34 // 4] >> 24

def get_extended_capability_start_offset(extended_config_space_map):
    return extended_config_space_map[0x100 // 4] >> 24

def initialize_writemask(config_space_map):
    return ['ffffffff' for _ in config_space_map]

def apply_writemask_update(writemask, update_values, start_index):
    end_index = min(start_index + len(update_values), len(writemask))
    writemask[start_index:end_index] = update_values[:end_index - start_index]
    return writemask

def main(file_in, file_out):
    config_space, extended_config_space = parse_pci_config_space(file_in)
    standard_capabilities = find_standard_capabilities(config_space)
    extended_capabilities = find_extended_capabilities(extended_config_space)
    writemask = initialize_writemask(config_space)
    writemask = apply_writemask_update(writemask, fixed_mask_section, 0)

    for capability_id, capability_offset in standard_capabilities.items():
        writemask_section = write_protection_masks.get(capability_id)
        capability_start_index = capability_offset // 4
        extended_capability_offset = extended_capabilities.get(capability_id)
        extended_capability_start_index = extended_capability_offset // 4 if extended_capability_offset else None
        if extended_capability_start_index is not None:
            writemask = apply_writemask_update(writemask, writemask_section, extended_capability_start_index)
        writemask = apply_writemask_update(writemask, writemask_section, capability_start_index)

    with open(file_out, 'w') as f:
        for i in range(0, len(writemask), 4):
            f.write(','.join(writemask[i:i + 4]) + ',\n')

    logging_enabled = True
    if logging_enabled:
        print(writemask)
        for index, dword in config_space.items():
            offset = hex(index * 4)
            print(f"Index: {index} DWord: {dword}   (offset: {offset} dword {hex(dword)})")
        for capability_id, capability_offset in standard_capabilities.items():
            print(f"Cap ID: {hex(capability_id)} offset: {hex(capability_offset)}")

if __name__ == "__main__":
    main('pcileech_cfgspace.coe', 'pcileech_wrmask.coe')
