from moviepy.editor import ImageSequenceClip
import os

# 定义图片所在的文件夹路径
image_folder = "pics"

# 获取图片文件名，并按顺序排列
image_files = [os.path.join(image_folder, img)
               for img in sorted(os.listdir(image_folder)) if img.endswith(".png")]

# 创建视频剪辑，设定每秒显示的帧数（可以调整fps值）
clip = ImageSequenceClip(image_files, fps=24)

# 导出视频文件
clip.write_videofile("output_video.mp4", codec="libx264")
