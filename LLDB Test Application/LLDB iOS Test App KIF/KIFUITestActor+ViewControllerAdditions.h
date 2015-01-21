//
//  KIFUITestActor+ViewControllerAdditions.h
//  LLDB Test Application
//
//  Created by Bartosz Janda on 21.01.2015.
//  Copyright (c) 2015 Bartosz Janda. All rights reserved.
//

#import "KIFUITestActor.h"

@interface KIFUITestActor (ViewControllerAdditions)

- (void)vc_goToBasicControls;
- (void)vc_goToPickersControls;
- (void)vc_goToAlertsControls;
- (void)vc_goToViewsControls;
- (void)vc_goToScrollViewControls;
- (void)vc_goToModalViewControls;

@end
