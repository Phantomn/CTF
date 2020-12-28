typedef struct _COMPRESSION_TRANSFORM_HEADER // All fields controllable
{
    ULONG ProtocolId;
    ULONG OriginalCompressedSegmentSize;
    USHORT CompressionAlgorithm;
    USHORT Flags;
    ULONG Offset;
} COMPRESSION_TRANSFORM_HEADER, *PCOMPRESSION_TRANSFORM_HEADER;
 
typedef struct _ALLOCATION_HEADER
{
    // ...
    PVOID UserBuffer;
    // ...
} ALLOCATION_HEADER, *PALLOCATION_HEADER;
 
NTSTATUS SmbCompressionDecompress(
    USHORT CompressionAlgorithm,
    PUCHAR UncompressedBuffer,
    ULONG  UncompressedBufferSize,
    PUCHAR CompressedBuffer,
    ULONG  CompressedBufferSize,
    PULONG FinalCompressedSize);

PALLOCATION_HEADER SrvNetAllocateBuffer(SIZE_T AllocSize, PALLOCATION_HEADER SourceBuffer)
{
    // ...
 
    if (SrvDisableNetBufferLookAsideList || AllocSize > 0x100100) {
        if (AllocSize > 0x1000100) {
            return NULL;
        }
        Result = SrvNetAllocateBufferFromPool(AllocSize, AllocSize);
    } else {
        int LookasideListIndex = 0;
        if (AllocSize > 0x1100) {
            LookasideListIndex = /* some calculation based on AllocSize */;
        }

        // LookasideListIndex's like...
        // [0x1100, 0x2100, 0x4100, 0x8100, ..., 0x100100]
        SOME_STRUCT list = SrvNetBufferLookasides[LookasideListIndex];
        Result = /* fetch result from list */;
    }
 
    // Initialize some Result fields...
 
    return Result;
}

NTSTATUS Srv2DecompressData(PCOMPRESSION_TRANSFORM_HEADER Header, SIZE_T TotalSize)
{
    // 1. Allocate buffer.
    // __int64 __fastcall SrvNetAllocateBuffer(unsigned __int64 size, __int64 buffer)
    PALLOCATION_HEADER Alloc = SrvNetAllocateBuffer(
        (ULONG)(Header->OriginalCompressedSegmentSize + Header->Offset),
        NULL);
    If (!Alloc) {
        return STATUS_INSUFFICIENT_RESOURCES;
    }

    /* At this time, the memory alignment looks like:

       +---------------------------------------+
       | ...                                   |
    +-->---------------------------------------+ <-----+
    |  | UserBuffer                            |       |
    |  |                                       |       | Amount of bytes as
    |  |                                       |       | requested by the caller.
    |  |                                       |       |
    |  +---------------------------------------+ <-----+
    |  | padding for 8-byte alignment          |
    |  +---------------------------------------+
    |  | ALLOCATION_HEADER {                   |
    |  | ...                                   |
    +--+ *UserBuffer (Pointer)                 |
       | ...                                   |
       | }                                     |
       +---------------------------------------+
       | ...                                   |
       +---------------------------------------+

    */
 
    ULONG FinalCompressedSize = 0;
 
    // 2. Decompress data.
    NTSTATUS Status = SmbCompressionDecompress(
        Header->CompressionAlgorithm, // Compression Algorithm
        (PUCHAR)Header + sizeof(COMPRESSION_TRANSFORM_HEADER) + Header->Offset, // UncompressedBuffer
        (ULONG)(TotalSize - sizeof(COMPRESSION_TRANSFORM_HEADER) - Header->Offset), // UncompressedBufferSize
        (PUCHAR)Alloc->UserBuffer + Header->Offset, // CompressedBuffer: Output buffer
        Header->OriginalCompressedSegmentSize, // CompressedBufferSize
        &FinalCompressedSize); // FinalCompressedSize
    if (Status < 0 || FinalCompressedSize != Header->OriginalCompressedSegmentSize) {
        SrvNetFreeBuffer(Alloc);
        return STATUS_BAD_DATA;
    }
 
    // 3. Copy user buffer.
    if (Header->Offset > 0) {
        memcpy(
            Alloc->UserBuffer,
            (PUCHAR)Header + sizeof(COMPRESSION_TRANSFORM_HEADER),
            Header->Offset);
    }
 
    Srv2ReplaceReceiveBuffer(some_session_handle, Alloc);
    return STATUS_SUCCESS;
}