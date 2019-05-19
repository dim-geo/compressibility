# compressibility
vapoursynth compressibility function &amp; vmaf comparison

In this small python script 2 function are implemented:

1.  Compressibility check: Use 5% of the file, in clips of 30 seconds, to use as a sample for the whole file. Useful when you want to determine compressibility of a long video. Long videos are expensive to encode and if you want to check how encoding algorithm switches affect the result this is one way to go.

2.resize to 1080p: according to VMAF FAQ (https://github.com/Netflix/vmaf/blob/master/FAQ.md). Clips to compare must be 1920X1080p so that results make sense. So, resizing and adding boarders achieves that.
