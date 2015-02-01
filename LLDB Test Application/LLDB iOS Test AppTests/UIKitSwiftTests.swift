//
//  UIKitSwiftTests.swift
//  LLDB Test Application
//
//  Created by Bartosz Janda on 01.02.2015.
//  Copyright (c) 2015 Bartosz Janda. All rights reserved.
//

import UIKit
import XCTest

class UIKitSwiftTests: SharedSwiftTestCase {

    // MARK: - Setup
    override func setUp() {
        super.setUp()
        // Put setup code here. This method is called before the invocation of each test method in the class.
    }
    
    override func tearDown() {
        // Put teardown code here. This method is called after the invocation of each test method in the class.
        super.tearDown()
    }
    
    // MARK: - UIEdgeInsets
//    func testUIEdgeInsets() {
//        let insets = UIEdgeInsetsMake(1, 2, 3, 4)
//        self.compareVariable(insets, type: "UIEdgeInsets", summary: "(top=1, left=2, bottom=3, right=4)")
//    }
    
    // MARK: - UIOffset
//    func testUIOffset() {
//        let offset = UIOffset(horizontal: 1, vertical: 2)
//        self.compareVariable(offset, type: "UIOffset", summary: "(horizontal=1, vertical=2)")
//    }
    
    // MARK: - UIScreen
    func testUIScreen() {
        let screen = UIScreen.mainScreen()
        self.compareObject(screen, type: "UIScreen", summary: "size=(320, 568), scale=2, idiom=Phone")
    }
    
    // MARK: - UIView
    func testUIView1() {
        let frame = CGRect(x: 10, y: 20, width: 300, height: 400)
        let view = UIView(frame: frame)
        self.compareObject(view, type: "UIView", summary: "frame=(10 20; 300 400)")
    }
    
    func testUIView2() {
        let frame = CGRect(x: 10, y: 20, width: 300, height: 400)
        let view = UIView(frame: frame)
        view.tag = 10
        self.compareObject(view, type: "UIView", summary: "frame=(10 20; 300 400), tag=10")
    }
    
    // MARK: - UIImageView
    func testUIImageView1() {
        let image = UIImage(named: "llvm")!
        let view = UIImageView(image: image)
        self.compareObject(view, type: "UIImageView", summary: "frame=(0 0; 128 128)")
    }
    
    // MARK: - UIWindow
    func testUIWindow() {
        let window = UIApplication.sharedApplication().delegate!.window!!
        self.compareObject(window, type: "UIWindow", summary: "frame=(0 0; 320 568)")
    }
    
    // MARK: - UILabel
    func testUILabel1() {
        let frame = CGRect(x: 10, y: 20, width: 100, height: 22)
        let label = UILabel(frame: frame)
        label.text = "asdaasd"
        self.compareObject(label, type: "UILabel", summary: "text=\"asdaasd\"")
    }
    
    func testUILabel2() {
        let frame = CGRect(x: 10, y: 20, width: 100, height: 22)
        let label = UILabel(frame: frame)
        label.text = "ęóąśłżźćń"
        self.compareObject(label, type: "UILabel", summary: "text=\"ęóąśłżźćń\"")
    }
    
    func testUILabel3() {
        let frame = CGRect(x: 10, y: 20, width: 100, height: 22)
        let label = UILabel(frame: frame)
        label.text = "ęóąśłżźćń"
        label.tag = 444
        self.compareObject(label, type: "UILabel", summary: "text=\"ęóąśłżźćń\", tag=444")
    }
    
    // MARK: - UIScrollView
    func testUIScrollView1() {
        let scrollView = UIScrollView(frame: CGRect(x: 0, y: 0, width: 30, height: 40))
        scrollView.contentSize = CGSize(width: 33, height: 44)
        self.compareObject(scrollView, type: "UIScrollView", summary: "frame=(0 0; 30 40), contentOffset=(0, 0), contentSize=(33, 44)")
    }
    
    func testUIScrollView2() {
        let scrollView = UIScrollView(frame: CGRect(x: 0, y: 0, width: 30, height: 40))
        scrollView.contentSize = CGSize(width: 33, height: 44)
        scrollView.contentOffset = CGPoint(x: 20, y: 21);
        self.compareObject(scrollView, type: "UIScrollView", summary: "frame=(0 0; 30 40), contentOffset=(20, 21), contentSize=(33, 44)")
    }
    
    func testUIScrollView3() {
        let scrollView = UIScrollView(frame: CGRect(x: 0, y: 0, width: 30, height: 40))
        scrollView.contentSize = CGSize(width: 33, height: 44)
        scrollView.contentInset = UIEdgeInsets(top: 1, left: 2, bottom: 3, right: 4)
        scrollView.contentOffset = CGPoint(x: 20, y: 21);
        self.compareObject(scrollView, type: "UIScrollView", summary: "frame=(0 0; 30 40), contentOffset=(20, 21), contentSize=(33, 44), inset=(1, 2, 3, 4)")
    }
    
    func testUIScrollView4() {
        let scrollView = UIScrollView(frame: CGRect(x: 0, y: 0, width: 30, height: 40))
        scrollView.contentSize = CGSize(width: 33, height: 44)
        scrollView.contentInset = UIEdgeInsets(top: 1, left: 2, bottom: 3, right: 4)
        scrollView.contentOffset = CGPoint(x: 20, y: 21);
        scrollView.minimumZoomScale = 0.2;
        self.compareObject(scrollView, type: "UIScrollView", summary: "frame=(0 0; 30 40), contentOffset=(20, 21), contentSize=(33, 44), inset=(1, 2, 3, 4), minScale=0.2")
    }
    
    func testUIScrollView5() {
        let scrollView = UIScrollView(frame: CGRect(x: 0, y: 0, width: 30, height: 40))
        scrollView.contentSize = CGSize(width: 33, height: 44)
        scrollView.contentInset = UIEdgeInsets(top: 1, left: 2, bottom: 3, right: 4)
        scrollView.contentOffset = CGPoint(x: 20, y: 21);
        scrollView.minimumZoomScale = 0.2;
        scrollView.maximumZoomScale = 3.5;
        self.compareObject(scrollView, type: "UIScrollView", summary: "frame=(0 0; 30 40), contentOffset=(20, 21), contentSize=(33, 44), inset=(1, 2, 3, 4), minScale=0.2, maxScale=3.5")
    }
    
    // MARK: - UIAlertAction
    func testUIAlertAction01() {
        let action = UIAlertAction(title: "alert title", style: .Cancel) { (action) -> Void in
            println("action")
        }
        self.compareObject(action, type: "UIAlertAction", summary: "title=\"alert title\", style=Cancel")
    }
    
    func testUIAlertAction02() {
        let action = UIAlertAction(title: "alert title", style: .Destructive) { (action) -> Void in
            println("action")
        }
        action.enabled = false
        self.compareObject(action, type: "UIAlertAction", summary: "title=\"alert title\", style=Destructive, disabled")
    }
    
    // MARK: - UIAlertController
    func testUIAlertController01() {
        let alertController = UIAlertController(title: "alert title", message: "alert message", preferredStyle: .ActionSheet)
        self.compareObject(alertController, type: "UIAlertController", summary: "title=\"alert title\", message=\"alert message\", preferredStyle=ActionSheet, actions=0")
    }
    
    func testUIAlertController02() {
        let alertController = UIAlertController(title: "alert title", message: "alert message", preferredStyle: .Alert)
        let action = UIAlertAction(title: "alert title", style: .Destructive) { (action) -> Void in
            println("action")
        }
        alertController.addAction(action)
        self.compareObject(alertController, type: "UIAlertController", summary: "title=\"alert title\", message=\"alert message\", preferredStyle=Alert, actions=1")
    }
    
    // MARK: - UIAlertView
    func testUIAlertView() {
        let alertView = UIAlertView(title: "title", message: "message", delegate: nil, cancelButtonTitle: "cancel", otherButtonTitles: "OK")
        self.compareObject(alertView, type: "UIAlertView", summary: "title=\"title\", message=\"message\", style=Default")
    }
    
    // MARK: - UIProgressView
    func testUIProgressView() {
        let progressView = UIProgressView(frame: CGRect(x: 0, y: 0, width: 66, height: 84))
        progressView.progress = 0.453
        self.compareObject(progressView, type: "UIProgressView", summary: "progress=0.45")
    }
    
    // MARK: - UIBarButtonItem
    func testUIBarButtonItem01() {
        let item = UIBarButtonItem(title: "title", style: .Done, target: nil, action: nil)
        self.compareObject(item, type: "UIBarButtonItem", summary: "title=\"title\"")
    }
    
    func testUIBarButtonItem02() {
        let item = UIBarButtonItem(title: "title", style: .Done, target: nil, action: nil)
        item.width = 123
        self.compareObject(item, type: "UIBarButtonItem", summary: "title=\"title\", width=123")
    }
    
    // MARK: - UIButton
    func testUIButton1() {
        let button = UIButton()
        button.setTitle("title", forState: .Normal)
        button.layoutIfNeeded()  // Hack to force drawing.
        self.compareObject(button, type: "UIButton", summary: "text=\"title\"")
    }
    
    func testUIButton2() {
        let button = UIButton()
        button.setTitle("title", forState: .Normal)
        button.tag = 123
        button.layoutIfNeeded()  // Hack to force drawing.
        self.compareObject(button, type: "UIButton", summary: "text=\"title\", tag=123")
    }
    
    // MARK: - UITextField
    func testUITextField1() {
        let frame = CGRect(x: 0, y: 0, width: 10, height: 10)
        let textField = UITextField(frame: frame)
        textField.text = "zzcxcx"
        self.compareObject(textField, type: "UITextField", summary: "text=\"zzcxcx\"")
    }
    
    func testUITextField2() {
        let frame = CGRect(x: 0, y: 0, width: 10, height: 10)
        let textField = UITextField(frame: frame)
        textField.attributedText = NSAttributedString(string: "ĘÓĄŚŁŻŹĆŃ")
        self.compareObject(textField, type: "UITextField", summary: "text=\"ĘÓĄŚŁŻŹĆŃ\"")
    }
    
    func testUITextField3() {
        let frame = CGRect(x: 0, y: 0, width: 10, height: 10)
        let textField = UITextField(frame: frame)
        textField.placeholder = "asdfghj"
        self.compareObject(textField, type: "UITextField", summary: "placeholder=\"asdfghj\"")
    }
    
    func testUITextField4() {
        let frame = CGRect(x: 0, y: 0, width: 10, height: 10)
        let textField = UITextField(frame: frame)
        textField.attributedPlaceholder = NSAttributedString(string: "ĘÓĄŚŁŻŹĆŃ2")
        self.compareObject(textField, type: "UITextField", summary: "placeholder=\"ĘÓĄŚŁŻŹĆŃ2\"")
    }
    
    // MARK: - UIDatePicker
    func testUIDatePicker() {
        let dateComponents = NSDateComponents()
        dateComponents.year = 2014
        dateComponents.month = 4
        dateComponents.day = 22
        dateComponents.hour = 11
        dateComponents.minute = 44
        dateComponents.second = 33
        
        let datePicker = UIDatePicker(frame: CGRect(x: 20, y: 10, width: 34, height: 234))
        datePicker.date = NSCalendar.currentCalendar().dateFromComponents(dateComponents)!
        self.compareObject(datePicker, type: "UIDatePicker", summary: "era=1, 2014-04-22 11:44:33, leapMonth=NO")
    }
    
    // MARK: - UIPageControl
    func testUIPageControl() {
        let pageControl = UIPageControl(frame: CGRect(x: 0, y: 0, width: 123, height: 41))
        pageControl.numberOfPages = 13
        pageControl.currentPage = 4
        self.compareObject(pageControl, type: "UIPageControl", summary: "currentPage=4, numberOfPages=13")
    }
    
    // MARK: - UISegmentedControl
    func testUISegmentedControl() {
        let segmentedControl = UISegmentedControl(items: ["a", "b", "c"])
        segmentedControl.selectedSegmentIndex = 1
        self.compareObject(segmentedControl, type: "UISegmentedControl", summary: "selected=1, segments=3")
    }
    
    // MARK: - UISlider
    func testUISlider() {
        let slider = UISlider(frame: CGRect(x: 0, y: 0, width: 30, height: 40))
        slider.minimumValue = 1.0
        slider.maximumValue = 10.0
        slider.value = 3.0
        self.compareObject(slider, type: "UISlider", summary: "value=3, min=1, max=10")
    }
    
    // MERK: - UIStepper
    func testUIStepper() {
        let stepper = UIStepper(frame: CGRect(x: 0, y: 0, width: 32, height: 52))
        stepper.minimumValue = 1.0
        stepper.maximumValue = 56.0
        stepper.value = 6.0
        stepper.stepValue = 1.5
        self.compareObject(stepper, type: "UIStepper", summary: "value=6, step=1.5, min=1, max=56")
    }
    
    // MARK: - UISwitch
    func testUISwitch1() {
        let switchControl = UISwitch(frame: CGRect(x: 0, y: 0, width: 23, height: 523))
        switchControl.on = true
        self.compareObject(switchControl, type: "UISwitch", summary: "on=YES")
    }
    
    func testUISwitch2() {
        let switchControl = UISwitch(frame: CGRect(x: 0, y: 0, width: 23, height: 523))
        switchControl.on = false
        self.compareObject(switchControl, type: "UISwitch", summary: "on=NO")
    }
    
    // MARK: - UIViewController
    func testUIViewController() {
        let vc = UIViewController()
        vc.title = "ęóąśłżźćń"
        self.compareObject(vc, type: "UIViewController", summary: "title=\"ęóąśłżźćń\"")
    }
    
    // MARK: - UINavigationController
    func testUINavigationController01() {
        let vc1 = UIViewController()
        vc1.title = "vc1"
        let vc2 = UIViewController()
        vc2.title = "vc2"
        let navc = UINavigationController(rootViewController: vc1)
        self.compareObject(navc, type: "UINavigationController", summary: "viewControllers=1")
        navc.pushViewController(vc2, animated: false)
        self.compareObject(navc, type: "UINavigationController", summary: "viewControllers=2")
    }
    
    // MARK: - UIStoryboard
    func testUIStoryboard01() {
        let storyboard = UIStoryboard(name: "Main_iPhone", bundle: nil)
        self.compareObject(storyboard, type: "UIStoryboard", summary: "fileName=\"Main_iPhone\"")
    }
    
    // MARK: - UIStoryboardSegue
    func testUIStoryboardSegue01() {
        let vc1 = UIViewController()
        let vc2 = UIViewController()
        let segue = UIStoryboardSegue(identifier: "idEntiFier", source: vc1, destination: vc2)
        self.compareObject(segue, type: "UIStoryboardSegue", summary: "identifier=\"idEntiFier\"")
    }
    
    // MARK: - UINib
    func testUINib01() {
        let nib = UINib(nibName: "View", bundle: nil)
        self.compareObject(nib, type: "UINib", summary: "resourceName=\"View\"")
    }
    
    // MARK: - UITableViewCell
    func testUITableViewCell01() {
        let cell = UITableViewCell(style: .Value1, reuseIdentifier: "reuseIdentifier")
        self.compareObject(cell, type: "UITableViewCell", summary: "reuseIdentifier=\"reuseIdentifier\"")
        cell.textLabel!.text = "Text"
        self.compareObject(cell, type: "UITableViewCell", summary: "textLabel=\"Text\", reuseIdentifier=\"reuseIdentifier\"")
        cell.detailTextLabel!.text = "Detail text"
        self.compareObject(cell, type: "UITableViewCell", summary: "textLabel=\"Text\", detailLabel=\"Detail text\", reuseIdentifier=\"reuseIdentifier\"")
    }
    
    func testUITableViewCell02() {
        let cell = UITableViewCell(style: .Default, reuseIdentifier: "reuseIdentifier")
        self.compareObject(cell, type: "UITableViewCell", summary: "reuseIdentifier=\"reuseIdentifier\"")
        cell.textLabel!.text = "Text"
        self.compareObject(cell, type: "UITableViewCell", summary: "textLabel=\"Text\", reuseIdentifier=\"reuseIdentifier\"")
        cell.tag = 325
        self.compareObject(cell, type: "UITableViewCell", summary: "textLabel=\"Text\", reuseIdentifier=\"reuseIdentifier\", tag=325")
    }
    
    // MARK: - UIColor
//    func testUIColor01() {
//        let color = UIColor.brownColor()
//        self.compareObject(color, type: "UIColor", summary: "rgb=#996633, red=0.6, green=0.4, blue=0.2, systemColorName=\"brownColor\"")
//    }
//    
//    func testUIColor02() {
//        let color = UIColor(white: 0.4, alpha: 1)
//        self.compareObject(color, type: "UIDeviceWhiteColor", summary: "white=0.4")
//    }
//    
//    func testUIColor03() {
//        let color = UIColor(white: 0.43, alpha: 0.65)
//        self.compareObject(color, type: "UIDeviceWhiteColor", summary: "white=0.43, alpha=0.65")
//    }
//    
//    func testUIColor04() {
//        let color = UIColor(red: 0.2, green: 0.3, blue: 0.4, alpha: 0.5)
//        self.compareObject(color, type: "UIDeviceRGBColor", summary: "rgba=#334D6680, red=0.2, green=0.3, blue=0.4, alpha=0.5")
//    }
//    
//    func testUIColor05() {
//        let color = UIColor(hue: 0.1, saturation: 0.3, brightness: 0.7, alpha: 0.9)
//        self.compareObject(color, type: "UIDeviceRGBColor", summary: "rgba=#B39D7DE6, red=0.7, green=0.62, blue=0.49, alpha=0.9")
//    }
//    
//    func testUIColor06() {
//        let color = UIColor(red: 0.3, green: 0.6, blue: 0.9, alpha: 1.0)
//        self.compareObject(color, type: "UIDeviceRGBColor", summary: "rgb=#4D99E6, red=0.3, green=0.6, blue=0.9")
//    }
}
