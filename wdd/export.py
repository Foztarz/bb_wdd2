from datetime import datetime
import numpy as np
import os
from os.path import join
from os import makedirs
import json
from skimage.io import imsave


class WaggleExporter:
    def __init__(
        self,
        cam_id,
        output_path,
        full_frame_buffer,
        full_frame_buffer_len,
        full_frame_buffer_roi_size,
        datetime_buffer,
        min_images=32,
    ):
        self.cam_id = cam_id
        self.output_path = output_path
        self.full_frame_buffer = full_frame_buffer
        self.full_frame_buffer_len = full_frame_buffer_len
        self.full_frame_buffer_roi_size = full_frame_buffer_roi_size
        self.datetime_buffer = datetime_buffer
        self.pad_size = self.full_frame_buffer_roi_size // 2
        self.min_images = min_images

    def export(self, frame_idx, waggle):
        dt = waggle.timestamp
        y, m, d, h, mn = dt.year, dt.month, dt.day, dt.hour, dt.minute
        waggle_path = join(
            self.output_path, str(self.cam_id), str(y), str(m), str(d), str(h), str(mn)
        )
        makedirs(waggle_path, exist_ok=True)
        waggle_idx = len(
            list(
                filter(
                    lambda x: os.path.isdir(os.path.join(waggle_path, x)), os.listdir(waggle_path)
                )
            )
        )
        waggle_path = join(waggle_path, str(waggle_idx))
        makedirs(waggle_path, exist_ok=True)

        print(
            "\n{} - {}: Saving new waggle: {}".format(self.cam_id, datetime.utcnow(), waggle_path)
        )

        frame_idx_offset = frame_idx - waggle.ts[0] - 20
        if frame_idx_offset >= self.full_frame_buffer_len:
            frame_idx_offset = self.full_frame_buffer_len - 1
            print("Warning: Waggle ({}) longer than frame buffer size".format(waggle_path))
        elif frame_idx_offset < self.min_images:
            frame_idx_offset = self.min_images

        # FIXME: why are coordinates inverted at this point?
        # FIXME: scaling factor should depend on camera resolution
        center_y = int(np.median(waggle.xs) * 2) + self.pad_size
        center_x = int(np.median(waggle.ys) * 2) + self.pad_size

        frame_timestamps = []
        for im_idx, idx in enumerate(range(frame_idx - frame_idx_offset, frame_idx)):
            idx %= self.full_frame_buffer_len
            roi = self.full_frame_buffer[
                idx,
                center_x - self.pad_size : center_x + self.pad_size,
                center_y - self.pad_size : center_y + self.pad_size,
            ]
            frame_timestamps.append(self.datetime_buffer[idx])
            imsave(join(waggle_path, "{:03d}.png".format(im_idx)), roi)

        json.dump(
            {
                "timestamp_begin": waggle.timestamp.isoformat(),
                "x_coordinates": waggle.xs,
                "y_coordinates": waggle.ys,
                "frame_timestamps": frame_timestamps,
                "camera_timestamps": waggle.camera_timestamps,
                "frame_buffer_indices": [ts % self.full_frame_buffer_len for ts in waggle.ts],
            },
            open(join(waggle_path, "waggle.json"), "w"),
        )
