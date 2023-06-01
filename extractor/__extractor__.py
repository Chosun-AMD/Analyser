from .__tokenizer__ import __tokenizer__
from .__preprocessor__ import __preprocessor__

import subprocess
import pefile
from capstone import *
import hashlib

class ASCIIExtractor(__tokenizer__):
    """
    Extracts the ASCII strings from the PE32 file.
    """

    def __init__(self) -> None:
        super().__init__(128)

    def parse(self):
        return subprocess.check_output(['strings', self.file]).decode().splitlines()

class UTF16LEExtractor(__tokenizer__):
    """
    Extracts the UTF16LE strings from the PE32 file.
    """

    def __init__(self) -> None:
        super().__init__(128)

    def parse(self):
        return subprocess.check_output(['strings', '-e', 'l', self.file]).decode().splitlines()

class OpcodeExtractor(__tokenizer__):
    """
    Extracts opcodes from the file.
    """

    def __init__(self) -> None:
        super().__init__(0)

    def parse(self):
        file = pefile.PE(self.file)
        opcodes = []

        entry_point = file.OPTIONAL_HEADER.AddressOfEntryPoint
        base_of_code = file.OPTIONAL_HEADER.BaseOfCode
        code_section = file.sections[0].get_data()
        md = Cs(CS_ARCH_X86, CS_MODE_32 if file.FILE_HEADER.Machine == pefile.MACHINE_TYPE['IMAGE_FILE_MACHINE_I386'] else CS_MODE_64)

        for i in md.disasm(code_section, entry_point):
            opcodes.append(i.mnemonic)

        return opcodes

class PEHeaderExtractor(__preprocessor__):
    """
    Extracts the PE header from the file.
    """

    def __init__(self) -> None:
        super().__init__(4096)

    def extract(self):
        file = pefile.PE(self.file)
        return file.header

class RichHeaderExtractor(__preprocessor__):
    def __init__(self) -> None:
        super().__init__(512)

    def extract(self):
        file = pefile.PE(self.file)

        if not hasattr(file, 'RICH_HEADER') or not file.RICH_HEADER:
            return b'\x00'

        return file.RICH_HEADER.raw_data