#from prettytable import PrettyTable
import re
from pandas import DataFrame as df

with open("log", "r") as infile:
    text = infile.read()
    passed = re.compile(r"passed.*::(test.*)\x1b", re.IGNORECASE)
    failed = re.compile(r"failed.*::(test.*) - (.*)\x1b", re.IGNORECASE)
    passed = passed.findall(text)
    failed = failed.findall(text)
    infile.close()

failed = [(i[0], ("\033[33mWARNING\033[0m","\033[31mFAILED\033[0m")["assertion" in i[1].lower()], i[1]) for i in failed]
passed = [(i, "\033[32mPASSED\033[0m", "") for i in passed]

frame = df(data=passed+failed, columns=["Test", "\033[37mStatus\033[0m", "Message"])
with open("log_summary", "w") as outfile:
    outfile.write(frame.to_string())
    outfile.close()

