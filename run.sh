winpty -Xallow-non-tty ~/Downloads/python-3.8.2-embed-amd64/Scripts/pytest.exe -m debug > log
sed "s/\\?//g" log > log.txt
sed "s/\\x1b\\[[0-9;]*[a-zA-Z]//g" log.txt > log2.txt
mv log2.txt log.txt
