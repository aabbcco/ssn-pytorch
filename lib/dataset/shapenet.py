from torch.utils.data import Dataset
from torch import Tensor
import os
import h5py
import numpy as np
from .pointcloud_io import read


def getFiles_full(path, suffix):
    return [
        os.path.join(root, file) for root, dirs, files in os.walk(path)
        for file in files if file.endswith(suffix)
    ]


def getFiles(path, suffix):
    return [
        file for root, dirs, files in os.walk(path) for file in files
        if file.endswith(suffix)
    ]


def convert_label(label, num=20):

    onehot = np.zeros((num, label.shape[0])).astype(np.float32)

    ct = 0
    for t in np.unique(label).tolist():
        if ct >= num:
            break
        else:
            onehot[ct, :] = (label == t)
        ct = ct + 1

    return onehot


def getFiles_full(path, suffix):
    return [
        os.path.join(root, file) for root, dirs, files in os.walk(path)
        for file in files if file.endswith(suffix)
    ]


class shapenet(Dataset):
    """
    shapenet dataset for Pytorch Dataloader\n
    too slow in init time,need another implemention

    Args:
        datafolder (string): folder containing shapenet result
        split (str, optional): options in train,test and val. Defaults to 'train'.
"""
    def __init__(self, datafolder, split='train'):
        assert split in ['train', 'val', 'test'], "split not exist"
        filepath = os.path.join(datafolder, split)
        datalist = []
        labelist = []
        flist = getFiles_full(filepath, '.h5')
        for fname in flist:
            f = h5py.File(fname, 'r')
            datalist.append(np.array(f['data']))
            labelist.append(np.array(f['pid']))
        self.data = np.concatenate(datalist, axis=0).transpose(0, 2, 1)
        self.label = np.concatenate(labelist, axis=0)

    def __getitem__(self, idx):
        return Tensor(self.data[idx]), Tensor(convert_label(
            self.label[idx])), Tensor(self.label[idx])

    def __len__(self):
        return len(self.data)


class shapenet_inst(Dataset):
    """
    shapenet dataset for Pytorch Dataloader\n
    too slow in init time,need another implemention

    Args:
        datafolder (string): folder containing shapenet result
        split (str, optional): options in train,test and val. Defaults to 'train'.
"""
    def __init__(self, datafolder, split='train'):
        assert split in ['train', 'val', 'test'], "split not exist"
        filepath = os.path.join(datafolder, split)
        datalist = []
        labelist = []
        flist = getFiles_full(filepath, '.h5')
        for fname in flist:
            f = h5py.File(fname, 'r')
            datalist.append(np.array(f['data']))
            labelist.append(np.array(f['pid']))
        self.data = np.concatenate(datalist, axis=0).transpose(0, 2, 1)
        self.label = np.concatenate(labelist, axis=0)

    def __getitem__(self, idx):
        return Tensor(self.data[idx]), Tensor(
            convert_label(self.label[idx], num=20)), Tensor(self.label[idx])

    def __len__(self):
        return len(self.data)


class shapenet_spix(Dataset):
    def __init__(self, datafolder, split='train', onehot=True):
        assert split in ['train', 'val', 'test'], "split not exist"
        filepath = os.path.join(datafolder, split)
        datalist = []
        labelist = []
        spixlist = []
        flist = getFiles_full(filepath, '.h5')
        for fname in flist:
            f = h5py.File( fname, 'r')
            datalist.append(np.array(f['data']))
            labelist.append(np.array(f['label']))
            spixlist.append(np.array(f['spix']))
        self.data = np.concatenate(datalist, axis=0).transpose(0, 2, 1)
        self.label = np.concatenate(labelist, axis=0)
        self.spix = np.concatenate(spixlist, axis=0)
        self.onehot = onehot

    def __getitem__(self, idx):
        label = self.label[idx]
        spix = self.spix[idx]
        if self.onehot:
            label = convert_label(label)
            spix = convert_label(spix)
        return Tensor(self.data[idx]), Tensor(label), Tensor(spix), Tensor(
            self.label[idx])

    def __len__(self):
        return len(self.data)


class shapenet_cpt(Dataset):
    def __init__(self, filepath) -> None:
        super().__init__()
        f = h5py.File(filepath)
        self.data = np.array(f["data"]).transpose(0, 2, 1)

    def __getitem__(self, idx: int):
        return Tensor(self.data[idx]), Tensor(self.data[idx]), Tensor(
            self.data[idx])

    def __len__(self) -> int:
        return len(self.data)


class shapenet_man(Dataset):
    def __init__(self, filepath) -> None:
        super().__init__()
        self.filelist = getFiles_full(filepath, ".pcd")

    def __getitem__(self, idx: int):
        filename = self.filelist[idx]
        data = read(filename)
        Tdata = Tensor(data[:, :3].transpose())
        return Tdata, Tdata, Tdata

    def __len__(self) -> int:
        return len(self.filelist)
