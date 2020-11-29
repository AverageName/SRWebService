import torch
import CSNLN.utility as utility
import CSNLN.model as models
from CSNLN.option import args
from tqdm import tqdm
import numpy as np
from PIL import Image
import sys
from CSNLN.data.common import set_channel, np2Tensor

def predict_sr(image):
    torch.manual_seed(args.seed)
    checkpoint = utility.checkpoint(args)

    # image = np.array(Image.open('/home/max/docker_test-docker/nn_microservice/images/comic.png'))

    if checkpoint.ok:
        with torch.no_grad():
            if image.shape[2] == 4:
                image = image[:, :, [2, 1, 0]]

            lr, = set_channel(image, n_channels=args.n_colors)
            lr = np2Tensor(lr, rgb_range=args.rgb_range)[0].unsqueeze(0).cpu()
            model = models.Model(args, checkpoint)

            model.eval()

            idx_scale = args.scale
            sr = model(lr, idx_scale)
            sr = utility.quantize(sr, args.rgb_range).squeeze()
            normalized = sr.mul(255 / args.rgb_range)
            sr = np.transpose(normalized.cpu().numpy(), (1, 2, 0)).astype(np.uint8)
            sr = sr[:, :, [2, 1, 0]]

        # sr = Image.fromarray(sr)
        # sr.save('/home/max/docker_test-docker/nn_microservice/images/result_cross.png')

        return sr


if __name__ == "__main__":
    predict_sr('blabla')