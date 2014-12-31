#! /bin/bash

# CLASSDUMP=`which class-dump`
CLASSDUMP="$HOME/Library/Developer/Xcode/DerivedData/class-dump-gywlitzvdxxnevhjqkhvwciuhkna/Build/Products/Debug/class-dump"
FRAMEWORKS_PATHS=("/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk/System/Library/Frameworks"
                  "/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk/System/Library/PrivateFrameworks"
                  "/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneSimulator.platform/Developer/SDKs/iPhoneSimulator.sdk/System/Library/Frameworks"
                  "/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneSimulator.platform/Developer/SDKs/iPhoneSimulator.sdk/System/Library/PrivateFrameworks"
                  )

for frameworks_path in ${FRAMEWORKS_PATHS[@]}; do
    # echo -e "${frameworks_path}"/*
    for framework_path in "${frameworks_path}/"*; do
        framework_dir_name=$(basename "${framework_path}")
        framework_name="${framework_dir_name%.*}"
        framework_extension="${framework_dir_name##*.}"
        echo -e "Dumping: \033[1m${framework_name}\033[0m"
        
        if [[ -e "${framework_path}/${framework_name}" ]]; then
            bin_path="${framework_path}/${framework_name}"
        elif [[ -e "${framework_path}/Versions/A/$framework_name" ]]; then
            bin_path="${framework_path}/Versions/A/$framework_name"
        else
            echo -e "Failed: ${framework_name}"
        fi

        # i386
        "${CLASSDUMP}" -a -A --arch i386 --sdk-ios-sim "" -H -j -o "dump_ios_json/${framework_dir_name}" "${bin_path}" 2>/dev/null
        # x86_64
        "${CLASSDUMP}" -a -A --arch x86_64 --sdk-ios-sim "" -H -j -o "dump_ios_json/${framework_dir_name}" "${bin_path}" 2>/dev/null
        # armv7
        # "${CLASSDUMP}" -a -A --arch armv7 --sdk-ios "" -H -j -o "dump_ios_json/${framework_dir_name}" "${bin_path}" 2>/dev/null
        # armv7s
        # "${CLASSDUMP}" -a -A --arch armv7s --sdk-ios "" -H -j -o "dump_ios_json/${framework_dir_name}" "${bin_path}" 2>/dev/null
        # arm64
        # "${CLASSDUMP}" -a -A --arch arm64 --sdk-ios "" -H -j -o "dump_ios_json/${framework_dir_name}" "${bin_path}" 2>/dev/null

        # List arch
        # class-dump --list-arch "${framework_path}"
    done
done
