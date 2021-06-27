// Fill out your copyright notice in the Description page of Project Settings.


#include "DBC.h"

FPStringBlock FPStringBlock::TotalBlks[TotalBlockCount];

void FPStringBlock::Reset(uint16 InBlkIdx)
{
	ensure(InBlkIdx < TotalBlockCount);
	FPStringBlock& Blk = TotalBlks[InBlkIdx];
	Blk.Size = 0;
	Blk.Data = nullptr;
}

void FPStringBlock::Bind(uint16 InBlkIdx, uint32 InSize, const TCHAR* InData)
{
	ensure(InBlkIdx < TotalBlockCount);
	FPStringBlock& Blk = TotalBlks[InBlkIdx];
	ensure(Blk.Data == nullptr);
	Blk.Data = InData;
	Blk.Size = InSize;
}

void FPStringBlock::Bind(uint16 InBlkIdx, const FStringView& InView)
{
	Bind(InBlkIdx, InView.Len(), InView.GetData());
}

const TCHAR* FPStringBlock::Get(uint16 InBlkIdx, uint32 Off)
{
	ensure(InBlkIdx < TotalBlockCount);
	FPStringBlock& Blk = TotalBlks[InBlkIdx];
	ensure(Blk.Data != nullptr);
	ensure(Off < Blk.Size);

	const TCHAR* Ret = Blk.Data + Off;
	return Ret;
}


FPString::FPString(uint16 InSize, uint32 InOff, uint16 InBlkIdx)
{
	ensure(InSize <= (1<<16) - 1); // max string size: 64KB
	ensure(InOff <= (1<<26) - 1); // total size: 64MB
	BlkIdx = static_cast<uint16>(InBlkIdx);
	Size = static_cast<uint16>(InSize);
	Off = static_cast<uint32>(InOff);
}

FPString::FPString(const FPString& InStr)
{
	BlkIdx = InStr.BlkIdx;
	Size = InStr.Size;
	Off = InStr.Off;
}

FStringView FPString::AsView() const
{
	const TCHAR* Str = FPStringBlock::Get(BlkIdx, Off);
	return FStringView(Str, Size);
}

const TCHAR* FPString::operator*() const
{
	return FPStringBlock::Get(BlkIdx, Off);
}

size_t FPString::GetSize() const
{
	return Size;
}

FPStringBuilder::FPStringBuilder(uint32 InBlkIdx)
{
	BlkIdx = InBlkIdx;
}

void FPStringBuilder::Reserve(uint32 InCapacity)
{
	TotalStr.Reserve(InCapacity);
}

FPString FPStringBuilder::Add(uint32 InSize, const TCHAR* InStr)
{
	size_t NewOff = TotalStr.Len();
	TotalStr.AppendChars(InStr, InSize + 1); // with null character
	return FPString(InSize, NewOff, BlkIdx);
}

FPString FPStringBuilder::Add(const FStringView& InStr)
{
	return Add(InStr.Len(), InStr.GetData());
}

FString& FPStringBuilder::GetTotalString()
{
	return TotalStr;
}

uint32 FPStringBuilder::GetBlockIndex() const
{
	return BlkIdx;
}
