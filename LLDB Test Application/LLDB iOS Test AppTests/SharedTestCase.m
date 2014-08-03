//
//  SharedTestCase.m
//  LLDB Test Application
//
//  Created by Bartosz Janda on 19.07.2014.
//  Copyright (c) 2014 Bartosz Janda. All rights reserved.
//

#import "SharedTestCase.h"

@implementation SharedTestCase

- (void)doNothing
{
    
}

- (NSNumber *)compareVariable:(void *)variable ofType:(NSString *)type toSumamry:(NSString *)summary
{
    NSNumber *equal;
    // Set breakpoint here:
    // compare_summary variable type summary equal
    
    [self doNothing];
    
    XCTAssertNotNil(equal, @"Python script doesn't work.");
    XCTAssertTrue(equal.boolValue, @"Wrong summary.");
    
    return equal;
}

- (NSNumber *)compareObject:(id)object ofType:(NSString *)type toSumamry:(NSString *)summary
{
    NSNumber *equal;
    // Set breakpoint here:
    // compare_summary object type summary equal
    
    [self doNothing];
    
    XCTAssertNotNil(equal, @"Python script doesn't work.");
    XCTAssertTrue(equal.boolValue, @"Wrong summary.");
    
    return equal;
}

@end
