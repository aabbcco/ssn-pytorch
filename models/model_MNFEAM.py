import torch
import torch.nn as nn
from lib.ssn.ssn import soft_slic_all, soft_slic_knn, soft_slic_pknn
from lib.MEFEAM.MEFEAM import MFEM, LFAM, discriminative_loss, sample_and_group_query_ball


class MFEAM_SSN(nn.Module):
    def __init__(self,
                 feature_dim,
                 nspix,
                 mfem_dim=10,
                 n_iter=10,
                 RGB=False,
                 normal=False,
                 backend=soft_slic_pknn):
        super().__init__()
        self.nspix = nspix
        self.n_iter = n_iter
        self.channel = 3
        self.backend = backend
        if RGB:
            self.channel += 3
        if normal:
            self.channel += 3

        self.mfem = MFEM([32, 64], [128, 128], [128, mfem_dim], 64, 3,
                         [0.2, 0.3, 0.4])
        self.lfam = LFAM(32, [128, 10], 128 + mfem_dim)

    def forward(self, x):
        global_feature, msf_feature = self.mfem(x)
        fusioned_feature = self.lfam(global_feature,
                                     msf_feature)

        return self.backend(fusioned_feature,
                            fusioned_feature[:, :, :self.nspix],
                            self.n_iter), msf_feature

#delete in few commits

# class MFEAM_SSKNN(nn.Module):
#     def __init__(self,
#                  feature_dim,
#                  nspix,
#                  mfem_dim=6,
#                  n_iter=10,
#                  RGB=False,
#                  normal=False,
#                  backend=soft_slic_all):
#         super().__init__()
#         self.nspix = nspix
#         self.backend = backend
#         self.n_iter = n_iter
#         self.channel = 3
#         if RGB:
#             self.channel += 3
#         if normal:
#             self.channel += 3

#         self.mfem = MFEM([32, 64], [64, 64], [64, mfem_dim], 32, 3,
#                          [0.2, 0.4, 0.6])
#         self.lfam = LFAM(32, [128, 10], 128 + mfem_dim)

#     def forward(self, x):
#         global_feature, msf_feature = self.mfem(x)
#         fusioned_feature = self.lfam(global_feature, msf_feature)

#         return self.backend(fusioned_feature,
#                             fusioned_feature[:, :, :self.nspix],
#                             self.n_iter), msf_feature
