# Import dependencies
import os
import cv2
import torch
import matplotlib.pyplot as plt
import time

# Download MiDaS
#model_type = "DPT_Large"     # MiDaS v3 - Large     (highest accuracy, slowest inference speed)
#model_type = "DPT_Hybrid"   # MiDaS v3 - Hybrid    (medium accuracy, medium inference speed)
model_type = "MiDaS_small"  # MiDaS v2.1 - Small   (lowest accuracy, highest inference speed)

midas = torch.hub.load("intel-isl/MiDaS", model_type)

#device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
device = torch.device("cpu")
print('Using device: ' + str(device))

midas.eval()

midas_transforms = torch.hub.load('intel-isl/MiDaS', 'transforms')
if model_type == "DPT_Large" or model_type == "DPT_Hybrid":
    transform = midas_transforms.dpt_transform
else:
    transform = midas_transforms.small_transform

# Hook into OpenCV
# Use image file instead of webcam
image_dir = '/home/ralph/data/data/ETS2'
image_files = [f for f in os.listdir(image_dir) if f.endswith('.jpg')]

for image_file in image_files:
    org_img = cv2.imread(os.path.join(image_dir, image_file))

    midas_img = cv2.resize(org_img, (org_img.shape[1] // 2, org_img.shape[0] // 2))
    cv2.imshow('Original Image', midas_img)
    midas_img = cv2.cvtColor(midas_img, cv2.COLOR_BGR2RGB)
    input_batch = transform(midas_img).to(device)

    with torch.no_grad():
        prediction = midas(input_batch)

        prediction = torch.nn.functional.interpolate(
            prediction.unsqueeze(1),
            size=midas_img.shape[:2],
            mode="bicubic",
            align_corners=False,
        ).squeeze()

    output = prediction.cpu().numpy()
    output_image = cv2.normalize(src=output, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    cv2.imshow('Depth Image', output_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()