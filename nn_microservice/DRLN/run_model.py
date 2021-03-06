import torch
import DRLN.utility as utility
import DRLN.model as models
from DRLN.option import args
from tqdm import tqdm
import numpy as np
from PIL import Image
import sys
from DRLN.data.common import set_channel, np2Tensor

def predict_sr(image):
    torch.manual_seed(args.seed)
    checkpoint = utility.checkpoint(args)

    # image = np.array(Image.open('/home/max/docker_test-docker/nn_microservice/images/butterfly_LRBD_x3.png'))

    if checkpoint.ok:
        with torch.no_grad():
            if image.shape[2] == 4:
                image = image[:, :, [2, 1, 0]]

            lr = set_channel([image], args.n_colors)[0]
            lr = np2Tensor([lr], args.rgb_range)[0].unsqueeze(0).cpu()
            model = models.Model(args, checkpoint)

            model.eval()

            idx_scale = args.scale
            sr = model(lr, idx_scale)
            sr = utility.quantize(sr, args.rgb_range).squeeze()
            normalized = sr.mul(255 / args.rgb_range)
            sr = np.transpose(normalized.cpu().numpy(), (1, 2, 0)).astype(np.uint8)
            sr = sr[:, :, [2, 1, 0]]

        # sr = Image.fromarray(sr)
        # sr.save('/home/max/docker_test-docker/nn_microservice/images/result_drln_2.png')
        #print("SAVED")

        return sr


if __name__ == "__main__":
    predict_sr('blabla')