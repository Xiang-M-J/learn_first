from PIL import Image
import numpy as np

Infty = np.inf

def cal_power_sum(x_i: np.ndarray, x_j: np.ndarray):
    return (x_i[:,:,0]-x_j[:,:,0])**2

def cal_energy(image: np.ndarray):
    left_diff = np.diff(image, 1, 1, prepend=np.expand_dims(image[:,0,:], 1))
    right_diff = np.roll(left_diff, -1, 1)
    energy = np.sqrt(np.sum(np.power(left_diff, 2), axis=2) + np.sum(np.power(right_diff, 2), axis=2))
    return energy

def find_min_energy(energy: np.ndarray):
    seamMap = np.zeros_like(energy)
    seamMap[0, :] = energy[0, :]
    prior = np.zeros_like(energy, np.int32) - 1
    for i in range(1, energy.shape[0]):
        right_energy = np.roll(energy[i, :], -1)
        left_energy = np.roll(energy[i, :], 1)
        right_energy[-1] = Infty
        left_energy[0] = Infty
        stack_energy = np.stack([left_energy, energy[i, :], right_energy])
        minV = np.min(stack_energy, 0)
        minI = np.arange(0, energy.shape[1]) + np.argmin(stack_energy, 0) - 1
        seamMap[i, :] = seamMap[i-1, :] + minV
        prior[i, :] = minI
    seam = []
    minI = np.argmin(seamMap[-1, :])
    seam.append(minI)
    for i in range(energy.shape[0]-1, 0, -1):
        seam.append(prior[i, seam[-1]])
    return seam[::-1]

def delete_seam(image, seam):
    new_image = image[:,:-1,:]
    for i in range(image.shape[0]):
        if seam[i] < image.shape[1] - 1:
            new_image[i, seam[i]:] = image[i, seam[i]+1:]
    return new_image

def resize_width(image, width):
    delete_width = image.shape[1] - width
    for _ in range(delete_width):
        energy = cal_energy(image)
        # print(energy)
        seam = find_min_energy(energy)
        # print(seam)
        image = delete_seam(image, seam)
    return image

if __name__ == "__main__":
    image = Image.open("test.png")
    image = np.array(image)
    
    image = resize_width(image, 50)
    image_ = Image.fromarray(image)
    image_.show()
    # print(image.shape)
