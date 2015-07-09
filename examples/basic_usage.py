#!/usr/bin/env python3

import E200
import matplotlib.pyplot as plt

# ===============================
# Load data
# ===============================
data = E200.E200_load_data_gui()

# ===============================
# Select a camera
# ===============================
camera = data.rdrill.data.raw.images.CMOS_ELAN

# ===============================
# Select first UID
# ===============================
uid = camera.UID[0]

# ===============================
# Load images
# ===============================
images = E200.E200_load_images(camera, uid)

# ===============================
# Display image
# ===============================
plt.imshow(images.images[0])
plt.show()
