LLDB missing iOS summaries
==========================

LLDB commands and summaries

## Instalation
1. Copy **lldbinit** to **~/.lldbinit**.
2. Copy **LLDBScripts** to **~/Library/**.

## Supported types:
- Foundation:
    - NSDateComponents
    - NSMutableURLRequest
    - NSObject
    - NSURLRequest
    - NSUUID
- CoreFoundation:
    - CGVector
- UIKit:
    - UIAlertView
    - UIButton
    - UIDatePicker
    - UIEdgeInsets
    - UIImageView (temporary disabled)
    - UILabel
    - UIOffset
    - UIPageControl
    - UIPickerView
    - UIProgressView
    - UIResponder
    - UIScreen
    - UIScrollView
    - UISegmentedControl
    - UISlider
    - UIStepper
    - UISwitch
    - UITextField
    - UIView (temporary disabled)
    - UIViewController
    - UIWindow (temporary disabled)
- StoreKit:
    - SKDownload (not tested!)
    - SKPayment
    - SKPaymentTransaction
    - SKProduct
    - SKProductsRequest
    - SKProductsResponse
    - SKRequest

## Summaries that I've failed to implement:
- NSIndexPath
Data is saved in the `void *_reserved` field. I have no idea how to get values from it.