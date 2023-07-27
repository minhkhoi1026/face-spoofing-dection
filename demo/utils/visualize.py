import cv2
import tempfile
import subprocess
from demo.utils.gradcam import show_cam_on_image

def visualize_frame_prediction(frame_data, fake_label, is_show_gradcam=False):
    image = cv2.imread(frame_data["frame_path"])
    for pred in frame_data["predict"]:
        x, y, p, q = pred["bbox"]
        score = pred["score"]
        
        if is_show_gradcam:
            gradcam = pred["grad_cam"] # * score / 100
            bbox = (x, y, p, q)
            image = show_cam_on_image(image / 255, gradcam, bbox)
        
        # Determine the color based on the score
        colors = [(0, 255, 0), # Green 
                  (0, 0, 255), # Red
                  (0, 255, 255) # Yellow
                ]
        color_id = fake_label & (0 if score < 40 else 1 if score > 60 else 2)
        color = colors[color_id]
            
        # Draw the bbox on the image
        cv2.rectangle(image, (x, y), (p, q), color, 2)
        height, _, _ = image.shape
        # Put the score text on top of the bbox
        text = f'{score:.2f}'
        text_position = (x, y - 10) if y > 10 else (x, y + q) if y + q + 10 > height else (x + 3,y)
        cv2.putText(image, text, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    return image

def create_video_from_frames(frames, frame_rate=30):
    output_file = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False).name
    with tempfile.TemporaryDirectory() as input_dir:
        input_dir = tempfile.mkdtemp()
        for i, frame in enumerate(frames):
            cv2.imwrite(f'{input_dir}/{i}.png', frame)
        # Run the ffmpeg command to generate the video
        cmd = f'/usr/bin/ffmpeg -framerate {frame_rate} -i {input_dir}/%d.png -c:v libx264 -r 30 -pix_fmt yuv420p -y {output_file}'
        subprocess.call(cmd, shell=True)
    return output_file
