LLDB missing summaries
======================

LLDB summaries for iOS Objective-C classes.

## Instalation
Clone this repository and add the following line to yout __~/.lldbinit__ file. If it doesn't exist, create it.

    # ~/.lldbinit
    ...
    command script import /path/to/lldb_summaries

The summaries will be available the next time Xcode starts.

## Supported summaries:
- CoreGraphics:
    - CGVector
- CFNetowrk:
    - NSURLRequest (NSMutableURLRequest)
- Foundation:
    - NSDateComponents
    - NSURLComponents (__NSConcreteURLComponents)
    - NSObject
    - NSUUID (__NSConcreteUUID)
- QuartzCore:
    - CALayer
- UIKit:
    - UIAlertAction
    - UIAlertController
    - UIAlertView
    - UIBarItem, UIBarButtonItem
    - UIButton
    - UIDatePicker
    - UIEdgeInsets
    - UILabel
    - UIOffset
    - UIPageControl
    - UIPickerView (Don't know what / how to show)
    - UIProgressView
    - UIScreen
    - UIScrollView
    - UISegmentedControl
    - UISlider
    - UIStepper
    - UISwitch
    - UITextField
    - UIView (UIImageView, UIWindow)
    - UIViewController
- StoreKit:
    - SKDownload (not tested!)
    - SKPayment
    - SKPaymentQueue
    - SKPaymentTransaction
    - SKProduct
    - SKProductsRequest
    - SKProductsResponse
    - SKReceiptRefreshRequest (doesn't return anything)
    - SKRequest

## Supported synthetic children:
- Foundation:
    - NSDateComponents
    - NSURLComponents
