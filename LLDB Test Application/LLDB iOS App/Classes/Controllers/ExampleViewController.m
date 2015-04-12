//
//  ExampleViewController.m
//  LLDB Test Application
//
//  Created by Bartosz Janda on 12.04.2015.
//  Copyright (c) 2015 Bartosz Janda. All rights reserved.
//

#import "ExampleViewController.h"

@interface ExampleViewController ()

#pragma mark - Properties
// Views
@property (weak, nonatomic) IBOutlet UITextField *loginTextField;
@property (weak, nonatomic) IBOutlet UITextField *passwordTextField;
@property (weak, nonatomic) IBOutlet UIButton *loginButton;
@property (weak, nonatomic) IBOutlet UIActivityIndicatorView *activityIndicator;

// Models.
@property (strong, nonatomic) NSURLSession *session;

@end

@implementation ExampleViewController

#pragma mark - Initialization
- (instancetype)initWithCoder:(NSCoder *)aDecoder
{
    self = [super initWithCoder:aDecoder];
    if (self) {
        NSURLSessionConfiguration *configuration = [NSURLSessionConfiguration defaultSessionConfiguration];
        _session = [NSURLSession sessionWithConfiguration:configuration];
        _session.sessionDescription = @"Example WS session";
    }
    return self;
}

#pragma mark - View life cycle
- (void)viewDidLoad
{
    [super viewDidLoad];
    self.title = @"Example";
}

#pragma mark - Actions
- (IBAction)loginButtonTouched:(UIButton *)sender forEvent:(UIEvent *)event
{
    UITextField *loginTextField = self.loginTextField;
    UITextField *passwordTextFIeld = self.passwordTextField;
    NSDictionary *params = @{
                             @"login": loginTextField.text,
                             @"password": passwordTextFIeld.text
                             };
    NSData *jsonParams = [NSJSONSerialization dataWithJSONObject:params options:0 error:nil];
    
    NSURLSession *session = self.session;
    NSURL *url = [NSURL URLWithString:@"https://example.org/login"];
    NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:url];
    request.HTTPMethod = @"POST";
    request.HTTPBody = jsonParams;
    
    NSLog(@"Sending");
}

@end
