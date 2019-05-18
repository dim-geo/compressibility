import vapoursynth as vs
import math

#resize to 1080 in order to compare quality through vmaf
#adding borders if needed
def resize_to_1080(video):
	height=video.height
	width=video.width
	if width/height >= 1920.0/1080.0:
		newheight=int(1920*height/width)
		borderup=int((1080-newheight)/2)
		if borderup % 2 == 1:
			borderup+=1
		borderdown=1080-borderup-newheight
		video=core.resize.Bicubic(clip=video,width=1920,height=newheight)
		video=core.std.AddBorders(clip=video,top=borderup,bottom=borderdown)
	else:
		newwidth=int(1080*width/height)
		borderleft=int((1920-newwidth)/2)
		if borderleft % 2==1:
			borderleft+=1
		borderright=1920-borderleft-newwidth
		video=core.resize.Bicubic(clip=video,width=newwidth,height=1080)
		video=core.std.AddBorders(clip=video,left=borderleft,right=borderright)
	return video

#compressibility check to keep 5% of the video in 30 seconds clips,
#spread equally to all video.
def compressibility_check(video):
	percentage = 5
	clipsduration=30
	
	clipframes=math.ceil(clipsduration*video.fps_num/video.fps_den)
	compressibilitiframes = math.ceil(percentage * video.num_frames / 100)
	numberofclips=math.floor(compressibilitiframes/clipframes)
	
	if numberofclips*clipframes/video.num_frames < 0.5:
		numberofclips+=1
	
	big_part_length=math.ceil(video.num_frames/numberofclips)
	center=math.floor(big_part_length/2)
	
	clips=[]
	for i in range(numberofclips):
	  start_point=big_part_length*i+center-math.ceil(clipframes/2)
	  endpoint=big_part_length*i+center+math.ceil(clipframes/2)
	  clip=video[start_point:endpoint]
	  clips.append(clip)
	
	compressclip=clips[0]
	for i in range(1,numberofclips):
	  compressclip=compressclip+clips[i]
	return compressclip
	

core = vs.get_core()
source = core.ffms2.Source(r'movie_original.mkv')
source=compressibility_check(source)
#source=resize_to_1080(source)

compressed=core.ffms2.Source(r'30_slow_half.mkv')
#compressed=core.std.AddBorders(clip=compressed,top=130,bottom=124)
compressed=resize_to_1080(compressed)

video3=core.vmaf.VMAF(source, compressed,  log_path="30_slow_half.xml", log_fmt=0, pool=1,ci=True)
video3.set_output()
