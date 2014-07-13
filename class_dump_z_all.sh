#! /bin/bash

FRAMEWORKS_PATH="/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS7.0.sdk/System/Library/Frameworks"

for framework_path in "$FRAMEWORKS_PATH"/*; do
	framework_dir_name=$(basename "${framework_path}")
	framework_name="${framework_dir_name%.*}"
	framework_extension="${framework_dir_name##*.}"
	
	if [[ -e "${framework_path}/${framework_name}" ]]; then
		bin_path="${framework_path}/${framework_name}"
	elif [[ -e "${framework_path}/Versions/A/${framework_name}" ]]; then
		bin_path="${framework_path}/Versions/A/${framework_name}"
	else
		echo -e "Failed: ${framework_name}"
	fi

	class-dump-z -a -A -k -k -R -b -H -o "${framework_dir_name}" "${bin_path}"
done
