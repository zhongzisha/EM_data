
import bisect
import zarr
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader


class Zarr3DDataset(Dataset):
    def __init__(self, patch_size=(8, 8, 8), normalize=True):
        """
        Args:
            patch_size (tuple): Size of the 3D patch to be extracted.
            normalize (bool): whether do normalization 
        """
        self.zarr_files = (
            # each item is one dataset,
            # filename, group_name, patch_step in [z, y, x], i.e. [depth, height, width]
            ("data/EMBL_Miron_FIB-SEM.zarr", None, (2, 2, 2)),
            ("data/EMPIAR-11759.zarr", None, (1, 4, 4)),
            ("data/data_em.zarr", None, (4, 4, 4)),
            ("data/jrc_mus-nacc-2/jrc_mus-nacc-2.zarr", "recon-2/em/fibsem-int16/s0", (4, 4, 4)),
            ("data/hemibrain-ng_1000x1000x1000.zarr", None, (8, 8, 8))
        )
        self.patch_size = patch_size
        self.normalize = normalize
        self.items = []

        self.start_indexes = [0] # store the start index for patches in each dataset, integral sum, e.g., [0, 100, 200, 500, 1000]
        for zarr_filename, zarr_group_name, patch_step in self.zarr_files:
            zarr_data = zarr.open(zarr_filename, mode='r')
            if zarr_group_name is not None:
                zarr_data = zarr_data[zarr_group_name]
            depth, height, width = zarr_data.shape

            # generate the 3-D coordinate grid
            zs = np.arange(0, depth-patch_size[0], patch_step[0], dtype=np.int32)
            ys = np.arange(0, height-patch_size[1], patch_step[1], dtype=np.int32)
            xs = np.arange(0, width-patch_size[2], patch_step[2], dtype=np.int32)
            new_shape = (len(zs), len(ys), len(xs))

            self.items.append((zarr_data, new_shape, zs, ys, xs))
            self.start_indexes.append(self.start_indexes[-1]+np.prod(new_shape))

    def __len__(self):
        return self.start_indexes[-1]
    
    def __getitem__(self, idx):
        # get the dataset index
        dataset_idx = bisect.bisect_right(self.start_indexes, idx) - 1

        # get the dataset item
        zarr_data, new_shape, zs, ys, xs = self.items[dataset_idx]

        dz, dy, dx = self.patch_size
        # get the flattend coordinate
        z_idx, y_idx, x_idx = np.unravel_index(idx - self.start_indexes[dataset_idx], new_shape)
        # get the 3-D coordinate
        z_idx, y_idx, x_idx = zs[z_idx], ys[y_idx], xs[x_idx]

        # extract the 3-D patch
        patch = zarr_data[z_idx:z_idx+dz, y_idx:y_idx+dy, x_idx:x_idx+dx]
        
        # convert to PyTorch tensor
        patch_tensor = torch.tensor(patch, dtype=torch.float32)

        # normalize if needed
        if self.normalize:
            patch_tensor = self.normalize_patch(patch_tensor)
        
        return patch_tensor, np.random.randint(low=0, high=2)

    def normalize_patch(self, patch):
        patch_min = patch.min()
        patch_max = patch.max()
        if patch_min == patch_max:
            return torch.zeros_like(patch)
        return (patch - patch_min) / (patch_max - patch_min)


class Simple3DCNN(nn.Module):
    def __init__(self):
        super(Simple3DCNN, self).__init__()
        self.conv1 = nn.Conv3d(1, 16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv3d(16, 32, kernel_size=3, padding=1)
        self.pool = nn.MaxPool3d(2)
        self.fc1 = nn.Linear(32 * 2 * 4 * 4, 128)  
        self.fc2 = nn.Linear(128, 2)  

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x


def main():
    # Build dataset and dataloader
    dataset = Zarr3DDataset(patch_size=(8, 16, 16))
    dataloader = DataLoader(dataset, batch_size=4, shuffle=True)

    # Initialize model, loss function, and optimizer
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = Simple3DCNN().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.0001)

    # Training loop
    num_epochs = 10
    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        for i, data in enumerate(dataloader, 0):
            inputs = data[0].unsqueeze(1).to(device) 
            labels = data[1].to(device) 

            optimizer.zero_grad()

            # Forward pass
            outputs = model(inputs)
            loss = criterion(outputs, labels)

            # Backward pass and optimize
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            if i % 10 == 9:  
                print(f"[Epoch={epoch+1}, Step={i+1}] loss: {running_loss / 10:.3f}")
                running_loss = 0.0


if __name__ == '__main__':
    main()













