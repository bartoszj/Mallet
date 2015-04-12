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
    [self compareVariable:&insets ofType:@"UIEdgeInsets *" toSummary:@"(top = 1, left = 2, bottom = 3, right = 4)"];
}

#pragma mark - UIOffset
- (void)testUIOffset
{
    UIOffset offset = UIOffsetMake(1, 2);
    [self compareVariable:&offset ofType:@"UIOffset *" toSummary:@"(horizontal = 1, vertical = 2)"];
}

#pragma mark - UIScreen
- (void)testUIScreen
{
    UIScreen *screen = [UIScreen mainScreen];
    [self compareObject:screen ofType:@"UIScreen *" toSummary:@"size=(320, 568), scale=2, idiom=Phone"];
}

#pragma mark - UIView
- (void)testUIView1
{
    CGRect frame = CGRectMake(10, 20, 300, 400);
    UIView *view = [[UIView alloc] initWithFrame:frame];
    [self compareObject:view ofType:@"UIView *" toSummary:@"frame=(10 20; 300 400)"];
}

- (void)testUIView2
{
    CGRect frame = CGRectMake(10, 20, 300, 400);
    UIView *view = [[UIView alloc] initWithFrame:frame];
    view.tag = 10;
    [self compareObject:view ofType:@"UIView *" toSummary:@"frame=(10 20; 300 400), tag=10"];
}

#pragma mark - UIImageView
- (void)testUIImageView1
{
    UIImage *image = [UIImage imageNamed:@"llvm"];
    UIImageView *view = [[UIImageView alloc] initWithImage:image];
    [self compareObject:view ofType:@"UIImageView *" toSummary:@"frame=(0 0; 128 128), image=(width=128, height=128)"];
}

- (void)testUIImageView2
{
    UIImage *image = [UIImage imageNamed:@"LLVM_scale"];
    UIImageView *view = [[UIImageView alloc] init];
    [self compareObject:view ofType:@"UIImageView *" toSummary:@"frame=(0 0; 0 0)"];
    view.image = image;
    [self compareObject:view ofType:@"UIImageView *" toSummary:@"frame=(0 0; 0 0), image=(width=75, height=83), @2x"];
}

#pragma mark - UIWindow
- (void)testUIWindow
{
    UIWindow *window = [[[UIApplication sharedApplication] delegate] window];
    [self compareObject:window ofType:@"UIWindow *" toSummary:@"frame=(0 0; 320 568)"];
}

#pragma mark - UILabel
- (void)testUILabel1
{
    CGRect frame = CGRectMake(10, 20, 100, 22);
    UILabel *label = [[UILabel alloc] initWithFrame:frame];
    label.text = @"asdaasd";
    [self compareObject:label ofType:@"UILabel *" toSummary:@"text=@\"asdaasd\""];
}

- (void)testUILabel2
{
    CGRect frame = CGRectMake(10, 20, 100, 22);
    UILabel *label = [[UILabel alloc] initWithFrame:frame];
    label.attributedText = [[NSAttributedString alloc] initWithString:@"ęóąśłżźćń"];
    [self compareObject:label ofType:@"UILabel *" toSummary:@"text=@\"ęóąśłżźćń\""];
}

- (void)testUILabel3
{
    CGRect frame = CGRectMake(10, 20, 100, 22);
    UILabel *label = [[UILabel alloc] initWithFrame:frame];
    label.attributedText = [[NSAttributedString alloc] initWithString:@"ęóąśłżźćń"];
    label.tag = 444;
    [self compareObject:label ofType:@"UILabel *" toSummary:@"text=@\"ęóąśłżźćń\", tag=444"];
}

#pragma mark - UIScrollView
- (void)testUIScrollView1
{
    UIScrollView *scrollView = [[UIScrollView alloc] initWithFrame:CGRectMake(0, 0, 30, 40)];
    scrollView.contentSize = CGSizeMake(33, 44);
    [self compareObject:scrollView ofType:@"UIScrollView *" toSummary:@"frame=(0 0; 30 40), contentOffset=(0, 0), contentSize=(33, 44)"];
}

- (void)testUIScrollView2
{
    UIScrollView *scrollView = [[UIScrollView alloc] initWithFrame:CGRectMake(0, 0, 30, 40)];
    scrollView.contentSize = CGSizeMake(33, 44);
    scrollView.contentOffset = CGPointMake(20, 21);
    [self compareObject:scrollView ofType:@"UIScrollView *" toSummary:@"frame=(0 0; 30 40), contentOffset=(20, 21), contentSize=(33, 44)"];
}

- (void)testUIScrollView3
{
    UIScrollView *scrollView = [[UIScrollView alloc] initWithFrame:CGRectMake(0, 0, 30, 40)];
    scrollView.contentSize = CGSizeMake(33, 44);
    scrollView.contentInset = UIEdgeInsetsMake(1, 2, 3, 4);
    scrollView.contentOffset = CGPointMake(20, 21);
    [self compareObject:scrollView ofType:@"UIScrollView *" toSummary:@"frame=(0 0; 30 40), contentOffset=(20, 21), contentSize=(33, 44), inset=(1, 2, 3, 4)"];
}

- (void)testUIScrollView4
{
    UIScrollView *scrollView = [[UIScrollView alloc] initWithFrame:CGRectMake(0, 0, 30, 40)];
    scrollView.contentSize = CGSizeMake(33, 44);
    scrollView.contentInset = UIEdgeInsetsMake(1, 2, 3, 4);
    scrollView.contentOffset = CGPointMake(20, 21);
    scrollView.minimumZoomScale = 0.2;
    [self compareObject:scrollView ofType:@"UIScrollView *" toSummary:@"frame=(0 0; 30 40), contentOffset=(20, 21), contentSize=(33, 44), inset=(1, 2, 3, 4), minScale=0.2"];
}

- (void)testUIScrollView5
{
    UIScrollView *scrollView = [[UIScrollView alloc] initWithFrame:CGRectMake(0, 0, 30, 40)];
    scrollView.contentSize = CGSizeMake(33, 44);
    scrollView.contentInset = UIEdgeInsetsMake(1, 2, 3, 4);
    scrollView.contentOffset = CGPointMake(20, 21);
    scrollView.minimumZoomScale = 0.2;
    scrollView.maximumZoomScale = 3.5;
    [self compareObject:scrollView ofType:@"UIScrollView *" toSummary:@"frame=(0 0; 30 40), contentOffset=(20, 21), contentSize=(33, 44), inset=(1, 2, 3, 4), minScale=0.2, maxScale=3.5"];
}

#pragma mark - UIAlertAction
- (void)testUIAlertAction01
{
    UIAlertAction *action = [UIAlertAction actionWithTitle:@"alert title" style:UIAlertActionStyleCancel handler:^(UIAlertAction *action) {
        NSLog(@"action");
    }];
    [self compareObject:action ofType:@"UIAlertAction *" toSummary:@"title=@\"alert title\", style=Cancel"];
}

- (void)testUIAlertAction02
{
    UIAlertAction *action = [UIAlertAction actionWithTitle:@"alert title" style:UIAlertActionStyleDestructive handler:^(UIAlertAction *action) {
        NSLog(@"action");
    }];
    action.enabled = NO;
    [self compareObject:action ofType:@"UIAlertAction *" toSummary:@"title=@\"alert title\", style=Destructive, disabled"];
}

#pragma mark - UIAlertController
- (void)testUIAlertController01
{
    UIAlertController *alertController = [UIAlertController alertControllerWithTitle:@"alert title" message:@"alert message" preferredStyle:UIAlertControllerStyleActionSheet];
    [self compareObject:alertController ofType:@"UIAlertController *" toSummary:@"title=@\"alert title\", message=@\"alert message\", preferredStyle=ActionSheet, actions=0"];
}

- (void)testUIAlertController02
{
    UIAlertController *alertController = [UIAlertController alertControllerWithTitle:@"alert title" message:@"alert message" preferredStyle:UIAlertControllerStyleAlert];
    
    UIAlertAction *action = [UIAlertAction actionWithTitle:@"alert title" style:UIAlertActionStyleCancel handler:^(UIAlertAction *action) {
        NSLog(@"action");
    }];
    
    [alertController addAction:action];
    
    [self compareObject:alertController ofType:@"UIAlertController *" toSummary:@"title=@\"alert title\", message=@\"alert message\", preferredStyle=Alert, actions=1"];
}

#pragma mark - UIAlertView
- (void)testUIAlertView
{
    UIAlertView *alertView = [[UIAlertView alloc] initWithTitle:@"title" message:@"message" delegate:nil cancelButtonTitle:@"cancel" otherButtonTitles:@"OK", nil];
    [self compareObject:alertView ofType:@"UIAlertView *" toSummary:@"title=@\"title\", message=@\"message\", style=Default"];
}

#pragma mark - UIProgressView
- (void)testUIProgressView
{
    UIProgressView *progresView = [[UIProgressView alloc] initWithFrame:CGRectMake(0, 0, 66, 84)];
    progresView.progress = 0.453;
    [self compareObject:progresView ofType:@"UIProgressView *" toSummary:@"progress=0.45"];
}

#pragma mark - UIBarButtonItem
- (void)testUIBarButtonItem01
{
    UIBarButtonItem *item = [[UIBarButtonItem alloc] initWithTitle:@"title" style:UIBarButtonItemStyleDone target:nil action:nil];
    [self compareObject:item ofType:@"UIBarButtonItem *" toSummary:@"title=@\"title\""];
}

- (void)testUIBarButtonItem02
{
    UIBarButtonItem *item = [[UIBarButtonItem alloc] initWithTitle:@"title" style:UIBarButtonItemStyleDone target:nil action:nil];
    item.width = 123;
    [self compareObject:item ofType:@"UIBarButtonItem *" toSummary:@"title=@\"title\", width=123"];
}

#pragma mark - UIButton
- (void)testUIButton1
{
    UIButton *button = [UIButton buttonWithType:UIButtonTypeCustom];
    [button setTitle:@"title" forState:UIControlStateNormal];
    [button layoutIfNeeded]; // Hack to force drawing.
    [self compareObject:button ofType:@"UIButton *" toSummary:@"text=@\"title\""];
}

- (void)testUIButton2
{
    UIButton *button = [UIButton buttonWithType:UIButtonTypeCustom];
    [button setTitle:@"title" forState:UIControlStateNormal];
    button.tag = 123;
    [button layoutIfNeeded]; // Hack to force drawing.
    [self compareObject:button ofType:@"UIButton *" toSummary:@"text=@\"title\", tag=123"];
}

#pragma mark - UITextField
- (void)testUITextField1
{
    CGRect frame = CGRectMake(0, 0, 10, 10);
    UITextField *textField = [[UITextField alloc] initWithFrame:frame];
    textField.text = @"zzcxcx";
    [self compareObject:textField ofType:@"UITextField *" toSummary:@"text=@\"zzcxcx\""];
}

- (void)testUITextField2
{
    CGRect frame = CGRectMake(0, 0, 10, 10);
    UITextField *textField = [[UITextField alloc] initWithFrame:frame];
    textField.attributedText = [[NSAttributedString alloc] initWithString:@"ĘÓĄŚŁŻŹĆŃ"];
    [self compareObject:textField ofType:@"UITextField *" toSummary:@"text=@\"ĘÓĄŚŁŻŹĆŃ\""];
}

- (void)testUITextField3
{
    CGRect frame = CGRectMake(0, 0, 10, 10);
    UITextField *textField = [[UITextField alloc] initWithFrame:frame];
    textField.placeholder = @"asdfghj";
    [self compareObject:textField ofType:@"UITextField *" toSummary:@"placeholder=@\"asdfghj\""];
}

- (void)testUITextField4
{
    CGRect frame = CGRectMake(0, 0, 10, 10);
    UITextField *textField = [[UITextField alloc] initWithFrame:frame];
    textField.attributedPlaceholder = [[NSAttributedString alloc] initWithString:@"ĘÓĄŚŁŻŹĆŃ2"];
    [self compareObject:textField ofType:@"UITextField *" toSummary:@"placeholder=@\"ĘÓĄŚŁŻŹĆŃ2\""];
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
    [self compareObject:datePicker ofType:@"UIDatePicker *" toSummary:@"era=1, 2014-04-22 11:44:33, leapMonth=NO"];
}

#pragma mark - UIPageControl
- (void)testUIPageControl
{
    UIPageControl *pageControl = [[UIPageControl alloc] initWithFrame:CGRectMake(0, 0, 123, 41)];
    pageControl.numberOfPages = 13;
    pageControl.currentPage = 4;
    [self compareObject:pageControl ofType:@"UIPageControl *" toSummary:@"currentPage=4, numberOfPages=13"];
}

#pragma mark - UISegmentedControl
- (void)testUISegmentedControl
{
    UISegmentedControl *segmentedControl = [[UISegmentedControl alloc] initWithItems:@[@"a", @"b", @"c"]];
    segmentedControl.selectedSegmentIndex = 1;
    [self compareObject:segmentedControl ofType:@"UISegmentedControl *" toSummary:@"selected=1, segments=3"];
}

#pragma mark - UISlider
- (void)testUISlider
{
    UISlider *slider = [[UISlider alloc] initWithFrame:CGRectMake(0, 0, 30, 40)];
    slider.minimumValue = 1.0;
    slider.maximumValue = 10.0;
    slider.value = 3.0;
    [self compareObject:slider ofType:@"UISlider *" toSummary:@"value=3, min=1, max=10"];
}

#pragma mark - UIStepper
- (void)testUIStepper
{
    UIStepper *stepper = [[UIStepper alloc] initWithFrame:CGRectMake(0, 0, 32, 52)];
    stepper.minimumValue = 1.0;
    stepper.maximumValue = 56.0;
    stepper.value = 6.0;
    stepper.stepValue = 1.5;
    [self compareObject:stepper ofType:@"UIStepper *" toSummary:@"value=6, step=1.5, min=1, max=56"];
}

#pragma mark - UISwitch
- (void)testUISwitch1
{
    UISwitch *switchControl = [[UISwitch alloc] initWithFrame:CGRectMake(0, 0, 23, 523)];
    switchControl.on = YES;
    [self compareObject:switchControl ofType:@"UISwitch *" toSummary:@"on=YES"];
}

- (void)testUISwitch2
{
    UISwitch *switchControl = [[UISwitch alloc] initWithFrame:CGRectMake(0, 0, 23, 523)];
    switchControl.on = NO;
    [self compareObject:switchControl ofType:@"UISwitch *" toSummary:@"on=NO"];
}

#pragma mark - UIViewController
- (void)testUIViewController
{
    UIViewController *vc = [[UIViewController alloc] init];
    vc.title = @"ęóąśłżźćń";
    [self compareObject:vc ofType:@"UIViewController *" toSummary:@"title=@\"ęóąśłżźćń\""];
}

#pragma mark - UINavigationController
- (void)testUINavigationController01
{
    UIViewController *vc1 = [[UIViewController alloc] init];
    vc1.title = @"vc1";
    UIViewController *vc2 = [[UIViewController alloc] init];
    vc2.title = @"vc2";
    UINavigationController *navc = [[UINavigationController alloc] initWithRootViewController:vc1];
    [self compareObject:navc ofType:@"UINavigationController *" toSummary:@"viewControllers=1"];
    [navc pushViewController:vc2 animated:NO];
    [self compareObject:navc ofType:@"UINavigationController *" toSummary:@"viewControllers=2"];
}

#pragma mark - UIStoryboard
- (void)testUIStoryboard01
{
    UIStoryboard *storyboard = [UIStoryboard storyboardWithName:@"Main_iPhone" bundle:nil];
    [self compareObject:storyboard ofType:@"UIStoryboard *" toSummary:@"fileName=\"Main_iPhone\""];
}

#pragma mark - UIStoryboardSegue
- (void)testUIStoryboardSegue01
{
    UIViewController *vc1 = [[UIViewController alloc] init];
    UIViewController *vc2 = [[UIViewController alloc] init];
    UIStoryboardSegue *segue = [[UIStoryboardSegue alloc] initWithIdentifier:@"idEntiFier" source:vc1 destination:vc2];
    
    [self compareObject:segue ofType:@"UIStoryboardSegue *" toSummary:@"identifier=@\"idEntiFier\""];
}

#pragma mark - UINib
- (void)testUINib01
{
    UINib *nib = [UINib nibWithNibName:@"View" bundle:nil];
    [self compareObject:nib ofType:@"UINib *" toSummary:@"resourceName=@\"View\""];
}

#pragma mark - UITableViewCell
- (void)testUITableViewCell01
{
    UITableViewCell *cell = [[UITableViewCell alloc] initWithStyle:UITableViewCellStyleValue1 reuseIdentifier:@"reuseIdentifier"];
    [self compareObject:cell ofType:@"UITableViewCell *" toSummary:@"reuseIdentifier=@\"reuseIdentifier\""];
    cell.textLabel.text = @"Text";
    [self compareObject:cell ofType:@"UITableViewCell *" toSummary:@"textLabel=@\"Text\", reuseIdentifier=@\"reuseIdentifier\""];
    cell.detailTextLabel.text = @"Detail text";
    [self compareObject:cell ofType:@"UITableViewCell *" toSummary:@"textLabel=@\"Text\", detailLabel=@\"Detail text\", reuseIdentifier=@\"reuseIdentifier\""];
}

- (void)testUITableViewCell02
{
    UITableViewCell *cell = [[UITableViewCell alloc] initWithStyle:UITableViewCellStyleDefault reuseIdentifier:@"reuseIdentifier"];
    [self compareObject:cell ofType:@"UITableViewCell *" toSummary:@"reuseIdentifier=@\"reuseIdentifier\""];
    cell.textLabel.text = @"Text";
    [self compareObject:cell ofType:@"UITableViewCell *" toSummary:@"textLabel=@\"Text\", reuseIdentifier=@\"reuseIdentifier\""];
    cell.tag = 325;
    [self compareObject:cell ofType:@"UITableViewCell *" toSummary:@"textLabel=@\"Text\", reuseIdentifier=@\"reuseIdentifier\", tag=325"];
}

#pragma mark - UIColor
- (void)testUIColor01
{
    UIColor *color = [UIColor brownColor];
    [self compareObject:color ofType:@"UIColor *" toSummary:@"rgb=#996633, red=0.6, green=0.4, blue=0.2, systemColorName=@\"brownColor\""];
}

- (void)testUIColor02
{
    UIColor *color = [UIColor colorWithWhite:0.4 alpha:1.0];
    [self compareObject:color ofType:@"UIDeviceWhiteColor *" toSummary:@"white=0.4"];
}

- (void)testUIColor03
{
    UIColor *color = [UIColor colorWithWhite:0.43 alpha:0.65];
    [self compareObject:color ofType:@"UIDeviceWhiteColor *" toSummary:@"white=0.43, alpha=0.65"];
}

- (void)testUIColor04
{
    UIColor *color = [UIColor colorWithRed:0.2 green:0.3 blue:0.4 alpha:0.5];
    [self compareObject:color ofType:@"UIDeviceRGBColor *" toSummary:@"rgba=#334D6680, red=0.2, green=0.3, blue=0.4, alpha=0.5"];
}

- (void)testUIColor05
{
    UIColor *color = [UIColor colorWithHue:0.1 saturation:0.3 brightness:0.7 alpha:0.9];
    [self compareObject:color ofType:@"UIDeviceRGBColor *" toSummary:@"rgba=#B39D7DE6, red=0.7, green=0.62, blue=0.49, alpha=0.9"];
}

- (void)testUIColor06
{
    UIColor *color = [UIColor colorWithRed:0.3 green:0.6 blue:0.9 alpha:1.0];
    [self compareObject:color ofType:@"UIDeviceRGBColor *" toSummary:@"rgb=#4D99E6, red=0.3, green=0.6, blue=0.9"];
}

#pragma mark - UIImage
- (void)testUIImage01
{
    UIImage *img = [UIImage imageNamed:@"LLVM_scale"];
    CGImageRef i = img.CGImage;
    
    if (img.scale == 1) {
        [self compareObject:img ofType:@"UIImage *" toSummary:@"(width=75, height=83)"];
        [self compareVariable:i ofType:@"CGImageRef" toSummary:@"(width=75, height=83)"];
    } else if (img.scale == 2) {
        [self compareObject:img ofType:@"UIImage *" toSummary:@"(width=75, height=83), @2x"];
        [self compareVariable:i ofType:@"CGImageRef" toSummary:@"(width=150, height=166)"];
    } else {
        [self compareObject:img ofType:@"UIImage *" toSummary:@"(width=75, height=83.33), @3x"];
        [self compareVariable:i ofType:@"CGImageRef" toSummary:@"(width=225, height=250)"];
    }
}

#pragma mark - UIActivityIndicatorView
- (void)testUIActivityIndicatorView01
{
    UIActivityIndicatorView *indicator = [[UIActivityIndicatorView alloc] init];
    [self compareObject:indicator ofType:@"UIActivityIndicatorView *" toSummary:@"hidesWhenStopped, style=White"];
    indicator.hidesWhenStopped = NO;
    [self compareObject:indicator ofType:@"UIActivityIndicatorView *" toSummary:@"style=White"];
    [indicator startAnimating];
    [self compareObject:indicator ofType:@"UIActivityIndicatorView *" toSummary:@"animating, style=White"];
}

@end
