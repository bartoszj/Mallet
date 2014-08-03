//
//  Compare.m
//  LLDB Test Application
//
//  Created by Bartosz Janda on 13.07.2014.
//  Copyright (c) 2014 Bartosz Janda. All rights reserved.
//

#import "Compare.h"

void DoNothing()
{
    
}

NSNumber* CompareVariableWithSummary(void *variable, NSString *type, NSString *summary)
{
    NSNumber *equal;
    // Set breakpoint here:
    // compare_summary variable type summary equal
    
    DoNothing();
    
    NSCAssert(equal, @"Python script doesn't work.");
    NSCAssert(equal.boolValue, @"Wrong summary.");
    
    return equal;
}

NSNumber* CompareObjectWithSummary(id object, NSString *type, NSString *summary)
{
    NSNumber *equal;
    // Set breakpoint here:
    // compare_summary object type summary equal
    
    DoNothing();
    
    NSCAssert(equal, @"Python script doesn't work.");
    NSCAssert(equal.boolValue, @"Wrong summary.");

    return equal;
}
