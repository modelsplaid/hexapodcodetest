ffmpeg -i input.mp4 -c copy -map 0 -segment_time 00:10:00 -f segment output_%03d.mp4

