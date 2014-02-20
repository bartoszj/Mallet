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
    - UITextField (only placeholder text works)
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

## Known problems:
- Summaries doesn't work on devices with arm64 but they works on 64bit simulator.

## Summaries that I've failed to implement:
- NSIndexPath
Data is saved in the `void *_reserved` field. I have no idea how to get values from it.