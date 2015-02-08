//
//  FoundationSwiftTests.swift
//  LLDB Test Application
//
//  Created by Bartosz Janda on 01.02.2015.
//  Copyright (c) 2015 Bartosz Janda. All rights reserved.
//

import UIKit
import XCTest

class FoundationSwiftTests: SharedSwiftTestCase {

    // MARK: - Setup
    override func setUp() {
        super.setUp()
        // Put setup code here. This method is called before the invocation of each test method in the class.
    }
    
    override func tearDown() {
        // Put teardown code here. This method is called after the invocation of each test method in the class.
        super.tearDown()
    }
    
    // MARK: - NSData
    func testNSData1() {
        let s = "ęóąśłżźćń"
        let d8 = s.dataUsingEncoding(NSUTF8StringEncoding)!
        self.compareObject(d8, type: "NSData", summary: "18 bytes")
    }
    
    func testNSData2() {
        let s = "ęóąśłżźćń"
        let d8 = s.dataUsingEncoding(NSUTF16StringEncoding)!
        self.compareObject(d8, type: "NSData", summary: "20 bytes")
    }
    
    func testNSData3() {
        let s = "ęóąśłżźćń"
        let d8 = s.dataUsingEncoding(NSUTF16LittleEndianStringEncoding)!
        self.compareObject(d8, type: "NSData", summary: "18 bytes")
    }
    
    func testNSData4() {
        let s = "ęóąśłżźćń"
        let d8 = s.dataUsingEncoding(NSUTF16BigEndianStringEncoding)!
        self.compareObject(d8, type: "NSData", summary: "18 bytes")
    }
    
    func testNSData5() {
        let s = "ęóąśłżźćń"
        let d8 = s.dataUsingEncoding(NSUTF32StringEncoding)!
        self.compareObject(d8, type: "NSData", summary: "40 bytes")
    }
    
    func testNSData6() {
        let s = "ęóąśłżźćń"
        let d8 = s.dataUsingEncoding(NSUTF32LittleEndianStringEncoding)!
        self.compareObject(d8, type: "NSData", summary: "36 bytes")
    }
    
    func testNSData7() {
        let s = "ęóąśłżźćń"
        let d8 = s.dataUsingEncoding(NSUTF32BigEndianStringEncoding)!
        self.compareObject(d8, type: "NSData", summary: "36 bytes")
    }
    
    // MARK: - NSUUID
    func testNSUUID1() {
        let uuid = NSUUID(UUIDString: "68753A44-4D6F-1226-9C60-0050E4C00067")!
        self.compareObject(uuid, type: "NSUUID", summary: "68753A44-4D6F-1226-9C60-0050E4C00067")
    }
    
    func testNSUUID2() {
//        let uuid = NSUUID(UUIDString: "68753A44-4D6F-1226-9C60-0050E4C00067")!
//        self.compareObject(uuid, type: "__NSConcreteUUID", summary: "68753A44-4D6F-1226-9C60-0050E4C00067")
    }
    
    // MARK: - NSURL
    func testNSURL() {
        let url = NSURL(string: "https://google.com")!
        self.compareObject(url, type: "NSURL", summary: "\"https://google.com\"")
    }
    
    // MARK: - NSDateComponents
    func testNSDateComponents01() {
        var dateComponents = NSDateComponents()
        dateComponents.era = 1
        self.compareObject(dateComponents, type: "NSDateComponents", summary: "era=1")
    }
    
    func testNSDateComponents02() {
        var dateComponents = NSDateComponents()
        dateComponents.year = 2
        self.compareObject(dateComponents, type: "NSDateComponents", summary: "year=2")
    }
    
    func testNSDateComponents03() {
        var dateComponents = NSDateComponents()
        dateComponents.month = 3
        self.compareObject(dateComponents, type: "NSDateComponents", summary: "month=3")
    }
    
    func testNSDateComponents04() {
        var dateComponents = NSDateComponents()
        dateComponents.day = 4
        self.compareObject(dateComponents, type: "NSDateComponents", summary: "day=4")
    }
    
    func testNSDateComponents05() {
        var dateComponents = NSDateComponents()
        dateComponents.hour = 5
        self.compareObject(dateComponents, type: "NSDateComponents", summary: "hour=5")
    }
    
    func testNSDateComponents06() {
        var dateComponents = NSDateComponents()
        dateComponents.minute = 6
        self.compareObject(dateComponents, type: "NSDateComponents", summary: "minute=6")
    }
    
    func testNSDateComponents07() {
        var dateComponents = NSDateComponents()
        dateComponents.second = 7
        self.compareObject(dateComponents, type: "NSDateComponents", summary: "second=7")
    }
    
//    func testNSDateComponents08() {
//        var dateComponents = NSDateComponents()
//        dateComponents.week = 8
//        self.compareObject(dateComponents, type: "NSDateComponents", summary: "week=8")
//    }
    
    func testNSDateComponents09() {
        var dateComponents = NSDateComponents()
        dateComponents.weekday = 9
        self.compareObject(dateComponents, type: "NSDateComponents", summary: "weekday=9")
    }
    
    func testNSDateComponents10() {
        var dateComponents = NSDateComponents()
        dateComponents.weekdayOrdinal = 10
        self.compareObject(dateComponents, type: "NSDateComponents", summary: "weekdayOrdinal=10")
    }
    
    func testNSDateComponents11() {
        var dateComponents = NSDateComponents()
        dateComponents.quarter = 11
        self.compareObject(dateComponents, type: "NSDateComponents", summary: "quarter=11")
    }
    
    func testNSDateComponents12() {
        var dateComponents = NSDateComponents()
        dateComponents.weekOfYear = 12
        self.compareObject(dateComponents, type: "NSDateComponents", summary: "weekOfYear=12")
    }
    
    func testNSDateComponents13() {
        var dateComponents = NSDateComponents()
        dateComponents.weekOfMonth = 13
        self.compareObject(dateComponents, type: "NSDateComponents", summary: "weekOfMonth=13")
    }
    
    func testNSDateComponents14() {
        var dateComponents = NSDateComponents()
        dateComponents.yearForWeekOfYear = 14
        self.compareObject(dateComponents, type: "NSDateComponents", summary: "yearForWeekOfYear=14")
    }
    
    func testNSDateComponents15() {
        var dateComponents = NSDateComponents()
        dateComponents.hour = 5
        dateComponents.minute = 6
        self.compareObject(dateComponents, type: "NSDateComponents", summary: "time=05:06")
    }
    
    func testNSDateComponents16() {
        var dateComponents = NSDateComponents()
        dateComponents.hour = 5
        dateComponents.minute = 6
        dateComponents.second = 7
        self.compareObject(dateComponents, type: "NSDateComponents", summary: "time=05:06:07")
    }
    
    func testNSDateComponents17() {
        var dateComponents = NSDateComponents()
        dateComponents.year = 2014
        dateComponents.month = 3
        dateComponents.day = 21
        self.compareObject(dateComponents, type: "NSDateComponents", summary: "date=2014-03-21")
    }
    
    func testNSDateComponents18() {
        var dateComponents = NSDateComponents()
        dateComponents.year = 2014
        dateComponents.month = 3
        dateComponents.day = 21
        dateComponents.hour = 5
        dateComponents.minute = 6
        dateComponents.second = 7
        self.compareObject(dateComponents, type: "NSDateComponents", summary: "2014-03-21 05:06:07")
    }
    
    // MARK: - NSURLComponents
    func testNSURLComponents01() {
        let components = NSURLComponents(string: "http://google.com")!
        self.compareObject(components, type: "NSURLComponents", summary: "url=\"http://google.com\"")
    }
    
    func testNSURLComponents02() {
        let components = NSURLComponents()
        components.scheme = "scheme"
        self.compareObject(components, type: "NSURLComponents", summary: "scheme=\"scheme\"")
        components.user = "user"
        self.compareObject(components, type: "NSURLComponents", summary: "scheme=\"scheme\", user=\"user\"")
        components.password = "password"
        self.compareObject(components, type: "NSURLComponents", summary: "scheme=\"scheme\", user=\"user\", password=\"password\"")
    }
    
    func testNSURLComponents03() {
        let components = NSURLComponents()
        components.host = "host"
        self.compareObject(components, type: "NSURLComponents", summary: "host=\"host\"")
        components.port = 1234
        self.compareObject(components, type: "NSURLComponents", summary: "host=\"host\", port=1234")
        components.path = "path1/path2"
        self.compareObject(components, type: "NSURLComponents", summary: "host=\"host\", port=1234, path=\"path1/path2\"")
        components.query = "query"
        self.compareObject(components, type: "NSURLComponents", summary: "host=\"host\", port=1234, path=\"path1/path2\", query=\"query\"")
        components.fragment = "fragment"
        self.compareObject(components, type: "NSURLComponents", summary: "host=\"host\", port=1234, path=\"path1/path2\", query=\"query\", fragment=\"fragment\"")
    }
    
    // MARK: - NSLayoutConstraint
    let nslayoutConstraintSummaryShort = false
    func testNSLayoutConstraint01() {
        let view = UIView(frame: CGRect(x: 0, y: 0, width: 100, height: 100))
        let constraint1 = NSLayoutConstraint(item: view, attribute: .Width, relatedBy: .Equal, toItem: nil, attribute: .NotAnAttribute, multiplier: 1, constant: 200)
        let constraint2 = NSLayoutConstraint(item: view, attribute: .Width, relatedBy: .GreaterThanOrEqual, toItem: nil, attribute: .NotAnAttribute, multiplier: 1, constant: 200)
        let constraint3 = NSLayoutConstraint(item: view, attribute: .Height, relatedBy: .LessThanOrEqual, toItem: nil, attribute: .NotAnAttribute, multiplier: 1, constant: 300)
        
        if !nslayoutConstraintSummaryShort {
            let ptr = ObjectIdentifier(view).uintValue()
            let summary1 = NSString(format: "H:[UIView:0x%lx(200)]", ptr)
            let summary2 = NSString(format: "H:[UIView:0x%lx(>=200)]", ptr)
            let summary3 = NSString(format: "V:[UIView:0x%lx(<=300)]", ptr)
            self.compareObject(constraint1, type: "NSLayoutConstraint", summary: summary1)
            self.compareObject(constraint2, type: "NSLayoutConstraint", summary: summary2)
            self.compareObject(constraint3, type: "NSLayoutConstraint", summary: summary3)
        } else {
            self.compareObject(constraint1, type: "NSLayoutConstraint", summary: "width == +200")
            self.compareObject(constraint2, type: "NSLayoutConstraint", summary: "width >= +200")
            self.compareObject(constraint3, type: "NSLayoutConstraint", summary: "height <= +300")
        }
    }
    
    func testNSLayoutConstraint02() {
        let view = UIView(frame: CGRect(x: 0, y: 0, width: 100, height: 100))
        let constraint1 = NSLayoutConstraint(item: view, attribute: .Width, relatedBy: .Equal, toItem: nil, attribute: .NotAnAttribute, multiplier: 1, constant: 200)
        constraint1.priority = 123
        let constraint2 = NSLayoutConstraint(item: view, attribute: .Width, relatedBy: .GreaterThanOrEqual, toItem: nil, attribute: .NotAnAttribute, multiplier: 1, constant: 200)
        constraint2.priority = 456
        let constraint3 = NSLayoutConstraint(item: view, attribute: .Height, relatedBy: .LessThanOrEqual, toItem: nil, attribute: .NotAnAttribute, multiplier: 1, constant: 300)
        constraint3.priority = 789
        
        if !nslayoutConstraintSummaryShort {
            let ptr = ObjectIdentifier(view).uintValue()
            let summary1 = NSString(format: "H:[UIView:0x%lx(200@123)]", ptr)
            let summary2 = NSString(format: "H:[UIView:0x%lx(>=200@456)]", ptr)
            let summary3 = NSString(format: "V:[UIView:0x%lx(<=300@789)]", ptr)
            self.compareObject(constraint1, type: "NSLayoutConstraint", summary: summary1)
            self.compareObject(constraint2, type: "NSLayoutConstraint", summary: summary2)
            self.compareObject(constraint3, type: "NSLayoutConstraint", summary: summary3)
        } else {
            self.compareObject(constraint1, type: "NSLayoutConstraint", summary: "width == +200@123")
            self.compareObject(constraint2, type: "NSLayoutConstraint", summary: "width >= +200@456")
            self.compareObject(constraint3, type: "NSLayoutConstraint", summary: "height <= +300@789")
        }
    }
    
    func testNSLayoutConstraint03() {
        let view1 = UIView(frame: CGRect(x: 0, y: 0, width: 100, height: 100))
        let view2 = UIView(frame: CGRect(x: 10, y: 20, width: 300, height: 400))
        let constraint1 = NSLayoutConstraint(item: view1, attribute: .Left, relatedBy: .Equal, toItem: view2, attribute: .Baseline, multiplier: 1, constant: -200)
        let constraint2 = NSLayoutConstraint(item: view1, attribute: .Trailing, relatedBy: .GreaterThanOrEqual, toItem: view2, attribute: .CenterX, multiplier: 2, constant: 200)
        let constraint3 = NSLayoutConstraint(item: view1, attribute: .TopMargin, relatedBy: .LessThanOrEqual, toItem: view2, attribute: .CenterYWithinMargins, multiplier: 1, constant: 300)
        constraint3.priority = 300
        
        if !nslayoutConstraintSummaryShort {
            let ptr1 = ObjectIdentifier(view1).uintValue()
            let ptr2 = ObjectIdentifier(view2).uintValue()
            let summary1 = NSString(format: "UIView:0x%lx.left == UIView:0x%lx.lastBaseline - 200", ptr1, ptr2)
            let summary2 = NSString(format: "UIView:0x%lx.trailing >= 2*UIView:0x%lx.centerX + 200", ptr1, ptr2)
            let summary3 = NSString(format: "UIView:0x%lx.topMargin <= UIView:0x%lx.centerYWithMargins + 300 @300", ptr1, ptr2)
            self.compareObject(constraint1, type: "NSLayoutConstraint", summary: summary1)
            self.compareObject(constraint2, type: "NSLayoutConstraint", summary: summary2)
            self.compareObject(constraint3, type: "NSLayoutConstraint", summary: summary3)
        } else {
            self.compareObject(constraint1, type: "NSLayoutConstraint", summary: "left == lastBaseline-200")
            self.compareObject(constraint2, type: "NSLayoutConstraint", summary: "trailing >= 2*centerX+200")
            self.compareObject(constraint3, type: "NSLayoutConstraint", summary: "topMargin <= centerYWithMargins+300@300")
        }
    }
    
    func testNSLayoutConstraint04() {
        let view = UINib(nibName: "AutolayoutView", bundle: nil).instantiateWithOwner(nil, options: nil).first! as UIView
        let subview = view.subviews[0] as UIView
        let constraints = view.constraints()
        let constraint1 = constraints[0] as NSLayoutConstraint
        let constraint2 = constraints[1] as NSLayoutConstraint
        
        if !nslayoutConstraintSummaryShort {
            let ptr1 = ObjectIdentifier(subview).uintValue()
            let ptr2 = ObjectIdentifier(view).uintValue()
            let summary1 = NSString(format: "UIView:0x%lx.top == UIView:0x%lx.top + standard", ptr1, ptr2)
            let summary2 = NSString(format: "UIView:0x%lx.leading == UIView:0x%lx.leading + standard", ptr1, ptr2)
            self.compareObject(constraint1, type: "NSLayoutConstraint", summary: summary1)
            self.compareObject(constraint2, type: "NSLayoutConstraint", summary: summary2)
        } else {
            self.compareObject(constraint1, type: "NSLayoutConstraint", summary: "top == top+standard")
            self.compareObject(constraint2, type: "NSLayoutConstraint", summary: "leading == leading+standard")
        }
    }
}
