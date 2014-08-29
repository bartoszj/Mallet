//
//  UIKitTests.m
//  LLDB Test Application
//
//  Created by Bartosz Janda on 19.07.2014.
//  Copyright (c) 2014 Bartosz Janda. All rights reserved.
//

#import "SharedTestCase.h"

@interface UIKitTests : SharedTestCase

@end

@implementation UIKitTests

#pragma mark - Setup
- (void)setUp
{
    [super setUp];
    // Put setup code here. This method is called before the invocation of each test method in the class.
}

- (void)tearDown
{
    // Put teardown code here. This method is called after the invocation of each test method in the class.
    [super tearDown];
}

#pragma mark - UIEdgeInsets
- (void)testUIEdgeInsets
{
    UIEdgeInsets insets = UIEdgeInsetsMake(1, 2, 3, 4);
    [self compareVariable:&insets ofType:@"UIEdgeInsets *" toSumamry:@"(top=1, left=2, bottom=3, right=4)"];
}

#pragma mark - UIOffset
- (void)testUIOffset
{
    UIOffset offset = UIOffsetMake(1, 2);
    [self compareVariable:&offset ofType:@"UIOffset *" toSumamry:@"(horizontal=1, vertical=2)"];
}

#pragma mark - UIScreen
- (void)testUIScreen
{
    UIScreen *screen = [UIScreen mainScreen];
    [self compareObject:screen ofType:@"UIScreen *" toSumamry:@"size=(320, 568), scale=2.0, idiom=Phone"];
}

#pragma mark - UIView
//- (void)testUIView1
//{
//    CGRect frame = CGRectMake(10, 20, 300, 400);
//    UIView *view = [[UIView alloc] initWithFrame:frame];
//    [self compareObject:view ofType:@"UIView *" toSumamry:@""];
//}
//
//- (void)testUIView2
//{
//    CGRect frame = CGRectMake(10, 20, 300, 400);
//    UIView *view = [[UIView alloc] initWithFrame:frame];
//    view.alpha = 0.98;
//    [self compareObject:view ofType:@"UIView *" toSumamry:@"alpha=0.98"];
//}
//
//- (void)testUIView3
//{
//    CGRect frame = CGRectMake(10, 20, 300, 400);
//    UIView *view = [[UIView alloc] initWithFrame:frame];
//    view.hidden = YES;
//    [self compareObject:view ofType:@"UIView *" toSumamry:@"hidden=YES"];
//}
//
//- (void)testUIView4
//{
//    CGRect frame = CGRectMake(10, 20, 300, 400);
//    UIView *view = [[UIView alloc] initWithFrame:frame];
//    view.alpha = 0.56;
//    view.hidden = YES;
//    [self compareObject:view ofType:@"UIView *" toSumamry:@"alpha=0.56, hidden=YES"];
//}

#pragma mark - UILabel
- (void)testUILabel1
{
    CGRect frame = CGRectMake(10, 20, 100, 22);
    UILabel *label = [[UILabel alloc] initWithFrame:frame];
    label.text = @"asdaasd";
    [self compareObject:label ofType:@"UILabel *" toSumamry:@"text=@\"asdaasd\""];
}

- (void)testUILabel2
{
    CGRect frame = CGRectMake(10, 20, 100, 22);
    UILabel *label = [[UILabel alloc] initWithFrame:frame];
    label.attributedText = [[NSAttributedString alloc] initWithString:@"ęóąśłżźćń"];
    [self compareObject:label ofType:@"UILabel *" toSumamry:@"text=@\"ęóąśłżźćń\""];
}

#pragma mark - UIScrollView
- (void)testUIScrollView1
{
    UIScrollView *scrollView = [[UIScrollView alloc] initWithFrame:CGRectMake(0, 0, 30, 40)];
    scrollView.contentSize = CGSizeMake(33, 44);
    [self compareObject:scrollView ofType:@"UIScrollView *" toSumamry:@"contentSize=(33, 44)"];
}

- (void)testUIScrollView2
{
    UIScrollView *scrollView = [[UIScrollView alloc] initWithFrame:CGRectMake(0, 0, 30, 40)];
    scrollView.contentSize = CGSizeMake(33, 44);
    scrollView.contentInset = UIEdgeInsetsMake(1, 2, 3, 4);
    [self compareObject:scrollView ofType:@"UIScrollView *" toSumamry:@"contentSize=(33, 44), inset=(1, 2, 3, 4)"];
}

- (void)testUIScrollView3
{
    UIScrollView *scrollView = [[UIScrollView alloc] initWithFrame:CGRectMake(0, 0, 30, 40)];
    scrollView.contentSize = CGSizeMake(33, 44);
    scrollView.contentInset = UIEdgeInsetsMake(1, 2, 3, 4);
    scrollView.minimumZoomScale = 0.2;
    [self compareObject:scrollView ofType:@"UIScrollView *" toSumamry:@"contentSize=(33, 44), inset=(1, 2, 3, 4), minScale=0.20"];
}

- (void)testUIScrollView4
{
    UIScrollView *scrollView = [[UIScrollView alloc] initWithFrame:CGRectMake(0, 0, 30, 40)];
    scrollView.contentSize = CGSizeMake(33, 44);
    scrollView.contentInset = UIEdgeInsetsMake(1, 2, 3, 4);
    scrollView.minimumZoomScale = 0.2;
    scrollView.maximumZoomScale = 3.5;
    [self compareObject:scrollView ofType:@"UIScrollView *" toSumamry:@"contentSize=(33, 44), inset=(1, 2, 3, 4), minScale=0.20, maxScale=3.50"];
}

#pragma mark - UIAlertView
- (void)testUIAlertView
{
    UIAlertView *alertView = [[UIAlertView alloc] initWithTitle:@"title" message:@"message" delegate:nil cancelButtonTitle:@"cancel" otherButtonTitles:@"OK", nil];
    [self compareObject:alertView ofType:@"UIAlertView *" toSumamry:@"title=@\"title\", message=@\"message\""];
}

#pragma mark - UIProgressView
- (void)testUIProgressView
{
    UIProgressView *progresView = [[UIProgressView alloc] initWithFrame:CGRectMake(0, 0, 66, 84)];
    progresView.progress = 0.453;
    [self compareObject:progresView ofType:@"UIProgressView *" toSumamry:@"progress=0.45"];
}

#pragma mark - UIButton
- (void)testUIButton
{
    UIButton *button = [UIButton buttonWithType:UIButtonTypeCustom];
    [button setTitle:@"title" forState:UIControlStateNormal];
//    [self compareObject:button ofType:@"UIButton *" toSumamry:@"text=@\"title\""];
}

#pragma mark - UITextField
- (void)testUITextField1
{
    CGRect frame = CGRectMake(0, 0, 10, 10);
    UITextField *textField = [[UITextField alloc] initWithFrame:frame];
    textField.text = @"zzcxcx";
    [self compareObject:textField ofType:@"UITextField *" toSumamry:@"text=@\"zzcxcx\""];
}

- (void)testUITextField2
{
    CGRect frame = CGRectMake(0, 0, 10, 10);
    UITextField *textField = [[UITextField alloc] initWithFrame:frame];
    textField.attributedText = [[NSAttributedString alloc] initWithString:@"ĘÓĄŚŁŻŹĆŃ"];
    [self compareObject:textField ofType:@"UITextField *" toSumamry:@"text=@\"ĘÓĄŚŁŻŹĆŃ\""];
}

- (void)testUITextField3
{
    CGRect frame = CGRectMake(0, 0, 10, 10);
    UITextField *textField = [[UITextField alloc] initWithFrame:frame];
    textField.placeholder = @"zzcxcx";
    [self compareObject:textField ofType:@"UITextField *" toSumamry:@"placeholder=@\"zzcxcx\""];
}

- (void)testUITextField4
{
    CGRect frame = CGRectMake(0, 0, 10, 10);
    UITextField *textField = [[UITextField alloc] initWithFrame:frame];
    textField.attributedPlaceholder = [[NSAttributedString alloc] initWithString:@"ĘÓĄŚŁŻŹĆŃ"];
    [self compareObject:textField ofType:@"UITextField *" toSumamry:@"placeholder=@\"ĘÓĄŚŁŻŹĆŃ\""];
}

#pragma mark - UIDatePicker
- (void)testUIDatePicker
{
    NSDateComponents *dateComponents = [[NSDateComponents alloc] init];
    dateComponents.year = 2014;
    dateComponents.month = 4;
    dateComponents.day = 22;
    dateComponents.hour = 11;
    dateComponents.minute = 44;
    dateComponents.second = 33;
    
    UIDatePicker *datePicker = [[UIDatePicker alloc] initWithFrame:CGRectMake(20, 10, 34, 234)];
    datePicker.date = [[NSCalendar currentCalendar] dateFromComponents:dateComponents];
    [self compareObject:datePicker ofType:@"UIDatePicker *" toSumamry:@"era=1, 2014-04-22 11:44:33, leapMonth=NO"];
}

#pragma mark - UIPageControl
- (void)testUIPageControl
{
    UIPageControl *pageControl = [[UIPageControl alloc] initWithFrame:CGRectMake(0, 0, 123, 41)];
    pageControl.numberOfPages = 13;
    pageControl.currentPage = 4;
    [self compareObject:pageControl ofType:@"UIPageControl *" toSumamry:@"currentPage=4, numberOfPages=13"];
}

#pragma mark - UISegmentedControl
- (void)testUISegmentedControl
{
    UISegmentedControl *segmentedControl = [[UISegmentedControl alloc] initWithItems:@[@"a", @"b", @"c"]];
    segmentedControl.selectedSegmentIndex = 1;
    [self compareObject:segmentedControl ofType:@"UISegmentedControl *" toSumamry:@"selected=1, segments=3"];
}

#pragma mark - UISlider
- (void)testUISlider
{
    UISlider *slider = [[UISlider alloc] initWithFrame:CGRectMake(0, 0, 30, 40)];
    slider.minimumValue = 1.0;
    slider.maximumValue = 10.0;
    slider.value = 3.0;
    [self compareObject:slider ofType:@"UISlider *" toSumamry:@"value=3, min=1, max=10"];
}

#pragma mark - UIStepper
- (void)testUIStepper
{
    UIStepper *stepper = [[UIStepper alloc] initWithFrame:CGRectMake(0, 0, 32, 52)];
    stepper.minimumValue = 1.0;
    stepper.maximumValue = 56.0;
    stepper.value = 6.0;
    stepper.stepValue = 1.5;
    [self compareObject:stepper ofType:@"UIStepper *" toSumamry:@"value=6, step=1.5, min=1, max=56"];
}

#pragma mark - UISwitch
- (void)testUISwitch
{
    UISwitch *switchControl = [[UISwitch alloc] initWithFrame:CGRectMake(0, 0, 23, 523)];
    switchControl.on = YES;
    [self compareObject:switchControl ofType:@"UISwitch *" toSumamry:@"on=YES"];
}

#pragma mark - UIViewController
- (void)testUIViewController
{
    UIViewController *vc = [[UIViewController alloc] init];
    vc.title = @"ęóąśłżźćń";
    [self compareObject:vc ofType:@"UIViewController *" toSumamry:@"title=@\"ęóąśłżźćń\""];
}

@end
