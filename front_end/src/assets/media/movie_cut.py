from moviepy.editor import VideoFileClip

clip = VideoFileClip("/root/Meteorological_prediction_platform/front_end/src/assets/media/weather_forecast.mp4")

cut_clip = clip.subclip(1, 4)

cut_clip.write_videofile("/root/Meteorological_prediction_platform/front_end/src/assets/media/humidity.mp4")

cut_clip = clip.subclip(5, 8)

cut_clip.write_videofile("/root/Meteorological_prediction_platform/front_end/src/assets/media/temperature.mp4")

cut_clip = clip.subclip(9.5, 13)

cut_clip.write_videofile("/root/Meteorological_prediction_platform/front_end/src/assets/media/windSpeed.mp4")