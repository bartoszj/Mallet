LLDB missing iOS summaries
==========================

LLDB commands and summaries

## Instalation
1. Copy **lldbinit** to **~/.lldbinit**.
2. Copy **LLDBScripts** to **~/Library/**.

## Supported types:
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

## Summaries that I've failed to implement:
- NSIndexPath
Data is saved in the `void *_reserved` field. I have no idea how to get values from it.