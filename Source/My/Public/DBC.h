// 2021 myevan

#pragma once

#include "CoreMinimal.h"

class MY_API FPStringBlock
{
public:
	static const uint32 TotalBlockCount = 1024;

public:
	static void Reset(uint16 InBlkIdx);
	static void Bind(uint16 InBlkIdx, uint32 InSize, const TCHAR* InData);
	static void Bind(uint16 InBlkIdx, const FStringView& InView);

	static const TCHAR* Get(uint16 InBlkIdx, uint32 Off);

private:
	uint32 Size = 0;
	const TCHAR* Data = nullptr;

private:
	static FPStringBlock TotalBlks[TotalBlockCount];
};

#pragma pack(push, 1)

class MY_API FPString
{
public:
	FPString(uint16 InSize, uint32 InOff, uint16 InBlkIdx);
	FPString(const FPString& InStr);

	FStringView AsView() const;

	const TCHAR* operator*() const;

	size_t GetSize() const;

private:	
	uint16 Size;
	uint16 BlkIdx;
	uint32 Off;
};

#pragma pack(pop)

class MY_API FPStringBuilder
{
public:
	FPStringBuilder(uint32 InBlkIdx);

	void Reserve(uint32 InCapacity);

	FPString Add(uint32 InSize, const TCHAR* InStr);
	FPString Add(const FStringView& InData);

	FString& GetTotalString();

	uint32 GetBlockIndex() const;
	
private:
	size_t BlkIdx;

private:
	FString TotalStr;
};