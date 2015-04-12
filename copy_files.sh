#! /bin/bash

# Usage.
function usage {
    echo -e "Usage:"
    echo -e "$0 <dir>"
}

# Check parameters.
if [[ "$1" == "" || ! -d "$1" ]]; then
    usage
    exit 1
fi

# Files to copy
CPY=(
    "CFNetwork.framework/NSHTTPURLResponse.json"
    "CFNetwork.framework/NSHTTPURLResponseInternal.json"
    "CFNetwork.framework/NSURLConnection.json"
    "CFNetwork.framework/NSURLConnectionInternal.json"
    "CFNetwork.framework/NSURLRequest.json"
    "CFNetwork.framework/NSURLRequestInternal.json"
    "CFNetwork.framework/NSURLResponse.json"
    "CFNetwork.framework/NSURLResponseInternal.json"
    "CFNetwork.framework/NSURLSession.json"
    "CFNetwork.framework/NSURLSessionConfiguration.json"
    "CFNetwork.framework/NSURLSessionDataTask.json"
    "CFNetwork.framework/NSURLSessionDownloadTask.json"
    "CFNetwork.framework/NSURLSessionTask.json"
    "CFNetwork.framework/__NSCFLocalDataTask.json"
    "CFNetwork.framework/__NSCFLocalDownloadFile.json"
    "CFNetwork.framework/__NSCFLocalDownloadTask.json"
    "CFNetwork.framework/__NSCFLocalSessionTask.json"

    "Foundation.framework/NSLayoutConstraint.json"
    "Foundation.framework/NSOperation.json"
    "Foundation.framework/NSOperationQueue.json"
    "Foundation.framework/NSURLComponents.json"
    "Foundation.framework/__NSConcreteURLComponents.json"
    "Foundation.framework/__NSOperationInternal.json"
    "Foundation.framework/__NSOperationQueueInternal.json"

    "QuartzCore.framework/CALayer.json"

    "StoreKit.framework/SKDownload.json"
    "StoreKit.framework/SKPayment.json"
    "StoreKit.framework/SKPaymentInternal.json"
    "StoreKit.framework/SKPaymentQueue.json"
    "StoreKit.framework/SKPaymentQueueInternal.json"
    "StoreKit.framework/SKPaymentTransaction.json"
    "StoreKit.framework/SKPaymentTransactionInternal.json"
    "StoreKit.framework/SKProduct.json"
    "StoreKit.framework/SKProductInternal.json"
    "StoreKit.framework/SKProductsRequest.json"
    "StoreKit.framework/SKProductsRequestInternal.json"
    "StoreKit.framework/SKProductsResponse.json"
    "StoreKit.framework/SKProductsResponseInternal.json"
    "StoreKit.framework/SKReceiptRefreshRequest.json"
    "StoreKit.framework/SKRequest.json"
    "StoreKit.framework/SKRequestInternal.json"

    "UIKit.framework/UIActivityIndicatorView.json"
    "UIKit.framework/UIAlertAction.json"
    "UIKit.framework/UIAlertController.json"
    "UIKit.framework/UIAlertView.json"
    "UIKit.framework/UIBarButtonItem.json"
    "UIKit.framework/UIBarItem.json"
    "UIKit.framework/UIButton.json"
    "UIKit.framework/UIColor.json"
    "UIKit.framework/UIControl.json"
    "UIKit.framework/UIDatePicker.json"
    "UIKit.framework/UIDeviceRGBColor.json"
    "UIKit.framework/UIDeviceWhiteColor.json"
    "UIKit.framework/UIEvent.json"
    "UIKit.framework/UIImage.json"
    "UIKit.framework/UIImageView.json"
    "UIKit.framework/UIInternalEvent.json"
    "UIKit.framework/UILabel.json"
    "UIKit.framework/UINavigationController.json"
    "UIKit.framework/UINib.json"
    "UIKit.framework/UINibStorage.json"
    "UIKit.framework/UIPageControl.json"
    "UIKit.framework/UIPickerView.json"
    "UIKit.framework/UIProgressView.json"
    "UIKit.framework/UIResponder.json"
    "UIKit.framework/UIScreen.json"
    "UIKit.framework/UIScrollView.json"
    "UIKit.framework/UISegmentedControl.json"
    "UIKit.framework/UISlider.json"
    "UIKit.framework/UIStepper.json"
    "UIKit.framework/UIStoryboard.json"
    "UIKit.framework/UIStoryboardSegue.json"
    "UIKit.framework/UISwitch.json"
    "UIKit.framework/UITableViewCell.json"
    "UIKit.framework/UITextField.json"
    "UIKit.framework/UITouch.json"
    "UIKit.framework/UITouchesEvent.json"
    "UIKit.framework/UIView.json"
    "UIKit.framework/UIViewController.json"
    "UIKit.framework/_UIDatePickerView.json"
    )

for c in ${CPY[@]}; do
    fileName=`basename "${c}"`
    framework=`dirname "${c}"`
    directoryName="${framework%\.framework}"
    inputFilePath="${1}/$c"
    outputDirectoryPath="ClassDumps/${directoryName}"
    outputFilePath="${outputDirectoryPath}/${fileName}"

    # Create output directory.
    if [[ ! -e "${outputDirectoryPath}" ]]; then
        mkdir -p "${outputDirectoryPath}"
    fi

    # Check if input file exists.
    if [[ ! -e "${inputFilePath}" ]]; then
        echo -e "File doesn't exists ${inputFilePath}"
        continue
    fi

    # Copy.
    echo -e "Copying: ${outputFilePath}"
    cp "${inputFilePath}" "${outputFilePath}"
done
