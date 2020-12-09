import torch
import torch.nn as nn
from lib.ssn.ssn import soft_slic_all
import torch.nn.functional as F
from lib.MEFEAM import MFEM, LFAM, discriminative_loss


class MFEAM_SSN(nn.Module):
    def __init__(self, feature_dim, nspix, n_iter=10, RGB=False, normal=False):
        super().__init__()
        self.nspix = nspix
        self.n_iter = n_iter
        self.channel = 3
        if RGB:
            self.channel += 3
        if normal:
            self.channel += 3

        self.mfem = MFEM([32, 64], [128, 128], [64, 3], 32, 3, [
                         0.2, 0.4, 0.6], kernel_start=[3, 1])
        self.lfam = LFAM(32, [128, 10], 131)

    def forward(self, x):
        global_feature, msf_feature = self.mfem(x)
        fusioned_feature = self.lfam(global_feature, msf_feature)

        return soft_slic_all(fusioned_feature, fusioned_feature[:, :, :self.nspix], self.n_iter)