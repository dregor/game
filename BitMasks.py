class Bits:
    FULL_BITS = 0xffff
    NOTHING_BITS = 0x0000
    GROUND_BITS = 0x0002
    BACKGROUND_OBJECT_BITS = 0x0004
    PERSONAGE_BITS = 0x0008
    PARTS_BITS = 0X0016

    FULL_MASK = 0xffff
    NOTHING_MASK = 0x0000
    GROUND_MASK = NOTHING_MASK
    BACKGROUND_OBJECT_MASK = NOTHING_MASK ^ PERSONAGE_BITS
    PERSONAGE_MASK = NOTHING_MASK ^ BACKGROUND_OBJECT_BITS
    PARTS_MASK = NOTHING_MASK ^ PARTS_BITS ^ BACKGROUND_OBJECT_BITS


