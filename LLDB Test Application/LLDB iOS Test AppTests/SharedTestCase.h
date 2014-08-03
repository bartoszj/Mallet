//
//  SharedTestCase.h
//  LLDB Test Application
//
//  Created by Bartosz Janda on 19.07.2014.
//  Copyright (c) 2014 Bartosz Janda. All rights reserved.
//

#import <XCTest/XCTest.h>

@interface SharedTestCase : XCTestCase

/**
 *  Do nothing. Perfect place to set breakpoint.
 */
- (void)doNothing;

/**
 *  Compare @c variable summary of type @c type with @summary.
 *
 *  @param variable Variable which summary will be compared.
 *  @param type     Type of object as string, eg. @"CGPoint *".
 *  @param summary  Summary.
 *
 *  @return Comarision result. @c @YES if everything is OK, @c @NO if @c variable summary is not equal to @c summary. @c nil if comparing function doesn't work.
 */
- (NSNumber *)compareVariable:(void *)variable ofType:(NSString *)type toSumamry:(NSString *)summary;

/**
 *  Compare @c object summary of type @c type with @summary.
 *
 *  @param object  Object which summary will be compared.
 *  @param type    Type of object as string, eg. @"NSString *".
 *  @param summary Summary.
 *
 *  @return Comarision result. @c @YES if everything is OK, @c @NO if @c object summary is not equal to @c summary. @c nil if comparing function doesn't work.
 */
- (NSNumber *)compareObject:(id)object ofType:(NSString *)type toSumamry:(NSString *)summary;

@end
