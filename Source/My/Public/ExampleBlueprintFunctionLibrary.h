// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "ExampleBlueprintFunctionLibrary.generated.h"

/**
 * 
 */
UCLASS()
class MY_API UExampleBlueprintFunctionLibrary : public UBlueprintFunctionLibrary
{
	GENERATED_BODY()

	UFUNCTION(BlueprintCallable, Category="Example")
	static void TestDBC();

	UFUNCTION(BlueprintCallable, Category = "Example")
	static void LoadDBC();
};
