import torch
from torchvision import transforms
from PIL import Image
import os
import glob
from torchvision.datasets import MNIST, CIFAR10, FashionMNIST, ImageFolder
import numpy as np

# Define data transformations and ground truth transformations
def get_data_transforms(size, isize):
    mean_train = [0.485, 0.456, 0.406]
    std_train = [0.229, 0.224, 0.225]
    data_transforms = transforms.Compose([
        transforms.Resize((size, size)),  # Resize image to specified size
        transforms.ToTensor(),  # Convert image to tensor
        transforms.CenterCrop(isize),  # Crop the center of the image to isize
        transforms.Normalize(mean=mean_train, std=std_train)  # Normalize the image
    ])
    gt_transforms = transforms.Compose([
        transforms.Resize((size, size)),
        transforms.CenterCrop(isize),
        transforms.ToTensor()  # Convert ground truth image to tensor
    ])
    return data_transforms, gt_transforms

# Custom dataset class for MVTec dataset
class MVTecDataset_no_seg(torch.utils.data.Dataset):
    def __init__(self, root, transform, phase):
        if phase == 'train':
            self.img_path = os.path.join(root, 'train')
        else:
            self.img_path = os.path.join(root, 'test')
        self.transform = transform
        # load dataset
        self.img_paths, self.labels, self.types = self.load_dataset()  # self.labels => good : 0, anomaly : 1

    def load_dataset(self):

        img_tot_paths = []
        tot_labels = []
        tot_types = []

        defect_types = os.listdir(self.img_path)

        for defect_type in defect_types:
            if defect_type == 'good':
                img_paths = glob.glob(os.path.join(self.img_path, defect_type) + "/*.png")
                img_tot_paths.extend(img_paths)
                tot_labels.extend([0] * len(img_paths))
                tot_types.extend(['good'] * len(img_paths))
            else:
                img_paths = glob.glob(os.path.join(self.img_path, defect_type) + "/*.png")
                img_paths.sort()
                img_tot_paths.extend(img_paths)
                tot_labels.extend([1] * len(img_paths))
                tot_types.extend([defect_type] * len(img_paths))

        #assert len(img_tot_paths) == len(gt_tot_paths), "Something wrong with test and ground truth pair!"

        return img_tot_paths, tot_labels, tot_types

    def __len__(self):
        return len(self.img_paths)

    def __getitem__(self, idx):
        img_path,  label, img_type = self.img_paths[idx],  self.labels[idx], self.types[idx]
        img = Image.open(img_path).convert('RGB')

        img = np.array(img)
        #print(img.shape)
        img = Image.fromarray(img)

        img = self.transform(img)

        #assert img.size()[1:] == gt.size()[1:], "image.size != gt.size !!!"
        #print(img.shape,img_type)
        return img, label, img_type

class MVTecDataset(torch.utils.data.Dataset):
    def __init__(self, root, transform, gt_transform, phase):
        if phase == 'train':
            self.img_path = os.path.join(root, 'train')  # Path for training images
        else:
            self.img_path = os.path.join(root, 'test')  # Path for test images
            self.gt_path = os.path.join(root, 'ground_truth')  # Path for ground truth images
        self.transform = transform
        self.gt_transform = gt_transform
        # Load dataset
        self.img_paths, self.gt_paths, self.labels, self.types = self.load_dataset()  # self.labels => good : 0, anomaly : 1

    def load_dataset(self):
        img_tot_paths = []
        gt_tot_paths = []
        tot_labels = []
        tot_types = []

        defect_types = os.listdir(self.img_path)  # List all defect types

        for defect_type in defect_types:
            if defect_type == 'good':  # Good images (no anomalies)
                img_paths = glob.glob(os.path.join(self.img_path, defect_type) + "/*.png")
                img_tot_paths.extend(img_paths)
                gt_tot_paths.extend([0] * len(img_paths))
                tot_labels.extend([0] * len(img_paths))
                tot_types.extend(['good'] * len(img_paths))
            else:  # Anomalous images
                img_paths = glob.glob(os.path.join(self.img_path, defect_type) + "/*.png")
                gt_paths = glob.glob(os.path.join(self.gt_path, defect_type) + "/*.png")
                img_paths.sort()
                gt_paths.sort()
                img_tot_paths.extend(img_paths)
                gt_tot_paths.extend(gt_paths)
                tot_labels.extend([1] * len(img_paths))
                tot_types.extend([defect_type] * len(img_paths))

        assert len(img_tot_paths) == len(gt_tot_paths), "Mismatch between test images and ground truth pairs!"

        return img_tot_paths, gt_tot_paths, tot_labels, tot_types

    def __len__(self):
        return len(self.img_paths)

    def __getitem__(self, idx):
        img_path, gt, label, img_type = self.img_paths[idx], self.gt_paths[idx], self.labels[idx], self.types[idx]
        img = Image.open(img_path).convert('RGB')  # Open image and convert to RGB
        img = self.transform(img)  # Apply transformations to image
        if gt == 0:
            gt = torch.zeros([1, img.size()[-2], img.size()[-2]])  # If ground truth is 0, create a zero tensor
        else:
            gt = Image.open(gt)  # Open ground truth image
            gt = self.gt_transform(gt)  # Apply transformations to ground truth image

        assert img.size()[1:] == gt.size()[1:], "Mismatch between image size and ground truth size!"

        return img, gt, label, img_type, img_path
    

# Custom dataset class for MVTec dataset
class MVTecDataset_no_seg(torch.utils.data.Dataset):
    def __init__(self, root, transform, phase):
        if phase == 'train':
            self.img_path = os.path.join(root, 'train')
        else:
            self.img_path = os.path.join(root, 'test')
        self.transform = transform
        # load dataset
        self.img_paths, self.labels, self.types = self.load_dataset()  # self.labels => good : 0, anomaly : 1

    def load_dataset(self):

        img_tot_paths = []
        tot_labels = []
        tot_types = []

        defect_types = os.listdir(self.img_path)

        for defect_type in defect_types:
            if defect_type == 'good':
                img_paths = glob.glob(os.path.join(self.img_path, defect_type) + "/*.png")
                img_tot_paths.extend(img_paths)
                tot_labels.extend([0] * len(img_paths))
                tot_types.extend(['good'] * len(img_paths))
            else:
                img_paths = glob.glob(os.path.join(self.img_path, defect_type) + "/*.png")
                img_paths.sort()
                img_tot_paths.extend(img_paths)
                tot_labels.extend([1] * len(img_paths))
                tot_types.extend([defect_type] * len(img_paths))

        #assert len(img_tot_paths) == len(gt_tot_paths), "Something wrong with test and ground truth pair!"

        return img_tot_paths, tot_labels, tot_types

    def __len__(self):
        return len(self.img_paths)

    def __getitem__(self, idx):
        img_path,  label, img_type = self.img_paths[idx],  self.labels[idx], self.types[idx]
        img = Image.open(img_path).convert('RGB')

        img = np.array(img)
        #print(img.shape)
        img = Image.fromarray(img)

        img = self.transform(img)

        #assert img.size()[1:] == gt.size()[1:], "image.size != gt.size !!!"
        #print(img.shape,img_type)
        return img, label, img_type
    

#######################  VAD   ###############################

# Custom dataset class for VAD dataset
class VADDataset_no_seg(torch.utils.data.Dataset):
    def __init__(self, root, transform, phase):
        if phase == 'train':
            self.img_path = os.path.join(root, 'train')
        else:
            self.img_path = os.path.join(root, 'test')
        self.transform = transform
        # load dataset
        self.img_paths, self.labels, self.types = self.load_dataset()  # self.labels => good : 0, anomaly : 1

    def load_dataset(self):

        img_tot_paths = []
        tot_labels = []
        tot_types = []

        defect_types = os.listdir(self.img_path)

        for defect_type in defect_types:
            if defect_type == 'good':
                img_paths = glob.glob(os.path.join(self.img_path, defect_type) + "/*.png")
                img_tot_paths.extend(img_paths)
                tot_labels.extend([0] * len(img_paths))
                tot_types.extend(['good'] * len(img_paths))
            else:
                img_paths = glob.glob(os.path.join(self.img_path, defect_type) + "/*.png")
                img_paths.sort()
                img_tot_paths.extend(img_paths)
                tot_labels.extend([1] * len(img_paths))
                tot_types.extend([defect_type] * len(img_paths))

        #assert len(img_tot_paths) == len(gt_tot_paths), "Something wrong with test and ground truth pair!"

        return img_tot_paths, tot_labels, tot_types

    def __len__(self):
        return len(self.img_paths)

    def __getitem__(self, idx):
        img_path,  label, img_type = self.img_paths[idx],  self.labels[idx], self.types[idx]
        img = Image.open(img_path).convert('RGB')

        img = np.array(img)
        #print(img.shape)
        img = Image.fromarray(img)

        img = self.transform(img)

        #assert img.size()[1:] == gt.size()[1:], "image.size != gt.size !!!"
        #print(img.shape,img_type)
        return img, label, img_type
    
#######################  visA  ###############################
    
# Custom dataset class for visA dataset
class visADataset_no_seg(torch.utils.data.Dataset):
    def __init__(self, root, transform, phase):
        if phase == 'train':
            self.img_path = os.path.join(root, 'train')
        else:
            self.img_path = os.path.join(root, 'test')
        self.transform = transform
        # load dataset
        self.img_paths, self.labels, self.types = self.load_dataset()  # self.labels => good : 0, anomaly : 1

    def load_dataset(self):

        img_tot_paths = []
        tot_labels = []
        tot_types = []

        defect_types = os.listdir(self.img_path)

        for defect_type in defect_types:
            if defect_type == 'good':
                img_paths = glob.glob(os.path.join(self.img_path, defect_type) + "/*.JPG")
                img_tot_paths.extend(img_paths)
                tot_labels.extend([0] * len(img_paths))
                tot_types.extend(['good'] * len(img_paths))
            else:
                img_paths = glob.glob(os.path.join(self.img_path, defect_type) + "/*.JPG")
                img_paths.sort()
                img_tot_paths.extend(img_paths)
                tot_labels.extend([1] * len(img_paths))
                tot_types.extend([defect_type] * len(img_paths))

        #assert len(img_tot_paths) == len(gt_tot_paths), "Something wrong with test and ground truth pair!"

        return img_tot_paths, tot_labels, tot_types

    def __len__(self):
        return len(self.img_paths)

    def __getitem__(self, idx):
        img_path,  label, img_type = self.img_paths[idx],  self.labels[idx], self.types[idx]
        img = Image.open(img_path).convert('RGB')

        img = np.array(img)
        #print(img.shape)
        img = Image.fromarray(img)

        img = self.transform(img)

        #assert img.size()[1:] == gt.size()[1:], "image.size != gt.size !!!"
        #print(img.shape,img_type)
        return img, label, img_type


class visADataset(torch.utils.data.Dataset):
    def __init__(self, root, transform, gt_transform, phase):
        if phase == 'train':
            self.img_path = os.path.join(root, 'train')  # Path for training images
        else:
            self.img_path = os.path.join(root, 'test')  # Path for test images
            self.gt_path = os.path.join(root, 'ground_truth')  # Path for ground truth images
        self.transform = transform
        self.gt_transform = gt_transform
        # Load dataset
        self.img_paths, self.gt_paths, self.labels, self.types = self.load_dataset()  # self.labels => good : 0, anomaly : 1

    def load_dataset(self):
        img_tot_paths = []
        gt_tot_paths = []
        tot_labels = []
        tot_types = []

        defect_types = os.listdir(self.img_path)  # List all defect types
        #print(defect_types)
        for defect_type in defect_types:
            if defect_type == 'good':  # Good images (no anomalies)
                img_paths = glob.glob(os.path.join(self.img_path, defect_type) + "/*.JPG")
                img_tot_paths.extend(img_paths)
                gt_tot_paths.extend([0] * len(img_paths))
                tot_labels.extend([0] * len(img_paths))
                tot_types.extend(['good'] * len(img_paths))
            else:  # Anomalous images
                img_paths = glob.glob(os.path.join(self.img_path, defect_type) + "/*.JPG")
                gt_paths = glob.glob(os.path.join(self.gt_path, defect_type) + "/*.png")
                img_paths.sort()
                gt_paths.sort()
                img_tot_paths.extend(img_paths)
                gt_tot_paths.extend(gt_paths)
                tot_labels.extend([1] * len(img_paths))
                tot_types.extend([defect_type] * len(img_paths))

        assert len(img_tot_paths) == len(gt_tot_paths), "Mismatch between test images and ground truth pairs!"

        return img_tot_paths, gt_tot_paths, tot_labels, tot_types

    def __len__(self):
        return len(self.img_paths)

    def __getitem__(self, idx):
        img_path, gt, label, img_type = self.img_paths[idx], self.gt_paths[idx], self.labels[idx], self.types[idx]
        img = Image.open(img_path).convert('RGB')  # Open image and convert to RGB
        img = self.transform(img)  # Apply transformations to image
        if gt == 0:
            gt = torch.zeros([1, img.size()[-2], img.size()[-2]])  # If ground truth is 0, create a zero tensor
        else:
            gt = Image.open(gt)  # Open ground truth image
            gt = self.gt_transform(gt)  # Apply transformations to ground truth image

        assert img.size()[1:] == gt.size()[1:], "Mismatch between image size and ground truth size!"

        return img, gt, label, img_type, img_path

# Load data function for different datasets
def load_data(dataset_name='mnist', normal_class=0, batch_size=16):

    if dataset_name == 'cifar10':
        img_transform = transforms.Compose([
            transforms.Resize((32, 32)),
            transforms.ToTensor(),
            transforms.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225))
        ])

        os.makedirs("./Dataset/CIFAR10/train", exist_ok=True)
        dataset = CIFAR10('./Dataset/CIFAR10/train', train=True, download=True, transform=img_transform)
        print("CIFAR10 DataLoader Called...")
        print("All Train Data: ", dataset.data.shape)
        dataset.data = dataset.data[np.array(dataset.targets) == normal_class]
        dataset.targets = [normal_class] * dataset.data.shape[0]
        print("Normal Train Data: ", dataset.data.shape)

        os.makedirs("./Dataset/CIFAR10/test", exist_ok=True)
        test_set = CIFAR10("./Dataset/CIFAR10/test", train=False, download=True, transform=img_transform)
        print("Test Data:", test_set.data.shape)

    elif dataset_name == 'mnist':
        img_transform = transforms.Compose([
            transforms.Resize((32, 32)),
            transforms.ToTensor()
        ])

        os.makedirs("./Dataset/MNIST/train", exist_ok=True)
        dataset = MNIST('./Dataset/MNIST/train', train=True, download=True, transform=img_transform)
        print("MNIST DataLoader Called...")
        print("All Train Data: ", dataset.data.shape)
        dataset.data = dataset.data[np.array(dataset.targets) == normal_class]
        dataset.targets = [normal_class] * dataset.data.shape[0]
        print("Normal Train Data: ", dataset.data.shape)

        os.makedirs("./Dataset/MNIST/test", exist_ok=True)
        test_set = MNIST("./Dataset/MNIST/test", train=False, download=True, transform=img_transform)
        print("Test Data:", test_set.data.shape)

    elif dataset_name == 'fashionmnist':
        img_transform = transforms.Compose([
            transforms.Resize((32, 32)),
            transforms.ToTensor()
        ])

        os.makedirs("./Dataset/FashionMNIST/train", exist_ok=True)
        dataset = FashionMNIST('./Dataset/FashionMNIST/train', train=True, download=True, transform=img_transform)
        print("FashionMNIST DataLoader Called...")
        print("All Train Data: ", dataset.data.shape)
        dataset.data = dataset.data[np.array(dataset.targets) == normal_class]
        dataset.targets = [normal_class] * dataset.data.shape[0]
        print("Normal Train Data: ", dataset.data.shape)

        os.makedirs("./Dataset/FashionMNIST/test", exist_ok=True)
        test_set = FashionMNIST("./Dataset/FashionMNIST/test", train=False, download=True, transform=img_transform)
        print("Test Data:", test_set.data.shape)

    elif dataset_name == 'retina':
        data_path = 'Dataset/OCT2017/train'

        orig_transform = transforms.Compose([
            transforms.Resize([128, 128]),
            transforms.ToTensor()
        ])

        dataset = ImageFolder(root=data_path, transform=orig_transform)

        test_data_path = 'Dataset/OCT2017/test'
        test_set = ImageFolder(root=test_data_path, transform=orig_transform)

    else:
        raise Exception(
            "You entered {} as dataset, which is not a valid dataset for this repository!".format(dataset_name))

    train_dataloader = torch.utils.data.DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=True,
    )
    test_dataloader = torch.utils.data.DataLoader(
        test_set,
        batch_size=1,
        shuffle=False,
    )

    return train_dataloader, test_dataloader