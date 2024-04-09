# 降低 markdown 的标题级别
from glob import glob
import re

files = glob("*.md")

if len(files) == 0:
	exit

firstHeading = r"^# \S"

for file in files:
	contents = []
	count = 0
	flag = True
	with open(file, mode='r', encoding="utf-8") as f:
		contents = f.readlines()
	for i in range(len(contents)):
		if contents[i].startswith("# "):
			count += 1
			if count > 1:
				flag = False
				break
		elif contents[i].startswith("##"):
			contents[i] = contents[i][1:]
		else:
			continue
	
	if flag:
		with open(file+"1", mode="w", encoding="utf-8") as f:
			f.writelines(contents)
	