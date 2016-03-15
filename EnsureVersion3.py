already_complained = False
if not already_complained:
   from sys import version_info, version
   if version_info[0] != 3:
      print("I'd prefer to be run on Python 3, instead of Python", str(version)[:5], "but that's OK.")
   already_complained = True