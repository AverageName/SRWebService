import torch
import utility
import data
import model as models
from option import args
from tqdm import tqdm
import numpy as np
from PIL import Image
import sys

def predict_sr(image):
    torch.manual_seed(args.seed)
    checkpoint = utility.checkpoint(args)


    if checkpoint.ok:
        with torch.no_grad():
            lr = torch.from_numpy(np.transpose(image[:, :, [2, 1, 0]], (2, 0, 1))).unsqueeze(0).cpu()
            lr = lr.float()
            model = models.Model(args, checkpoint)

            model.eval()

            idx_scale = args.scale
            sr = model(lr, idx_scale)
            #sr = sr.clamp_(0, 1).squeeze().numpy().astype(np.uint8)
            sr = utility.quantize(sr, args.rgb_range).squeeze().numpy()
            sr = np.transpose(sr[[2, 1, 0], :, :], (1, 2, 0)).astype(np.uint8)
        # sr = sr.clamp(0, 1)*255
        #sr = sr.astype(np.uint8)

        return sr


if __name__ == "__main__":
    predict_sr('blabla')