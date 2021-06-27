// Fill out your copyright notice in the Description page of Project Settings.


#include "ExampleBlueprintFunctionLibrary.h"
#include "DBC.h"

#pragma pack(push, 1)

struct FDBCHeader
{
	uint32 Magic;
	uint32 RecCnt;
	uint16 RecLen;
	uint16 BlkIdx;
};

struct FPCharacter
{
	uint32 PChId;
	FPString Name;
};

#pragma pack(pop)

void UExampleBlueprintFunctionLibrary::TestDBC()
{
	FPStringBuilder SB(0);
	TArray<FPCharacter> Chars1;
	Chars1.Add(FPCharacter { 101, SB.Add(TEXT("Warrior")) });
	Chars1.Add(FPCharacter { 102, SB.Add(TEXT("Archer")) });

	FPStringBlock::Bind(0, SB.GetTotalString());

	TArray<uint8> TempData;
	FMemoryWriter Writer(TempData, true);
	Writer.Serialize(Chars1.GetData(), sizeof(FPCharacter) * Chars1.Num());
	Writer << SB.GetTotalString();

	FString StrBuf;
	TArray<FPCharacter> Chars2;
	FMemoryReader Reader(TempData, true);
	Chars2.AddUninitialized(2);
	Reader.Serialize(Chars2.GetData(), sizeof(FPCharacter) * Chars2.Num());
	Reader << StrBuf;

	FPStringBlock::Reset(0);
	FPStringBlock::Bind(0, StrBuf);

	UE_LOG(LogTemp, Log, TEXT("Hello, %s!"), *Chars2[1].Name);
}
void UExampleBlueprintFunctionLibrary::LoadDBC()
{
	FString DBCFilePath = FPaths::ProjectContentDir() / TEXT("DBCs") / TEXT("PCharacter.dbc");
	TArray<uint8> DBCBytes;
	if (!FFileHelper::LoadFileToArray(DBCBytes, *DBCFilePath))
	{
		UE_LOG(LogTemp, Error, TEXT("NOT_LOADED_FILE: %s"), *DBCFilePath);
		return;
	}	

	uint32 HeaderLen = sizeof(FDBCHeader);
	uint32 RecordLen = sizeof(FPCharacter);
	UE_LOG(LogTemp, Log, TEXT("dbc_loaded: %s header:%d record:%d"), *DBCFilePath, HeaderLen, RecordLen);

	FDBCHeader* Header = reinterpret_cast<FDBCHeader*>(&DBCBytes[0]);	
	FPCharacter* Records = reinterpret_cast<FPCharacter*>(&DBCBytes[HeaderLen]);
	ensure(Header->RecLen == RecordLen);
	
	FString StrBuf;	
	int32 UTF8Off = HeaderLen + Header->RecLen * Header->RecCnt;
	int32 StrCap = DBCBytes.Num() - UTF8Off;
	StrBuf.Reserve(StrCap);

	const ANSICHAR* UTF8Base = (const ANSICHAR*)(DBCBytes.GetData());	
	while (UTF8Off < DBCBytes.Num())
	{		
		const ANSICHAR* UTF8Str = UTF8Base + UTF8Off;
		int32 UTF8Len = TCString<ANSICHAR>::Strlen(UTF8Str);
		FString NewStr = FUTF8ToTCHAR(UTF8Str).Get();
		StrBuf.AppendChars(*NewStr, NewStr.Len() + 1);
		UTF8Off += UTF8Len + 1;
	}	
	FPStringBlock::Bind(Header->BlkIdx, StrBuf);

	UE_LOG(LogTemp, Log, TEXT("Hello, %d: %s"), Records[1].PChId, *Records[1].Name);
}
