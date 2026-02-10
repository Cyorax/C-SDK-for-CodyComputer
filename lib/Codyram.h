// Writes a 16-bit value to the specified address
void poke(int* address, int value);

// Writes an 8-bit value to the specified address
void poke1byte(short* address, short value);

// Returns the 16-bit value stored at the specified address
int peek(int* address);

// Returns the 8-bit value stored at the specified address as a 16-bit int
int peek1byte(short* address);

/*
    With this function it is possible to access the bytes specified
    in the data.lib file.

    startAddressRam:
        Specifies the starting address in RAM where the bytes
        will be copied to.

    startAddressData:
        Specifies the byte index in the data.lib file
        from which copying starts.

    amount:
        Specifies the number of bytes to be copied.

    Example:

        copy_from_data(3, 1, 2);

        This would copy the bytes EF and 10 to RAM starting at address 3.

    data.lib:
        00 EF 10 20 30
*/
void copy_from_data(int startAddressRam, int startAddressData, int amount);

