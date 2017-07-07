#!/usr/bin/python3
'''
# downlod pathc
'''
import urllib.request

URL_BASE = 'https://patchwork.kernel.org/patch/'
PATCHES = [9817743, 9817803, 9817747, 9817745, 9817817,
           9817753, 9817759, 9817811, 9817749, 9817755,
           9817809, 9817751, 9817757, 9817813, 9817799,
           9817819, 9817815, 9817797, 9817807, 9817793,
           9817805, 9817787, 9817785, 9817781, 9817795,
           9817791, 9817789, 9817769, 9817777, 9817783,
           9817775, 9817779, 9817763, 9817771, 9817761,
           9817765, 9817773]
TOTAL = len(PATCHES)
for index, patch in enumerate(PATCHES):
    url = URL_BASE+str(patch)+'/raw/'
    file_name = '%02d-%d_%d.patch' % (index+1, TOTAL, patch)
    print('download patch:%d %dof%d' % (patch, index+1, TOTAL)) 
    urllib.request.urlretrieve(url, file_name)

